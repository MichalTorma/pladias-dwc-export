import logging
import os
import sys
from datetime import datetime
# Assuming the other imports remain the same

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Your existing imports
from libs.database import query_to_csv
# from libs.zenodo_uploader import ZenodoDeposition # commented as per your script
from libs.api.zenodo_api import ZenodoDeposition

def read_sql_query(file_path):
    """Reads SQL query from a file."""
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        logger.error("SQL file not found.")
        sys.exit(1)

def main():
    sql_query = read_sql_query("/app/libs/sql/dwc-select.sql")

    # Define the path for the CSV file
    csv_file_path = "/app/occurrences.csv"
    query_to_csv(sql_query, csv_file_path)

    deposition_id = os.environ.get("ZENODO_DEPOSITION_ID")
    zen = ZenodoDeposition(deposition_id=deposition_id, sandbox=True)  # Ensure sandbox is appropriately set

    try:
        logger.info("Retrieving original metadata.")
        orig_metadata = zen.get_metadata()

        logger.info("Creating a new version of the deposition.")
        zen.create_new_version()

        logger.info("Deleting existing files from the new version.")
        zen.delete_files()

        logger.info("Uploading new file to the deposition.")
        zen.upload_file(csv_file_path)

        new_metadata = orig_metadata['metadata']
        for key in ['prereserve_doi', 'doi']:
            new_metadata.pop(key, None)  # Use pop with default to avoid KeyError
        new_metadata['publication_date'] = datetime.now().date().isoformat()

        logger.info("Updating metadata for the new version.")
        zen.update_metadata(new_metadata)

        logger.info("Publishing the new version.")
        zen.publish()

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

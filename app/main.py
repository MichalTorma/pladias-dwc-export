# %%
import sys
sys.path.append('/app')
import os
from libs.database import query_to_csv
from libs.zenodo_uploader import upload_dataset_to_zenodo

# Define the SQL query (you can also load this from a file)
with open("/app/libs/sql/dwc-select.sql", "r") as f:
    sql_query = f.read()

# %%
# Define the path for the CSV file
csv_file_path = "/app/occurrences.csv"

# Execute the query and save to CSV
# query_to_csv(sql_query, csv_file_path)

# Upload the CSV file to Zenodo
upload_dataset_to_zenodo(
    csv_file_path, deposition_id=os.environ.get("ZENODO_DEPOSITION_ID"), sandbox=True
)  # Set sandbox=False for production

# %%
deposition_id=os.environ.get("ZENODO_DEPOSITION_ID")

from libs.api.zenodo_api import create_new_deposition, create_new_version, upload_file_to_deposition, publish_deposition, delete_files_from_deposition
# %%
deposition_id
# %%
from zenodo_client import Creator, Metadata, ensure_zenodo

# Define the metadata that will be used on initial upload
data = Metadata(
    title='Test Upload 1',
    upload_type='dataset',
    description='test description',
    creators=[
        Creator(
            name='Torma, Michal',
            affiliation='GBIF Norway',
            orcid='0000-0002-2690-9509',
            gnd=None
        ),
    ],
)
#%%
res = ensure_zenodo(
    key='test3',  # this is a unique key you pick that will be used to store
                  # the numeric deposition ID on your local system's cache
    data=data,
    paths=[
        '/app/occurrences.csv',
    ],
    sandbox=True,  # remove this when you're ready to upload to real Zenodo
)
from pprint import pprint

pprint(res.json())

# %%

from libs.api.zenodo_api import create_new_deposition, create_new_version, upload_file_to_deposition, publish_deposition, delete_files_from_deposition

def upload_dataset_to_zenodo(file_path, deposition_id=None, sandbox=True):
    try:
        if deposition_id:
            print("Removing files from the existing deposition...")
            delete_files_from_deposition(deposition_id, sandbox=sandbox)

            print("Creating a new version of the existing deposition...")
            deposition_id = create_new_version(deposition_id, sandbox=sandbox)
        else:
            print("Creating a new deposition...")
            deposition = create_new_deposition(sandbox=sandbox)
            deposition_id = deposition['id']

        print(f"Uploading file to deposition {deposition_id}...")
        upload_file_to_deposition(deposition_id, file_path, sandbox=sandbox)

        print(f"Publishing deposition {deposition_id}...")
        publish_deposition(deposition_id, sandbox=sandbox)

        print("Dataset successfully uploaded and published.")
    except Exception as e:
        print(e)

def create_and_publish_new_version(file_path, deposition_id, sandbox=True):
    try:
        # Step 1: Create a new version draft
        print("Creating a new version of the existing deposition...")
        new_draft_id = create_new_version(deposition_id, sandbox=sandbox)

        # Step 2: Upload new files to the new version draft
        print(f"Uploading new file to the new version draft {new_draft_id}...")
        upload_file_to_deposition(new_draft_id, file_path, sandbox=sandbox)

        # Step 3: Publish the new version
        print(f"Publishing the new version draft {new_draft_id}...")
        publish_deposition(new_draft_id, sandbox=sandbox)

        print("New version successfully created and published.")
    except Exception as e:
        print(e)

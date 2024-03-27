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

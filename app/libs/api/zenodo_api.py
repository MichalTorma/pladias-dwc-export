import requests
import os

def create_new_deposition(sandbox=True):
    """Creates a new deposition on Zenodo."""
    zenodo_token = os.environ.get('ZENODO_TOKEN')
    base_url = "https://sandbox.zenodo.org/api/deposit/depositions" if sandbox else "https://zenodo.org/api/deposit/depositions"
    headers = {"Content-Type": "application/json"}
    params = {'access_token': zenodo_token}

    response = requests.post(base_url, json={}, params=params, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to create new deposition: {response.status_code} {response.text}")

def create_new_version(deposition_id, sandbox=True):
    """Creates a new version draft of an existing deposition on Zenodo."""
    zenodo_token = os.environ.get('ZENODO_TOKEN')
    base_url = "https://sandbox.zenodo.org/api/deposit/depositions" if sandbox else "https://zenodo.org/api/deposit/depositions"
    params = {'access_token': zenodo_token}
    new_version_url = f"{base_url}/{deposition_id}/actions/newversion"

    response = requests.post(new_version_url, params=params)
    if response.status_code == 201:
        return response.json()['links']['latest_draft'].split('/')[-1]
    else:
        raise Exception(f"Failed to create new version: {response.status_code} {response.text}")

def upload_file_to_deposition(deposition_id, file_path, sandbox=True):
    """Uploads a file to the specified deposition draft on Zenodo."""
    zenodo_token = os.environ.get('ZENODO_TOKEN')
    base_url = "https://sandbox.zenodo.org/api/deposit/depositions" if sandbox else "https://zenodo.org/api/deposit/depositions"
    files_url = f"{base_url}/{deposition_id}/files"
    params = {'access_token': zenodo_token}

    with open(file_path, 'rb') as fp:
        data = {'name': os.path.basename(file_path)}
        files = {'file': fp}
        response = requests.post(files_url, data=data, files=files, params=params)
    if response.status_code != 201:
        raise Exception(f"Failed to upload file: {response.status_code} {response.text}")

def publish_deposition(deposition_id, sandbox=True):
    """Publishes the specified deposition on Zenodo."""
    zenodo_token = os.environ.get('ZENODO_TOKEN')
    base_url = "https://sandbox.zenodo.org/api/deposit/depositions" if sandbox else "https://zenodo.org/api/deposit/depositions"
    publish_url = f"{base_url}/{deposition_id}/actions/publish"
    params = {'access_token': zenodo_token}

    response = requests.post(publish_url, params=params)
    if response.status_code != 202:
        raise Exception(f"Failed to publish dataset: {response.status_code} {response.text}")

def delete_files_from_deposition(deposition_id, sandbox=True):
    """Deletes all files from the specified deposition."""
    zenodo_token = os.environ.get('ZENODO_TOKEN')
    base_url = "https://sandbox.zenodo.org/api/deposit/depositions" if sandbox else "https://zenodo.org/api/deposit/depositions"
    headers = {"Content-Type": "application/json"}
    params = {'access_token': zenodo_token}
    files_url = f"{base_url}/{deposition_id}/files"

    # Get a list of all files in the deposition
    response = requests.get(files_url, params=params)
    if response.status_code == 200:
        files = response.json()
        for file in files:
            # Delete each file
            file_id = file['id']
            delete_url = f"{files_url}/{file_id}"
            del_response = requests.delete(delete_url, params=params)
            if del_response.status_code != 204:
                raise Exception(f"Failed to delete file {file_id}: {del_response.status_code} {del_response.text}")
    else:
        raise Exception(f"Failed to list files: {response.status_code} {response.text}")


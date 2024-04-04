import requests
import os

class ZenodoDeposition:
    def __init__(self, zenodo_token, deposition_id=None, sandbox=True):
        self.deposition_id = deposition_id
        self.sandbox = sandbox
        self.base_url = "https://sandbox.zenodo.org/api/deposit/depositions" if self.sandbox else "https://zenodo.org/api/deposit/depositions"
        self.zenodo_token = zenodo_token
        self.headers = {"Content-Type": "application/json"}
        self.params = {'access_token': self.zenodo_token}

    def create_new(self):
        """Creates a new deposition on Zenodo."""
        response = requests.post(self.base_url, json={}, params=self.params, headers=self.headers)
        if response.status_code == 201:
            self.deposition_id = response.json()['id']
            return response.json()
        else:
            raise Exception(f"Failed to create new deposition: {response.status_code} {response.text}")

    def create_new_version(self):
        """Creates a new version draft of an existing deposition on Zenodo."""
        if not self.deposition_id:
            raise Exception("Deposition ID is not set.")
        new_version_url = f"{self.base_url}/{self.deposition_id}/actions/newversion"
        response = requests.post(new_version_url, params=self.params)
        if response.status_code == 201:
            self.deposition_id = response.json()['links']['latest_draft'].split('/')[-1]
            return self.deposition_id
        else:
            raise Exception(f"Failed to create new version: {response.status_code} {response.text}")

    def upload_file(self, file_path):
        """Uploads a file to the specified deposition draft on Zenodo."""
        if not self.deposition_id:
            raise Exception("Deposition ID is not set.")
        files_url = f"{self.base_url}/{self.deposition_id}/files"
        with open(file_path, 'rb') as fp:
            data = {'name': os.path.basename(file_path)}
            files = {'file': fp}
            response = requests.post(files_url, data=data, files=files, params=self.params)
        if response.status_code != 201:
            raise Exception(f"Failed to upload file: {response.status_code} {response.text}")

    def publish(self):
        """Publishes the specified deposition on Zenodo."""
        if not self.deposition_id:
            raise Exception("Deposition ID is not set.")
        publish_url = f"{self.base_url}/{self.deposition_id}/actions/publish"
        response = requests.post(publish_url, params=self.params)
        if response.status_code != 202:
            raise Exception(f"Failed to publish dataset: {response.status_code} {response.text}")

    def delete_files(self):
        """Deletes all files from the specified deposition."""
        if not self.deposition_id:
            raise Exception("Deposition ID is not set.")
        files_url = f"{self.base_url}/{self.deposition_id}/files"
        response = requests.get(files_url, params=self.params)
        if response.status_code == 200:
            files = response.json()
            for file in files:
                file_id = file['id']
                delete_url = f"{files_url}/{file_id}"
                del_response = requests.delete(delete_url, params=self.params)
                if del_response.status_code != 204:
                    raise Exception(f"Failed to delete file {file_id}: {del_response.status_code} {del_response.text}")
        else:
            raise Exception(f"Failed to list files: {response.status_code} {response.text}")

    def list_files(self):
        """Lists all files attached to the specified deposition."""
        if not self.deposition_id:
            raise Exception("Deposition ID is not set.")
        files_url = f"{self.base_url}/{self.deposition_id}/files"
        response = requests.get(files_url, params=self.params)
        if response.status_code == 200:
            files = response.json()
            return files  # Return the list of files
        else:
            raise Exception(f"Failed to list files: {response.status_code} {response.text}")

    def update_metadata(self, metadata):
        """Updates the metadata for the specified deposition."""
        if not self.deposition_id:
            raise Exception("Deposition ID is not set.")
        metadata_url = f"{self.base_url}/{self.deposition_id}"
        response = requests.put(metadata_url, json={'metadata': metadata}, params=self.params, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to update metadata: {response.status_code} {response.text}")

    def get_metadata(self):
        """Retrieves the metadata for the specified deposition."""
        if not self.deposition_id:
            raise Exception("Deposition ID is not set.")
        deposition_url = f"{self.base_url}/{self.deposition_id}"
        response = requests.get(deposition_url, params=self.params)
        if response.status_code == 200:
            return response.json()  # Return the deposition metadata
        else:
            raise Exception(f"Failed to retrieve deposition metadata: {response.status_code} {response.text}")

    def get_all_version_ids(self):
        """Retrieves a list of deposition IDs for all versions of the specified deposition."""
        if not self.deposition_id:
            raise Exception("Deposition ID is not set.")
        metadata = self.get_metadata()
        if 'conceptdoi' in metadata:
            conceptdoi = metadata['conceptdoi']
            search_url = f"{self.base_url}?q=conceptdoi:\"{conceptdoi}\""
            response = requests.get(search_url, params=self.params)
            if response.status_code == 200:
                versions = response.json()
                version_ids = [version['id'] for version in versions['hits']['hits']]
                return version_ids
            else:
                raise Exception(f"Failed to retrieve version IDs: {response.status_code} {response.text}")
        else:
            raise Exception("Concept DOI not found in metadata.")

import os

from pydstk.api_sdk import repositories
from pydstk.api_sdk.clients.base_client import BaseClient


def _files_to_upload(paths):
    """Pairs each local file with its name under the version.

    A folder uploads its contents, keeping paths relative to the folder.
    """
    uploads = []
    for path in paths:
        if os.path.isdir(path):
            for root, _dirs, files in os.walk(path):
                for name in sorted(files):
                    local_path = os.path.join(root, name)
                    relative = os.path.relpath(local_path, path)
                    uploads.append((local_path, relative.replace(os.sep, "/")))
        else:
            uploads.append((path, os.path.basename(path)))
    return uploads


class ModelVersionsClient(BaseClient):
    entity = "modelVersion"

    def list(self, model_id, include_archived=False):
        """Get list of versions of a model

        :param str model_id:
        :param bool include_archived:
        :rtype: list[models.ModelVersion]
        """
        repository = self.build_repository(repositories.ListModelVersions)
        return repository.list(model_id, include_archived=include_archived)

    def get(self, model_version_id):
        """
        :param str model_version_id:
        :rtype: models.ModelVersion
        """
        repository = self.build_repository(repositories.GetModelVersion)
        return repository.get(model_version_id)

    def create(self, model_id, description=None):
        """Start a new, unpublished version of a model

        :param str model_id:
        :param str description:
        :rtype: models.ModelVersion
        """
        repository = self.build_repository(repositories.CreateModelVersion)
        return repository.create(model_id, description)

    def edit(self, model_version_id, description):
        """
        :param str model_version_id:
        :param str description:
        :rtype: models.ModelVersion
        """
        repository = self.build_repository(repositories.EditModelVersion)
        return repository.edit(model_version_id, description)

    def publish(self, model_version_id):
        """Publish a version. Published versions can't take new files

        :param str model_version_id:
        :rtype: models.ModelVersion
        """
        repository = self.build_repository(repositories.PublishModelVersion)
        return repository.publish(model_version_id)

    def archive(self, model_version_id):
        """Archive a version, or restore it if it is already archived

        :param str model_version_id:
        :rtype: models.ModelVersion
        """
        repository = self.build_repository(repositories.ArchiveModelVersion)
        return repository.archive(model_version_id)

    def list_files(self, model_version_id, prefix=None):
        """
        :param str model_version_id:
        :param str prefix: only files whose name starts with this
        :rtype: list[models.ModelVersionFile]
        """
        repository = self.build_repository(repositories.ListModelVersionFiles)
        return repository.list(model_version_id, prefix=prefix)

    def upload(self, model_version_id, paths, on_file=None, on_progress=None):
        """Upload files or folders to an unpublished version

        :param str model_version_id:
        :param list[str] paths: files, or folders whose contents to upload
        :param on_file: called with (filename, size) before each file starts
        :param on_progress: called with the byte count of each uploaded part
        :rtype: list[str]
        :returns: storage keys of the uploaded files
        """
        repository = self.build_repository(repositories.UploadModelVersionFile)
        keys = []
        for local_path, filename in _files_to_upload(paths):
            if on_file:
                on_file(filename, os.path.getsize(local_path))
            keys.append(
                repository.upload(
                    model_version_id, local_path, filename, on_progress=on_progress
                )
            )
        return keys

    @staticmethod
    def upload_size(paths):
        """
        :param list[str] paths:
        :rtype: int
        :returns: total bytes `upload` would send
        """
        return sum(
            os.path.getsize(local_path) for local_path, _ in _files_to_upload(paths)
        )

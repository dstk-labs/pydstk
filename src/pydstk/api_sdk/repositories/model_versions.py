import requests
from gql import gql

from pydstk.api_sdk import serializers
from pydstk.api_sdk.exceptions import DstkSdkError, ResourceCreatingError
from pydstk.api_sdk.repositories.common import BaseRepository, ListResources

PART_SIZE = 64 * 1024 * 1024
PART_UPLOAD_TIMEOUT_SECONDS = 300

MODEL_VERSION_FIELDS = """
    modelVersionId
    numericVersion
    description
    isArchived
    isFinalized
    s3Prefix
    modelId {
        modelId
        modelName
    }
    createdBy {
        realName
    }
    dateCreated
"""

LIST_MODEL_VERSIONS = gql(
    """
    query ListMLModelVersions(
        $after: String
        $modelId: String!
        $includeArchived: Boolean!
    ) {
        modelVersion {
            list(after: $after, modelId: $modelId, includeArchived: $includeArchived) {
                pageInfo {
                    continuationToken
                    hasNextPage
                }
                edges {
                    node {
                        %s
                    }
                }
            }
        }
    }
    """
    % MODEL_VERSION_FIELDS
)

GET_MODEL_VERSION = gql(
    """
    query GetMLModelVersion($modelVersionId: String!) {
        modelVersion {
            get(modelVersionId: $modelVersionId) {
                %s
            }
        }
    }
    """
    % MODEL_VERSION_FIELDS
)

CREATE_MODEL_VERSION = gql(
    """
    mutation CreateModelVersion($data: ModelVersionInput!) {
        modelVersion {
            create(data: $data) {
                %s
            }
        }
    }
    """
    % MODEL_VERSION_FIELDS
)

EDIT_MODEL_VERSION = gql(
    """
    mutation EditModelVersion($modelVersionId: String!, $data: EditModelVersion!) {
        modelVersion {
            edit(modelVersionId: $modelVersionId, data: $data) {
                %s
            }
        }
    }
    """
    % MODEL_VERSION_FIELDS
)

PUBLISH_MODEL_VERSION = gql(
    """
    mutation PublishModelVersion($modelVersionId: String!) {
        modelVersion {
            publish(modelVersionId: $modelVersionId) {
                %s
            }
        }
    }
    """
    % MODEL_VERSION_FIELDS
)

ARCHIVE_MODEL_VERSION = gql(
    """
    mutation ArchiveModelVersion($modelVersionId: String!) {
        modelVersion {
            archive(modelVersionId: $modelVersionId) {
                %s
            }
        }
    }
    """
    % MODEL_VERSION_FIELDS
)

PRESIGN_URL = gql(
    """
    mutation PresignURL($data: PresignedURLInput!) {
        modelVersion {
            presignURL(data: $data) {
                uploadId
                key
                partNumber
                url
                ETag
            }
        }
    }
    """
)

LIST_MODEL_VERSION_FILES = gql(
    """
    query ListObjectsForModelVersion(
        $after: String
        $modelVersionId: String!
        $prefix: String
    ) {
        storageProvider {
            listObjects(after: $after, modelVersionId: $modelVersionId, prefix: $prefix) {
                pageInfo {
                    continuationToken
                    hasNextPage
                }
                edges {
                    node {
                        name
                        size
                        lastModified
                    }
                }
            }
        }
    }
    """
)


class ListModelVersions(ListResources):
    SERIALIZER_CLS = serializers.ModelVersion

    def list(self, model_id, include_archived=False):
        version_dicts = self._fetch_all(
            LIST_MODEL_VERSIONS,
            ("modelVersion", "list"),
            {"modelId": model_id, "includeArchived": include_archived},
        )
        return self._parse_objects(version_dicts)


class GetModelVersion(BaseRepository):
    SERIALIZER_CLS = serializers.ModelVersion

    def get(self, model_version_id):
        result = self._execute(GET_MODEL_VERSION, {"modelVersionId": model_version_id})
        return self._parse_object(result["modelVersion"]["get"])


class CreateModelVersion(BaseRepository):
    SERIALIZER_CLS = serializers.ModelVersion

    def create(self, model_id, description=None):
        data = {"modelId": model_id, "description": description}
        result = self._execute(CREATE_MODEL_VERSION, {"data": data})
        return self._parse_object(result["modelVersion"]["create"])


class EditModelVersion(BaseRepository):
    SERIALIZER_CLS = serializers.ModelVersion

    def edit(self, model_version_id, description):
        variables = {
            "modelVersionId": model_version_id,
            "data": {"description": description},
        }
        result = self._execute(EDIT_MODEL_VERSION, variables)
        return self._parse_object(result["modelVersion"]["edit"])


class PublishModelVersion(BaseRepository):
    SERIALIZER_CLS = serializers.ModelVersion

    def publish(self, model_version_id):
        result = self._execute(
            PUBLISH_MODEL_VERSION, {"modelVersionId": model_version_id}
        )
        return self._parse_object(result["modelVersion"]["publish"])


class ArchiveModelVersion(BaseRepository):
    SERIALIZER_CLS = serializers.ModelVersion

    def archive(self, model_version_id):
        result = self._execute(
            ARCHIVE_MODEL_VERSION, {"modelVersionId": model_version_id}
        )
        return self._parse_object(result["modelVersion"]["archive"])


class ListModelVersionFiles(ListResources):
    SERIALIZER_CLS = serializers.ModelVersionFile

    def list(self, model_version_id, prefix=None):
        file_dicts = self._fetch_all(
            LIST_MODEL_VERSION_FILES,
            ("storageProvider", "listObjects"),
            {"modelVersionId": model_version_id, "prefix": prefix},
        )
        return self._parse_objects(file_dicts)


class UploadModelVersionFile(BaseRepository):
    def upload(self, model_version_id, local_path, filename, on_progress=None):
        """Uploads one file in PART_SIZE parts through presigned S3 URLs

        :param str model_version_id:
        :param str local_path: file on disk
        :param str filename: name under the version, may contain "/"
        :param on_progress: called with the byte count of each uploaded part
        :rtype: str
        :returns: the object's storage key
        """
        upload_id = self._presign(model_version_id, filename, "createMultipartUpload")[
            "uploadId"
        ]

        try:
            parts = self._upload_parts(
                model_version_id, local_path, filename, upload_id, on_progress
            )
            finalized = self._presign(
                model_version_id,
                filename,
                "finalizeMultipartUpload",
                uploadId=upload_id,
                multipartUpload={"Parts": parts},
            )
        except BaseException:
            self._abort(model_version_id, filename, upload_id)
            raise

        return finalized["key"]

    def _upload_parts(
        self, model_version_id, local_path, filename, upload_id, on_progress
    ):
        parts = []
        with open(local_path, "rb") as local_file:
            part_number = 1
            while True:
                chunk = local_file.read(PART_SIZE)
                if not chunk and part_number > 1:
                    return parts

                url = self._presign(
                    model_version_id,
                    filename,
                    "uploadPart",
                    uploadId=upload_id,
                    partNumber=part_number,
                )["url"]
                response = requests.put(
                    url, data=chunk, timeout=PART_UPLOAD_TIMEOUT_SECONDS
                )
                if not response.ok:
                    raise ResourceCreatingError(
                        "Uploading part {} of {} failed with HTTP {}".format(
                            part_number, filename, response.status_code
                        )
                    )

                parts.append(
                    {"ETag": response.headers["ETag"], "PartNumber": part_number}
                )
                if on_progress:
                    on_progress(len(chunk))

                if len(chunk) < PART_SIZE:
                    return parts
                part_number += 1

    def _abort(self, model_version_id, filename, upload_id):
        try:
            self._presign(
                model_version_id, filename, "abortMultipartUpload", uploadId=upload_id
            )
        except DstkSdkError:
            pass

    def _presign(self, model_version_id, filename, method, **extra):
        data = dict(
            extra, modelVersionId=model_version_id, filename=filename, method=method
        )
        result = self._execute(PRESIGN_URL, {"data": data})
        return result["modelVersion"]["presignURL"]

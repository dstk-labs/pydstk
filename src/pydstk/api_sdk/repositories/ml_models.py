from gql import gql

from pydstk.api_sdk import serializers
from pydstk.api_sdk.repositories.common import BaseRepository, ListResources

MODEL_FIELDS = """
    modelId
    modelName
    description
    isArchived
    project {
        projectId
        name
    }
    storageProvider {
        providerId
        bucket
    }
    currentModelVersion {
        numericVersion
    }
    createdBy {
        realName
    }
    dateCreated
    dateModified
"""

LIST_MODELS = gql(
    """
    query ListMLModels(
        $after: String
        $teamId: String!
        $projectId: String
        $includeArchived: Boolean!
        $modelName: String
    ) {
        model {
            list(
                after: $after
                teamId: $teamId
                projectId: $projectId
                includeArchived: $includeArchived
                modelName: $modelName
            ) {
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
    % MODEL_FIELDS
)

GET_MODEL = gql(
    """
    query GetMLModel($modelId: String!) {
        model {
            get(modelId: $modelId) {
                %s
            }
        }
    }
    """
    % MODEL_FIELDS
)

CREATE_MODEL = gql(
    """
    mutation CreateModel($data: ModelInput!) {
        model {
            create(data: $data) {
                %s
            }
        }
    }
    """
    % MODEL_FIELDS
)

EDIT_MODEL = gql(
    """
    mutation EditModel($modelId: String!, $data: ModelInput!) {
        model {
            edit(modelId: $modelId, data: $data) {
                %s
            }
        }
    }
    """
    % MODEL_FIELDS
)

ARCHIVE_MODEL = gql(
    """
    mutation ArchiveModel($modelId: String!) {
        model {
            archive(modelId: $modelId) {
                %s
            }
        }
    }
    """
    % MODEL_FIELDS
)


def _model_input(project_id, storage_provider_id, name, description):
    return {
        "projectId": project_id,
        "storageProviderId": storage_provider_id,
        "modelName": name,
        "description": description,
    }


class ListModels(ListResources):
    SERIALIZER_CLS = serializers.Model

    def list(self, team_id, project_id=None, include_archived=False, name=None):
        model_dicts = self._fetch_all(
            LIST_MODELS,
            ("model", "list"),
            {
                "teamId": team_id,
                "projectId": project_id,
                "includeArchived": include_archived,
                "modelName": name,
            },
        )
        return self._parse_objects(model_dicts)


class GetModel(BaseRepository):
    SERIALIZER_CLS = serializers.Model

    def get(self, model_id):
        result = self._execute(GET_MODEL, {"modelId": model_id})
        return self._parse_object(result["model"]["get"])


class CreateModel(BaseRepository):
    SERIALIZER_CLS = serializers.Model

    def create(self, project_id, storage_provider_id, name, description):
        data = _model_input(project_id, storage_provider_id, name, description)
        result = self._execute(CREATE_MODEL, {"data": data})
        return self._parse_object(result["model"]["create"])


class EditModel(BaseRepository):
    SERIALIZER_CLS = serializers.Model

    def edit(self, model_id, project_id, storage_provider_id, name, description):
        data = _model_input(project_id, storage_provider_id, name, description)
        result = self._execute(EDIT_MODEL, {"modelId": model_id, "data": data})
        return self._parse_object(result["model"]["edit"])


class ArchiveModel(BaseRepository):
    SERIALIZER_CLS = serializers.Model

    def archive(self, model_id):
        result = self._execute(ARCHIVE_MODEL, {"modelId": model_id})
        return self._parse_object(result["model"]["archive"])

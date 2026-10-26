from gql import gql

from pydstk.api_sdk import serializers
from pydstk.api_sdk.repositories.common import BaseRepository, ListResources

PROJECT_FIELDS = """
    projectId
    name
    description
    isArchived
    createdBy {
        realName
    }
    dateCreated
    dateModified
"""

LIST_PROJECTS = gql(
    """
    query ListProjects(
        $after: String
        $teamId: String!
        $includeArchived: Boolean!
        $projectName: String
    ) {
        project {
            list(
                after: $after
                teamId: $teamId
                includeArchived: $includeArchived
                projectName: $projectName
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
    % PROJECT_FIELDS
)

GET_PROJECT = gql(
    """
    query GetProject($projectId: String!) {
        project {
            get(projectId: $projectId) {
                %s
            }
        }
    }
    """
    % PROJECT_FIELDS
)

CREATE_PROJECT = gql(
    """
    mutation CreateProject($data: ProjectInput!) {
        project {
            create(data: $data) {
                %s
            }
        }
    }
    """
    % PROJECT_FIELDS
)

EDIT_PROJECT = gql(
    """
    mutation EditProject($data: EditProjectInput!) {
        project {
            edit(data: $data) {
                %s
            }
        }
    }
    """
    % PROJECT_FIELDS
)

ARCHIVE_PROJECT = gql(
    """
    mutation ArchiveProject($projectId: String!) {
        project {
            archive(projectId: $projectId) {
                %s
            }
        }
    }
    """
    % PROJECT_FIELDS
)


class ListProjects(ListResources):
    SERIALIZER_CLS = serializers.Project

    def list(self, team_id, include_archived=False, name=None):
        project_dicts = self._fetch_all(
            LIST_PROJECTS,
            ("project", "list"),
            {
                "teamId": team_id,
                "includeArchived": include_archived,
                "projectName": name,
            },
        )
        return self._parse_objects(project_dicts)


class GetProject(BaseRepository):
    SERIALIZER_CLS = serializers.Project

    def get(self, project_id):
        result = self._execute(GET_PROJECT, {"projectId": project_id})
        return self._parse_object(result["project"]["get"])


class CreateProject(BaseRepository):
    SERIALIZER_CLS = serializers.Project

    def create(self, team_id, name, description):
        data = {"teamId": team_id, "name": name, "description": description}
        result = self._execute(CREATE_PROJECT, {"data": data})
        return self._parse_object(result["project"]["create"])


class EditProject(BaseRepository):
    SERIALIZER_CLS = serializers.Project

    def edit(self, project_id, name, description):
        data = {"projectId": project_id, "name": name, "description": description}
        result = self._execute(EDIT_PROJECT, {"data": data})
        return self._parse_object(result["project"]["edit"])


class ArchiveProject(BaseRepository):
    SERIALIZER_CLS = serializers.Project

    def archive(self, project_id):
        result = self._execute(ARCHIVE_PROJECT, {"projectId": project_id})
        return self._parse_object(result["project"]["archive"])

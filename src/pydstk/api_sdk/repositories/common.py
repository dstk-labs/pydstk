import abc

import six
from gql.transport.exceptions import TransportError, TransportQueryError

from pydstk.api_sdk.exceptions import ResourceFetchingError
from pydstk.api_sdk.graphql import graphql_client


@six.add_metaclass(abc.ABCMeta)
class BaseRepository(object):
    SERIALIZER_CLS = None

    def __init__(self, api_key, logger, client_name=None):
        self.api_key = api_key
        self.logger = logger
        self.client_name = client_name

    def _execute(self, document, variables=None, anonymous=False):
        client = graphql_client(api_key=self.api_key, anonymous=anonymous)
        try:
            return client.execute(document, variable_values=variables)
        except TransportQueryError as error:
            message = error.errors[0]["message"] if error.errors else str(error)
            raise ResourceFetchingError(message)
        except TransportError as error:
            raise ResourceFetchingError("DSTK request failed: {}".format(error))

    def _parse_object(self, instance_dict):
        """
        :param dict instance_dict:
        :return: model instance
        """
        return self.SERIALIZER_CLS().get_instance(instance_dict)


@six.add_metaclass(abc.ABCMeta)
class ListResources(BaseRepository):
    def _fetch_all(self, document, path, variables=None):
        """Follows continuation tokens until every page of a connection is read

        :param document: query that takes an `$after` variable
        :param tuple[str] path: keys from the result root to the connection
        :param dict variables:
        :rtype: list[dict]
        """
        nodes = []
        after = None
        while True:
            result = self._execute(document, dict(variables or {}, after=after))
            page = result
            for key in path:
                page = page[key]

            nodes.extend(edge["node"] for edge in page["edges"] or [])

            if not page["pageInfo"]["hasNextPage"]:
                return nodes

            after = page["pageInfo"]["continuationToken"]

    def _parse_objects(self, instance_dicts):
        return [self._parse_object(instance_dict) for instance_dict in instance_dicts]

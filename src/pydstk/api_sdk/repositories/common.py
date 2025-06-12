import abc
import six

from pydstk.api_sdk.graphql import graphql_client


@six.add_metaclass(abc.ABCMeta)
class BaseRepository(object):
    VALIDATION_ERROR_MESSAGE = "Failed to fetch data"

    def __init__(self, api_key, logger, client_name=None):
        self.api_key = api_key
        self.logger = logger
        self.client_name = client_name

    @abc.abstractmethod
    def _get_api_url(self, **kwargs):
        """Get base url to the api

        :rtype: str
        """
        pass

    def _get_client(self, **kwargs):
        """
        :rtype: http_client.API
        """
        client = graphql_client(api_key=self.api_key)
        return client

    def _get(self, **kwargs):
        query = self._get_request_query(kwargs)
        params = self._get_request_params(kwargs)
        url = self._get_api_url(**kwargs)
        client = self._get_client(**kwargs)
        response = self._send_request(client, url, query=query, variable_values=params)

        return response

    def _send_request(self, client, url, json=None, params=None):
        response = client.get(url, json=json, params=params)
        return response

    def _get_request_query(self, kwargs):
        return None

    def _get_request_params(self, kwargs):
        return None


@six.add_metaclass(abc.ABCMeta)
class ListResources(BaseRepository):
    SERIALIZER_CLS = None

    def _parse_objects(self, data, **kwargs):
        instances = []
        instance_dicts = self._get_instance_dicts(data, **kwargs)
        for instance_dict in instance_dicts:
            instance = self._parse_object(instance_dict)
            instances.append(instance)

        return instances

    def _get_instance_dicts(self, data, **kwargs):
        return data

    def _get_meta_data(self, resp):
        pass

    def _parse_object(self, instance_dict):
        """
        :param dict instance_dict:
        :return: model instance
        """
        instance = self.SERIALIZER_CLS().get_instance(instance_dict)
        return instance

    def list(self, **kwargs):
        response = self._get(**kwargs)
        instances = self._get_instances(response, **kwargs)
        return instances

    def _get_instances(self, response, **kwargs):
        if not response.data:
            return []

        objects = self._parse_objects(response.data, **kwargs)
        return objects

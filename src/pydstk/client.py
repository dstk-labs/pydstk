import tempfile

from pydstk import frameworks
from pydstk.api_sdk import clients
from pydstk.api_sdk.config import config
from pydstk.api_sdk.exceptions import UnsupportedModelError


class Client(object):
    def __init__(self, api_key=None, team_id=None):
        """Entry point for using DSTK from Python

        :param str api_key: defaults to PYDSTK_API_KEY, the saved key, then the
            saved login
        :param str team_id: team for methods that need one and aren't given one.
            Defaults to PYDSTK_TEAM_ID, then the team saved with `pydstk teams use`
        """
        options = {"api_key": api_key, "team_id": team_id or config.TEAM_ID or None}

        self.teams = clients.TeamsClient(**options)
        self.projects = clients.ProjectsClient(**options)
        self.storage = clients.StorageProvidersClient(**options)
        self.models = clients.ModelsClient(**options)
        self.versions = clients.ModelVersionsClient(**options)
        self.invitations = clients.InvitationsClient(**options)
        self.users = clients.UsersClient(**options)
        self.api_keys = clients.ApiKeysClient(**options)

    def log_model(self, model, model_id, description=None, publish=False):
        """Save a trained model as a new version of model_id, detecting its framework

        :param model: a scikit-learn, xgboost, lightgbm or torch model
        :param str model_id:
        :param str description:
        :param bool publish: publish the version once the files are uploaded
        :rtype: models.ModelVersion
        """
        framework = frameworks.detect(model)

        with tempfile.TemporaryDirectory() as directory:
            files = framework.save(model, directory)
            metadata = frameworks.describe(framework, model, files)
            version = self.versions.create(model_id, description, metadata)
            self.versions.upload(version.model_version_id, [directory])

        if publish:
            return self.versions.publish(version.model_version_id)
        return version

    def load_model(self, model_version_id):
        """Download a version saved with log_model and load it into memory

        :param str model_version_id:
        :returns: the model, as the framework loads it
        """
        metadata = self.versions.get(model_version_id).metadata or {}
        if "framework" not in metadata:
            raise UnsupportedModelError(
                "{} wasn't saved with log_model, so pydstk doesn't know how to "
                "load it".format(model_version_id)
            )

        framework = frameworks.get(metadata["framework"])
        with tempfile.TemporaryDirectory() as directory:
            self.versions.download(model_version_id, directory, metadata["files"])
            return framework.load(directory, metadata)

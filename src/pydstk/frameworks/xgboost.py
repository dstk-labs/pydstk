import importlib
import json
import os

from pydstk.api_sdk.exceptions import UnsupportedModelError
from pydstk.frameworks.common import Framework

MODEL_FILE = "model.json"


class XGBoostFramework(Framework):
    NAME = "xgboost"

    def save(self, model, directory):
        model.save_model(os.path.join(directory, MODEL_FILE))
        return [MODEL_FILE]

    def params(self, model):
        import xgboost

        if isinstance(model, xgboost.Booster):
            learner = json.loads(model.save_config())["learner"]
            return dict(
                learner["learner_train_param"],
                **learner["gradient_booster"].get("tree_train_param", {}),
            )

        return {
            name: value
            for name, value in model.get_params().items()
            if value is not None
        }

    def load(self, directory, metadata):
        import xgboost

        model_class = _xgboost_class(metadata["model_class"])
        path = os.path.join(directory, MODEL_FILE)
        if model_class is xgboost.Booster:
            return xgboost.Booster(model_file=path)

        model = model_class()
        model.load_model(path)
        return model


def _xgboost_class(path):
    module_name, _, class_name = path.rpartition(".")
    try:
        return getattr(importlib.import_module(module_name), class_name)
    except (ImportError, AttributeError):
        raise UnsupportedModelError(
            "Can't import {} to load this xgboost model".format(path)
        )

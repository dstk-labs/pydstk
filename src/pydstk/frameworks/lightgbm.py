import os

from pydstk.frameworks.common import Framework

BOOSTER_FILE = "model.txt"
ESTIMATOR_FILE = "model.joblib"


class LightGBMFramework(Framework):
    NAME = "lightgbm"

    def save(self, model, directory):
        import joblib
        import lightgbm

        if isinstance(model, lightgbm.Booster):
            model.save_model(os.path.join(directory, BOOSTER_FILE))
            return [BOOSTER_FILE]

        joblib.dump(model, os.path.join(directory, ESTIMATOR_FILE))
        model.booster_.save_model(os.path.join(directory, BOOSTER_FILE))
        return [ESTIMATOR_FILE, BOOSTER_FILE]

    def params(self, model):
        import lightgbm

        if isinstance(model, lightgbm.Booster):
            return model.params
        return model.get_params()

    def load(self, directory, metadata):
        import joblib
        import lightgbm

        if ESTIMATOR_FILE in metadata["files"]:
            return joblib.load(os.path.join(directory, ESTIMATOR_FILE))
        return lightgbm.Booster(model_file=os.path.join(directory, BOOSTER_FILE))

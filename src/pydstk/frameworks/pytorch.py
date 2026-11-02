import os

from pydstk.frameworks.common import Framework

MODEL_FILE = "model.pt"


class PyTorchFramework(Framework):
    NAME = "torch"

    def save(self, model, directory):
        import torch

        torch.save(model, os.path.join(directory, MODEL_FILE))
        return [MODEL_FILE]

    def params(self, model):
        parameters = list(model.parameters())
        return {
            "num_parameters": sum(p.numel() for p in parameters),
            "trainable_parameters": sum(
                p.numel() for p in parameters if p.requires_grad
            ),
            "layers": {
                name: type(child).__name__ for name, child in model.named_children()
            },
        }

    def load(self, directory, metadata):
        import torch

        return torch.load(os.path.join(directory, MODEL_FILE), weights_only=False)

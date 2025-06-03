from keyword_extractor.config import Config
from keyword_extractor.predictor import Predictor


class PredictorFactory:
    """
    Factory class that dynamically instantiates and returns the correct Predictor
    based on the configuration. This approach ensures that only the configured model
    is loaded at startup.
    """

    def __new__(cls, *args, **kwargs) -> Predictor:
        if Config.MODEL == 'gliner':
            from keyword_extractor.gliner import GLiNERModel
            return GLiNERModel(*args, **kwargs)

        raise ValueError(f"Unsupported model: {Config.MODEL}")


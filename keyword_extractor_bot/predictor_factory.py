from keyword_extractor_bot.config import Config
from keyword_extractor_bot.predictor import Predictor


class PredictorFactory:
    """
    Factory class that dynamically instantiates and returns the correct Predictor
    based on the configuration. This approach ensures that only the configured model
    is loaded at startup.
    """

    def __new__(cls, *args, **kwargs) -> Predictor:
        if Config.MODEL == 'ner':
            from keyword_extractor_bot.ner import Ner
            return Ner(*args, **kwargs)

        raise ValueError(f"Unsupported model: {Config.MODEL}")


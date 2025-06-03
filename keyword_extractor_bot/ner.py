from keyword_extractor_bot.config import Config
from keyword_extractor_bot.predictor import Predictor
# import model libraries

class Ner(Predictor):

    # add huggingface model name (e.g. facebook/bart-large-cnn)
    # needed for using the modelinfo endpoint
    model_name = None

    def __init__(self):
        # instantiate model here
        self.model = None

    def predict(self):
        # add inference code here
        raise NotImplementedError("The class Ner must implement the 'predict' method")

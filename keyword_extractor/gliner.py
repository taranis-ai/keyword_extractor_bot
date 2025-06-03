from gliner import GLiNER
from keyword_extractor.config import Config
from keyword_extractor.predictor import Predictor


class GLiNERModel(Predictor):
    model_name = "selfconstruct3d/AITSecNER"

    def __init__(self):
        self.model = GLiNER.from_pretrained("selfconstruct3d/AITSecNER", load_tokenizer=True)
        self.labels = ["CLICommand/CodeSnippet", "CON", "DATE", "GROUP", "LOC", "MALWARE", "ORG", "SECTOR", "TACTIC", "TECHNIQUE", "TOOL"]

    def predict(self, text: str) -> dict[str, str]:
        if entities := self.model.predict_entities(text, self.labels, threshold=Config.CONFIDENCE_THRESHOLD):
            return {entity["text"]: entity["label"] for entity in entities if isinstance(entity, dict) and entity.get("score", 0)}

        return {}

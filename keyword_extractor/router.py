from flask import Flask, Blueprint, jsonify, request
from flask.views import MethodView

from keyword_extractor.predictor import Predictor
from keyword_extractor.predictor_factory import PredictorFactory
from keyword_extractor.decorators import api_key_required, debug_request
from keyword_extractor.config import Config

class BotEndpoint(MethodView):
    def __init__(self, bot: Predictor) -> None:
        super().__init__()
        self.bot = bot

    @debug_request(Config.DEBUG)
    @api_key_required
    def post(self):

        # TODO 
        # Add wordlist extraction
        # Add IOC

        data = request.get_json()
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided for NER extraction"}), 400
        try:
            return jsonify(self.bot.predict(text))
        except ValueError as e:
            return jsonify({"error": str(e)}), 400


class HealthCheck(MethodView):
    @debug_request(Config.DEBUG)
    def get(self):
        return jsonify({"status": "ok"})

class ModelInfo(MethodView):
    def __init__(self, bot: Predictor):
        super().__init__()
        self.bot = bot

    @debug_request(Config.DEBUG)
    def get(self):
        return jsonify(self.bot.modelinfo)


def init(app: Flask):
    bot = PredictorFactory()
    app.url_map.strict_slashes = False
    bot_bp = Blueprint("bot", __name__)
    bot_bp.add_url_rule("/", view_func=BotEndpoint.as_view("predict", bot=bot))
    bot_bp.add_url_rule("/health", view_func=HealthCheck.as_view("health"))
    bot_bp.add_url_rule("/modelinfo", view_func=ModelInfo.as_view("modelinfo", bot=bot))
    app.register_blueprint(bot_bp)

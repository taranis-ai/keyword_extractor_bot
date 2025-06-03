from flask import Flask, Blueprint, jsonify, request
from flask.views import MethodView

from keyword_extractor_bot.predictor import Predictor
from keyword_extractor_bot.predictor_factory import PredictorFactory
from keyword_extractor_bot.decorators import api_key_required, debug_request
from keyword_extractor_bot.config import Config

class BotEndpoint(MethodView):
    def __init__(self, bot: Predictor) -> None:
        super().__init__()
        self.bot = bot

    @debug_request(Config.DEBUG)
    @api_key_required
    def post(self):
        data = request.get_json()

        # pre-process data here and pass it to self.bot.predict method
        # e.g. extracted_data = data.get("key", "")
        #      bot_result = self.bot.predict(extracted_data)
        bot_result = None

        # return bot_result as JSON
        return jsonify({"result": bot_result})


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

from fastapi import FastAPI

from src.common.config import load_settings
from src.common.logger import get_logger
from src.serving.api.routes import register_routes
from src.serving.inference.predictor import ReadmissionPredictor


settings = load_settings()
logger = get_logger("api.main", log_file="artifacts/logs/api.log")

app = FastAPI(title=settings.app.app_name)
predictor = ReadmissionPredictor()

register_routes(app, predictor)

logger.info("API application initialized.")
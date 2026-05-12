from fastapi import HTTPException

from src.common.logger import get_logger
from src.serving.api.schemas import PredictionRequest, PredictionResponse


logger = get_logger("api.routes")

def register_routes(app, predictor) -> None:
    @app.get("/health")
    def health_check(): 
        return {"status": "ok"}
    
    @app.get("/model-info")
    def model_info():
        # return {
        #     "model_name": predictor.model_name,
        #     "model_version": predictor.model_version,
        #     "input_schema": predictor.input_schema,
        #     "output_schema": predictor.output_schema
        # }
        return {
            "model_type": "logistic_regression_pipeline",
            "task": "hospital_readmission_prediction",
            "target": "readmitted_<30",
        }
    
    @app.post("/predict", response_model=PredictionResponse)
    def predict(request: PredictionRequest):
        try:
            payload = request.model_dump()
            result = predictor.predict_one(payload)
            logger.info(f"Prediction successful: {result}")
            return result
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Prediction failed")
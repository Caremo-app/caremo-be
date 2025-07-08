from fastapi import APIRouter, HTTPException
from ...services.ml_services import ArrhythmiaPredictor, PPGInput

predictor = ArrhythmiaPredictor('/app/app/gradient_boost_arrhythmia_model.pkl')

router = APIRouter(
    prefix='/v1/ai',
    tags=['AI']
)

@router.post("/predict")
def predict(name_persona: str, ppg_input: PPGInput):
    result = predictor.predict(ppg_input.signal, ppg_input.sampling_rate)
    if not result.get('success'):
        raise HTTPException(status_code=400, detail=result.get('error', 'Prediction failed'))
    return result

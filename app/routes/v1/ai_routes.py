from fastapi import APIRouter, HTTPException
from ...services.ml_services import ArrhythmiaPredictor, PPGInput
from ...services.whatsapp_services import WhatsAppService, PhoneEnum

predictor = ArrhythmiaPredictor('/app/app/gradient_boost_arrhythmia_model.pkl')
whatsapp_api = WhatsAppService('EAAVChHGh8UABPH2qNukbklV8XWnZC7wPtmsgTMT9uMIgx4MOF8vRPnZAXZAzaZB7PvQH8MK6pwPzGkL6Hx8Rfn8qxIBirZBRuwmVWZBZC1fLZCkrZCbpoQZCZAAAkgNSWHEdVJuJ1PKCab9V3nOLmzyGCibxASS50wgBet2Xc7KvSrvE63pgOcH3KA5ptPlbWkNZBZChaDTVj8nOhnZB0vGZCm9ZC1e17YDu3FK3LEcAwuEJ4zgZBOXVBhAZDZD', '758357087357144')

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

@router.post("/simulate-family")
def simulate_family():
    whatsapp_api.send_template_message(PhoneEnum.NO_EDBERT, 'hello_world', 'Kakek', 'Edbert')
    return {"msg": "Succeed"}

@router.post("/simulate-hospital")
def simulate_hospital():
    return {"msg": "Succeed"}
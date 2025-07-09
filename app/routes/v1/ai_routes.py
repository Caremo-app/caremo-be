from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response
from ...services.ml_services import ArrhythmiaPredictor, PPGInput
from ...services.whatsapp_services import WhatsAppService, PhoneEnum
from ...services.twillio_services import call_hospital
import os

predictor = ArrhythmiaPredictor('/app/app/gradient_boost_arrhythmia_model.pkl')
whatsapp_api = WhatsAppService(os.environ.get("WHATSAPP_TOKEN"), os.environ.get("WHATSAPP_ID"))

router = APIRouter(
    prefix='/v1/ai',
    tags=['AI']
)

@router.post("/predict")
def predict(name_persona: str, ppg_input: PPGInput):
    
    if 60 <= ppg_input.heartbeat <= 100:
        return {"status": "healthy", "message": "Heartbeat normal"}
    
    result = predictor.predict(ppg_input.signal, ppg_input.sampling_rate)
        
    if not result.get('success'):
        raise HTTPException(status_code=400, detail=result.get('error', 'Prediction failed'))
    
    if True: # ini untuk dangerous
        whatsapp_api.send_template_message(
            recipient_number=PhoneEnum.NO_EDBERT.value,
            template_name="hello_world",
            persona_relay="System",
            persona_receive=name_persona
        )
        call_hospital(
            phone_number="+6285345871185",
            persona=name_persona,
            location="Jl. Beringin No. 7, Bekasi"
        )
        
    return result

@router.post("/simulate-family")
def simulate_family():
    whatsapp_api.send_template_message(PhoneEnum.NO_EDBERT, 'hello_world', 'Kakek', 'Edbert')
    return {"msg": "Succeed"}

@router.post("/simulate-hospital")
def simulate_hospital():
    return {"msg": "Succeed"}

@router.get("/twiml")
def twiml(request: Request, persona: str = "Unknown", location: str = "an unknown location"):
    message = f"This is an emergency from {persona}. Please go to {location} immediately. They might have fallen."

    twiml = f"""
    <Response>
        <Say voice="alice" language="en-US">{message}</Say>
    </Response>
    """
    return Response(content=twiml.strip(), media_type="application/xml")

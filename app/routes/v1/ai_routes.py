from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from ...services.ml_services import ArrhythmiaPredictor, PPGInput, Location
from ...services.whatsapp_services import WhatsAppService, PhoneEnum
from ...services.twillio_services import call_hospital
from ...services.geoapify_services import GeoapifyService
from ...util.jwt_generator import verify_token
from ...util.use_db import get_db
from ...repositories.emailfamily_repositories import EmailFamilyRepository
from ...controllers.emailfamily_controllers import EmailFamilyController
import os

predictor = ArrhythmiaPredictor('/app/app/gradient_boost_arrhythmia_model.pkl')
whatsapp_api = WhatsAppService(os.environ.get("WHATSAPP_TOKEN"), os.environ.get("WHATSAPP_ID"))
geo_service = GeoapifyService()

router = APIRouter(
    prefix='/v1/ai',
    tags=['AI']
)


@router.post("/predict")
def predict(
    name_persona: str,
    ppg_input: PPGInput,
    location: Location,
    payload: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    # Early exit if normal
    if 60 <= ppg_input.heartbeat <= 100:
        return {"status": "healthy", "message": "Heartbeat normal"}

    # Predict arrhythmia
    resolved_address = geo_service.reverse_geocode(location.latitude, location.longitude)
    result = predictor.predict(ppg_input.signal, ppg_input.sampling_rate)

    if not result.get('success'):
        raise HTTPException(status_code=400, detail=result.get('error', 'Prediction failed'))

    # Get email from JWT
    user_email = payload['sub']

    # Retrieve family personas
    family_repo = EmailFamilyRepository(db)
    family_controller = EmailFamilyController(family_repo)
    personas = family_controller.get_family_personas(user_email)

    # Filter receivers and send WhatsApp
    receiver_personas = [p for p in personas if p.role == "receiver"]
    for persona in receiver_personas:
        whatsapp_api.send_template_message(
            recipient_number=persona.phone_number,
            template_name="health_warning",
            persona_relay=name_persona,
            persona_receive=persona.name,
            bpm=ppg_input.heartbeat,
            location=resolved_address
        )
      
    # call_hospital(
    #     phone_number="+6285345871185",
    #     persona=name_persona,
    #     location="Jl. Beringin No. 7, Bekasi"
    # )
        
    return result

@router.post("/simulate-family")
def simulate_family(name_persona: str, location: Location, payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    resolved_address = geo_service.reverse_geocode(location.latitude, location.longitude)
    
    user_email = payload['sub']
    
    whatsapp_api.send_template_message(PhoneEnum.NO_AKMAL, 'health_warning', name_persona, 'SYSTEM', 150, resolved_address)
    return {"msg": "Succeed"}

@router.post("/simulate-hospital")
def simulate_hospital(name_persona: str, location: Location, payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    resolved_address = geo_service.reverse_geocode(location.latitude, location.longitude)
    whatsapp_api.send_template_message(PhoneEnum.NO_AKMAL, 'health_warning', name_persona, 'SYSTEM', 150, resolved_address)
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

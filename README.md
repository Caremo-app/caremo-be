# CAREMO Back End

![alt text](<1024x1024 remove bg.png>)

**CAREMO (Care Remote)** is a backend system designed to monitor elderly individuals using wearable devices. The system supports Non-Communicable Disease (NCD) detection, real-time anomaly alerts, family notifications via voice call, and AI-powered health chat. Built with **FastAPI**, **PostgreSQL**, and integrates with **Twilio**, it is optimized for scalable deployment using Docker.


## Features

- **PPG Signal Ingestion** – Accepts real-time PPG signals and metadata from wearable/mobile devices.
- **Anomaly Detection AI** – Triggers alerts for abnormal heart rate or vital signs.
- **Smart Emergency Calling** – Uses Twilio Voice to call family/caretaker upon anomaly.
- **Location Tracking** – Stores last known GPS location of the user.
- **Persona & Family Models** – Links each elderly user to assigned caretakers/family.
- **JWT Authentication** – Secure auth for both mobile clients and admin dashboard.

## Architecture Overview

- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL + SQLAlchemy ORM
- **AI Layer**: Custom anomaly detection model (using SciKit)
- **Notifications**: Twilio Voice API for calls
- **Deployment**: Docker-based with `.env` support
- **Frontend**: To be integrated (separate repo)

## API Endpoint Documentation

> See full docs at `/docs` ([api.caremo.id/docs](https://api.caremo.id/docs))

## 🛠️ Tech Stack

* [FastAPI](https://fastapi.tiangolo.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Twilio Voice API](https://www.twilio.com/voice)
* [Meta WhatsApp Business API](https://developers.facebook.com/docs/whatsapp/)
* [Docker](https://www.docker.com/)
* [NGINX](https://www.nginx.com/)


## 📄 License

MIT License – see `LICENSE` file.


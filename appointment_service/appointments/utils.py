import requests

PATIENT_SERVICE_URL = 'http://localhost:8002/api/patients/'
DOCTOR_SERVICE_URL = 'http://localhost:8003/api/doctors/'

def get_patients():
    try:
        res = requests.get(PATIENT_SERVICE_URL)
        res.raise_for_status()
        return res.json()
    except requests.RequestException:
        return []

def get_doctors():
    try:
        res = requests.get(DOCTOR_SERVICE_URL)
        res.raise_for_status()
        return res.json()
    except requests.RequestException:
        return []

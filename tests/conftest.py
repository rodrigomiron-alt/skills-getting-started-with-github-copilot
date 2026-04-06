import pytest
import copy
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Adicionar src ao path para importar app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Cria um cliente de teste para a API FastAPI"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reseta as atividades para o estado inicial antes de cada teste"""
    # Estado original das atividades
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for intramural and regional tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Co-ed soccer team and recreational play",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["jordan@mergington.edu", "casey@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and mixed media art techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["ava@mergington.edu"]
        },
        "Theater Club": {
            "description": "Drama, acting, and stage performance",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Build and program robots for competitions",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["ryan@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Compete in science competitions and experiments",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 15,
            "participants": ["sarah@mergington.edu", "tom@mergington.edu"]
        }
    }
    
    # Limpar atividades atuais e restaurar estado original
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Reset após teste
    activities.clear()
    activities.update(original_activities)
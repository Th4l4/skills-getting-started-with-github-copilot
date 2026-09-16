"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
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
    "Soccer Club": {
        "description": "Practice soccer skills and compete in friendly matches",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 24,
        "participants": []
    },
    "Track and Field": {
        "description": "Train in running, jumping, and throwing events",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 30,
        "participants": []
    },
    "Art Club": {
        "description": "Explore drawing, painting, and other visual art techniques",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Drama Club": {
        "description": "Develop acting skills and perform theatrical productions",
        "schedule": "Thursdays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": []
    },
    "Debate Club": {
        "description": "Build public speaking and critical thinking skills through debates",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific discoveries",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


def normalize_email(email: str) -> str:
    """Normalize student emails for consistent duplicate checks."""
    return email.strip().lower()


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    normalized_email = normalize_email(email)
    if not normalized_email:
        raise HTTPException(status_code=400, detail="Email is required")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    normalized_participants = [normalize_email(participant) for participant in activity["participants"]]
    if normalized_email in normalized_participants:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")

    # Validate activity still has room for additional participants
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def unregister_participant(activity_name: str, email: str):
    """Remove a student from an activity."""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    normalized_email = normalize_email(email)

    for participant in list(activity["participants"]):
        if normalize_email(participant) == normalized_email:
            activity["participants"].remove(participant)
            return {"message": f"Removed {participant} from {activity_name}"}

    raise HTTPException(status_code=404, detail="Participant not found for this activity")

from fastapi import FastAPI, Body
from ai_utils import get_chapters, create_teacher_persona, get_teacher_persona, create_quests


app = FastAPI()
from typing import ClassVar


@app.get("/")
def home():
    return {"message": "Welcome to the Educational Game API"}


@app.post("/chapters")
def chapters_endpoint(topic: str = Body(...), user_details: str = Body(None)):
    """
    Endpoint to generate chapters for a given topic tailored to a student's details.
    """
    return get_chapters(
        topic,
        user_details
        or "The student has ADHD and has a hard time focusing. They are 14 years old and are interested in video games.",
    )


@app.post("/teacher_persona")
def teacher_persona_endpoint(topic: str = Body(...), user_details: str = Body(None)):
    """
    Endpoint to create teacher personas based on the topic and student's details.
    """
    return create_teacher_persona(
        topic,
        user_details
        or "The student has ADHD and has a hard time focusing. They are 14 years old and are interested in video games.",
    )


@app.get("/teacher_persona/{teacher_name}")
def get_teacher_persona_endpoint(teacher_name: str):
    """
    Endpoint to retrieve details of a specific teacher persona by name.
    """
    return get_teacher_persona(teacher_name)


@app.post("/quests")
def quests_endpoint(
    topic: str = Body(...),
    teacher_name: str = Body(...),
    chapter_name: str = Body(...),
    level: int = Body(...),
    user_details: str = Body(None),
):
    """
    Endpoint to create quests for a specific chapter and teacher persona.
    """
    return create_quests(
        topic,
        teacher_name,
        chapter_name,
        level,
        user_details
        or "The student has ADHD and has a hard time focusing. They are 14 years old and are interested in video games.",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, Body
from ai_utils import chat_with_teacher, get_chapters, create_teacher_persona, get_teacher_persona, create_quests
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
from typing import ClassVar


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. Replace with specific origins for better security.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods.
    allow_headers=["*"],  # Allow all headers.
)


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


@app.get("/chat_with_teacher")
def chat_with_teacher_endpoint(
    teacher_name: str = Body(...),
    topic: str = Body(...),
    user_details: str = Body(None),
    user_msg: str = Body("Continue"),
):
    """
    Endpoint to chat with a teacher persona about a specific chapter and level.
    """
    s = chat_with_teacher(
        teacher_name,
        topic,
        user_details
        or "The student has ADHD and has a hard time focusing. They are 14 years old and are interested in video games.",
        user_msg,
    )

    json_res = {"teacher_response": s}

    return json_res


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

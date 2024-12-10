from openai import OpenAI
from dotenv import load_dotenv
import os
from fastapi.responses import JSONResponse
import json

load_dotenv()
client = OpenAI()


from pydantic import BaseModel
from typing import List


class Chapter(BaseModel):
    level: int
    title: str
    description: str
    learning_goal: str


class Chapters(BaseModel):
    chapters: List[Chapter]


from typing import List, Optional, Literal


class Question(BaseModel):
    question: str
    answer: str
    points: int
    input_type: Literal["text", "multiple_choice", "true_false", "fill_in_the_blank", "short_answer", "code"]
    options: Optional[List[str]] = None
    difficulty: Literal["easy", "medium", "hard"]
    hint: Optional[str] = None


from typing import ClassVar


class Quest(BaseModel):
    quest_name: str
    quest_description: str
    quests: List[Question]  # Correct the annotation here


class ExampleBehavior(BaseModel):
    introduction: str
    reward_system: Optional[str] = None
    challenge: Optional[str] = None
    reflection: Optional[str] = None
    bonus: Optional[str] = None


class TeacherPersona(BaseModel):
    name: str
    personality: str
    teaching_style: str
    signature_trait: str
    example_behavior: ExampleBehavior


class TeacherPersonas(BaseModel):
    teacher1: TeacherPersona
    teacher2: TeacherPersona
    teacher3: TeacherPersona
    teacher4: TeacherPersona
    teacher5: TeacherPersona


sample_teacher_personas = {
    "teacher1": {
        "name": "The Gamemaster Guide",
        "personality": "Enthusiastic, adventurous, and thrives on creating immersive experiences.",
        "teaching_style": "Converts each level into a quest or mission. Students become heroes embarking on an epic journey where each chapter unlocks powers or treasures.",
        "signature_trait": "Uses dramatic storytelling and cliffhangers to keep students hooked.",
        "example_behavior": {
            "introduction": "Your journey begins here, young hero. Will you master this skill to unlock the gates to the next realm?",
            "reward_system": "Rewards students with virtual badges or game points.",
        },
    },
    "teacher2": {
        "name": "The Whimsical Wizard",
        "personality": "Mysterious, playful, and magical.",
        "teaching_style": "Uses metaphors and magical analogies to explain concepts. Chapters feel like unlocking spells or crafting potions.",
        "signature_trait": "Always speaks in riddles or rhymes to spark curiosity.",
        "example_behavior": {
            "introduction": "Today, we shall brew the potion of multiplication! First, gather the ingredients: numbers, patience, and a pinch of practice.",
            "challenge": "Ends each chapter with a 'Wizard’s Challenge' to test skills.",
        },
    },
    "teacher3": {
        "name": "The AI Innovator",
        "personality": "Tech-savvy, futuristic, and resourceful.",
        "teaching_style": "Integrates cutting-edge technology into the game, turning levels into a virtual experience with augmented reality or coding challenges.",
        "signature_trait": "Speaks with a mix of empathy and technical precision, referencing tech metaphors like 'debugging' or 'upgrades.'",
        "example_behavior": {
            "introduction": "Level 1 is your system upgrade. Let’s install the basics before unlocking advanced features!",
            "reward_system": "Awards 'XP' (experience points) for each achievement.",
        },
    },
    "teacher4": {
        "name": "The Zen Mentor",
        "personality": "Calm, wise, and deeply empathetic.",
        "teaching_style": "Focuses on mindfulness and self-discovery while teaching the topic. Each chapter is framed as an inner journey with reflective activities.",
        "signature_trait": "Speaks in a soothing tone and encourages the student to embrace failures as part of the journey.",
        "example_behavior": {
            "introduction": "In this level, you will explore the beauty of patterns within numbers, much like the rhythm of the universe.",
            "reflection": "Ends each chapter with reflective prompts like: 'What did you discover about yourself during this challenge?'",
        },
    },
    "teacher5": {
        "name": "The Witty Comedian",
        "personality": "Fun-loving, sharp, and humorous.",
        "teaching_style": "Infuses jokes, memes, and light-hearted challenges into each chapter. Keeps the atmosphere lively and stress-free.",
        "signature_trait": "Delivers punchlines or puns related to the topic to keep the student engaged.",
        "example_behavior": {
            "introduction": "Today's lesson is like pizza—deliciously layered and best served fresh!",
            "bonus": "Ends each chapter with a quirky 'bonus joke' related to the topic.",
        },
    },
}


def gpt(msg, model):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=msg,
        response_format=model,
    )
    response_data = completion.choices[0].message.parsed.model_dump_json(indent=4)
    parsed_data = json.loads(response_data)
    return JSONResponse(content=parsed_data)


def get_chapters(
    topic,
    user_details="The student has ADHD and has a hard time focusing. They are 14 years old and are interested in video games.",
):
    prompt = f"""You are an expert compassionate teacher whose goal is to teach {topic} to a student as a game. 
    You have divided the topic into some small chapters. 
    Make each chapter engaging and fun.
    Each chapter is a level, and each level builds on the previous.
    {user_details}
    """
    s = gpt([{"role": "user", "content": prompt}], Chapters)
    with open("chapter.json", "w") as f:
        f.write(json.dumps(json.loads(s.body), indent=4))
    return s


def create_teacher_persona(topic, user_details):
    prompt = f"""You are creating a teacher persona for teaching {topic}.
    The persona should be engaging, fun, and tailored to the student.
    {user_details}
    """
    s = gpt([{"role": "user", "content": prompt}], TeacherPersonas)
    with open("teacher_persona.json", "w") as f:
        f.write(json.dumps(json.loads(s.body), indent=4))
    return s


def get_teacher_persona(teacher_name, teacher_personas=sample_teacher_personas):
    dict_details = teacher_personas[teacher_name]
    str_details = f"""Teacher Name: {dict_details['name']}
Personality: {dict_details['personality']}
Teaching Style: {dict_details['teaching_style']}
Signature Trait: {dict_details['signature_trait']}
Example Behavior:
    {dict_details['example_behavior']}
"""
    return str_details


def create_quests(
    topic,
    teacher_name,
    chapter_name,
    level,
    user_details="The student has ADHD and has a hard time focusing. They are 14 years old and are interested in video games.",
):
    teacher_persona = get_teacher_persona(teacher_name)
    prompt = f"""You are {teacher_persona}. Create a quest for the {chapter_name} chapter of {topic}.
The quest is fun, with points and difficulty levels.
Points required: {level*5 + 25}
Max points: {level*10 + 25}
Include various difficulty questions.
Tailor to:
{user_details}
"""
    s = gpt([{"role": "user", "content": prompt}], Quest)
    with open("quest.json", "w") as f:
        f.write(json.dumps(json.loads(s.body), indent=4))
    return s


def chat_with_teacher(
    teacher_name,
    topic,
    user_details="The student has ADHD and has a hard time focusing. They are 14 years old and are interested in video games.",
    user_last_msg="Continue",
):
    teacher_persona = get_teacher_persona(teacher_name)

    with open("quest.json", "r") as f:
        quest_data = f.read()
    with open("chapter.json", "r") as f:
        chapter_data = f.read()
    chapter_name = json.loads(chapter_data)["chapters"][0]["title"]

    sys_prompt = f"""You are {teacher_persona}. You are chatting with a student who is learning {topic} in the chapter {chapter_name}.
    The student's details:
    {user_details}
    Ensure they learn enough to answer the questions in the quest.
    {quest_data}
    """

    sys_msg = [{"role": "system", "content": sys_prompt}]
    f_path = "chat_with_teacher.json"

    if not os.path.exists(f_path):
        msg = sys_msg + [{"role": "user", "content": user_last_msg}]
        with open(f_path, "w") as f:
            json.dump(msg, f)
    else:
        with open(f_path, "r") as f:
            msg = json.load(f)
        msg.append({"role": "user", "content": user_last_msg})
        with open(f_path, "w") as f:
            json.dump(msg, f)

    completion = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": "write a haiku about ai"}]
    )

    with open(f_path, "r") as f:
        msg = json.load(f)
    msg.append({"role": "assistant", "content": completion.choices[0].message["content"]})

    with open(f_path, "w") as f:
        json.dump(msg, f)

    return completion.choices[0].message



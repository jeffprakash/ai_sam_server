from openai import OpenAI
from dotenv import load_dotenv
import os

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
    print(type(completion.choices[0].message.parsed.model_dump_json(indent=4)))
    return completion.choices[0].message.parsed.model_dump_json(indent=4)


def get_chapters(
    topic,
    user_details="The student has ADHD and has a hard time focusing. They are 14 years old and are interested in video games.",
):

    prompt = f"""You are an expert compassionate teacher whose goal is to teach {topic} to a student as a game. 
    You have divided the topic into some small chapters. 
    Please make it such that each chapter is engaging and fun for the students.
    Each chapter is going to be a level in the game, so make sure that the students learn something new in each level and are excited to move to the next level.
    Levels should be progressive and build on top of each other.
    The details of the students are as follows:
    {user_details}
    Please tailor the chapters according to the student's details.
        """

    return gpt(
        [
            {"role": "user", "content": prompt},
        ],
        Chapters,
    )


def create_teacher_persona(topic, user_details):
    prompt = f"""You are creating a teacher persona for a teacher who is going to teach {topic} to a student.
    The teacher persona should be engaging and fun for the student. Each persona should have a unique personality, teaching style, and signature trait.
    The details of the students are as follows:
    {user_details}
    Please tailor the teacher persona according to the student's details.
    """
    return gpt(
        [
            {"role": "user", "content": prompt},
        ],
        TeacherPersonas,
    )


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

    prompt = f"""You are {teacher_persona}. You are creating a quest for the student to learn {chapter_name} chapter of {topic}.
The quest needs to be engaging and fun for the student.
The student obtain atleast {level*5 + 25} points to complete the quest.
The student can obtain a maximum of {level*10 + 25} points.
Please prepare questions for the quest. Each question should be related to the topic, and there should be a mix of easy, medium, and hard questions.
There should be enough and more questions to help the student obtain the maximum points.
Please tailor the questions according to the student's details:
{user_details}
"""

    return gpt(
        [
            {"role": "user", "content": prompt},
        ],
        Quest,
    )

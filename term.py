import json
import time
import sys
import os
from ai_utils import  get_chapters, create_teacher_persona, create_quests, chat_with_teacher 
import sys, time, json, random

def color_text(text, color_code="\033[0m"):
    return f"{color_code}{text}\033[0m"

def slow_print(text, delay=0.009, color="\033[0m"):
    # Using random small delay for variation
    for char in text:
        sys.stdout.write(color + char + "\033[0m")
        sys.stdout.flush()
        time.sleep(delay + random.uniform(0,0.002))
    print()

def spinner(text, duration=2):
    # Slightly quicker rotation for a more dynamic feel
    chars = ['|','/','-','\\']
    end_time = time.time()+duration
    while time.time()<end_time:
        for c in chars:
            sys.stdout.write(f"\r{text} {c}")
            sys.stdout.flush()
            time.sleep(0.05)
    sys.stdout.write("\r"+ " "*len(text)+"\r")

def choose_teacher(teachers_data):
    slow_print("Choose your teacher persona:", color="\033[95m")
    for i,(k,v) in enumerate(teachers_data.items(),1):
        slow_print(f"{i}. {v['name']}", color="\033[94m")
    while True:
        choice = input("> ")
        if choice.isdigit() and 1 <= int(choice) <= len(teachers_data):
            return teachers_data[list(teachers_data.keys())[int(choice)-1]]
        slow_print("Invalid choice. Try again:", color="\033[91m")

def choose_chapter(chapters_data):
    slow_print("Available Chapters:",color="\033[95m")
    for i,c in enumerate(chapters_data["chapters"],1):
        slow_print(f"{i}. {c['title']} - {c['description']}",color="\033[94m")
    while True:
        choice = input("> ")
        if choice.isdigit() and 1 <= int(choice) <= len(chapters_data["chapters"]):
            return chapters_data["chapters"][int(choice)-1]
        slow_print("Invalid choice. Try again:", color="\033[91m")

def choose_difficulty():
    slow_print("Choose difficulty (1-Easy, 2-Medium, 3-Hard):", color="\033[93m")
    while True:
        diff = input("> ")
        if diff in ["1","2","3"]:
            return int(diff)
        slow_print("Invalid choice. Try again:", color="\033[91m")

def main():
    slow_print("Welcome to the Learning Adventure!", color="\033[92m")
    slow_print("Enter the topic:", color="\033[93m")
    topic = input("> ").strip()
    slow_print("Enter details (e.g. 'ADHD,14,games'):", color="\033[93m")
    user_details = input("> ").strip()
    difficulty = choose_difficulty()
    slow_print("Gathering chapters...", color="\033[96m")
    spinner("Thinking",2)
    get_chapters(topic,user_details) # Assume implemented elsewhere
    with open("chapter.json","r") as f:
        chapters_data = json.load(f)
    slow_print("Creating teacher personas...",color="\033[96m")
    spinner("Crafting",2)
    create_teacher_persona(topic,user_details) # Assume implemented elsewhere
    with open("teacher_persona.json","r") as f:
        teacher_personas_data = json.load(f)
    teacher = choose_teacher(teacher_personas_data)
    teacher_name = teacher["name"]
    selected_chapter = choose_chapter(chapters_data)
    slow_print("Creating Quests...",color="\033[96m")
    spinner("Generating",2)
    create_quests(topic,teacher_name,selected_chapter["title"],selected_chapter["level"],user_details) # Assume implemented
    with open("quest.json","r") as f:
        quest_data = json.load(f)

    slow_print(f"\n{teacher_name} says: {teacher.get('example_behavior',{}).get('introduction','Welcome!')}",color="\033[92m")
    slow_print("Start the quest? (y/n)",color="\033[93m")
    if input("> ").lower()!='y':
        slow_print("Come back when ready.",color="\033[91m")
        return

    score=0
    penalty = {1:0,2:1,3:2}[difficulty]
    for q in quest_data["quests"]:
        slow_print(f"\nQuestion: {q['question']}",color="\033[94m")
        ans=input("> ")
        if ans.strip().lower()==q["answer"].lower():
            slow_print("Correct!",color="\033[92m")
            score+=q["points"]
        else:
            slow_print("Incorrect.",color="\033[91m")
            score-=penalty
            if q.get("hint"):
                slow_print(f"Hint: {q['hint']}",color="\033[93m")
                ans2=input("> ")
                if ans2.strip().lower()==q["answer"].lower():
                    slow_print("Correct on second try!",color="\033[92m")
                    score+=q["points"]//2
                else:
                    slow_print("Still incorrect.",color="\033[91m")
                    score-=penalty

        slow_print("Chat with teacher? (y/n)",color="\033[93m")
        if input("> ").lower()=='y':
            while True:
                user_msg=input(color_text("You: ","\033[93m"))
                if user_msg.lower() in ["exit","quit"]:
                    break
                response=chat_with_teacher(teacher_name,topic,user_details,user_msg) # Assume implemented
                slow_print("\nTeacher:",color="\033[95m")
                slow_print(response,color="\033[94m")

    slow_print(f"\nYour total score: {score} points.",color="\033[92m")
    slow_print("\nFinal chat with teacher? (y/n)",color="\033[93m")
    if input("> ").lower()=='y':
        while True:
            user_msg=input(color_text("You: ","\033[93m"))
            if user_msg.lower() in ["exit","quit"]:
                break
            response=chat_with_teacher(teacher_name,topic,user_details,user_msg)
            slow_print("\nTeacher:",color="\033[95m")
            slow_print(response,color="\033[94m")

if __name__=="__main__":
    main()
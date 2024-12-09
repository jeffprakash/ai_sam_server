# ai_sam_server

Here is the documentation for using this FastAPI backend in a React TypeScript frontend.

---

### Base URL
The base URL for all API endpoints is:  
`http://localhost:8000`

---

## **API Endpoints**

### 1. **`GET /`**
**Description:** Returns a welcome message.

**Response:**
```json
{
  "message": "Welcome to the Educational Game API"
}
```

---

### 2. **`POST /chapters`**
**Description:** Generates chapters for a given topic tailored to a student's details.

**Request:**
- `topic` (string, required): The topic to generate chapters for.
- `user_details` (string, optional): Details about the student (default provided if not supplied).

**Request Example:**
```ts
const requestBody = {
  topic: "Mathematics",
  user_details: "The student loves puzzles and logic games, is 15 years old, and struggles with focus."
};
```

**Response Example:**
```json
{
  "chapters": [
    {
      "level": 1,
      "title": "Introduction to Numbers",
      "description": "Learn the basics of numbers and their properties.",
      "learning_goal": "Understand the foundational concepts of numbers."
    },
    {
      "level": 2,
      "title": "Arithmetic Operations",
      "description": "Explore addition, subtraction, multiplication, and division.",
      "learning_goal": "Master basic arithmetic operations."
    }
  ]
}
```

---

### 3. **`POST /teacher_persona`**
**Description:** Creates teacher personas tailored to the topic and student's details.

**Request:**
- `topic` (string, required): The topic to generate a teacher persona for.
- `user_details` (string, optional): Details about the student.

**Request Example:**
```ts
const requestBody = {
  topic: "Science",
  user_details: "The student is 12 years old, loves experiments, and prefers hands-on learning."
};
```

**Response Example:**
```json
{
  "teacher1": {
    "name": "The Gamemaster Guide",
    "personality": "Enthusiastic, adventurous, and thrives on creating immersive experiences.",
    "teaching_style": "Converts each level into a quest or mission.",
    "signature_trait": "Uses dramatic storytelling and cliffhangers.",
    "example_behavior": {
      "introduction": "Your journey begins here, young hero. Will you master this skill to unlock the gates to the next realm?",
      "reward_system": "Rewards students with virtual badges or game points."
    }
  },
  ...
}
```

---

### 4. **`GET /teacher_persona/{teacher_name}`**
**Description:** Retrieves the details of a specific teacher persona by name.

**Path Parameter:**
- `teacher_name` (string, required): The name of the teacher persona.

**Request Example:**
```ts
const teacherName = "teacher1";
```

**Response Example:**
```json
{
  "Teacher Name": "The Gamemaster Guide",
  "Personality": "Enthusiastic, adventurous, and thrives on creating immersive experiences.",
  "Teaching Style": "Converts each level into a quest or mission.",
  "Signature Trait": "Uses dramatic storytelling and cliffhangers.",
  "Example Behavior": {
    "introduction": "Your journey begins here, young hero. Will you master this skill to unlock the gates to the next realm?",
    "reward_system": "Rewards students with virtual badges or game points."
  }
}
```

---

### 5. **`POST /quests`**
**Description:** Creates quests for a specific chapter and teacher persona.

**Request:**
- `topic` (string, required): The topic for the quest.
- `teacher_name` (string, required): The teacher persona name.
- `chapter_name` (string, required): The chapter to generate a quest for.
- `level` (number, required): The current level of the chapter.
- `user_details` (string, optional): Details about the student.

**Request Example:**
```ts
const requestBody = {
  topic: "Physics",
  teacher_name: "teacher2",
  chapter_name: "Newton's Laws of Motion",
  level: 1,
  user_details: "The student is 14 years old, enjoys practical examples, and is interested in space."
};
```

**Response Example:**
```json
{
  "quest_name": "Newton's Laws Adventure",
  "quest_description": "An engaging quest to understand Newton's laws through real-world examples.",
  "quests": [
    {
      "question": "What is the first law of motion?",
      "answer": "An object will remain at rest or in uniform motion unless acted upon by an external force.",
      "points": 10,
      "input_type": "text",
      "difficulty": "easy"
    },
    {
      "question": "Which force is responsible for objects falling to the ground?",
      "answer": "Gravity",
      "points": 15,
      "input_type": "text",
      "difficulty": "medium",
      "hint": "Think of the force pulling us towards the Earth."
    }
  ]
}
```

---

## **React TypeScript Integration**

### Setup Axios for API Calls
Install Axios if not already done:
```bash
npm install axios
```

Create an `api.ts` file:
```ts
import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});

export default API;
```

---

### Example API Calls

#### Fetch Chapters
```ts
import API from "./api";

const fetchChapters = async (topic: string, userDetails?: string) => {
  const response = await API.post("/chapters", {
    topic,
    user_details: userDetails
  });
  return response.data;
};
```

#### Fetch Teacher Personas
```ts
const fetchTeacherPersonas = async (topic: string, userDetails?: string) => {
  const response = await API.post("/teacher_persona", {
    topic,
    user_details: userDetails
  });
  return response.data;
};
```

#### Fetch Specific Teacher Persona
```ts
const fetchTeacherPersona = async (teacherName: string) => {
  const response = await API.get(`/teacher_persona/${teacherName}`);
  return response.data;
};
```

#### Fetch Quests
```ts
const fetchQuests = async (
  topic: string,
  teacherName: string,
  chapterName: string,
  level: number,
  userDetails?: string
) => {
  const response = await API.post("/quests", {
    topic,
    teacher_name: teacherName,
    chapter_name: chapterName,
    level,
    user_details: userDetails
  });
  return response.data;
};
```

---

### Integration Example
```tsx
import React, { useEffect, useState } from "react";
import { fetchChapters, fetchTeacherPersonas, fetchQuests } from "./apiCalls";

const App: React.FC = () => {
  const [chapters, setChapters] = useState([]);
  
  useEffect(() => {
    const fetchData = async () => {
      const chapters = await fetchChapters("Mathematics");
      setChapters(chapters);
    };
    fetchData();
  }, []);
  
  return (
    <div>
      <h1>Educational Game</h1>
      {chapters.map((chapter, index) => (
        <div key={index}>
          <h2>{chapter.title}</h2>
          <p>{chapter.description}</p>
        </div>
      ))}
    </div>
  );
};

export default App;
```

This provides React components to interact with the backend, including example API calls and a simple interface to display data.
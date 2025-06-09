import os
import time
import requests
import fitz  # PyMuPDF
import json
from ollama import chat

# Ensure the Ollama host is set for Docker Compose networking
os.environ["OLLAMA_HOST"] = "http://ollama:11434"

# Wait for the Ollama server to be ready
while True:
    try:
        requests.get("http://ollama:11434")
        break
    except requests.exceptions.ConnectionError:
        print("Waiting for Ollama to start...")
        time.sleep(2)

class ResumeParser:
    def __init__(self):
        self.model = "mistral"  # or your preferred model
        self.skill_pool = {
            "C++", "Azure", "AWS", "Linux", "Docker", "Kubernetes",
            "TensorFlow", "PyTorch",
            "OpenCV", "NumPy"
        }

    def extract_text_from_pdf(self, file) -> str:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def extract_with_llm(self, full_text: str) -> dict:
        prompt = f"""
You are an expert resume parser. Parse the following resume text into JSON with keys:
Name, Email, Phone Number, LinkedIn, Education (list of dicts), Experience (list of dicts), Projects (list of dicts), Skills (list of strings).
Exclude any "Others" section from output.

Resume Text:
\"\"\"{full_text}\"\"\"

Return ONLY a valid JSON object. Do not add explanations.
"""
        response = chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        text = response.message.content

        try:
            parsed_json = json.loads(text)
        except Exception as e:
            print("Error parsing JSON:", e)
            parsed_json = {}
        return parsed_json

    def ask_question(self, full_text: str, question: str) -> str:
        prompt = f"""
You are a helpful assistant that answers questions based on the following resume text:

Resume:
\"\"\"{full_text}\"\"\"

Question: {question}

Answer briefly and clearly.
"""
        response = chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response.message.content

    def calculate_score(self, skills_list) -> tuple:
        if not skills_list:
            return 0, [], list(self.skill_pool)

        flat_skills = set()
        for item in skills_list:
            if isinstance(item, str):
                split_skills = [skill.strip() for skill in item.split(",")]
                flat_skills.update(split_skills)
            elif isinstance(item, dict):
                for v in item.values():
                    if isinstance(v, str):
                        flat_skills.add(v.strip())

        matched = [skill for skill in self.skill_pool if skill.lower() in (s.lower() for s in flat_skills)]
        missing = [skill for skill in self.skill_pool if skill.lower() not in (s.lower() for s in flat_skills)]

        score = int(len(matched) / len(self.skill_pool) * 100)
        return score, matched, missing

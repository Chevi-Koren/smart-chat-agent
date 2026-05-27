import os
from openai import OpenAI
from prompts import SUMMARIZE_PROMPT, TASKS_PROMPT, REPLY_PROMPT
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_ai(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "אתה עוזר AI עסקי חכם ומדויק"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"שגיאה ב-AI: {str(e)}"


def summarize(text: str):
    return call_ai(SUMMARIZE_PROMPT.format(text=text))


def extract_tasks(text: str):
    return call_ai(TASKS_PROMPT.format(text=text))


def generate_reply(text: str):
    return call_ai(REPLY_PROMPT.format(text=text))
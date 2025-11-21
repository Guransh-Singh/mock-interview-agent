from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def call_llm(system_prompt, user_prompt, model = "llama-3.3-70b-versatile"):
    try:
        res = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return res.choices[0].message.content
    except Exception as e:
        print("Groq Error:", e)
        return "{}"

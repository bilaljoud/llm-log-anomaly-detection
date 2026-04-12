import os
# from urllib import response

from openai import OpenAI
from google import genai
import anthropic
import json

def load_prompt(path):
    with open(path, "r") as f:
        prompt = f.read()
    return prompt

def prompt_gpt(log_sequence, prompt_template):
    # Placeholder for actual ChatGPT API call
    print("Prompting GPT with log sequence and prompt template...")
    print("api key: ", os.getenv("OPENAI_API_KEY"))
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # client = OpenAI()
    log_sequence_str = "\n".join(log_sequence)
    # print(f"Filled template: {prompt_template.format(eval_seq=log_sequence_str)}")
    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=[
            {"role": "system", "content": "You are an anomaly detection system analyzing security-relevant windows system events and identifying anomalous activity."},
            {"role": "user", "content": f"{prompt_template.format(eval_seq=log_sequence_str)}"}
        ]
    )
    return response.choices[0].message.content
    # return "Placeholder GPT Response"

def prompt_claude(log_sequence, prompt_template):
    # Placeholder for actual Claude API call
    # In practice, this would involve sending the events and prompt to the API and receiving a response
    # client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    # response = client.messages.create(
    #     model="claude-3-opus-20241022",
    #     max_tokens=500,
    #     temperature=0.2,
    #     messages=[
    #         {"role": "system", "content": "You are an anomaly detection system analyzing security-relevant windows system events and identifying anomalous activity."},
    #         {"role": "user", "content": f"{prompt_template.format(eval_seq=log_sequence)}"}
    #     ]
    # )
    # return response.choices[0].message.content
    # return "Placeholder Claude Response"
    client = anthropic.Client(api_key=os.getenv("CLAUDE_API_KEY"))
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"{prompt_template.format(eval_seq=log_sequence)}"
        }]
    )
    return message.content[0].text

def prompt_gemini(log_sequence, prompt_template):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=f"{prompt_template.format(eval_seq=log_sequence)}"
    )
    return response.text
import os
# from google.generativeai import genai
# import google.generativeai as genai
# from google import genai
import anthropic

# def sanity_check_gpt():
#     print("Performing sanity check for GPT...")
#     # Placeholder for actual ChatGPT API call
#     # In practice, this would involve sending a simple prompt to the API and checking for a valid response
#     # return "GPT Sanity Check Passed"
#     client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
#     response = client.generate_content(
#         model="gemini-1.5-pro",
#         contents=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": "What is 2 + 2?"}
#         ],
#         generation_config={
#             "max_output_tokens": 10,
#             "temperature": 0.0
#         }
#     )
#     return response.text

# def sanity_check_gemini():
#     print("Performing sanity check for Gemini...")
#     # # Placeholder for actual Gemini API call
#     # # In practice, this would involve sending a simple prompt to the API and checking for a valid response
#     # return "Gemini Sanity Check Passed"
#     client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
#     response = client.models.generate_content(
#         model="gemini-3.1-flash-preview",
#         contents="What is 2 + 2?"
#     )
#     return response.text

def sanity_check_claude():
    print("Performing sanity check for Claude...")
    # Placeholder for actual Claude API call
    # In practice, this would involve sending a simple prompt to the API and checking for a valid response
    # return "Claude Sanity Check Passed"
    client = anthropic.Client(api_key=os.getenv("CLAUDE_API_KEY"))
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": "What's 2 + 2?"
        }]
    )
    return message.content[0].text

# print(sanity_check_gemini())
print(sanity_check_claude())



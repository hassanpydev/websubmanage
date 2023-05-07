API_KEY = "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"
# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai

openai.api_key = API_KEY


def create_article(message: str):
    print("Creating article {}".format(message))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f": أكتب مقال من 400 كلمة عن: {message}"}
        ],
    )
    return response['choices'][0].get('message').get("content")


def rephrase_title(title: str) -> dict:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"أعد صياغة هذا عنوان المقال هذا لعنوان جديد: {title.strip()}",
            }
        ],
    )
    return response

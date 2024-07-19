import json
import torch
import webbrowser
from openai import OpenAI

client = OpenAI(
    api_key='sk-proj-0JVE7hHtzn4s0viyhCaBT3BlbkFJt5XQJg8we3UhRAUHS9Mm'
)


def get_response(msg):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": msg,
            }
        ],
        model="gpt-3.5-turbo",
    )


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

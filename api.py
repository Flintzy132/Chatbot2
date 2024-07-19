from openai import OpenAI
import time
import re


def send_answer(text, ):
    client = OpenAI(
        api_key='sk-proj-0JVE7hHtzn4s0viyhCaBT3BlbkFJt5XQJg8we3UhRAUHS9Mm'
    )

    assistant = client.beta.assistants.retrieve("asst_Omtf2IUI6rl6DRbf9dXcPAZV")

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please search the file in the vector and give me only my answer without any other word"
    )

    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id,
                                                       run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            print("Run failed:", run_status.last_error)
            break
        time.sleep(1)

    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    number_of_messages = len(messages.data)
    print(f'Number of messages: {number_of_messages}')

    for message in reversed(messages.data):
        role = message.role
        for content in message.content:
            if content.type == 'text':
                if role == 'assistant':
                    response = content.text.value
                    pattern = r'【\d:\d†source】'
                    cleaned_text = re.sub(pattern, '', response)
                    print(f'\n{role}: {cleaned_text}')
                    return cleaned_text

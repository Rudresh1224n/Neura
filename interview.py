from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_questions(resume_text, interview_type):

    prompt = f"""
    You are a professional AI interviewer.

    Candidate Resume:
    {resume_text}

    Conduct a {interview_type} interview.

    Ask only ONE question at a time.
    Be human-like and conversational.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def continue_interview(chat_history, user_answer):

    messages = []

    for human, ai in chat_history:
        messages.append({
            "role": "user",
            "content": human
        })

        messages.append({
            "role": "assistant",
            "content": ai
        })

    messages.append({
        "role": "user",
        "content": user_answer
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return response.choices[0].message.content
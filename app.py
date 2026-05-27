import gradio as gr
from resume_parser import extract_resume_text
from interview import generate_questions, continue_interview
from cheating_detection import detect_cheating
from gtts import gTTS
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()

resume_text_global = ""


def process_resume(file, interview_type):

    global resume_text_global

    if file is None:
        return (
            "Please upload resume",
            "",
            None
        )

    if not file.name.endswith(".pdf"):
        return (
            "Invalid file. Upload PDF resume.",
            "",
            None
        )

    text = extract_resume_text(file.name)

    if len(text) < 100:
        return (
            "Uploaded file does not look like a resume.",
            "",
            None
        )

    resume_text_global = text

    first_question = generate_questions(
        text,
        interview_type
    )

    tts = gTTS(first_question)

    audio_path = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    ).name

    tts.save(audio_path)

    return (
        "✅ Resume Verified",
        first_question,
        audio_path
    )


def chat_function(message, history):

    response = continue_interview(
        history,
        message
    )

    tts = gTTS(response)

    audio_path = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    ).name

    tts.save(audio_path)

    history.append((message, response))

    return (
        history,
        audio_path
    )


with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown(
        """
        # 🤖 NEURA AI Interviewer
        
        AI Powered Technical + HR Interview Platform
        """
    )

    with gr.Row():

        with gr.Column():

            camera = gr.Image(
                sources=["webcam"],
                streaming=True,
                label="Candidate Camera"
            )

            cheating_status = gr.Textbox(
                label="Monitoring"
            )

            detect_btn = gr.Button(
                "Check Candidate"
            )

        with gr.Column():

            resume = gr.File(
                label="Upload Resume PDF"
            )

            interview_type = gr.Radio(
                ["Technical", "HR"],
                value="Technical",
                label="Interview Type"
            )

            verify_btn = gr.Button(
                "Start Interview"
            )

            verification_output = gr.Textbox(
                label="Resume Status"
            )

    ai_question = gr.Textbox(
        label="AI Interviewer"
    )

    audio_output = gr.Audio(
        autoplay=True
    )

    chatbot = gr.Chatbot()

    msg = gr.Textbox(
        label="Your Answer"
    )

    send_btn = gr.Button(
        "Send Answer"
    )

    detect_btn.click(
        fn=detect_cheating,
        inputs=camera,
        outputs=cheating_status
    )

    verify_btn.click(
        fn=process_resume,
        inputs=[
            resume,
            interview_type
        ],
        outputs=[
            verification_output,
            ai_question,
            audio_output
        ]
    )

    send_btn.click(
        fn=chat_function,
        inputs=[
            msg,
            chatbot
        ],
        outputs=[
            chatbot,
            audio_output
        ]
    )

demo.launch()
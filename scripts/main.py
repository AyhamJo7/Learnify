import gradio as gr
import json
import time
import random
from utils.data_handler import load_subject_text, save_progress, load_progress

# Load progress data
user_progress = load_progress("data/progress.json")

def reset_data():
    global user_progress
    user_progress = {}
    save_progress(user_progress, "data/progress.json")
    return "Progress reset!"

def get_subject_text(grade, subject):
    return load_subject_text(f"data/subjects/Grade{grade}/{subject}.txt")

def llama_response(user_input, username, grade, subject, session_duration):
    # Sample question-answer interaction
    # For demonstration, assume the correct answer is "42"
    correct_answer = "42"
    is_correct = user_input.strip() == correct_answer
    response = "Correct!" if is_correct else f"Try again! The correct answer is {correct_answer}."

    # Track session info
    if username not in user_progress:
        user_progress[username] = {
            "total_sessions": 0,
            "correct_answers": 0,
            "total_questions": 0,
            "time_spent": 0,
            "grade": grade,
            "subject": subject
        }

    user_progress[username]["total_sessions"] += 1
    user_progress[username]["correct_answers"] += 1 if is_correct else 0
    user_progress[username]["total_questions"] += 1
    user_progress[username]["time_spent"] += session_duration

    # Save progress
    save_progress(user_progress, "data/progress.json")

    # Add encouragement
    if is_correct:
        image = random.choice(["assets/images/encouragement1.png", "assets/images/encouragement2.png"])
        return response, image
    else:
        return response, None

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("<h1>Learnify - Interactive Learning Assistant</h1>")
    gr.Markdown("Have fun learning!")

    with gr.Row():
        grade = gr.Dropdown(label="Grade", choices=[str(i) for i in range(1, 7)], value="1")
        subject = gr.Dropdown(label="Subject", choices=["Math", "Science", "English"], value="Math")

    with gr.Row():
        username = gr.Textbox(label="Username")
        start_session = gr.Button("Start Session")

    with gr.Row():
        question_area = gr.Textbox(label="Question", readonly=True)
        answer_area = gr.Textbox(label="Your Answer")
        submit_answer = gr.Button("Submit Answer")

    with gr.Row():
        response_area = gr.Textbox(label="Response")
        image_area = gr.Image(label="Encouragement", visible=False)

    reset_button = gr.Button("Reset Progress")
    reset_output = gr.Textbox(label="Reset Status")

    # Session timer
    session_start_time = gr.State(None)
    session_duration = gr.State(0)

    # Load question on session start
    start_session.click(
        fn=lambda: time.time(),
        inputs=None,
        outputs=session_start_time
    ).success(
        fn=get_subject_text,
        inputs=[grade, subject],
        outputs=question_area
    )

    # Submit answer
    submit_answer.click(
        fn=lambda: time.time() - session_start_time.value if session_start_time.value else 0,
        inputs=None,
        outputs=session_duration
    ).success(
        fn=llama_response,
        inputs=[answer_area, username, grade, subject, session_duration],
        outputs=[response_area, image_area]
    )

    # Reset progress
    reset_button.click(
        fn=reset_data,
        inputs=None,
        outputs=reset_output
    )

demo.launch()
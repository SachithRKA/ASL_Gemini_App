import gradio as gr
import google.generativeai as genai
import os
import markdown
import cv2
import numpy as np 
from tensorflow.keras.models import load_model
import mediapipe as mp
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("API_KEY"))

# Setup the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[])

model = load_model('asl_landmark_mine_model_one.h5')


def preprocess_image(img, target_size=(64, 64)):
    img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0
    return img


def predict_asl_letter(image, model):
    img = preprocess_image(image)
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions)
    asl_letter = chr(predicted_class + ord('A'))
    return asl_letter


def asl_video():
    cap = cv2.VideoCapture(0)
    sentence = ""

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Ignoring empty camera frame.")
            continue

        frame.flags.writeable = False
        results = hands.process(frame)

        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            asl_letter = predict_asl_letter(frame, model)
            cv2.putText(frame, "Predicted Letter: " + asl_letter, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                        2)
            sentence += asl_letter

        cv2.imshow('MediaPipe Hands', frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return sentence


def greet():
    global convo

    sentence = "Hello"
    expected = "Hello"
    questionsRight = 4
    numberOfQuestions = 10
    questionNumber = 5

    sentence = asl_video()
    prompt = f"Analyze the user's sign for \"{expected}\" and provide feedback. Did they sign it correctly? If not, explain what went wrong and how to improve. If they got it right, offer encouragement. The user's sign was \"{sentence}\". This is question number {questionNumber} out of {numberOfQuestions}, and the user has gotten {questionsRight} questions right so far."
    convo.send_message(prompt)
    result = markdown.markdown(convo.last.text)

    return result


if __name__ == "__main__":
    gr.Interface(
        fn=greet,
        inputs=None,
        outputs="html"
    ).launch()

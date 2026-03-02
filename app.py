
from flask import Flask, render_template, Response, redirect, url_for, jsonify, request
import cv2
import mediapipe as mp
import numpy as np
from keras.models import load_model          # 👈 add this
import threading
import pyttsx3
from googletrans import Translator
from db_config import get_db_connection
app = Flask(__name__)

model = load_model("sign_model.h5", compile=False)
with open("labels.txt") as f:
    labels = [line.strip() for line in f if line.strip()]

engine = pyttsx3.init()
translator = Translator()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

cap = None
last_detected = ""
camera_running = False
detection_active = False
detected_history = []
detection_buffer = []
buffer_size = 5

current_lang = "en"
translation_cache = {}

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def translate_text(text):
    global translation_cache
    if not text:
        return text
    if text in translation_cache:
        return translation_cache[text]
    try:
        translated = translator.translate(text, dest=current_lang)
        translation_cache[text] = translated.text
        return translated.text
    except Exception:
        return text

def gen_frames():
    global last_detected, cap, detected_history, camera_running, detection_buffer, detection_active
    while camera_running and cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if detection_active and results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            data = []
            for lm in hand.landmark:
                data.extend([lm.x, lm.y, lm.z])

            if len(data) == model.input_shape[1]:
                prediction = model.predict(np.array([data]))[0]
                class_id = np.argmax(prediction)
                detected_sign = labels[class_id]

                detection_buffer.append(detected_sign)
                if len(detection_buffer) > buffer_size:
                    detection_buffer.pop(0)

                if detection_buffer.count(detected_sign) > buffer_size // 2:
                    if detected_sign != last_detected:
                        last_detected = detected_sign
                        detected_history.append(detected_sign)
                        detection_active = False

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return redirect(url_for('homepage'))

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/sign_to_text')
def sign_to_text():
    return redirect(url_for('sign_to_text_lang', lang=current_lang))

@app.route('/sign_to_text/<lang>')
def sign_to_text_lang(lang):
    global cap, camera_running, detected_history, detection_buffer, last_detected, current_lang, translation_cache, detection_active
    current_lang = lang
    detected_history = []
    detection_buffer = []
    last_detected = ""
    translation_cache = {}
    detection_active = False
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)
    camera_running = True
    return render_template('sign_to_text.html', lang=lang)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_detection', methods=['POST'])
def start_detection():
    global detection_active, last_detected
    last_detected = ""
    detection_active = True
    return jsonify({"status": "started"})

@app.route('/get_sign')
def get_sign():
    return translate_text(last_detected)

@app.route('/get_history')
def get_history():
    translated_words = [translate_text(word) for word in detected_history]
    return jsonify({
        "original": detected_history,
        "translated": translated_words
    })

@app.route('/clear_history', methods=['POST'])
def clear_history():
    global detected_history, last_detected, detection_buffer, translation_cache
    detected_history = []
    last_detected = ""
    detection_buffer = []
    translation_cache = {}
    return jsonify({"status": "ok"})

@app.route('/speak')
def speak():
    global last_detected
    if last_detected:
        threading.Thread(target=speak_text, args=(last_detected,)).start()
        return jsonify({"status": "ok", "spoken": last_detected})
    return jsonify({"status": "error", "message": "No sign detected"})

@app.route('/close_camera')
def close_camera():
    global camera_running, cap, last_detected, detection_buffer, detection_active
    camera_running = False
    detection_active = False
    last_detected = ""
    detection_buffer = []

    if cap is not None and cap.isOpened():
        cap.release()
        cap = None

    return redirect(url_for('homepage'))

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')
    
@app.route('/feedback')
def feedback():
    page = request.args.get('page', default=1, type=int)
    reviews_per_page = 3
    offset = (page - 1) * reviews_per_page

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM feedbacks")
    total_reviews = cursor.fetchone()["total"]
    total_pages = (total_reviews + reviews_per_page - 1) // reviews_per_page

    cursor.execute("""
        SELECT * FROM feedbacks 
        ORDER BY created_at DESC 
        LIMIT %s OFFSET %s
    """, (reviews_per_page, offset))
    reviews = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'feedback.html',
        reviews=reviews,
        total_pages=total_pages,
        current_page=page
    )

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    rating = int(request.form['rating'])
    description = request.form['description']
    reviewer_name = request.form['reviewer_name']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedbacks (rating, description, reviewer_name)
        VALUES (%s, %s, %s)
    """, (rating, description, reviewer_name))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('feedback'))

if __name__ == '__main__':
    app.run(debug=True)

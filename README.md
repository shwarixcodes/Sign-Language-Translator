# Sign Language Translator

**Sign Language Translator** is a web-based application that bridges communication gaps between the deaf and hearing communities.  
It uses AI and computer vision to translate American Sign Language (ASL) gestures into real-time text. Users can also learn ASL interactively with tutorials and an AI-powered chatbot.

---

## 🔑 Key Features
- ✅ **Real-Time Sign Detection**: Captures hand gestures through the camera and instantly converts them into accurate text.  
- ✅ **Multilingual Output**: Supports Hindi, Marathi, and English for wider accessibility.  
- ✅ **Learn with a Chatbot**: Ask the AI how to sign any word or phrase and get visual guidance.  
- ✅ **Feedback System**: Receive suggestions and corrections to improve signing.  
- ✅ **User-Friendly GUI**: Simple and intuitive interface for all users.  

---

## 🧩 Tech Stack
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask)  
- **Machine Learning & Computer Vision:** TensorFlow, OpenCV, MediaPipe  
- **Other Libraries:** Streamlit, NumPy, googletrans  

---

## ⚙️ How It Works
- **Homepage** offers two options: **Sign to Text Translator** and **Chatbot**.  
- **Sign to Text Translator**: Opens the camera, lets users select a language, and translates ASL gestures into text in real-time. A history panel shows previous translations.  
- **Chatbot**: Enter a word or phrase, and it displays the corresponding sign language video from a stored dictionary.  

---

## Installation & Setup

1. **Clone the repository**
    ```bash
    git clone https://github.com/khuship2005/Sign-Language-Translator.git
    cd Sign-Language-Translator
    ```

2. **Create a virtual environment**
    ```bash
    python3.10 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the streamlit chatbot**
    ```bash
    streamlit run chatbot.py
    ```
5. **Run the main application**
    ```bash
    python app.py
    ```
   Access it at `http://localhost:5000` in your web browser.

**Note: Mediapipe requires Python version 3.9 or earlier. Please install a compatible Python version before installing Mediapipe.**

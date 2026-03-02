import cv2
import os
import mediapipe as mp
import shutil

SAVE_DIR = "custom_dataset"

# 🔹 Your NEW dataset labels
LABELS = ["Hello", "Thank_you", "Yes", "No", "Please", 
          "Help", "What", "Where", "More", "Like"]

def reset_dataset():
    """Delete old dataset"""
    if os.path.exists(SAVE_DIR):
        shutil.rmtree(SAVE_DIR)
        print("✅ Old dataset deleted.")
    os.makedirs(SAVE_DIR, exist_ok=True)

def collect_data(label, num_samples=300):
    """Collect data for a given label"""
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
    cap = cv2.VideoCapture(0)
    os.makedirs(f"{SAVE_DIR}/{label}", exist_ok=True)
    collected = 0

    while collected < num_samples:
        ret, frame = cap.read()
        if not ret:
            continue
        image = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0]
            data = []
            for lm in landmarks.landmark:
                data.extend([lm.x, lm.y, lm.z])

            with open(f"{SAVE_DIR}/{label}/{label}_{collected}.txt", "w") as f:
                f.write(",".join(map(str, data)))

            collected += 1
            cv2.putText(image, f"{label}: {collected}/{num_samples}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Collecting Data", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("\n--- Sign Language Dataset Creator ---")
    print("Resetting dataset...")
    reset_dataset()

    for label in LABELS:
        print(f"\n>>> Collecting data for: {label}")
        collect_data(label)

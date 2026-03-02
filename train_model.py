import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

with open("labels.txt") as f:
    LABELS = [line.strip() for line in f]

DATASET_DIR = "custom_dataset"

X, y = [], []

for idx, label in enumerate(LABELS):
    folder = os.path.join(DATASET_DIR, label)
    if not os.path.exists(folder):
        print(f"⚠️ Folder not found: {folder}")
        continue
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            with open(os.path.join(folder, file), "r") as f:
                values = list(map(float, f.read().split(",")))
                X.append(values)
                y.append(idx)

X = np.array(X)
y = np.array(y)

print(f"✅ Dataset Loaded: {X.shape[0]} samples, {len(LABELS)} classes")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training samples: {X_train.shape[0]}, Test samples: {X_test.shape[0]}")

model = Sequential([
    Dense(128, activation='relu', input_shape=(X.shape[1],)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(len(LABELS), activation='softmax')
])

model.compile(
    optimizer=Adam(0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(
    X_train, y_train,
    epochs=30,
    batch_size=16,
    validation_data=(X_test, y_test)
)

model.save("sign_model.h5")
print("✅ Model trained and saved as sign_model.h5")
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

# --------------------
# LOAD DATASET
# --------------------
df = pd.read_csv("fake_news_sample_dataset.csv")

# Use title + text as input
df["content"] = df["title"] + " " + df["text"]

# --------------------
# SPLIT DATA
# --------------------
X = df["content"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --------------------
# FEATURE EXTRACTION
# --------------------
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# --------------------
# TRAIN MODEL
# --------------------
model = PassiveAggressiveClassifier(max_iter=1000)
model.fit(X_train_vec, y_train)

# --------------------
# EVALUATE
# --------------------
y_pred = model.predict(X_test_vec)
acc = accuracy_score(y_test, y_pred)

print("\n======================================")
print("      FAKE NEWS DETECTION RESULT")
print("======================================")
print(f"\nModel Accuracy: {acc * 100:.2f}%")

cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:")
print(cm)

# --------------------
# HEATMAP OUTPUT
# --------------------
plt.imshow(cm, cmap="hot")
plt.title("Fake News Heatmap Output")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.colorbar()
plt.show()

# --------------------
# USER INPUT PREDICTION
# --------------------
while True:
    print("\n---------------------------------")
    user_text = input("Enter a news article to check (or type 'exit'): ")

    if user_text.lower() == "exit":
        break

    user_vec = vectorizer.transform([user_text])
    result = model.predict(user_vec)[0]

    print("\nPrediction:", "FAKE ❌" if result == "fake" else "REAL ✔")

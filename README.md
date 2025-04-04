# 🧬 BioLens: AI-Powered Calorie & Wellness Tracker

**BioLens** is an intelligent health and nutrition companion that simplifies calorie tracking using AI. It integrates real-time visual recognition, e-message food classification, e-bill analysis, and personalized wellness insights — all designed to encourage healthier eating habits and lifestyle improvements.

---

## 🌟 Key Features

### 🍔 Food Detection with AI
- Snap a picture of your meal and instantly get **calorie estimates**.
- Built using **custom image recognition models** (no YOLO dependency).

### 📩 E-Message & SMS Classification
- Classifies grocery orders from messages into **healthy** or **junk** categories.
- Learns from past food purchase patterns to give suggestions.

### 📑 E-Bill Reader and Logger
- Automatically reads online bills and logs your **food purchases**.
- Tracks how much you're spending on unhealthy foods.

### 📊 Weekly Reports & AI Insights
- Generates weekly insights based on food consumption.
- Detects patterns and suggests small changes for **sustainable health**.

### 🤖 Smart Meal Suggestions *(Hackathon Feature)*
- Suggests meals according to **your body type, health goals, and conditions**.
- Tracks your lifestyle and adapts suggestions using machine learning.

---

## 🔮 Coming Soon

- 🧘‍♀️ **Posture Detection** using MediaPipe
- 🏋️ **Exercise Tracker** with AI-based **rep counting & form correction**
- 🧠 Mood-based meal suggestions using facial emotion recognition
- 🌍 AI-powered **Calorie Lens** for global cuisines

---

## 💻 Tech Stack

| Layer        | Tech Used                         |
|--------------|-----------------------------------|
| Backend      | Supabase, Firebase, Flask         |
| AI/ML        | Python, OpenCV, NumPy, Pandas     |
| Model        | Custom CNNs for food recognition  |
| Notification | Firebase Cloud Messaging (FCM)    |

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/yourusername/BioLens.git
cd BioLens

# Install Python dependencies
pip install -r requirements.txt

# Run backend API
python app.py

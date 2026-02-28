# AI-Stylist-Smart-Clothing-Recommendation-System-
AI-powered personal stylist that detects body proportions using pose estimation and recommends sustainable, body-shape-based outfit suggestions aligned with SDG 12.
# 👗🤖 AI Personal Stylist – Body Shape Based Outfit Recommender

## 🌍 Domain
Sustainable Fashion | SDG 12 – Responsible Consumption & Production

## 🎯 Project Overview
AI Personal Stylist is an intelligent fashion recommendation system that analyzes body proportions from a full-body image using pose estimation techniques and suggests personalized, body-shape-appropriate outfits with sustainable alternatives.

The goal is to promote confident styling while encouraging responsible fashion consumption.

---

## 🧍 Core Feature – Body Shape Detection

User uploads a full-body image.

The system uses pose estimation (MediaPipe / keypoint detection) to extract body measurements:

- Shoulder width
- Waist width
- Hip ratio
- Height proportions

Based on computed ratios, body type is classified into:

- Rectangle
- Hourglass
- Pear
- Apple
- Inverted Triangle

---

## 👗 Smart Outfit Recommendation Engine

Each body type receives personalized suggestions:

- Pear → A-line skirts, V-neck tops
- Rectangle → Belted dresses, Peplum tops
- Inverted Triangle → Bootcut jeans, Wide-leg trousers
- Apple → Empire waist dresses
- Hourglass → Fitted silhouettes

---

## 🎨 AI Color Palette Suggestion

- Detects dominant skin tone using image processing.
- Suggests flattering color combinations.
- Example: “Pastel blue + beige complements your tone.”

---

## 🎉 Occasion-Based Styling

User selects event type:
- Interview
- Casual
- Party
- Wedding

System adapts outfit recommendations accordingly.

---

## 🌱 Eco-Friendly Fashion Suggestions

Each outfit recommendation includes a sustainable alternative:

Example:
Instead of Polyester → Organic Cotton (reduces CO₂ impact)
Encourages mindful and responsible consumption.

---

## 📈 Confidence Score & Trend Check

- Each recommendation includes a confidence percentage.
- Indicates whether the outfit is trending or classic.
- Based on a small curated fashion trend dataset.

---

## 🚀 Future Enhancements

- Virtual Try-On using clothing overlay (Prototype planned)
- Generative AI Fashion Designer (Stable Diffusion integration)
- Real-time fashion trend API integration
- Mobile application deployment

---

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe (Pose Estimation)
- NumPy
- Pandas
- Machine Learning
- Flask / Streamlit (if used)

---

## 📂 Project Structure

AI-Personal-Stylist/
│
├── app.py
├── body_detection.py
├── recommendation_engine.py
├── dataset.csv
├── requirements.txt
└── README.md

---

## 👩‍💻 Author
Priya Jha

# 🌍 Personalized Carbon Emission Calculator

A Streamlit-based interactive web app that helps users estimate their personal carbon emissions across four major lifestyle categories and provides actionable insights to reduce their footprint. This tool also includes a **chatbot powered by Google Gemini** that answers user queries related to sustainability and emissions reduction.

---
## 📁 Folder Structure

```bash
Personalized-Carbon-Emission-Calculator/
│
├── app.py               # Main Streamlit application
└── requirements.txt     # Required Python libraries
```
---

## 🔍 Features

- 🔢 **Category-wise Emission Calculation**  
  Calculates your annual CO₂ emissions based on:
  - 🚗 **Transportation** (km/day)
  - 💡 **Electricity Usage** (kWh/month)
  - 🍽️ **Diet** (meals/day)
  - 🗑️ **Waste** (kg/week)

- 📊 **Visual Insights**  
  Generates a **dynamic pie chart** showing the proportion of your carbon footprint from each category.

- 🤖 **Carbon Reduction Chatbot**  
  Integrated chatbot using **Google Gemini API**:
  - Provides tailored advice based on your inputs
  - Only answers questions about sustainability, emissions, green practices, etc.

---

## 🚀 How It Works

1. Select your country (currently supports **India**).
2. Enter your lifestyle data:
   - Daily travel in km
   - Monthly electricity usage
   - Weekly waste generation
   - Daily meals
3. The app:
   - Converts inputs to yearly values
   - Calculates category-wise emissions
   - Displays totals in **tonnes/year**
4. Chat with the **Gemini-powered assistant** for improvement strategies.

---

## 💬 Chatbot with Google Gemini

> **To use the chatbot**, you must enter your **Google Gemini API key**.

### How to get your API key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Log in with your Google account
3. Click **"Create API Key"**
4. Copy and paste the key into the input field in the app

---

## 📦 Installation

```bash
- git clone https://github.com/yourusername/Personalized-Carbon-Emission-Calculator.git
  cd Personalized-Carbon-Emission-Calculator

- pip install streamlit plotly pandas google-generativeai
```
---

## 📈 Future Improvements

  - Support for more countries and emission factors
  - Export report as PDF
  - Integration with real-time energy footprint APIs
  - Save and compare history of footprints

---

Built with 💚 by \[LOVENEW YADAV] — a simple and powerful demonstration of Streamlit + Plotly + Gemini AI for personalized carbon footprint analysis and sustainability awareness.

# 🌍 Personalized Carbon Emission Calculator 

An interactive web application built using HTML, CSS, and JavaScript that helps users estimate their personal carbon emissions across four key lifestyle categories. This tool provides visual insights through a pie chart and suggests practical tips for reducing one's carbon footprint—all running directly in your browser without any server or backend.

---
## 📁 Folder Structure

```bash
Personalized-Carbon-Emission-Calculator/
│
├── index.html     # Main web page
├── style.css      # Styling for layout and visuals
└── script.js      # Logic for emission calculation and pie chart rendering
```
---
## 🔍 Features

  - 🔢 **Category-wise Emission Calculator**
    Estimates annual CO₂ emissions based on:

    - 🚗 **Transportation** (km/day)
    - 💡 **Electricity Usage** (kWh/month)
    - 🍽️ **Diet** (meals/day)
    - 🗑️ **Waste** (kg/week)

  - 📊 **Live Visual Insights**
      Generates a dynamic pie chart using the input data
      Displays total carbon footprint in tonnes per year

  - 🤖 **Carbon Reduction Chatbot**  
    Integrated chatbot using **Google Gemini API**:
  - Provides tailored advice based on your inputs
  - Only answers questions about sustainability, emissions, green practices, etc.

---
## 🚀 How It Works
 
 1. Open index.html in any modern browser.
 
 2. Enter your:
  - Daily distance traveled (km)
  - Monthly electricity usage (kWh)
  - Weekly waste generated (kg)
  - Number of daily meals (avg.)
 
 3. Click “Calculate Emissions”.

 4. The app:
    - Converts inputs to yearly emissions
    - Calculates per-category and total carbon footprint
    - Renders a pie chart visualizing the breakdown
    - Displays relevant eco-friendly tips for each input category
---

## 💬 Chatbot with Google Gemini

> **To use the chatbot**, you must enter your **Google Gemini API key**.

### How to get your API key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Log in with your Google account
3. Click **"Create API Key"**
4. Copy and paste the key into the input field in the app

---

## 💡 Future Improvements
 - Add ability to export the chart and summary as PDF
 - Support for different countries' emission factors
 - Allow users to save and compare historical data (via localStorage)
 - Improve tips with collapsible sections or tooltips

---

Built with 💚 by \[LOVENEW YADAV] — a simple and powerful demonstration of Streamlit + Plotly + Gemini AI for personalized carbon footprint analysis and sustainability awareness.

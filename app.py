import streamlit as st
import plotly.express as px
import pandas as pd

# Try to import google.generativeai with error handling
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    st.error("⚠️ Google Generative AI package is not installed!")
    st.code("pip install google-generativeai", language="bash")
    st.stop()

# Define emission factors (example values, replace with accurate data)
EMISSION_FACTORS = {
    "India": {
        "Transportation": 0.14,  # kgCO2/km
        "Electricity": 0.82,  # kgCO2/kWh
        "Diet": 1.25,  # kgCO2/meal, 2.5kgco2/kg
        "Waste": 0.1  # kgCO2/kg
    }
}

# Set wide layout and page name
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

# Streamlit app code
st.title("Personalized Carbon Emission Calculator ⚠️")

# User inputs
st.subheader("🌍 Your Country")
country = st.selectbox("Select", ["India"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚗 Daily Travel Footprint (in km)")
    distance = st.slider("Distance", 0.0, 100.0, key="distance_input")

    st.subheader("💡 Electricity consumption per month (in kWh)")
    electricity = st.slider("Electricity", 0.0, 1000.0, key="electricity_input")

with col2:
    st.subheader("🗑️ Waste generated per week (in kg)")
    waste = st.slider("Waste", 0.0, 100.0, key="waste_input")

    st.subheader("🍽️ Meals consumed per day")
    meals = st.number_input("Meals", 0, key="meals_input")

# Normalize inputs
if distance > 0:
    distance = distance * 365  # Convert daily distance to yearly
if electricity > 0:
    electricity = electricity * 12  # Convert monthly electricity to yearly
if meals > 0:
    meals = meals * 365  # Convert daily meals to yearly
if waste > 0:
    waste = waste * 52  # Convert weekly waste to yearly

# Calculate carbon emissions
transportation_emissions = EMISSION_FACTORS[country]["Transportation"] * distance
electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * electricity
diet_emissions = EMISSION_FACTORS[country]["Diet"] * meals
waste_emissions = EMISSION_FACTORS[country]["Waste"] * waste

# Convert emissions to tonnes and round off to 2 decimal points
transportation_emissions = round(transportation_emissions / 1000, 2)
electricity_emissions = round(electricity_emissions / 1000, 2)
diet_emissions = round(diet_emissions / 1000, 2)
waste_emissions = round(waste_emissions / 1000, 2)

# Calculate total emissions
total_emissions = round(
    transportation_emissions + electricity_emissions + diet_emissions + waste_emissions, 2
)

if st.button("Calculate CO2 Emissions"):

    # Display results
    st.header("Results")

    # Create data for pie chart
    categories = ["🚗 Transportation", "💡 Electricity", "🍽️ Diet", "🗑️ Waste"]
    emissions_values = [transportation_emissions, electricity_emissions, diet_emissions, waste_emissions]

    # Filter out zero values for better visualization
    filtered_data = [(cat, val) for cat, val in zip(categories, emissions_values) if val > 0]

    if filtered_data:
        filtered_categories, filtered_values = zip(*filtered_data)

        # Create DataFrame for pie chart
        df_pie = pd.DataFrame({
            'Category': filtered_categories,
            'Emissions': filtered_values
        })

        # Create pie chart
        fig = px.pie(df_pie,
                     values='Emissions',
                     names='Category',
                     title='Carbon Emissions Distribution by Category',
                     color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])

        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            showlegend=True,
            width=500,
            height=400,
            font=dict(size=12)
        )

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Carbon Emissions by Category")
        st.info(f"🚗 Transportation: {transportation_emissions} tonnes CO2 per year")
        st.info(f"💡 Electricity: {electricity_emissions} tonnes CO2 per year")
        st.info(f"🍽️ Diet: {diet_emissions} tonnes CO2 per year")
        st.info(f"🗑️ Waste: {waste_emissions} tonnes CO2 per year")

    with col4:
        st.subheader("Total Carbon Footprint")
        st.success(f"🌍 Your total carbon footprint is: {total_emissions} tonnes CO2 per year")
        st.warning("According to sources like Worldometer and IEA, India's CO2 emissions per capita was 1.89 tons of CO2 per person in 2022. This was an increase from 1.79 tons per person in 2021.")

    # Display pie chart
    if filtered_data:
        st.subheader("📊 Emissions Breakdown")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Enter some values above to see the emissions breakdown chart!")

    # Additional insights
    if total_emissions > 0:
        st.subheader("💡 Insights & Recommendations")

        # Find the highest emission category
        max_emission = max(emissions_values)
        max_category_index = emissions_values.index(max_emission)
        max_category = categories[max_category_index].split(' ', 1)[1]  # Remove emoji

        if max_emission > 0:
            st.info(f"🎯 Your highest emission source is **{max_category}** at {max_emission} tonnes CO2/year")

            # Provide category-specific recommendations
            recommendations = {
                "Transportation": "Consider using public transport, carpooling, or electric vehicles to reduce transportation emissions.",
                "Electricity": "Switch to renewable energy sources, use energy-efficient appliances, and reduce overall consumption.",
                "Diet": "Consider reducing meat consumption, eating locally sourced food, and minimizing food waste.",
                "Waste": "Focus on reducing, reusing, and recycling. Compost organic waste and buy products with minimal packaging."
            }

            if max_category in recommendations:
                st.success(f"💚 Recommendation: {recommendations[max_category]}")

        # Compare with national average
        if total_emissions > 1.9:
            st.warning(
                f"⚠️ Your footprint ({total_emissions} tonnes) is above India's average of 1.9 tonnes per capita.")
        else:
            st.success(
                f"✅ Great! Your footprint ({total_emissions} tonnes) is below India's average of 1.9 tonnes per capita.")

# Carbon Emission Chatbot Section
st.header("🤖 Carbon Reduction Assistant")
st.write(
    "Ask me anything about reducing your carbon footprint! I can help with tips, strategies, and personalized advice based on your emissions profile.")

# Initialize Gemini client
if 'gemini_client' not in st.session_state:
    # User needs to add their API key
    api_key = st.text_input("Enter your Google Gemini API Key:", type="password", key="api_key_input",
                            help="Get your API key from: https://makersuite.google.com/app/apikey")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # FIXED: Use the current model name instead of deprecated 'gemini-pro'
            model = genai.GenerativeModel('gemini-1.5-flash')
            st.session_state.gemini_model = model
            st.success("✅ Gemini API key configured successfully!")
        except Exception as e:
            st.error(f"❌ Invalid API key or connection error: {str(e)}")
    else:
        st.info("🔑 Please enter your Google Gemini API key to use the chatbot.")
        st.markdown("**How to get your Gemini API key:**")
        st.markdown("1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)")
        st.markdown("2. Sign in with your Google account")
        st.markdown("3. Click 'Create API Key'")
        st.markdown("4. Copy and paste the key above")

# Chat functionality
if 'gemini_model' in st.session_state:
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Function to check if question is carbon-related
    def is_carbon_related(question):
        carbon_keywords = [
            'carbon', 'emission', 'footprint', 'co2', 'climate', 'environment',
            'green', 'sustainable', 'energy', 'transport', 'electricity', 'diet',
            'waste', 'pollution', 'renewable', 'reduce', 'eco', 'environmental'
        ]
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in carbon_keywords)

    # Function to get chatbot response using Gemini
    def get_chatbot_response(user_question, user_emissions_data):
        if not is_carbon_related(user_question):
            return "I'm sorry, but I can only help with questions related to carbon emissions and environmental sustainability. Please ask me something about reducing your carbon footprint, sustainable living, or environmental impact."

        # Create context with user's emission data
        if user_emissions_data['total'] > 0:
            context = f"""
            You are a carbon footprint reduction specialist. The user's current emissions are:
            - Transportation: {user_emissions_data['transportation']} tonnes CO2/year
            - Electricity: {user_emissions_data['electricity']} tonnes CO2/year  
            - Diet: {user_emissions_data['diet']} tonnes CO2/year
            - Waste: {user_emissions_data['waste']} tonnes CO2/year
            - Total: {user_emissions_data['total']} tonnes CO2/year

            Provide specific, actionable advice for reducing carbon emissions based on their current footprint. Be concise and practical.
            Only answer questions related to carbon footprint, sustainability, and environmental impact.

            User Question: {user_question}
            """
        else:
            context = f"""
            You are a carbon footprint reduction specialist. The user hasn't calculated their emissions yet, but they're asking about carbon footprint reduction.

            Provide general, actionable advice for reducing carbon emissions. Be concise and practical.
            Only answer questions related to carbon footprint, sustainability, and environmental impact.
            Encourage them to use the calculator above to get personalized recommendations.

            User Question: {user_question}
            """

        try:
            response = st.session_state.gemini_model.generate_content(context)
            return response.text
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}. Please check your API key and try again."

    # Chat interface
    with st.container():
        # Display chat history
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            with st.expander(f"Q{i + 1}: {question[:50]}..." if len(question) > 50 else f"Q{i + 1}: {question}"):
                st.write(f"**You:** {question}")
                st.write(f"**Assistant:** {answer}")

        # Input for new question
        user_input = st.text_input("Ask your carbon footprint question:", key="chat_input",
                                   placeholder="e.g., How can I reduce my transportation emissions?")

        col_send, col_clear = st.columns([1, 4])
        with col_send:
            send_button = st.button("Send", key="send_btn")
        with col_clear:
            if st.button("Clear Chat History", key="clear_btn"):
                st.session_state.chat_history = []
                st.rerun()

        if send_button and user_input:
            # Prepare user emissions data for context (use 0 if not calculated yet)
            emissions_data = {
                'transportation': transportation_emissions if 'transportation_emissions' in locals() else 0,
                'electricity': electricity_emissions if 'electricity_emissions' in locals() else 0,
                'diet': diet_emissions if 'diet_emissions' in locals() else 0,
                'waste': waste_emissions if 'waste_emissions' in locals() else 0,
                'total': total_emissions if 'total_emissions' in locals() else 0
            }

            # Get response
            with st.spinner("Thinking..."):
                response = get_chatbot_response(user_input, emissions_data)

            # Add to chat history
            st.session_state.chat_history.append((user_input, response))

            # Clear the input and rerun
            st.rerun()

    # Quick suggestion buttons
    st.subheader("💡 Quick Questions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Reduce Transportation Emissions", key="transport_btn"):
            st.session_state.quick_question = "What are the best ways to reduce my transportation carbon emissions?"

    with col2:
        if st.button("Save Energy at Home", key="energy_btn"):
            st.session_state.quick_question = "How can I reduce my electricity consumption and carbon footprint at home?"

    with col3:
        if st.button("Sustainable Diet Tips", key="diet_btn"):
            st.session_state.quick_question = "What dietary changes can help me reduce my carbon footprint?"

    # Handle quick questions
    if 'quick_question' in st.session_state:
        emissions_data = {
            'transportation': transportation_emissions if 'transportation_emissions' in locals() else 0,
            'electricity': electricity_emissions if 'electricity_emissions' in locals() else 0,
            'diet': diet_emissions if 'diet_emissions' in locals() else 0,
            'waste': waste_emissions if 'waste_emissions' in locals() else 0,
            'total': total_emissions if 'total_emissions' in locals() else 0
        }

        with st.spinner("Getting personalized advice..."):
            response = get_chatbot_response(st.session_state.quick_question, emissions_data)

        st.session_state.chat_history.append((st.session_state.quick_question, response))
        del st.session_state.quick_question
        st.rerun()

# Sample questions section
st.subheader("❓ Example Questions You Can Ask")
sample_questions = [
    "What's the most effective way to reduce my carbon footprint?",
    "How can I make my daily commute more sustainable?",
    "What are some eco-friendly alternatives for my high electricity usage?",
    "How does my diet impact my carbon emissions?",
    "What are some zero-waste practices I can adopt?",
    "How can I offset my carbon emissions?",
    "What renewable energy options are available for homes?",
    "How can I reduce food waste and its environmental impact?"
]

for i, question in enumerate(sample_questions, 1):
    st.write(f"{i}. {question}")


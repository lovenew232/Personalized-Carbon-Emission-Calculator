// Emission factors
const EMISSION_FACTORS = {
    "India": {
        "Transportation": 0.14,  // kgCO2/km
        "Electricity": 0.82,     // kgCO2/kWh
        "Diet": 1.25,            // kgCO2/meal
        "Waste": 0.1             // kgCO2/kg
    }
};

let apiKey = '';
let chatHistory = [];
let userEmissions = {
    transportation: 0,
    electricity: 0,
    diet: 0,
    waste: 0,
    total: 0
};

// Update slider values in real-time
document.getElementById('distance').addEventListener('input', function() {
    document.getElementById('distanceValue').textContent = this.value;
});

document.getElementById('electricity').addEventListener('input', function() {
    document.getElementById('electricityValue').textContent = this.value;
});

document.getElementById('waste').addEventListener('input', function() {
    document.getElementById('wasteValue').textContent = this.value;
});

// Enter key support for chat
document.getElementById('chatInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function calculateEmissions() {
    const country = document.getElementById('country').value;
    const distance = parseFloat(document.getElementById('distance').value) * 365; // Convert to yearly
    const electricity = parseFloat(document.getElementById('electricity').value) * 12; // Convert to yearly
    const waste = parseFloat(document.getElementById('waste').value) * 52; // Convert to yearly
    const meals = parseFloat(document.getElementById('meals').value) * 365; // Convert to yearly

    // Calculate emissions
    const transportationEmissions = EMISSION_FACTORS[country]["Transportation"] * distance;
    const electricityEmissions = EMISSION_FACTORS[country]["Electricity"] * electricity;
    const dietEmissions = EMISSION_FACTORS[country]["Diet"] * meals;
    const wasteEmissions = EMISSION_FACTORS[country]["Waste"] * waste;

    // Convert to tonnes and round
    userEmissions.transportation = Math.round((transportationEmissions / 1000) * 100) / 100;
    userEmissions.electricity = Math.round((electricityEmissions / 1000) * 100) / 100;
    userEmissions.diet = Math.round((dietEmissions / 1000) * 100) / 100;
    userEmissions.waste = Math.round((wasteEmissions / 1000) * 100) / 100;
    userEmissions.total = Math.round((userEmissions.transportation + userEmissions.electricity + userEmissions.diet + userEmissions.waste) * 100) / 100;

    // Display results
    document.getElementById('transportResult').textContent = `${userEmissions.transportation} tonnes CO2/year`;
    document.getElementById('electricityResult').textContent = `${userEmissions.electricity} tonnes CO2/year`;
    document.getElementById('dietResult').textContent = `${userEmissions.diet} tonnes CO2/year`;
    document.getElementById('wasteResult').textContent = `${userEmissions.waste} tonnes CO2/year`;
    document.getElementById('totalEmissions').textContent = `${userEmissions.total} tonnes CO2/year`;

    // Show results section
    document.getElementById('results').style.display = 'block';
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });

    // Create chart
    createChart();

    // Generate insights
    generateInsights();
}

function createChart() {
    const ctx = document.getElementById('emissionsChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (window.emissionsChart instanceof Chart) {
        window.emissionsChart.destroy();
    }

    const data = [
        userEmissions.transportation,
        userEmissions.electricity,
        userEmissions.diet,
        userEmissions.waste
    ];

    const labels = ['🚗 Transportation', '💡 Electricity', '🍽️ Diet', '🗑️ Waste'];
    const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'];

    // Filter out zero values
    const filteredData = [];
    const filteredLabels = [];
    const filteredColors = [];

    for (let i = 0; i < data.length; i++) {
        if (data[i] > 0) {
            filteredData.push(data[i]);
            filteredLabels.push(labels[i]);
            filteredColors.push(colors[i]);
        }
    }

    if (filteredData.length > 0) {
        window.emissionsChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: filteredLabels,
                datasets: [{
                    data: filteredData,
                    backgroundColor: filteredColors,
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Carbon Emissions Distribution by Category',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            font: {
                                size: 12
                            }
                        }
                    }
                }
            }
        });
    }
}

function generateInsights() {
    const insightContent = document.getElementById('insightContent');
    let insights = '';

    if (userEmissions.total > 0) {
        // Find highest emission category
        const emissions = [
            { name: 'Transportation', value: userEmissions.transportation },
            { name: 'Electricity', value: userEmissions.electricity },
            { name: 'Diet', value: userEmissions.diet },
            { name: 'Waste', value: userEmissions.waste }
        ];

        const maxEmission = emissions.reduce((prev, current) => (prev.value > current.value) ? prev : current);

        if (maxEmission.value > 0) {
            insights += `<p><strong>🎯 Your highest emission source is ${maxEmission.name} at ${maxEmission.value} tonnes CO2/year</strong></p>`;

            const recommendations = {
                'Transportation': 'Consider using public transport, carpooling, or electric vehicles to reduce transportation emissions.',
                'Electricity': 'Switch to renewable energy sources, use energy-efficient appliances, and reduce overall consumption.',
                'Diet': 'Consider reducing meat consumption, eating locally sourced food, and minimizing food waste.',
                'Waste': 'Focus on reducing, reusing, and recycling. Compost organic waste and buy products with minimal packaging.'
            };

            if (recommendations[maxEmission.name]) {
                insights += `<p><strong>💚 Recommendation:</strong> ${recommendations[maxEmission.name]}</p>`;
            }
        }

        // Compare with national average
        if (userEmissions.total > 1.89) {
            insights += `<div class="warning"><p>⚠️ Your footprint (${userEmissions.total} tonnes) is above India's average of 1.89 tonnes per capita.</p></div>`;
        } else {
            insights += `<div class="success"><p>✅ Great! Your footprint (${userEmissions.total} tonnes) is below India's average of 1.89 tonnes per capita.</p></div>`;
        }
    }

    insightContent.innerHTML = insights;
}

function configureAPI() {
    const key = document.getElementById('apiKey').value.trim();
    if (key) {
        apiKey = key;
        document.getElementById('chatInterface').style.display = 'block';
        showMessage('✅ Gemini API key configured successfully!', 'system');
    } else {
        alert('Please enter a valid API key');
    }
}

function isCarbonRelated(question) {
    const carbonKeywords = [
        'carbon', 'emission', 'footprint', 'co2', 'climate', 'environment',
        'green', 'sustainable', 'energy', 'transport', 'electricity', 'diet',
        'waste', 'pollution', 'renewable', 'reduce', 'eco', 'environmental'
    ];
    const questionLower = question.toLowerCase();
    return carbonKeywords.some(keyword => questionLower.includes(keyword));
}

async function getChatbotResponse(userQuestion) {
    if (!isCarbonRelated(userQuestion)) {
        return "I'm sorry, but I can only help with questions related to carbon emissions and environmental sustainability. Please ask me something about reducing your carbon footprint, sustainable living, or environmental impact.";
    }

    let context;
    if (userEmissions.total > 0) {
        context = `You are a carbon footprint reduction specialist. The user's current emissions are:
- Transportation: ${userEmissions.transportation} tonnes CO2/year
- Electricity: ${userEmissions.electricity} tonnes CO2/year
- Diet: ${userEmissions.diet} tonnes CO2/year
- Waste: ${userEmissions.waste} tonnes CO2/year
- Total: ${userEmissions.total} tonnes CO2/year

Provide specific, actionable advice for reducing carbon emissions based on their current footprint. Be concise and practical.
Only answer questions related to carbon footprint, sustainability, and environmental impact.

User Question: ${userQuestion}`;
    } else {
        context = `You are a carbon footprint reduction specialist. The user hasn't calculated their emissions yet, but they're asking about carbon footprint reduction.

Provide general, actionable advice for reducing carbon emissions. Be concise and practical.
Only answer questions related to carbon footprint, sustainability, and environmental impact.
Encourage them to use the calculator above to get personalized recommendations.

User Question: ${userQuestion}`;
    }

    try {
        // Updated API endpoint - using v1 instead of v1beta
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
        
        console.log('Making API request to:', apiUrl); // Debug log
        
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: context
                    }]
                }],
                generationConfig: {
                    temperature: 0.7,
                    topK: 40,
                    topP: 0.95,
                    maxOutputTokens: 1024,
                }
            })
        });

        console.log('Response status:', response.status); // Debug log

        if (!response.ok) {
            const errorText = await response.text();
            console.error('API Error Response:', errorText); // Debug log
            throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
        }

        const data = await response.json();
        console.log('API Response:', data); // Debug log
        
        if (data.candidates && data.candidates.length > 0 && data.candidates[0].content) {
            return data.candidates[0].content.parts[0].text;
        } else {
            throw new Error('Invalid response format from API');
        }
    } catch (error) {
        console.error('Chatbot Error:', error); // Debug log
        return `Sorry, I encountered an error: ${error.message}. Please check your API key and try again.`;
    }
}

function showMessage(message, type) {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type === 'user' ? 'user-message' : 'bot-message'}`;
    messageDiv.innerHTML = message;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (!message) return;
    if (!apiKey) {
        showMessage('Please configure your Gemini API key first.', 'system');
        return;
    }

    showMessage(message, 'user');
    chatInput.value = '';
    
    document.getElementById('loading').style.display = 'block';
    
    try {
        const response = await getChatbotResponse(message);
        showMessage(response, 'bot');
    } catch (error) {
        showMessage('Sorry, something went wrong. Please try again.', 'bot');
    }
    
    document.getElementById('loading').style.display = 'none';
}

function askQuickQuestion(question) {
    document.getElementById('chatInput').value = question;
    sendMessage();
}

function clearChat() {
    document.getElementById('chatContainer').innerHTML = '';
    chatHistory = [];
}
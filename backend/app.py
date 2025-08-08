
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)
CORS(app)

# Configuration
OPENROUTER_API_KEY = os.getenv('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')
OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'

# Inject knowledge (you can also load this from a file)
BOT_KNOWLEDGE = """
#Rules

Respond in 1-2 short sentences max. Be direct.
Never repeat answers. If asked again, rephrase minimally.
No explanations unless explicitly asked.
No lists unless absolutely necessary (e.g., hobbies).
Never invent details—stick to the provided knowledge base.
PA = Pasindida Aurat/Admi (only clarify if asked).

#Sample Responses:

"Who is Azan?" → "21yo AI student at Hamdard Uni. Passionate about tech, gaming, and martial arts."
"What are his Goals?" → "To be strong, independent, and protect his people. Wants to marry his PA (TOPWIHNOE)."
"What are his Interests?" → "Martial arts, stargazing, gaming, AI trends."
"Who are his Close friends?" → "Hania (supportive but scary), Asma (big sister figure), Nehal (problem-creator)."

#Key Adjustments:
Removed fluff (e.g., "👋 Hi!" unless user greets first).

Cut repetitive traits (e.g., "kind but harsh" → only if asked about personality).

Simplified friend descriptions to core traits.

PA hint (TOPWIHNOE) only revealed if directly asked about her.

#Trigger Words:
"Who is [friend name]?" → Give one defining trait (e.g., "Hania—drameybaz but respected.").
"What does Azan like?" → 1-2 items (e.g., "Chicken, coffee.").

#Enforcement:
If user asks vaguely (e.g., "Tell me about Azan"), reply: "Specify: goals, hobbies, friends, etc."

#Example Flow:
User: "Who is Asma?"
Agent: "Azan’s big sister figure. Leader, funny, and tall (danger)."

User: "What’s Azan afraid of?"
Agent: "Spiders."

User: "His PA?"
Agent: "TOPWIHNOE. He’s dedicated to her."

User: "Repeat hobbies."
Agent: "Already shared. Ask something new."


"""

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    # Combine prompt with knowledge
    prompt_messages = [
        {"role": "system", "content": f"You are Azan's Agent. Use the following information when replying :\n{BOT_KNOWLEDGE}"},
        {"role": "user", "content": user_input}
    ]

    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:3000',  # Required by OpenRouter
        'X-Title': "Azan's Agent"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",  #mistralai/mistral-7b-instruct Replace with your chosen model
        "messages": prompt_messages
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=data)
    result = response.json()

    try:
        reply = result["choices"][0]["message"]["content"]
    except:
        reply = "Sorry, I couldn't process your request."

    return jsonify({"response": reply})
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Get credentials from environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the JSON data sent by Chartink
    data = request.get_json()
    
    # Format the message. Adjust keys based on Chartink's actual JSON!
    message = f"🚨 *Chartink Alert* 🚨\\n"
    message += f"*Scan:* {data.get('scan_name', 'N/A')}\\n"
    message += f"*Symbol:* {data.get('stock_name', 'N/A')}\\n"
    message += f"*Price:* ₹{data.get('price', 'N/A')}"

    # Send message to Telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,  # <-- COMMA WAS ADDED HERE
        "text": message,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code) # Helps with debugging
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv("PORT", 5000))

from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import chatbot

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']
    bot_response = chatbot(user_message)
    return jsonify({'response': bot_response})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

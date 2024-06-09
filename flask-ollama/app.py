from flask import Flask, request, jsonify
import requests
from pprint import pprint

app = Flask(__name__)

@app.route('/extract_embeddings', methods=['POST'])
def generate():
    data = request.get_json()
    pprint(data)
    try:
        response = requests.post('http://localhost:11434/api/generate', json=data)
        response.raise_for_status()  # Check if the request was successful
        try:
            response_json = response.json()
        except ValueError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Response content: {response.content}")
            return jsonify({"error": "Failed to decode JSON response from the server"}), 500

        final_response = {
            "model": data.get("model"),
            "prompt": data.get("prompt"),
            "response": response_json.get('response', 'No response field in the JSON')
        }

        pprint(final_response['response'])
        return jsonify(final_response)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return jsonify({"error": "Request to external server failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

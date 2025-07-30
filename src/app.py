from flask import Flask, request, jsonify
import os
import requests
import json

app = Flask(__name__)

CREDLY_API_KEY = os.environ.get('CREDLY_API_KEY', 'dummy_key') #Consider reading from config instead of env
CREDLY_API_URL = 'https://api.credly.com/v1/badges'

@app.route('/workday', methods=['POST'])
def receive_workday_data():
    try:
        data = request.get_json()
        # Basic validation - should be more robust
        if not data or 'employee_id' not in data or 'badge_name' not in data:
            return jsonify({'error': 'Invalid Workday data'}), 400
        
        #Transform Workday data to Credly format
        credly_data = transform_workday_to_credly(data)

        # Issue badge via Credly API
        issue_badge(credly_data)

        return jsonify({'message': 'Badge issuance initiated'}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal server error'}), 500


def transform_workday_to_credly(workday_data):
    # Simple transformation - needs to be more comprehensive based on actual data structures
    return {
        'recipient_email': f'employee{workday_data['employee_id']}@example.com', #Should use actual employee email from Workday
        'badge_name': workday_data['badge_name'],
        'description': f'Badge awarded for {workday_data['badge_name']}' #Add more context here
    }

def issue_badge(credly_data):
    headers = {
        'Authorization': f'ApiKey {CREDLY_API_KEY}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(CREDLY_API_URL, headers=headers, data=json.dumps(credly_data))
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"Credly API Response: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling Credly API: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

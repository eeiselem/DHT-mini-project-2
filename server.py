# server.py
from flask import Flask, request, render_template_string, jsonify
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from datetime import timedelta

master_key = b"0123456789123456" # Encryption key

app = Flask(__name__)

# In-memory storage for team data
team_data = {}

@app.route('/')
def index():
    # Sort team_data by team number
    sorted_team_data = dict(sorted(team_data.items(), key=lambda item: int(item[0])))
    
    # Debugging print to check the data
    # print("DEBUGGING PRINT, Sorted team data:", sorted_team_data)

    return render_template_string('''
        <!doctype html>
        <html>
        <head>
            <title>ESP32 Sensor Readings</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    text-align: center;
                }
                table {
                    margin-left: auto;
                    margin-right: auto;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 8px;
                }
                th {
                    background-color: #007bff;
                    color: white;
                }
                tr:nth-child(even){background-color: #f2f2f2;}
                tr:hover {background-color: #ddd;}
            </style>
            <script>
                setTimeout(function(){
                    location.reload();
                }, 5000); // Refresh page every 5 seconds
            </script>
        </head>
        <body>
            <h1>ESP32 Sensor Readings</h1>
            <table>
                <tr>
                    <th>Team #</th>
                    <th>Temperature</th>
                    <th>Humidity</th>
                    <th>Timestamp</th>
                    <th>Post Count</th>
                </tr>
                {% for team, data in sorted_team_data.items() %}
                    <tr>
                        <td>{{ team }}</td>
                        <td>{{ data.temperature }}°C</td>
                        <td>{{ data.humidity }}%</td>
                        <td>{{ data.timestamp }}</td>
                        <td>{{ data.count }}</td>
                    </tr>
                {% endfor %}
            </table>
        </body>
        </html>
    ''', sorted_team_data=sorted_team_data)

@app.route('/post-data', methods=['POST'])
def receive_data():
    data_json = request.get_json() # Get incoming json
    
    # Show incoming json (this should include encrypted data)
    print("================================")
    print("Incoming json:", data_json)
    print("================================")
    
    # Check if the ESP32 sent encrypted data
    try:
        # Attempt to decrypt. If it fails, assume the string was unencrypted.
        temperature = decrypt_data(data_json.get('temperature'))
        humidity = decrypt_data(data_json.get('humidity'))
        raw_timestamp = decrypt_data(data_json.get('timestamp'))
        
        if "Error decoding" in temperature:
            temperature = data_json.get('temperature')
            humidity = data_json.get('humidity')
            raw_timestamp = data_json.get('timestamp')
            
    except Exception:
        # Fallback if decryption completely fails
        temperature = data_json.get('temperature')
        humidity = data_json.get('humidity')
        raw_timestamp = data_json.get('timestamp')

    # Convert the millis() timestamp to HH:MM:SS
    timestamp = convert_time(raw_timestamp)

    team_number = data_json.get('team_number') # Get team number
    if team_number not in team_data: # Add team to team_data if not already in it
        team_data[team_number] = {
            'temperature': temperature,
            'humidity': humidity,
            'timestamp': timestamp,
            'count': 1  # Initialize count
        }
        print(f"New connection from Team {team_number}: Temp {temperature}C")
    else: # Already in team data so update values
        team_data[team_number]['temperature'] = temperature
        team_data[team_number]['humidity'] = humidity
        team_data[team_number]['timestamp'] = timestamp
        team_data[team_number]['count'] += 1  # Increment count
        print(f"Update from Team {team_number}: Temp {temperature}C")

    return "Data Received" # Return to sender

# Decrypts data <16 bytes using base64 and ECB
def decrypt_data(data: str) -> str:    
    try:
        decoded_bytes = base64.b64decode(data) # Get bytes from base64 string
        cipher = AES.new(master_key, AES.MODE_ECB) # Set up cipher object
        decrypted_raw = cipher.decrypt(decoded_bytes) # Decrypt using ECB algorithm
        decrypted_data = decrypted_raw.rstrip(b'\x00') # Remove any null bytes
        return decrypted_data.decode('utf-8') # Return decoded string
    except Exception as e:
        return f"Error decoding: {e}" # Show exception
    
# Converts the ESP32 millis() output to a readable timestamp
def convert_time(time_millis) -> str:
    try:
        total_seconds = int(time_millis) / 1000 # Get seconds
        time = str(timedelta(seconds=total_seconds)) # Get time as string
        return time[:-3] # Return time
    except (ValueError, TypeError):
        return "Invalid Time"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888) # Start Flask server
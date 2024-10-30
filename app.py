from flask import Flask, request, jsonify
import openai
import sqlite3

app = Flask(__name__)
openai.api_key = "YOUR_OPENAI_API_KEY"  # Add your API key here

# Connect to hospital database
def get_nearby_hospitals(location):
    conn = sqlite3.connect('hospitals.db')
    cursor = conn.cursor()
    query = "SELECT name, address, contact FROM hospitals WHERE city = ? LIMIT 5"
    cursor.execute(query, (location,))
    hospitals = cursor.fetchall()
    conn.close()
    return hospitals

# Route for symptom checking
@app.route("/check_symptoms", methods=["POST"])
def check_symptoms():
    data = request.json
    symptoms = data.get("symptoms")
    
    # OpenAI API call for symptom checking
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Provide probable diagnoses for these symptoms: {symptoms}",
        max_tokens=100
    )
    
    result = response.choices[0].text.strip()
    return jsonify({"diagnosis": result})

# Route for locating nearby hospitals
@app.route("/find_hospitals", methods=["POST"])
def find_hospitals():
    data = request.json
    location = data.get("location")
    
    hospitals = get_nearby_hospitals(location)
    if hospitals:
        response = [{"name": h[0], "address": h[1], "contact": h[2]} for h in hospitals]
    else:
        response = "No nearby hospitals found."
    
    return jsonify({"hospitals": response})

if __name__ == "__main__":
    app.run(debug=True)

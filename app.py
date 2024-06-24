# Import necessary libraries
from flask import Flask, render_template, request, jsonify
import csv
from pymongo import MongoClient
import streamlit as st
import pandas as pd
from datetime import datetime
import time
# from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# from pymongo.server_api import ServerApi

app = Flask(__name__)

# Get the current timestamp and format it for date and timestamp
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

# Corrected file name concatenation
filename = f"Attendance_{date}.csv"  # Using the formatted date in the file name

# Assuming the file is generated with this name
df = pd.read_csv(filename)

# Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017")

uri = "mongodb+srv://suryansharma09:sharma0904@cluster0.elxu23c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


db = client["Attendance"]
collection = db["attendance"]

def save_attendance(name, status):
    # Insert attendance data into MongoDB
    collection.insert_one({"name": name, "status": status})

# Use Streamlit to display the DataFrame in an interactive web app
st.dataframe(df.style.highlight_max(axis=0))




# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    try:
        name = request.json.get('name')
        status = request.json.get('status')

        if not name or not status:
            return jsonify({'error': 'Name and status are required'}), 400

        try:
            save_attendance(name, status)
            return jsonify({'message': 'Attendance marked successfully'}), 200
        except Exception as e:
            return jsonify({'error': 'Failed to save attendance: ' + str(e)}), 500

    except Exception as e:
        return jsonify({'error': 'Invalid request: ' + str(e)}), 400




header = ['NAME','TIME']
csvFile = open('Attendance_06-04-2024.csv' , 'r')
reader = csv.DictReader(csvFile)

for each in reader:
    row= {}
    for field in header:
        row[field]= each[field]
    print(row)
    collection.insert_one(row)


# ... (existing code)

# Use a unique identifier or timestamp field to determine latest additions
unique_field = 'TIME'  # Replace with the appropriate field name

def insert_latest_attendance(data):
    # Filter for latest entries before insertion
    latest_entries = []
    for entry in data:
        if not collection.find_one({unique_field: entry[unique_field]}):
            latest_entries.append(entry)

    if latest_entries:
        collection.insert_many(latest_entries)
        print("Inserted latest attendance entries into MongoDB")
    else:
        print("No new attendance entries to insert")





# ... (existing Flask routes and Streamlit code)

if __name__ == '__main__':
    # 1. Load CSV data
    df = pd.read_csv(filename)

    # 2. Convert DataFrame to list of dictionaries
    data = df.to_dict('records')

    # 3. Insert only latest attendance entries into MongoDB
    insert_latest_attendance(data)


    # 4. Start the Flask app
app.run(debug=True)


# if _name_ == 'main':
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from loadmodel import get_prediction_string
import tweepy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access API credentials
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

#print(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET,sep= '\n')

# Authenticate using Client and API
client = tweepy.Client(bearer_token=BEARER_TOKEN,
                       consumer_key=API_KEY,
                       consumer_secret=API_SECRET_KEY,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET)

# Authenticate with OAuth1 for media upload
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', prediction=None)

@app.route('/coordinates', methods=['POST'])
def receive_coordinates():
    # Receive coordinates from the client
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    # Log received coordinates (you may also save them as needed)
    print(f'Received coordinates: Latitude={latitude}, Longitude={longitude}')
    return jsonify({'message': 'Coordinates received successfully'}), 200

@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded file from the form
    uploaded_file = request.files['image']
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    # Save the file temporarily
    image_path = 'uploaded_image.jpg'
    uploaded_file.save(image_path)

    # Call the prediction function
    prediction_string = get_prediction_string(image_path)

    # Check for pothole detection and post on Twitter if found
    print(prediction_string, latitude, longitude)
    if prediction_string == "POTHOLE" and latitude and longitude:
        tweet_text = f"Pothole detected at Latitude: {latitude}, Longitude: {longitude}. #PotholeAlert #RoadSafety"

        # Upload media using API
        media = api.media_upload(image_path)

        # Post tweet with Client using media ID from API
        client.create_tweet(text=tweet_text, media_ids=[media.media_id])
        print("Tweet posted successfully.")

    # Render the result on the webpage
    return render_template('index.html', prediction=prediction_string)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
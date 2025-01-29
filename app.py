from fastapi import FastAPI, HTTPException  
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd


app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
origins = ["*"]  # You might want to restrict this to specific origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the machine learning model
app.state.model = joblib.load('model/best_model.pkl')


@app.get("/predict") ## the request shall be here get not post
def predict(popularity=1,
            acousticness=1,
            danceability=1,
            duration_ms=50,
            energy=1,
            instrumentalness=1,
            liveness=1,
            loudness=1,
            speechiness=1,
            tempo=1,
            valence=1):
    
    try:

        # Handle the POST request and make predictions
        data = pd.DataFrame({
            'popularity': [popularity],
            'acousticness': [acousticness],
            'danceability': [danceability],
            'duration_ms': [duration_ms],
            'energy': [energy],
            'instrumentalness': [instrumentalness],
            'liveness': [liveness],
            'loudness': [loudness],
            'speechiness': [speechiness],
            'tempo': [tempo],
            'valence': [valence]
        })

        model = app.state.model
        
        # Make predictions using the loaded model
        prediction = model.predict(data)
        prediction = int(prediction[0])
        return {"prediction": prediction}
    

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Define a route and a function to handle requests to that route
@app.get("/")
def read_root():
    return {"Message": "Welcome to the Playlist Generator App!"}


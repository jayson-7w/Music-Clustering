# MLOps Music Clustering 🎸

<p>
    <img src="/images/cassette.jpg"/>
    </p>

This is a personal MLOps project based on this [Kaggle](https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db) dataset with music features from Spotify. Below you can find some instructions to understand the project content. Feel free to ⭐ and clone this repo 😉


## Tech Stack

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23d9ead3.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Anaconda](https://img.shields.io/badge/Anaconda-%2344A833.svg?style=for-the-badge&logo=anaconda&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)


## Project Structure

The project has been structured with the following folders and files:

- `.github/workflows`: CI/CD Pipeline
- `data`: dataset 
- `images:` images from results
- `streamlit`: streamlit app
- `notebooks:` EDA and Modelling performed at the beginning of the project to establish a baseline
- `model:` saved best model
- `requirements.txt:` project requirements
- `Dockerfile`: docker image for deployment
- `app.py`: FastAPI app

## Project Description

### Exploratory Data Analysis

The dataset was obtained from Kaggle and contains 232'725 rows and various columns with song features: 

- genre
- danceability
  loudness      
- artist_name
- duration_ms
- mode   
- track_name
- energy
- speechiness
- track_id
- instrumentalness
- tempo
- popularity
- keys
- time_signature
- acousticness
- liveness
- valence
 			 			
To prepare the data for modelling, an **Exploratory Data Analysis** was conducted to preprocess the numerical features, and suitable scalers were chosen for the preprocessing pipeline. Prior to scaling by plotting 3 features, it can be seen that they are not very correlated except from acousticness, energy and loudness. 

<p align="center">
    <img src="/images/scatter_non_scaled.png"/>
    </p>

<p align="center">
    <img src="/images/correlation.png"/>
    </p>

For choosing the scalers, the distribution and boxplot of each features was analyzed. The features with significant outliers were scaled with RobustScaler, features normally distributed with StandardScaler and the rest with MinMmaxScaler. 

<p>
    <img src="/images/popularity.png"/>
    </p>
<p>
    <img src="/images/acousticness.png"/>
    </p>

Afterwards, the scaled features were fitted in a **PCA model** with the following objectives: 

- reduce dimensionality to get a better visual feedback on our clustering
- use the orthogonality of the principal components so that the KMeans algorithm increases its clustering power

A threshold of **95% explained variance** was set up in order to get the number of principal components, which ended up being 3.

<p>
    <img src="/images/PCAs.png"/>
    </p>

Then we determine the optimal number of clusters for **K-Means** using the within-cluster sum of squares (WCSS) method and the "elbow" or "knee" point in the WCSS curve:

- **Calculate WCSS for different numbers of clusters**: The code iterates through a range of cluster numbers from 1 to max_clusters - 1 and fits a K-Means model to the data. The kmeans.inertia_ attribute returns the WCSS for the current number of clusters, which is then appended to the wcss list.

- **Determine the optimal number of clusters**: The KneeLocator is used to find the optimal number of clusters based on the WCSS values. The 'elbow' or 'knee' point represents the optimal number of clusters where adding more clusters doesn't significantly reduce the WCSS.

<p>
    <img src="/images/elbow.png"/>
    </p>

The results after scaling, getting the number of PCs (3) and clusters (5), show a clear grouping of the numerical features, as well as the distribution of the features along each cluster.

<p align="center">
    <img src="/images/scatter_scaled.png"/>
    </p>

<p align="center">
    <img src="/images/radar.png"/>
    </p>

### Modelling

After the EDA, a classifier modelling was performed using the following models:

- KNeighborsClassifier
- MLPClassifier
- SVC
- AdaBoostClassifier
- DecisionTreeClassifier
- GaussianNB
- RandomForestClassifier
- QuadraticDiscriminantAnalysis

All models performed an accuracy above 0.9, being the SVC the one with the better results with only 58 FN and FP.

<p align="center">
    <img src="/images/confusion_matrix.png"/>
    </p>

<p align="center">
    <img src="/images/f1_precission_recall.png"/>
    </p>
    
## Deployment

For the deployment a CICD Pipeline was set up pushing a Dockerimage into an ECR and launching it in an EC2 in AWS. Then the app can be used in Streamlit wither loading the model or using the Service URL of the EC2 instance.

### AWS CICD

Create an IAM user with the following policies:

- AmazonEC2ContainerRegistryFullAccess
- AmazonEC2FullAccess

Create EC2 instance:

- t2.micro
- Allow: HTTPS, SSH and HTTP
- 30 instead of 8 gp2 storage
- Get keypair
- Add security group port range 8000

Create an ECR Repository for the Dockerimage
- 406345071577.dkr.ecr.eu-central-1.amazonaws.com/music

Open the EC2 instance and install docker with the following commands:

```bash
sudo apt-get update -y

sudo apt-get upgrade

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker
```

Check that docker is installed
```bash
docker --version
```
Configure EC2 as self-hosted runner:

- In GitHub repository: setting -> actions -> runner -> new self hosted runner -> choose OS Linux -> then run each command one by one in the EC2 terminal

Setup GitHub secrets:

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- AWS_ECR_LOGIN_URI 
- ECR_REPOSITORY_NAME 

Make sure all data are the same in the yaml file and push the code to GitHub.

### App

The Streamlit [App](https://music-clustering-playlist.streamlit.app/) can be run with the saved model or the Service URL. By selecting the desired features, a music playlist will be generated which correspond to a cluster. By clicking search on YouTube a random song will be selected and will redirect you to YouTube to listen that song

<p align="center">
    <img src="/images/streamlit.png"/>
    </p>


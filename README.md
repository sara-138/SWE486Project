Step 1: Create an Azure Account and Set Up the Speech Service

Go to Azure Portal and sign in or create an account.

In the Azure Portal, search for Speech in the search bar.

Click Create and choose the subscription and resource group.

Select the region closest to you (e.g., uaenorth).

Choose Standard (S0) pricing tier (or a free trial if available).

Once the resource is created, navigate to Keys and Endpoint to get your Subscription Key and Region.

Save these credentials for later use in the script.

Step 2: Install Required Dependencies

Run the following commands to install necessary Python packages:

pip install azure-cognitiveservices-speech
pip install librosa
pip install requests

Dependency Explanations:

azure-cognitiveservices-speech:
Allows communication with Azure Speech-to-Text services.

librosa:
Loads and processes audio files. Used to determine audio duration before sending to the Azure service.

requests:
Sends HTTP requests to measure network latency to the Azure Speech endpoint.

Step 3: Understanding the Imported Libraries in the Code

import azure.cognitiveservices.speech as speechsdkPurpose: Connects to Azure's Speech-to-Text service and handles the transcription process.

import time: Used for measuring timing such as response time and inference duration.

import os: Helps with file handling and path management.

import librosa: Processes audio files and calculates their duration.

import requests: Measures latency to the Azure endpoint via a test HTTP request.

Step 4: Code Execution and Processing Steps

– Load the Audio File – The script reads each audio file using librosa and determines its duration in seconds.

– Initialize Azure Speech Recognizer – The recognizer is initialized using the audio file path, subscription key, and region, allowing connection to Azure’s STT service.

– Process Speech Recognition – The script uses continuous recognition with event-based callbacks to collect speech. It tracks response and inference times.

– Measure Network Latency – The script sends a test HTTP request to Azure's endpoint to calculate the network latency.

– Save Results to a File – The recognized speech (or a NoMatch message), along with audio duration, response time, inference time, and latency, are all saved to a results text file.

Output: All final results are written to speech_recognition_results.txt.


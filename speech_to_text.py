import azure.cognitiveservices.speech as speechsdk
import time
import os
import psutil  # For monitoring system resource usage

# Replace with your Azure Speech API key and region
subscription_key = "Ca0879Tngsx97WcFb2hijYztIgBiRUXCFYD4gW9a6ME4n078WXWKJQQJ99BCACF24PCXJ3w3AAAYACOGcsYZ"
region = "uaenorth"  

# Initialize the Azure Speech SDK client
def initialize_speech_recognition_client():
    try:
        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        audio_config = speechsdk.audio.AudioConfig(filename="your_audio_file.wav")  # Replace with your audio file path
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        return speech_recognizer
    except Exception as e:
        print(f"Error initializing Speech SDK: {e}")
        return None

# Function to get system resource usage
def get_system_resource_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage

# Function for speech recognition (Converting speech to text)
def recognize_speech():
    speech_recognizer = initialize_speech_recognition_client()
    
    if speech_recognizer:
        print("Starting speech recognition...")

        # Measure inference time (Time taken for speech recognition)
        start_time = time.time()

        # Start recognition and wait for result
        result = speech_recognizer.recognize_once()

        end_time = time.time()
        inference_time = end_time - start_time

        # Get system resource usage (CPU and Memory)
        cpu_usage, memory_usage = get_system_resource_usage()

        # Process result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"Recognized Speech: {result.text}")
            print(f"Inference Time: {inference_time:.3f} seconds")
            print(f"CPU Usage: {cpu_usage}%")
            print(f"Memory Usage: {memory_usage}%")
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech Recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error Details: {cancellation_details.error_details}")

# Main function to start the speech-to-text process
if __name__ == "__main__":
    print("Starting Azure Speech-to-Text Benchmarking...")

    # Call the recognize_speech function to start processing
    recognize_speech()

    print("Azure Speech-to-Text benchmarking completed.")

import azure.cognitiveservices.speech as speechsdk
import time
import os
import psutil  # For monitoring system resource usage
import librosa  # For audio file processing

# Azure Speech API key and region
subscription_key = "Ca0879Tngsx97WcFb2hijYztIgBiRUXCFYD4gW9a6ME4n078WXWKJQQJ99BCACF24PCXJ3w3AAAYACOGcsYZ"
region = "uaenorth"

# Get audio file length in seconds using librosa
def get_audio_length(audio_file):
    try:
        y, sr = librosa.load(audio_file, sr=None)  # Load audio with librosa
        duration = librosa.get_duration(y=y, sr=sr)  # Get duration in seconds
        return duration
    except Exception as e:
        print(f"Error loading audio file {audio_file}: {e}")
        return 0

# Initialize the Azure Speech SDK client
def initialize_speech_recognition_client(audio_file):
    try:
        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        return speech_recognizer
    except Exception as e:
        print(f"Error initializing Speech SDK: {e}")
        return None

# Function to get system resource usage
def get_system_resource_usage():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        return cpu_usage, memory_usage
    except Exception as e:
        print(f"Error monitoring system resources: {e}")
        return 0, 0

# Function for speech recognition
def recognize_speech(audio_file, result_file):
    # Get audio length
    audio_length = get_audio_length(audio_file)
    
    speech_recognizer = initialize_speech_recognition_client(audio_file)
    
    if speech_recognizer:

        # Measure total response time (including network latency)
        total_start_time = time.time()

        # Measure inference time
        inference_start_time = time.time()
        result = speech_recognizer.recognize_once()
        inference_end_time = time.time()

        # Measure total response time
        total_end_time = time.time()

        # Calculate times
        inference_time = inference_end_time - inference_start_time
        response_time = total_end_time - total_start_time

        # Get system resource usage
        cpu_usage, memory_usage = get_system_resource_usage()

        # Process result
        with open(result_file, "a") as f:
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                f.write(f"Recognized Speech: {result.text}\n")
                f.write(f"Audio Length: {audio_length:.2f} seconds\n")
                f.write(f"Inference Time: {inference_time:.3f} seconds\n")
                f.write(f"Response Time: {response_time:.3f} seconds\n")
                f.write(f"CPU Usage: {cpu_usage}%\n")
                f.write(f"Memory Usage: {memory_usage}%\n")
                f.write("="*50 + "\n")
            elif result.reason == speechsdk.ResultReason.NoMatch:
                f.write(f"No speech could be recognized in {audio_file}\n")
                f.write("="*50 + "\n")
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                f.write(f"Speech Recognition canceled for {audio_file}: {cancellation_details.reason}\n")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    f.write(f"Error Details: {cancellation_details.error_details}\n")
                f.write("="*50 + "\n")

# Main function
if __name__ == "__main__":
    result_file = "speech_recognition_results.txt"  # File to save the results
    audio_files = ["AudioWAV\\34sec.wav", "AudioWAV\\45sec.wav", "AudioWAV\\60sec.wav", "AudioWAV\\LDC2004S13.wav"]
    
    # Clear previous results from the text file
    open(result_file, "w").close()

    # Process selected audio files
    for audio_file in audio_files:
        recognize_speech(audio_file, result_file)

    print(f"Results saved to {result_file}")

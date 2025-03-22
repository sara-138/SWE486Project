import azure.cognitiveservices.speech as speechsdk
import time
import os
import psutil  # For monitoring system resource usage
from pydub import AudioSegment  # For audio format conversion

# Azure Speech API key and region
subscription_key = "Ca0879Tngsx97WcFb2hijYztIgBiRUXCFYD4gW9a6ME4n078WXWKJQQJ99BCACF24PCXJ3w3AAAYACOGcsYZ"
region = "uaenorth"

# Convert MP3 to WAV if needed
def convert_mp3_to_wav(mp3_file):
    wav_file = mp3_file.replace(".mp3", ".wav")  # Output WAV filename
    audio = AudioSegment.from_mp3(mp3_file)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)  # Ensure correct format
    audio.export(wav_file, format="wav")
    return wav_file

# Get audio file length in seconds
def get_audio_length(audio_file):
    audio = AudioSegment.from_file(audio_file)
    return len(audio) / 1000  # Convert milliseconds to seconds

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
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage

# Function for speech recognition
def recognize_speech(audio_file, result_file):
    # Convert MP3 to WAV if needed
    if audio_file.lower().endswith(".mp3"):
        print(f"Converting {audio_file} to WAV...")
        audio_file = convert_mp3_to_wav(audio_file)

    # Get audio length
    audio_length = get_audio_length(audio_file)
    
    speech_recognizer = initialize_speech_recognition_client(audio_file)
    
    if speech_recognizer:
        print(f"Starting speech recognition for {audio_file}...")

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
    audio_files = ["your_audio_file1.mp3", "your_audio_file2.wav"]  # List your audio files here
    
    # Clear previous results from the text file
    open(result_file, "w").close()

    # Process selected audio files
    for audio_file in audio_files:
        recognize_speech(audio_file, result_file)

    print(f"Results saved to {result_file}")

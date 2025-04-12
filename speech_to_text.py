import azure.cognitiveservices.speech as speechsdk
import time
import os
import librosa  # For audio file processing

# Azure Speech API key and region
subscription_key = "Ca0879Tngsx97WcFb2hijYztIgBiRUXCFYD4gW9a6ME4n078WXWKJQQJ99BCACF24PCXJ3w3AAAYACOGcsYZ"
region = "uaenorth"

# Get audio file length in seconds using librosa
def get_audio_length(audio_file):
    try:
        y, sr = librosa.load(audio_file, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
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

# Speech recognition with continuous recognition
def recognize_speech(audio_file, result_file):
    audio_length = get_audio_length(audio_file)
    speech_recognizer = initialize_speech_recognition_client(audio_file)
    
    if not speech_recognizer:
        return

    recognized_text = []

    def handle_final_result(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            recognized_text.append(evt.result.text)
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            recognized_text.append("[NoMatch]")

    # Hook the events
    speech_recognizer.recognized.connect(handle_final_result)

    # Measure timing
    total_start_time = time.time()
    inference_start_time = time.time()

    # Start continuous recognition and wait for it to finish
    done = False

    def stop_cb(evt):
        nonlocal done
        done = True

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(0.5)
    speech_recognizer.stop_continuous_recognition()

    inference_end_time = time.time()
    total_end_time = time.time()

    inference_time = inference_end_time - inference_start_time
    response_time = total_end_time - total_start_time

    # Save results
    with open(result_file, "a", encoding="utf-8") as f:
        if recognized_text:
            full_text = " ".join(recognized_text)
            f.write(f"Recognized Speech: {full_text}\n")
        else:
            f.write(f"No speech could be recognized in {audio_file}\n")

        f.write(f"Audio Length: {audio_length:.2f} seconds\n")
        f.write(f"Inference Time: {inference_time:.3f} seconds\n")
        f.write(f"Response Time: {response_time:.3f} seconds\n")
        f.write("="*50 + "\n")

# Main function
if __name__ == "__main__":
    result_file = "speech_recognition_results.txt"
    audio_folder = "AudioWAV"
    audio_filenames = [
        "2sec.wav", "10sec.wav", "20sec.wav", "30sec.wav",
        "34sec.wav", "45sec.wav", "60sec.wav", "LDC2004S13.wav", "all.wav"
    ]
    audio_files = [os.path.join(audio_folder, name) for name in audio_filenames]

    # Clear previous results
    open(result_file, "w").close()

    for audio_file in audio_files:
        if not os.path.exists(audio_file):
            print(f"⚠️ File not found: {audio_file}")
            continue
        recognize_speech(audio_file, result_file)

    print(f"✅ Results saved to {result_file}")

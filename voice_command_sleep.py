
import speech_recognition as sr
import pyttsx3
import os
import threading
from queue import Queue

def process_audio(q, recognizer, engine):
    while True:
        audio = q.get()
        if audio is None:
            break
        try:
            text = recognizer.recognize_google(audio)
            print(f"Text: {text}")
            if "sleep" in text.lower():
                respond("Going to sleep mode", engine)
                os.system("rundll32.exe powrprof.dll, SetSuspendState Sleep")
                break
        except sr.UnknownValueError:
            pass
        q.task_done()

def respond(text, engine):
    engine.say(text)
    engine.runAndWait()

def continuous_speech_to_text():
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()
    recognition_queue = Queue()

    # Start a separate thread to process audio data
    audio_thread = threading.Thread(target=process_audio, args=(recognition_queue, recognizer, engine))
    audio_thread.daemon = True
    audio_thread.start()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        respond("Say 'sleep' to put the computer to sleep.", engine)

        while True:
            try:
                audio = recognizer.listen(source, timeout=0.5)
                recognition_queue.put(audio)
            except sr.WaitTimeoutError:
                pass

            except KeyboardInterrupt:
                print("Stopping...")
                break
            
    # Stop the audio processing thread
    recognition_queue.put(None)
    audio_thread.join()

if __name__ == "__main__":
    continuous_speech_to_text()

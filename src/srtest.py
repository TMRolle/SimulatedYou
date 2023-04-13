
import speech_recognition as sr

def speech_to_text(recognizer, audio):
    try:
        print(recognizer.recognize_google(audio, language="de"))
    except sr.UnknownValueError:
        print("[!] UnknownValueError")
    except sr.RequestError as e:
        print("RequestError: ", e)

def get_audio():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        try:
           stop_listening = r.listen_in_background(source, speech_to_text)
        except:
            print('please say that again')
            return get_audio()

if __name__ == "__main__":
    get_audio()

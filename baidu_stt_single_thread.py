from aip import AipSpeech
import speech_recognition as sr

APP_ID = '48393846'
API_KEY = '7xLd77QtRyfKvDGVLLTZDq1G'
SECRET_KEY = 'GNuRDk4Icr4ldcbG2tVSFWb4EacDdefb'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def get_text(wav_bytes):
    result = client.asr(wav_bytes, 'wav', 16000, {'dev_pid': 1536, })
    text = ""
    try:
        text = result['result'][0]
    except Exception as e:
        print(e)
    return text


def main():
    r = sr.Recognizer()
    mic = sr.Microphone()

    while 1:
        print("\nPlease try to speak something...")
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            audio_data = audio.get_wav_data(convert_rate=16000)
            print("\nGot you, now I'm trying to recognize that...")
        text = get_text(audio_data)
        print(f"\n{text}")


if __name__ == '__main__':
    main()

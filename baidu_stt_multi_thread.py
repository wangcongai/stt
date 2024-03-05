import threading
import pyaudio
import os
import time
import wave
from aip import AipSpeech

# 百度AI平台提供的凭证信息
APP_ID = '48393846'
API_KEY = '7xLd77QtRyfKvDGVLLTZDq1G'
SECRET_KEY = 'GNuRDk4Icr4ldcbG2tVSFWb4EacDdefb'

# 创建AipSpeech对象
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 录音参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 10


# 语音识别函数
def recognize_speech():
    while True:
        # 等待音频文件生成
        while not os.path.exists('output.wav'):
            time.sleep(0.1)

        # 读取音频数据
        with open('output.wav', 'rb') as f:
            speech = f.read()

        time.sleep(8)
        # 调用百度语音识别API
        result = client.asr(speech, 'wav', RATE, {'dev_pid': 1537})

        # text = ""
        try:
            text = result['result'][0]
            print(text)
        except Exception as e:
            # print(e)
            print('heartbreak')
            continue


# 录音函数
def record_audio():
    while True:
        # 创建PyAudio对象
        p = pyaudio.PyAudio()

        # 打开音频流
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        # 录音缓存
        frames = []

        # 录音
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        # 关闭音频流
        stream.stop_stream()
        stream.close()
        p.terminate()

        # 保存音频数据
        wf = wave.open('output.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        # 等待一段时间
        time.sleep(0.1)


if __name__ == '__main__':
    # 创建两个线程
    speech_thread = threading.Thread(target=recognize_speech)
    audio_thread = threading.Thread(target=record_audio)

    # 启动线程
    speech_thread.start()
    audio_thread.start()

    # 等待线程结束
    speech_thread.join()
    audio_thread.join()

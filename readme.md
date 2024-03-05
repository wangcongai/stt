# 语音识别STT

## 原理

**Speech to Text**，也被称为语音识别，是一种将人类的语音转化为文本的技术。这个过程通常涉及以下几个步骤：

1. **声音信号的采集和预处理**：首先，需要通过麦克风等设备捕获声音信号，并进行噪声消除、静音检测等预处理步骤，以提高语音识别的准确性。
2. **特征提取**：然后，从预处理后的声音信号中提取有用的特征，如梅尔频率倒谱系数（MFCC），这些特征能够有效地表示语音的内容。
3. **声学模型**：接下来，使用声学模型将提取的特征映射到音素或者词的概率分布。这个模型通常是一个深度神经网络，如长短期记忆网络（LSTM）。
4. **解码**：最后，使用解码算法，如维特比算法，从音素或词的概率分布中找出最可能的序列，即识别结果

目前，主流的语音识别模型包括：

- **CTC（Connectionist Temporal Classification）**：CTC是一种用于序列学习任务的损失函数，它可以让循环神经网络（RNN）直接对序列数据进行学习，而无需事先标注好训练数据中输入序列和输出序列的映射关系。
- **Attention-based模型**：这种模型使用一种称为“注意力”的技术来对输入进行加权汇聚。在每个时间步骤上，该模型会根据当前状态和所有输入计算出一个分布式权重向量，并将其应用于所有输入以产生一个加权平均值作为输出。
- **RNN-Transducer**：这个算法结合了编码器-解码器框架和自回归建模思想，在生成目标序列时同时考虑源语言句子和已生成部分目标语言句子之间的交互作用。

详细参考：[目前效果最好、应用较广且比较成熟的语音识别模型是什么？]([目前效果最好、应用较广且比较成熟的语音识别模型是什么？ - 知乎 (zhihu.com)](https://www.zhihu.com/question/349970899))



## 实现方案

登录[百度智能云平台语音技术](https://console.bce.baidu.com/ai/#/ai/speech/overview/index)，领取免费的短语音识别和实时语音服务。短语音免费赠送**15w**次调用。最大**并发度限制为5**。

![image-20240201183703034](https://piclist-1321200338.cos.ap-nanjing.myqcloud.com/image-20240201183703034.png)

需要预先安装`PyAudio`  Python库，它提供了对音频输入和输出的支持。使用`PyAudio`你可以在Python程序中播放和录制音频

核心调用代码：

```python
# 创建AipSpeech对象
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
# 调用百度语音识别API, 语音模型id为1537
result = client.asr(speech, 'wav', RATE, {'dev_pid': 1537})
```



## 双线程实时语音SST

参考：[python百度语音实时识别成文字](https://blog.csdn.net/zcs2632008/article/details/123334807)，但是该脚本是单线程，在录制麦克风讲话的时候，无法进行语音识别。我将代码逻辑进行了改造，采用双线程。一个线程用来录制麦克风讲话，一个线程用来对语音文件进行语音识别。这样可以保证不遗漏麦克风的讲话内容：

```python
import threading
import pyaudio
import os
import time
import wave
from aip import AipSpeech

# 百度AI平台提供的凭证信息
APP_ID = 'your app id'
API_KEY = 'your api key'
SECRET_KEY = 'your secret key'

# 创建AipSpeech对象
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 录音参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 15


# 语音识别函数
def recognize_speech():
    while True:
        # 等待音频文件生成
        while not os.path.exists('output.wav'):
            time.sleep(0.1)

        # 读取音频数据
        with open('output.wav', 'rb') as f:
            speech = f.read()

        time.sleep(10)
        # 调用百度语音识别API
        result = client.asr(speech, 'wav', RATE, {'dev_pid': 1537})

        # text = ""
        try:
            text = result['result'][0]
            print(text)
        except Exception as e:
            # print(e)
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
```



# 后台OCR和STT效果展示

使用Tmux同时展示两个shell窗口。上窗口为实时语音识别；下窗口每次截屏后做OCR

![](https://piclist-1321200338.cos.ap-nanjing.myqcloud.com/gif-snapshot.gif)



# 参考资料

[How Does Optical Character Recognition Work](https://www.baeldung.com/cs/ocr)

[python百度语音实时识别成文字](https://blog.csdn.net/zcs2632008/article/details/123334807)

[目前效果最好、应用较广且比较成熟的语音识别模型是什么？]([目前效果最好、应用较广且比较成熟的语音识别模型是什么？ - 知乎 (zhihu.com)](https://www.zhihu.com/question/349970899))
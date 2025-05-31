from vosk import Model, KaldiRecognizer
import wave
from pydub import AudioSegment

audio = AudioSegment.from_wav("examples123/5321208452448548848.wav")
audio = audio.set_frame_rate(16000).set_channels(1).normalize()
audio.export("processed.wav", format="wav")
model = Model("vosk-model-small-ru-0.22")  # Скачайте модель с сайта Vosk

wf = wave.open("processed.wav", "rb")
recognizer = KaldiRecognizer(model, wf.getframerate())

while True:
    data = wf.readframes(16000)
    if len(data) == 0:
        break
    if recognizer.AcceptWaveform(data):
        print(recognizer.Result()[14:-3])  # Вывод текста

print(recognizer.FinalResult())  # Финальный результат

if __name__ == "__main__":
	pass

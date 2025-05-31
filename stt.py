from vosk import Model, KaldiRecognizer
import wave
from pydub import AudioSegment
import os

model = Model("vosk-model-small-ru-0.22")  # Скачайте модель с сайта Vosk


def get_text_from_audio(wavfilename: str) -> str:
    """
    Извлекает текст из аудиофайла (формат: 16kHz, моно, WAV).
    Возвращает распознанный текст.
    """
    if not os.path.exists(wavfilename):
        raise FileNotFoundError(f"Файл {wavfilename} не найден")

    with wave.open(wavfilename, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
            raise ValueError("Требуется WAV-файл с моно-звуком (16-bit PCM)")

        recognizer = KaldiRecognizer(model, wf.getframerate())
        recognizer.SetWords(True)  # Включаем распознавание слов для детализации

        full_text = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                # Извлекаем текст между '"text" : "' и '"' без использования json
                text_start = result.find('"text" : "') + 10
                text_end = result.find('"', text_start)
                if text_start != -1 and text_end != -1:
                    full_text.append(result[text_start:text_end])

        final_result = recognizer.FinalResult()
        # Обрабатываем финальный результат аналогичным образом
        final_text_start = final_result.find('"text" : "') + 10
        final_text_end = final_result.find('"', final_text_start)
        if final_text_start != -1 and final_text_end != -1:
            full_text.append(final_result[final_text_start:final_text_end])

    return " ".join(full_text).strip()

# get_text_from_audio("./audios/1.wav")

import pyaudio
# Для записи голосовых сообщений в режиме реального времени можно использовать библиотеку pyaudio.
import requests

API_KEY = 'your_api_key'


def record_and_send(file_name):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=1024)

    frames = []

    print('Запись началась')
    while True:
        data = stream.read(1024)
        frames.append(data)
        # В этом месте можно добавить логику прерывания записи, если пользователь ввел какую-то команду

    print('Запись завершена')
    stream.stop_stream()
    stream.close()
    audio.terminate()

    with open(file_name, 'wb') as f:
        f.write(b''.join(frames))

    url = 'http://server_ip:routing_port/recognize'

    files = {'file': open(file_name, 'rb')}
    headers = {'api_key': API_KEY}

    response = requests.post(url, headers=headers, files=files)

    print('Результат распознавания:', response.text)


def main():
    while True:
        command = input('Ввод команды (запись, выход): ')
        if command == 'запись':
            file_name = input('Введите имя файла: ')
            record_and_send(file_name)
        elif command == 'выход':
            break


if __name__ == '__main__':
    main()

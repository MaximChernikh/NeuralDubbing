import torch
import torchaudio
import sounddevice as sd
import time
import os
import sys
import boto3
import click

# аргументы

array = sys.argv
text = ''
array.pop(0)

name = array[0] + '.wav'

for i in array:
	text = text + i
	text = text + ' '
print(text)

# s3 подключение к yandex cloud

session = boto3.session.Session()
s3 = session.client(

	service_name='s3',
	aws_access_key_id='',
	aws_secret_access_key='',
	endpoint_url=''
)

# настройки ИИ

language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000
speaker = 'aidar'
put_accent = True
put_yo = True
device = torch.device('cpu') # либо gpu

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
						  model='silero_tts',
						  language=language,
						  speaker=model_id)

model.to(device)

audio = model.apply_tts(text=text,
						speaker=speaker,
						sample_rate=sample_rate,
						put_accent=put_accent,
						put_yo=put_yo)

# воспроизведение

print(text)

sd.play(audio, sample_rate)
time.sleep(len(audio) / sample_rate)
sd.stop()

# сохранение

save_audio = torchaudio.save(name, audio.unsqueeze(0), sample_rate=48000)

# Загрузить объекты в бакет
## Из файла
s3.upload_file(name, '', 'audio/' + name)

# удаление

os.remove(name)





# ## Из строки
# s3.put_object(Bucket='', Key='', Body='TEST')

# # Получить список объектов в бакете
# for key in s3.list_objects(Bucket='bucket-name')['Contents']:
# 	print(key['Key'])

# # Получить объект
# get_object_response = s3.get_object(Bucket='bucket-name',Key='py_script.py')
# print(get_object_response['Body'].read())
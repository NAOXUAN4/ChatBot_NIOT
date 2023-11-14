from gradio_client import Client
import os
import json

import requests
from io import BytesIO

API_URL = 'https://genshinvoice.top/api'
#txt=input("Text=")
spk="派蒙"#input("Speaker=")
#print("音色_"+spk)

def vioce(text):
  vnum=0
  """"调用GenshinVoice API进行TTS"""
  for i in range((len(text)-1)//200+1):
    vnum+=1
    params = {
      'speaker': "芭芭拉",
      'text': text[i*200:len(text)-(i*200)-1],
      'format': 'wav',
      'length': 1,
      'noise': 0.5,
      'noisew': 0.9,
      'sdp_ratio': 0.2
    }
    response = requests.get(API_URL, params=params)
    audio = response.content
    #print(response.url)
    audioop = BytesIO(audio)
    with open(f"E:\py_project\ChatCLM+genshinTTS/audio/{vnum}.mp3", "wb") as f:
      f.write(audioop.getbuffer())

  for i in range(vnum):
    os.system(f"start E:\py_project\ChatCLM+genshinTTS/audio/{vnum}.mp3")


def openjosn(filename,num):
  with open(filename) as f:
    chat_history = json.load(f)

  question = chat_history[num][0]
  answer = chat_history[num][1]
  q=question[3:-5]
  a=answer[3:-5]
  #print("User asked: " + q)
  print("Chatbot answered: " + a)

  return [q,a]

def delete_files_except(folder, patterns):
  # 这是一个函数，用于删除文件夹里面除了特定模式之外的所有文件
  # folder 是要删除文件的文件夹的路径，比如 "C:/Users/Desktop/test"
  # patterns 是要保留的文件的模式的列表，比如 [".txt", ".jpg"]
  for file in os.listdir(folder):  # 遍历文件夹中的所有文件

    if not any(file.endswith(p) for p in patterns):  # 判断文件是否符合任何一个保留的模式

      file_path = os.path.join(folder, file)  # 获取文件的完整路径

      os.remove(file_path)  # 删除文件

      #print(f"Deleted {file_path}")  #打印删除信息


delete_files_except("E:\py_project\genshenTTS_APITest/audio",["***.png"])  #首次启动清文件夹


client = Client("http://localhost:7860/")

initjo = client.predict(fn_index=2)
print(initjo)
"""创建初始josn"""
#print(initjo)

def input_cglm(promptin,resultjo):

  result = client.predict(
    promptin,
    resultjo,
    1024,
    0.8,
    0.95,
    fn_index=0
  )
  return result

num=0

prompt = input("User：")
resultout = input_cglm(prompt,initjo)
resultoutfin=resultout[-16:]
QAresult=openjosn(resultout, num)

vioce(QAresult[1])
delete_files_except("C:/Users/annanyi\AppData\Local\Temp\gradio", [resultoutfin,"."])
#一次


while 1:
  num+=1

  delete_files_except("E:\py_project\genshenTTS_APITest/audio", ["***.png"])  #清理音频缓存
  prompt = input("User：")
  resultout = input_cglm(prompt, resultout)
  print(resultout)

  resultoutfin = resultout[-16:]

  QAresult=openjosn(resultout, num)

  vioce(QAresult[1])

  delete_files_except("C:/Users/annanyi\AppData\Local\Temp\gradio", [resultoutfin,"."])

  # 无限次









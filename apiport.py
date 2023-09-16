import json
import gui
from gradio_client import Client
import os

class ChatRs:
    def __init__(self):

        self.client = Client("http://localhost:7860/")
        self.initjo = self.client.predict(fn_index=2)
        print(self.initjo)
        """创建初始josn"""

        self.resultoutALL= self.initjo
        self.folder="E:\py_project\genshenTTS_APITest/audio"

        self.resultout=""
        self.resultoutfin=""

        self.DelExcept=""
        """删除筛选"""

    def openjosn(self,text,timesnum):

        self.cut_Port(text,timesnum)

        """生成结果文件（对话记录）"""

        with open(self.resultoutALL) as f:
            chat_history = json.load(f)


        print("NUM=",timesnum)
        print("chat_history=",chat_history)
        question = chat_history[timesnum][0]
        answer = chat_history[timesnum][1]
        #q = question[3:-5]
        a = answer[3:-5]
        # print("User asked: " + q)
        #print("Chatbot answered: " + a)
        return a

    def delete_files_except(self):

        # 这是一个函数，用于删除文件夹里面除了特定模式之外的所有文件
        # folder 是要删除文件的文件夹的路径，比如 "C:/Users/Desktop/test"
        # patterns 是要保留的文件的模式的列表，比如 [".txt", ".jpg"]
        for file in os.listdir(self.folder):  # 遍历文件夹中的所有文件

            if not any(file.endswith(p) for p in [self.resultoutfin,self.DelExcept]):  # 判断文件是否符合任何一个保留的模式

                file_path = os.path.join(self.folder,file)  # 获取文件的完整路径

                os.remove(file_path)  # 删除文件

                # print(f"Deleted {file_path}")  #打印删除信息


    def input_cglm(self,text,timesnum):

        print("连接")
        result = self.client.predict(
            text,
            self.resultoutALL,
            1024,
            0.8,
            0.95,
            fn_index=0
        )
        return [result,timesnum]


    def cut_Port(self,text,timesnum):

        self.resultoutALLAndNum = self.input_cglm(text,timesnum)
        self.resultoutALL = self.resultoutALLAndNum[0]
        self.resultoutfin = self.resultoutALL[-16:]
        print("get res")

    def NewOne(self):

        with open(self.resultoutALL) as f:

            data = json.load(f)
            data = []

        with open(self.resultoutALL,"w") as f:

            json.dump(data, f)



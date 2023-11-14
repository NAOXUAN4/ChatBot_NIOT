import sys
import os

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from io import BytesIO
import TTS
import apiport
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist,QMediaContent
import pygame
from pygame import mixer
import wave


class MyApp:
    def __init__(self):

        self.num1=0
        """第n条对话"""

        self.chatGlm=apiport.ChatRs()
        self.TTs=TTS.GenshinTTS()
        """oop"""

        self.app = QApplication(sys.argv)
        """创建对象"""
        self.w = QWidget()
        """调用控件"""

        self.layout = QVBoxLayout()
        """组件添加器"""
        # 背景
        """
        self.bg_label = QLabel()
        self.bg_label.setStyleSheet("background-color: #121212")
        """

        self.w.resize(500, 800)
        """设置窗口大小"""

        self.w.move(1700, 250)
        """设置窗口位置"""

        self.FontDic = {1: "color: #f9f1db; font-size: 20px; font-weight: bold; font-family: Arial",
                        2: "color: #61649f; font-size: 20px; font-weight: bold;",
                        3: "color: #63bbd0; font-size: 20px; font-weight: bold; font-family: Arial"}
        """字体仓库"""

        style = "background-color: #61649f;border-color: rgb(87, 124, 138);"
        self.w.setStyleSheet(style)

        self.num = 0
        """第几轮对话"""

        self.Usrinput=""

        self.resultGLM=""

        self.w.setWindowIcon(QIcon("E:\py_project\ChatCLM+genshinTTS/ico.jpg"))
        """设置窗口图标"""

        self.w.setWindowTitle("ChatGlm+GenshinTTS")
        """设置标题"""

        self.button1()
        """定义Button"""

        self.textbox()
        """定义Textbox"""

        self.inputUser()
        """定义用户输入接口函数->传递用户输入向Apiport"""

        self.tTsResSWi()
        """定义TT二进制文件输出转换"""

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        """创建播放器"""

        self.player.setVolume(50)
        """设置音量"""







    """def menu(self):

        self.File1 = self.QMenu()
        self.btn = QPushButton("File",self.w)
    """
    def button1(self):
        self.width1 = self.w.width()
        self.height1 = self.w.height()
        """获取窗口大小"""

        self.Bthand = QPushButton(self.w)
        self.Btcl = QPushButton(self.w)
        self.BtADv = QPushButton(self.w)


        self.Bthand.setText("InputText",)
        self.Btcl.setText("CleanMen")
        self.BtADv.setText("ADvanceSet")

        self.Bthand.setStyleSheet(self.FontDic[1])
        self.Btcl.setStyleSheet(self.FontDic[1])
        self.BtADv.setStyleSheet(self.FontDic[1])

        self.Bthand.clicked.connect(self.BthandAct)
        self.Btcl.clicked.connect(self.BtclAct)
        self.BtADv.clicked.connect(self.BtADvAct)
        """检测点击"""

        self.Bthand.setGeometry(self.width1 // 2+10, self.height1 // 2 + 180, self.width1 // 5+100, self.height1 // 20)
        self.Btcl.setGeometry(self.width1 // 2+10, self.height1 // 2 +260, self.width1 // 5+100, self.height1 // 20)
        self.BtADv.setGeometry(self.width1//2-200, self.height1 // 2+180, self.width1 // 3, self.height1//10+42)
        """前xy后宽高"""
        """设置位置"""

        """
        self.layout.addWidget(self.Bthand)
        self.layout.addWidget(self.Btcl)
        """
        """添加组件"""

    def textbox(self):

        self.textbox1= QLineEdit(self.w)
        self.textbox2 = QTextEdit(self.w)


        #self.textbox1.setText("Please Input")
        self.textbox1.setPlaceholderText("UserInput=")
        self.textbox1.setStyleSheet(self.FontDic[1])


        self.textbox1.setGeometry(self.width1 // 2-200, self.height1 // 2+90, self.width1//3+self.width1//5+145, self.height1 // 16)
        self.textbox2.setGeometry(self.width1 // 2 - 200, self.height1//22,
                                  self.width1 // 3 + self.width1 // 5 + 145, self.height1 // 2+21)

        self.textbox1.returnPressed.connect(self.BthandAct)  #回车发送

    def BthandAct(self):

        inputToPort=self.inputUser()
        print("input=",inputToPort)

        self.textbox1.setText("")
        """输入后清空textbox"""

        self.resultGLM = apiport.ChatRs.openjosn(self.chatGlm,inputToPort[0],inputToPort[1])
        print("chatglmres=",self.resultGLM)

        self.num += 1
        #apiport.ChatRs.delete_files_except(self.chatGlm)

        self.tTsResSWi()
        """TTs"""

        self.ChathisTxBox()






    def inputUser(self):



        self.UsrText=self.textbox1.text()

        return [self.textbox1.text(),self.num]

    def BtclAct(self):

        self.num=0

        self.chatGlm.NewOne()

        self.textbox2.clear()
        """清理text历史"""


    def BtADvAct(self):
        pass

    def ChathisTxBox(self):


        ChatHisresUSR= (f"User:"
                        f"{self.UsrText}")
        ChatHisresBOT= (f"ChatBot:"
                        f"{self.resultGLM}")


        usr_text = f"<span style='{self.FontDic[1]}'>" + ChatHisresUSR + "</span>"

        bot_text = f"<span style='{self.FontDic[3]}'>" + ChatHisresBOT + "</span>"

        self.textbox2.append(usr_text)
        self.textbox2.append(bot_text)



    def tTsResSWi(self):

        if self.resultGLM != "":
            TTsResALL=self.TTs.genshin_tts(self.resultGLM)
            TTsResAudio=TTsResALL[1]
            print("TTsResUrl=",TTsResALL[0])

            self.num1 += 1
            audioop = BytesIO(TTsResAudio)
            with open(f"E:\py_project\ChatCLM+genshinTTS\\audio\\Tmp{self.num1}.wav", "wb") as f:
                f.write(audioop.getbuffer())

            self.tTsResPlay()

    def tTsResPlay(self):
        # 设置音频文件路径



        audio_data = f"E:\py_project\ChatCLM+genshinTTS\\audio\\Tmp{self.num1}.wav"

        pygame.init()
        mixer.init()

        mixer.music.load(audio_data)
        mixer.music.play()

        while mixer.music.get_busy():
            pygame.time.Clock().tick(10)


        """
        os.system('start /min E:/py_project/ChatCLM+genshinTTS/audio/Tmp.mp3')
        #os.system("start E:/py_project/ChatCLM+genshinTTS/audio/Tmp.mp3")
        os.system('taskkill /im wmplayer.exe /f')
        """


    def run(self):

        self.w.show()
        """显示控件"""
        self.app.exec_()
        """实现LOOP"""


if __name__ == "__main__":
    myapp = MyApp()
    myapp.run()








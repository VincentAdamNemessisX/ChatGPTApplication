"""
File : contextsChatUIVersion.py
Time : 2:24 PM
Author : vincent
version : python 3.8
Description: 循环调用 ChatGPT，将对话输出到屏幕并写入文件
"""
import os.path
import random
import sys

import openai
from PyQt5.QtWidgets import QWidget, QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QApplication

# 设置 API 密钥
openai.api_key = "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"

context = []


class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        from PyQt5 import QtGui
        font = QtGui.QFont()
        font.setFamily("GEETYPE-LiShuGBT-Flash")
        font.setPointSize(20)

        # 创建组件
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.user_input = QLineEdit()
        self.new_chat_button = QPushButton('新聊天')
        self.send_button = QPushButton('发送')
        self.send_button.setFont(font)
        self.chat_history.setFont(font)
        self.user_input.setFont(font)
        self.new_chat_button.setFont(font)

        # 创建布局
        chat_layout = QVBoxLayout()
        new_chats_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        new_chats_layout.addWidget(self.new_chat_button)
        input_layout.addWidget(self.user_input)
        input_layout.addWidget(self.send_button)
        chat_layout.addLayout(new_chats_layout)
        chat_layout.addWidget(self.chat_history)
        chat_layout.addLayout(input_layout)
        self.setLayout(chat_layout)

        # 绑定事件
        self.send_button.clicked.connect(self.on_send_clicked)
        self.user_input.returnPressed.connect(self.on_send_clicked)
        self.new_chat_button.clicked.connect(self.reset)

        # 设置窗口属性
        self.setWindowTitle('Chat Widget')
        self.setMinimumSize(800, 600)

    def reset(self):
        write_to_file()
        self.chat_history.clear()
        self.user_input.clear()
        global context
        context = []

    def on_send_clicked(self):
        user_input = self.user_input.text().strip()
        prompt = ""
        for j in context:
            prompt += j['user'] + ":" + j['text'] + "\n"
        prompt += "user:" + user_input
        context.append({"user": "user", "text": user_input})
        response = call_chat(prompt)
        self.update_chat(response, user_input)
        self.user_input.setText("")

    def update_chat(self, response, user_input):
        response_text = response.choices[0].text.strip().lstrip("?!。，").lstrip("ChatGPT:")
        context.append({"text": response_text, "user": "ChatGPT"})
        self.chat_history.append("User: " + user_input)
        self.chat_history.append("ChatGPT: " + response_text + "\n")

    def closeEvent(self, event):
        write_to_file()
        event.accept()


filename = "conversation.txt"


def write_to_file():
    global filename
    if os.path.exists(filename):
        filename = "conversation" + str(random.randint(1, 100)) + ".txt"
    with open(filename, "a+") as f:
        for i in context:
            f.write(i['user'] + ":" + i['text'] + "\n")


def call_chat(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # 使用哪个 GPT 版本
            prompt=prompt,
            max_tokens=3000,  # 生成的最大 token 数量
            n=1,  # 生成的回复数量
            stop=None,
            temperature=0.7  # 控制生成文本的 k 比例
        )
    except openai.error.Timeout as to:
        print("你或许无法连接世界，请检查网络后再来吧！\n" + to.user_message)
        exit(0)
    except openai.error.InvalidRequestError as ir:
        print("很有可能是上下文到上限了！\n" + ir.user_message)
        exit(0)
    finally:
        pass
    return response


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_widget = ChatWidget()
    chat_widget.show()
    sys.exit(app.exec_())
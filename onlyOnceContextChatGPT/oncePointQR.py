"""
# File       : oncePointQR.py
# Time       : 4:50 PM
# Author     : vincent
# version    : python 3.8
# Description:
"""
import openai
import textwrap
import os

openai.api_key = "private-API-Key"
chats_content = []


def call_chat(p):
    try:
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=p,
            max_tokens=3000,
            n=1,
            stop=None,
            temperature=0.9
        )
    except Exception as _:
        print("\nCause network error, you can't use it in your current country!")
        exit(1)
    return completion


def format_print(text, completion):
    if completion.choices[0].finish_reason == "length":
        print("ChatGPT：", "回答过长\n", "这是部分回答：")
        lines = textwrap.wrap("ChatGPT：" + completion.choices[0].text.strip()
                              .lstrip("？  ").lstrip("！  ").lstrip("。  ").lstrip("，"), width=40)
        # 将每行字符串连接起来并输出
        output = "\n".join(lines)
        print(output)
    else:
        lines = textwrap.wrap("ChatGPT：" + completion.choices[0].text.strip()
                              .lstrip("？  ").lstrip("！  ").lstrip("。  ").lstrip("，"), width=40)
        # 将每行字符串连接起来并输出
        output = "\n".join(lines)
        print(output)
    chats_content.append("我：" + text + "\n")
    chats_content.append(output + "\n")


def write_to_file():
    if os.path.exists("chatsContent.txt"):
        os.remove("chatsContent.txt")
    with open("chatsContent.txt", "a+") as file:
        for c in chats_content:
            file.write(c)


def main():
    text = ""
    print("退出并保存本次聊天内容至文件输入'X', 重新生成答案回复'reg'")
    while True:
        prompt = input("我：")
        if prompt == "X":
            format_print("再见!", call_chat("再见!"))
            write_to_file()
            break
        elif prompt == "reg":
            if text != "":
                completions = call_chat(text)
                format_print(text, completions)
            else:
                print("你还没有问过ChatGPT呢！")
        else:
            text = prompt
            completions = call_chat(prompt)
            format_print(text, completions)

"""
File : contextsChat.py
Time : 2:24 PM
Author : vincent
version : python 3.8
Description: 循环调用 ChatGPT，将对话输出到屏幕并写入文件

"""
import openai
import os
import textwrap

# 设置您的 API 密钥
openai.api_key = "private-API-Key"
context = []


def write_to_file():
    if os.path.exists('conversation.txt'):
        os.remove('conversation.txt')
    with open("conversation.txt", "a+") as f:
        # 将对话写入文件
        for i in context:
            f.write(i['user'] + ":" + i['text'] + "\n")
        f.flush()  # 强制写入文件


def call_chat(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # 使用哪个 GPT 版本
            prompt=prompt,
            max_tokens=3000,  # 生成的最大 token 数量
            n=1,  # 生成的回复数量
            stop=None,  # 可选，表示生成的回复应该在哪个 token 停止
            temperature=0.5,  # 控制生成的回复的创造力和多样性
        )
    except openai.error.Timeout as e:
        print("OpenAI API 请求超时: {}".format(e))
        return call_chat("")
    except openai.error.InvalidRequestError as e1:
        print("上下文已达上限!\n" + e1.user_message)
        return call_chat("")
    return response


def handle_print(response):
    response_text = response.choices[0].text.strip().lstrip("?!。，").lstrip("ChatGPT:")
    context.append({"text": response_text, "user": "ChatGPT"})
    print("\n".join(textwrap.wrap("ChatGPT:" + response_text, width=40)))


def main():
    print("退出请输入'X', 你最多只有10次机会")
    # 循环调用 ChatGPT
    for i in range(10):
        # 准备要发送给 ChatGPT 的文本，包含历史对话上下文
        prompt = ""
        for j in context:
            prompt += j['user'] + ":" + j['text'] + "\n"
        text = input("user:")

        if text != 'X':
            prompt += "user:" + text
            context.append({"user": "user", "text": text})
            # 调用 ChatGPT
            response = call_chat(prompt)
            # 处理 ChatGPT 返回的回复并打印
            handle_print(response)
        else:
            break
    write_to_file()

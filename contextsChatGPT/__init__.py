"""
# File       : __init__.py.py
# Time       : 2:18 PM
# Author     : vincent
# version    : python 3.8
# Description:
"""
import sys
import contextsChatUIVersion
from PyQt5.QtWidgets import QApplication

# from contextsChatGPT import contextsChat

if __name__ == '__main__':
    # contextsChat.main()
    app = QApplication(sys.argv)
    chat_widget = contextsChatUIVersion.ChatWidget()
    chat_widget.show()
    sys.exit(app.exec_())
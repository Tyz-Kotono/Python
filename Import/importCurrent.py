
import sys
import os

# 添加当前目录的父目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 或者添加绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
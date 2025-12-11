import os
import json
import re

def parse_ue_struct_string(s):
    """
    将 UE4 结构体字符串解析为 Python dict
    例：
    (Event=None,ID=False,Time=(Event="/Game/.../Play_BEEP_03",ID=False))
    """
    s = s.strip()
    if not s.startswith("(") or not s.endswith(")"):
        return s  # 非结构体，直接返回

    result = {}
    content = s[1:-1]

    fields = []
    start = 0
    level = 0
    for i, c in enumerate(content):
        if c == "(":
            level += 1
        elif c == ")":
            level -= 1
        elif c == "," and level == 0:
            fields.append(content[start:i])
            start = i + 1
    fields.append(content[start:])

    for field in fields:
        if "=" in field:
            key, value = field.split("=", 1)
            key = key.strip()
            value = value.strip()
            if value.startswith("(") and value.endswith(")"):
                result[key] = parse_ue_struct_string(value)
            else:
                if value == "None":
                    result[key] = None
                elif value == "True":
                    result[key] = True
                elif value == "False":
                    result[key] = False
                else:
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    result[key] = value
    return result

def recursively_parse_fields(obj, struct_fields=None):
    """
    遍历 JSON 对象，自动解析指定的结构体字段
    :param obj: list 或 dict
    :param struct_fields: 要解析的字段列表，默认 None 表示解析所有可能的结构体字符串
    """
    if isinstance(obj, list):
        return [recursively_parse_fields(x, struct_fields) for x in obj]
    elif isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if struct_fields is None or k in struct_fields:
                if isinstance(v, str) and v.startswith("(") and v.endswith(")"):
                    new_obj[k] = parse_ue_struct_string(v)
                else:
                    new_obj[k] = recursively_parse_fields(v, struct_fields)
            else:
                new_obj[k] = recursively_parse_fields(v, struct_fields)
        return new_obj
    else:
        return obj

def modify_json_field(data, key_path, new_value):
    """
    根据 key_path 修改数据，支持嵌套 dict
    key_path: ['Life','Time','Event'] 这样的列表
    """
    if not key_path:
        return
    current_key = key_path[0]
    if len(key_path) == 1:
        if isinstance(data, dict) and current_key in data:
            data[current_key] = new_value
    else:
        if isinstance(data, dict) and current_key in data:
            modify_json_field(data[current_key], key_path[1:], new_value)
        elif isinstance(data, list):
            for item in data:
                modify_json_field(item, key_path, new_value)

def process_json_file(file_path, struct_fields=None, modifications=None):
    """
    解析 JSON 文件，解析结构体字段，应用修改
    modifications: [{'key_path': [...], 'new_value': ...}, ...]
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data = recursively_parse_fields(data, struct_fields)

    if modifications:
        for mod in modifications:
            modify_json_field(data, mod['key_path'], mod['new_value'])

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"[Modified] {file_path}")

def batch_process_json(folder_path, struct_fields=None, modifications=None):
    """
    批量扫描文件夹 JSON 并处理
    """
    if not os.path.exists(folder_path):
        print(f"[Error] 文件夹不存在: {folder_path}")
        return

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".json"):
                file_path = os.path.join(root, file)
                process_json_file(file_path, struct_fields, modifications)

# ----------------- 示例使用 -----------------

# 需要解析的嵌套结构体字段，例如 Life
struct_fields = ["Life"]

# 需要修改的字段
modifications = [
    {
        "key_path": ["Life", "Time", "Event"],  # 修改 Life.Time.Event
        "new_value": "/Game/WwiseAudio/Events/Default_Work_Unit/UI/Play_NEW_EVENT.Play_NEW_EVENT"
    }
]

folder_path = "./DT_Audio"

batch_process_json(folder_path, struct_fields, modifications)

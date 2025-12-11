import json
import os

def modify_json_event_id(json_path, target_event, new_id_value=True):
    """
    修改指定 JSON 文件中 Event 对应的 ID 值
    :param json_path: JSON 文件路径
    :param target_event: 需要匹配的 Event 字符串
    :param new_id_value: 要设置的 ID 值，默认 True
    """
    if not os.path.exists(json_path):
        print(f"[Warning] 文件不存在: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[Error] 解析 JSON 失败: {json_path}, {e}")
            return

    modified = False
    for row in data:
        if row.get("Event") == target_event:
            row["ID"] = True
            modified = True

    if modified:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[Modified] 已修改文件: {json_path}")
    else:
        print(f"[Skipped] 文件中未找到匹配 Event: {json_path}")

def batch_modify_json(folder_path, target_event, new_id_value=True):
    """
    批量扫描文件夹内的 JSON 文件并修改
    :param folder_path: 文件夹路径
    :param target_event: 需要匹配的 Event 字符串
    :param new_id_value: 要设置的 ID 值
    """
    if not os.path.exists(folder_path):
        print(f"[Error] 文件夹不存在: {folder_path}")
        return

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".json"):
                json_path = os.path.join(root, file)
                modify_json_event_id(json_path, target_event, new_id_value)

# 示例使用
target_event = "/Game/WwiseAudio/Events/Default_Work_Unit/UI/Play_BEEP_01.Play_BEEP_01"
folder_path = "./DT_Audio"

batch_modify_json(folder_path, target_event)

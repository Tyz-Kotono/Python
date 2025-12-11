import unreal
import os

def import_json_to_data_table(json_file, data_table_path):
    unreal.log(f"[DataTable Import] Loading: {data_table_path}")

    dt = unreal.load_object(None, data_table_path)
    if not dt:
        unreal.log_error(f"[DataTable Import] Failed to load: {data_table_path}")
        return False

    if not os.path.exists(json_file):
        unreal.log_error(f"[DataTable Import] JSON 文件不存在: {json_file}")
        return False

    success = dt.fill_from_json_file(json_file)

    if not success:
        unreal.log_error("[DataTable Import] 反导失败")
        return False

    unreal.log("[DataTable Import] 成功从 JSON 更新 DataTable")

    return True


# Main
if __name__ == "__main__":
    DATA_TABLE_PATH = "/Game/Dev/Temp/Data/DT_Audio.DT_Audio"
    JSON_FILE = "Z:\Projects\GameClient\Python\DT_Audio\DT_Audio.json"

    import_json_to_data_table(JSON_FILE, DATA_TABLE_PATH)

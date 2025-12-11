# -*- coding: utf-8 -*-
import unreal
import json
import os

def export_data_table_to_json(data_table_path, output_dir):
    unreal.log(f"[DataTable JSON] Loading: {data_table_path}")

    dt = unreal.load_object(None, data_table_path)
    if not dt:
        unreal.log_error(f"[DataTable JSON] Failed to load: {data_table_path}")
        return False

    # 直接导出整个 DataTable 的 JSON 字符串
    json_str = dt.export_to_json_string()

    if not json_str:
        unreal.log_error("[DataTable JSON] export_to_json_string() 返回空内容")
        return False

    # 转为 Python dict（让 JSON 更漂亮）
    json_obj = json.loads(json_str)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    out_path = os.path.join(output_dir, dt.get_name() + ".json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(json_obj, f, indent=4, ensure_ascii=False)

    # unreal.log(f"[DataTable JSON] Exported: {out_path}")
    # unreal.log(f"[DataTable JSON] abspath: {os.path.abspath(out_path)}")
    return True


# Main
if __name__ == "__main__":
    DATA_TABLE_PATH = "/Game/Dev/Temp/Data/DT_Audio.DT_Audio"
    OUTPUT_DIR = "Z:\Projects\GameClient\Python\DT_Audio"

    unreal.log("启动 DataTable → JSON 工具")
    unreal.log(f"DataTable Path: {DATA_TABLE_PATH}")
    unreal.log(f"Output Dir: {OUTPUT_DIR}")

    success = export_data_table_to_json(DATA_TABLE_PATH, OUTPUT_DIR)
    if success:
        unreal.log("转换成功")
    else:
        unreal.log_error("转换失败")

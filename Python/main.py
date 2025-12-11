import unreal

import sys
import os
from pprint import pprint
# 添加当前目录的父目录
current_file = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 或者添加绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from DataTable.DataTableToJson import export_data_table_to_json

# 指定目标结构体
target_struct = unreal.load_object(None, '/Game/Dev/Temp/Data/SAudioEvent.SAudioEvent')

asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

# 获取所有资产
all_assets = asset_registry.get_all_assets(True)

matched_tables = []

for asset_data in all_assets:
    # 判断类型
    if asset_data.asset_class_path.asset_name == 'DataTable':
        dt = asset_data.get_asset()
        if dt and isinstance(dt, unreal.DataTable):
            # 获取行结构体
            row_struct_obj = dt.get_editor_property('row_struct')  # 代替 dt.row_struct
            if isinstance(row_struct_obj, unreal.SoftObjectPath):
                row_struct_obj = row_struct_obj.resolve_object()
            if row_struct_obj == target_struct:
                matched_tables.append(dt)



dt_audio_dir = os.path.join(current_dir, "DT_Audio")
 
print(dt_audio_dir)
print('===========')

# 输出结果 DTList
for dt in matched_tables:
    row_count = len(dt.get_row_names()) if dt.get_row_names() else 0
    unreal.log(f"Found DataTable: {dt.get_path_name()}, Rows: {row_count}")
   

unreal.log(f"Total matched DataTables: {len(matched_tables)}")


# 输出结果 DTList
for dt in matched_tables:
   export_data_table_to_json(dt.get_path_name(),dt_audio_dir)

unreal.log(f"Total 转Json: {len(matched_tables)}")
#反写
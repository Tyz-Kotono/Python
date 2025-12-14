import unreal

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

# 输出结果
for dt in matched_tables:
    row_count = len(dt.get_row_names()) if dt.get_row_names() else 0
    unreal.log(f"Found DataTable: {dt.get_path_name()}, Rows: {row_count}")

unreal.log(f"Total matched DataTables: {len(matched_tables)}")

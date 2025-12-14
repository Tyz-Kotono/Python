import unreal

def get_assets_by_class(scan_folder: str, class_name: str):
    """
    扫描指定文件夹下的 UObject 资产，按类名过滤，返回 UObject 实例列表。

    :param scan_folder: 内容浏览器路径，例如 "/Game/WwiseAudio/Events"
    :param class_name: 要过滤的类名，例如 "AkAudioEvent"
    :return: UObject 实例列表
    """
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

    # 扫描文件夹下的所有资产
    asset_data_list = asset_registry.get_assets_by_path(scan_folder, recursive=True)
    unreal.log(f"[Python] Found {len(asset_data_list)} assets in {scan_folder}")

    filtered_assets = []

    for ad in asset_data_list:
        # 使用 ad.get_full_name() 获取完整路径，代替不存在的 object_path
        class_path_str = str(ad.asset_class_path)
        object_path_str = ad.get_full_name()

        # 打印每个资产信息
        unreal.log(f"[Python] Asset: {ad.asset_name} | ClassPath: {class_path_str} | FullName: {object_path_str}")

        # 如果 class_path 中包含目标类名，则认为匹配
        if class_name in class_path_str:
            try:
                obj = ad.get_asset()  # 获取 UObject 实例
                filtered_assets.append(obj)
            except Exception as e:
                unreal.log_warning(f"[Python] Failed to load asset {ad.asset_name}: {e}")

    unreal.log(f"[Python] Filtered {len(filtered_assets)} assets matching '{class_name}'")

    return filtered_assets


# ----------------------------
# 使用示例
# ----------------------------
if __name__ == "__main__":
    folder = "/Game/WwiseAudio/Events"
    class_name = "AkAudioEvent"

    assets = get_assets_by_class(folder, class_name)

    for a in assets:
        unreal.log(f"[Python] Loaded asset object: {a}")

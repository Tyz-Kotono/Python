import unreal

folder = "/Game/WwiseAudio/Events"
class_name = "AkAudioEvent"

# 获取资产注册器
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
asset_data_list = asset_registry.get_assets_by_path(folder, recursive=True)

for ad in asset_data_list:
    if class_name in str(ad.asset_class_path):
        try:
            # 获取 UObject 实例
            event_obj = ad.get_asset()
            # unreal.log(f"[Python] Loaded: {event_obj.get_name()}")

            # 访问 EventCookedData
            event_cooked_data = event_obj.get_editor_property("EventCookedData")

            # 访问 DebugName 属性
            debug_name = event_cooked_data.get_editor_property("DebugName")
            unreal.log(f"[Python] Wwise.path = {debug_name}")

        except Exception as e:
            unreal.log_warning(f"[Python] Failed to read asset {ad.asset_name}: {e}")

from pprint import pprint

import unreal
import os
import sys

folder = "/Game/WwiseAudio/Events"
class_name = "AkAudioEvent"

# 获取资产注册器
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
asset_data_list = asset_registry.get_assets_by_path(folder, recursive=True)
const_path = 'Game/WwiseAudio/'


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from PickleData.KeyValueStore import KeyValueStore
store = KeyValueStore()

for ad in asset_data_list:
    if class_name in str(ad.asset_class_path):
        try:

            # 获取 UObject 实例
            event_obj = ad.get_asset()
            event_path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(event_obj)
            event_name = event_obj.get_name()
            # 访问 EventCookedData
            event_cooked_data = event_obj.get_editor_property("EventCookedData")

            # 访问 DebugName 属性
            debug_name = str(event_cooked_data.get_editor_property("DebugName"))
            wwise_path = debug_name.replace("\\", "/")

            key = event_path
            value = f"{const_path}{wwise_path}.{event_name}"

            unreal.log_warning(f"[Python] Wwise : {const_path}{wwise_path}.{event_name}")
            unreal.log_error(f"[Python] Loaded: {event_path}")
            store.set(key,value)

            pprint(store.get(key))
        except Exception as e:
            unreal.log_warning(f"[Python] Failed to read asset {ad.asset_name}: {e}")

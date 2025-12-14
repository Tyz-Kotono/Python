
from PickleData.KeyValueStore import KeyValueStore

store = KeyValueStore()

# 写入
store.set("name", "Kotono")
store.set("age", 20)

# 读取
print(store.get("name"))   # "Kotono"
print(store.get("age"))    # 20
print(store.get("xxx"))    # None

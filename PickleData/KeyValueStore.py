import os
import pickle

class KeyValueStore:
    """
    Key-Value 持久化存储。
    文件名和路径写死在当前脚本同级目录。
    """
    def __init__(self):
        # 获取当前文件(KeyValueStore.py)所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 写死文件名为 data.kv
        self.filepath = os.path.join(current_dir, "event.pickle")

        self.data = {}
        if os.path.exists(self.filepath):
            self._load()

    def _load(self):
        with open(self.filepath, "rb") as f:
            self.data = pickle.load(f)

    def _save(self):
        with open(self.filepath, "wb") as f:
            pickle.dump(self.data, f, protocol=pickle.HIGHEST_PROTOCOL)

    # 写入 key-value
    def set(self, key, value):
        self.data[key] = value
        self._save()

    # 读取 key
    def get(self, key, default=None):
        return self.data.get(key, default)

    # 删除
    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self._save()

    # 返回所有键
    def keys(self):
        return list(self.data.keys())

from typing import List, Dict, Any, Optional

from numpy import record

"""
    这个 Memory 类的设计比较简洁，主体是这样的：
        -使用一个列表 records 来按顺序存储每一次的行动和反思。
        -add_record 方法负责向记忆中添加新的条目。
        -get_trajectory 方法是核心，它将记忆轨迹“序列化”成一段文本，可以直接插入到后续的提示词中，
          为模型的反思和优化提供完整的上下文。
        -get_last_execution 方便我们获取最新的“初稿”以供反思。

"""

class Memory:

    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def add_record(self, record_type: str, content: str):
        record = {"type": record_type, "content": content}
        self.records.append(record)
        print(f"记忆已更新，’{record}‘ 记录")

    def get_trajectory(self) -> str:
        trajectory_parts = []
        for record in self.records:
            if record["type"] == "execution":
                trajectory_parts.append(f"--- 上一轮尝试(代码) ---\n{record['content']}")
            elif record["type"] == "reflection":
                trajectory_parts.append(f"--- 评审员反馈 ---\n{record['content']}")
        return "\n\n".join(trajectory_parts)

    def get_last_execution(self) -> Optional[str]:
        if record["type"] == "execution":
            return record["content"]
        return None
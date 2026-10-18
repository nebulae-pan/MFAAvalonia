import random
import json
from typing import List, Union, Optional, Tuple, Dict, Any
from pathlib import Path

class Utils:
    @staticmethod
    def random_point_in_rect(box: List[int]) -> Tuple[int, int]:
        """
        生成矩形区域内的随机点坐标
        
        Args:
            box: 矩形区域
            
        Returns:
            Tuple[float, float]: 随机点的(x, y)坐标
        """
        random_x = random.randint(box[0], box[0] + box[2])
        random_y = random.randint(box[1], box[1] + box[3])
        return random_x, random_y 


    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """
        读取JSON配置文件
        
        Args:
            file_path: JSON文件路径
            
        Returns:
            Dict: 配置数据字典
            
        Raises:
            FileNotFoundError: 文件不存在
            json.JSONDecodeError: JSON格式错误
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件不存在: {file_path}")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"JSON格式错误: {file_path}", file_path, 0)

    @staticmethod
    def load_project_nodes() -> Dict[str, Any]:
        """
        Load all JSON files from the pipeline directory
        Returns a dictionary with filename as key and file content as value
        """
        task_nodes = {}
        pipeline_dir = Path("./resource/pipeline")
        if not pipeline_dir.exists():
            print(f"Pipeline directory {pipeline_dir} does not exist")
            return task_nodes
        
        # 遍历所有JSON文件
        for json_file in pipeline_dir.rglob("*.json"):
            try:
                pipeline_data = Utils.load_json(str(json_file))
                for key, value in pipeline_data.items():
                    task_nodes[key] = value
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
        
        print(f"Loaded {len(task_nodes)} pipeline nodes")
        return task_nodes
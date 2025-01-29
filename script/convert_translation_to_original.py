import os
import json
from pathlib import Path

def convert_file(file_path):
    """转换单个JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 处理description
    if 'description' in data and 'original' in data['description']:
        data['description']['translation'] = data['description']['original']
    
    # 处理dict
    if 'dict' in data:
        data['dict'] = {k: k for k in data['dict'].keys()}
    
    return data

def process_directory(root_dir):
    """处理整个目录"""
    for root, dirs, files in os.walk(root_dir):
        if 'zh-cn' in root:
            # 构建目标路径（移除zh-cn目录）
            target_dir = root.replace('/zh-cn', '')
            Path(target_dir).mkdir(parents=True, exist_ok=True)
            
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    target_path = os.path.join(target_dir, file)
                    
                    # 转换并保存到新位置
                    converted_data = convert_file(file_path)
                    with open(target_path, 'w', encoding='utf-8') as f:
                        json.dump(converted_data, f, ensure_ascii=False, indent=2)
                    
                    print(f'Processed: {file_path} -> {target_path}')

if __name__ == '__main__':
    # 设置translation/dict为根目录
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'translation', 'dict')
    process_directory(base_dir)
    print('All files processed successfully.')
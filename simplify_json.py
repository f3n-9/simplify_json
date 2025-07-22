import json
import os

# 读取 JSON 文件
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# 从JSON中提取spans内容
def extract_spans_from_json(data):
    simplified_data = []

    # 递归查找spans
    def find_all_spans(obj):
        if isinstance(obj, dict):
            # 如果当前对象有spans字段，添加
            if 'spans' in obj and isinstance(obj['spans'], list):
                simplified_data.extend(obj['spans'])

            # 递归处理字典中的所有值
            for value in obj.values():
                find_all_spans(value)

        elif isinstance(obj, list):
            # 递归处理列表中的所有元素
            for item in obj:
                find_all_spans(item)

    # 开始递归查找
    find_all_spans(data)

    return simplified_data


# 保存简化后的 JSON 到文件
def save_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# 简化JSON文件的主函数
def simplify_json(input_folder='input', output_to_folder=False, output_folder='output'):
    """
    简化 JSON 文件的主要处理函数

    Args:
        input_folder (str): 输入文件夹路径，默认为'input'
        output_to_folder (bool): 是否输出到指定文件夹，False为默认模式（原地输出），True为集中输出模式
        output_folder (str): 输出文件夹路径，默认为'output'

    Returns:
        list: 成功处理的文件列表
    """
    # 递归搜索所有layout.json文件
    layout_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file == 'layout.json':
                layout_files.append(os.path.join(root, file))

    if not layout_files:
        print(f"No layout.json files found in {input_folder}")
        return []

    # 如果选择集中输出模式，确保输出文件夹存在
    if output_to_folder:
        os.makedirs(output_folder, exist_ok=True)

    processed_files = []

    for layout_file in layout_files:
        try:
            if output_to_folder:
                # 集中输出模式：获取原文件夹名称
                folder_name = os.path.basename(os.path.dirname(layout_file))
                output_filename = f'simplified_layout_{folder_name}.json'
                output_path = os.path.join(output_folder, output_filename)
            else:
                # 默认模式：在同一目录下输出
                output_path = os.path.join(os.path.dirname(layout_file), 'simplified_layout.json')

            # 加载 JSON
            data = load_json(layout_file)

            # 简化 JSON
            simplified_data = extract_spans_from_json(data)

            # 保存结果
            save_json(simplified_data, output_path)
            print(f"Processed {layout_file} -> {output_path}")
            processed_files.append(layout_file)

        except Exception as e:
            print(f"Error processing {layout_file}: {e}")

    return processed_files


# 主函数
def main(input_folder='input', output_to_folder=True, output_folder='output'):
    simplify_json(input_folder, output_to_folder, output_folder)


if __name__ == '__main__':
    main()
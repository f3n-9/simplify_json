import json
import os

# 读取 JSON 文件
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# 从JSON中提取spans内容
def extract_spans_from_json(data):
    """
    从嵌套的JSON结构中提取所有的 'spans' 列表，并将它们扁平化到一个列表中。
    每个 span 字典都会被添加一个 'page_num' 键，表示它所在的页面。

    Args:
        data (dict): 从 layout.json 文件加载的原始JSON数据。

    Returns:
        list: 一个包含所有提取出的 span 字典的列表。
    """
    simplified_data = []  # 用于存储所有提取出的 span
    current_page = 0  # 默认页码
    page_span_indices = {} # 用于存储每个页面的 span 索引

    def find_spans_recursive(obj, page):
        nonlocal page_span_indices
        """
        一个递归函数，用于深度遍历JSON对象（字典或列表）以查找 'spans'。

        Args:
            obj (dict or list): 当前正在遍历的JSON部分。
            page (str): 当前上下文的页码。
        """
        if isinstance(obj, dict):
            # 如果在字典中找到 'page_num'，则更新当前页码。
            # 这允许更深层级的对象覆盖从上层传递下来的页码。
            if "page_num" in obj:
                page_val = obj["page_num"]
                if isinstance(page_val, str) and page_val.startswith("page_"):
                    try:
                        page = int(page_val.split('_')[1])
                    except (ValueError, IndexError):
                        pass # 如果格式不正确，则保持当前页码
                elif isinstance(page_val, int):
                    page = page_val

            # 如果找到 'spans' 键，并且其值是一个列表
            if 'spans' in obj and isinstance(obj['spans'], list):
                for span in obj['spans']:
                    # 获取或初始化当前页面的索引
                    if page not in page_span_indices:
                        page_span_indices[page] = 1

                    span_index = page_span_indices[page]

                    # 创建一个新字典，首先添加 index
                    indexed_span = {'index': span_index}
                    # 然后添加原始 span 的所有键值对
                    indexed_span.update(span)
                    # 最后添加或更新 page_num
                    indexed_span['page_num'] = page
                    simplified_data.append(indexed_span)

                    # 增加当前页面的索引
                    page_span_indices[page] += 1

            # 递归遍历字典中的所有值
            for key, value in obj.items():
                # 避免重复处理已经添加的 spans
                if key != 'spans':
                    find_spans_recursive(value, page)

        elif isinstance(obj, list):
            # 如果是列表，则递归遍历列表中的每一项
            for item in obj:
                find_spans_recursive(item, page)

    # 函数执行的入口点：从 "pdf_info" 开始遍历
    if "pdf_info" in data and isinstance(data["pdf_info"], list):
        # 遍历每一页的信息
        for pdf_page_info in data["pdf_info"]:
            # 从页面信息中确定页码，如果不存在则使用默认值
            page_from_pdf_info = pdf_page_info.get('page_idx', current_page)

            # 检查页面中是否有 "para_blocks"（段落块）
            if "para_blocks" in pdf_page_info and isinstance(pdf_page_info["para_blocks"], list):
                # 遍历每个段落块
                for para_block in pdf_page_info["para_blocks"]:
                    # 段落块级别也可能有页码，优先使用它
                    page_from_para_block = para_block.get('page_idx', page_from_pdf_info)
                    # 从这个段落块开始递归查找 spans
                    find_spans_recursive(para_block, page_from_para_block)

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
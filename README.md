# Simplify JSON 工具使用文档

## 概述

Simplify JSON 是一个专门用于处理 MinerU 输出的 `layout.json` 文件的工具。该工具能够从复杂的 PDF 布局分析结果中提取纯文本内容，将其转换为适合大模型 RAG（检索增强生成）系统输入的简化格式。

MinerU 输出的 layout.json 文件包含详细的页面布局信息、坐标数据和各种元数据，而 RAG 系统通常只需要其中的文本内容。本工具通过递归提取所有 `spans` 字段中的内容，生成清洁、结构化的文本数据。

## 主要功能

- 🔍 **自动搜索**：递归搜索指定目录下所有名为 `layout.json` 的文件
- 📝 **内容提取**：从复杂的 JSON 结构中递归提取所有 `spans` 内容
- ✨ **页码注入**：为每个提取的 `span` 自动添加整数格式的 `page_num` 字段，标明其所在的页码
- 🔢 **页内索引**：为每个 `span` 添加一个从1开始的、在**当前页面内**唯一的 `index`，方便后续处理和溯源
- 📂 **灵活输出**：支持两种输出模式（原地输出/集中输出）
- 🚀 **批量处理**：一次性处理多个文件
- 🛡️ **错误处理**：包含异常处理，确保单个文件错误不影响整体处理

## 安装要求

- Python 3.6+
- 无需额外依赖包（仅使用标准库）

## 使用方法

### 1. 基本用法

```python
from simplify_json import simplify_json

# 使用默认参数（集中输出模式）
simplify_json()

# 指定输入目录
simplify_json(input_folder='my_input_folder')

# 指定输出目录
simplify_json(output_folder='my_output_folder')
```

### 2. 命令行使用

```bash
# 直接运行脚本（使用默认参数）
python simplify_json.py
```

### 3. 输出模式选择

#### 集中输出模式（默认）
```python
simplify_json(
    input_folder='input',
    output_to_folder=True,        # 集中输出
    output_folder='output'
)
```

#### 原地输出模式
```python
simplify_json(
    input_folder='input',
    output_to_folder=False,       # 原地输出
    output_folder='output'        # 此参数在原地输出模式下会被忽略
)
```

## 参数说明

### `simplify_json()` 函数参数

| 参数 | 类型 | 默认值        | 说明 |
|------|------|------------|------|
| `input_folder` | str | `'input'`  | 输入文件夹路径，工具会递归搜索此目录下的所有 `layout.json` 文件 |
| `output_to_folder` | bool | `True`     | 输出模式选择：<br/>- `True`：集中输出到指定文件夹<br/>- `False`：在原文件同目录下输出 |
| `output_folder` | str | `'output'` | 输出文件夹路径（仅在集中输出模式下有效） |

## 输入文件格式

工具处理的输入文件必须命名为 `layout.json`，文件应包含嵌套的 JSON 结构，其中包含 `spans` 字段。

### 示例输入结构：
```json
{
    "pdf_info": [
        {
            "para_blocks": [
                {
                    "type": "title",
                    "bbox": [x1, y1, x2, y2],
                    "lines": [
                        {
                            "bbox": [x1, y1, x2, y2],
                            "spans": [
                                {
                                    "bbox": [x1, y1, x2, y2],
                                    "score": 1.0,
                                    "content": "文本内容",
                                    "type": "text"
                                }
                            ],
                            "index": 0
                        }
                    ],
                    "index": 0
                }
            ]
        }
    ]
}
```

## 输出文件格式

工具会提取所有 `spans` 内容并生成简化的 JSON 数组。每个 `span` 对象都会被添加 `index` 和 `page_num` 字段。

### 示例输出：
```json
[
    {
        "index": 1,
        "bbox": [x1, y1, x2, y2],
        "score": 1.0,
        "content": "文本内容1",
        "type": "text",
        "page_num": 0
    },
    {
        "index": 2,
        "bbox": [x1, y1, x2, y2],
        "score": 1.0,
        "content": "文本内容2",
        "type": "text",
        "page_num": 0
    },
    {
        "index": 1,
        "bbox": [x1, y1, x2, y2],
        "score": 1.0,
        "content": "另一页的文本",
        "type": "text",
        "page_num": 1
    }
]
```

## 输出文件命名规则

### 集中输出模式
- 文件名格式：`simplified_layout_{文件夹名}.json`
- 示例：
  - `input/doc1/layout.json` → `output/simplified_layout_doc1.json`
  - `input/doc2/layout.json` → `output/simplified_layout_doc2.json`

### 原地输出模式
- 文件名：`simplified_layout.json`
- 位置：与原 `layout.json` 文件相同目录
- 示例：
  - `input/doc1/layout.json` → `input/doc1/simplified_layout.json`

## 目录结构示例

```
项目根目录/
├── simplify_json.py      # 主程序文件
├── input/                # 输入目录
│   ├── doc1/
│   │   └── layout.json
│   └── doc2/
│       └── layout.json
└── output/               # 输出目录（集中输出模式）
    ├── simplified_layout_doc1.json
    └── simplified_layout_doc2.json
```

## 错误处理

- 如果指定目录中没有找到 `layout.json` 文件，程序会显示提示信息
- 如果处理单个文件时出现错误，程序会显示错误信息但继续处理其他文件
- 程序会返回成功处理的文件列表

## 返回值

`simplify_json()` 函数返回一个列表，包含所有成功处理的 `layout.json` 文件路径。

```python
processed_files = simplify_json()
print(f"成功处理了 {len(processed_files)} 个文件")
```

## 常见用例

### 1. 批量处理 PDF 解析结果
```python
# 处理 OCR 或 PDF 解析工具生成的布局文件
simplify_json(
    input_folder='pdf_layouts',
    output_to_folder=True,
    output_folder='simplified_results'
)
```

### 2. 数据预处理
```python
# 为机器学习或文本分析准备数据
processed = simplify_json(input_folder='raw_data')
print(f"预处理完成，共处理 {len(processed)} 个文件")
```

### 3. 集成到数据处理管道
```python
import os
from simplify_json import simplify_json

def process_pdf_data(source_dir, target_dir):
    """处理PDF数据的完整流程"""
    # 确保输出目录存在
    os.makedirs(target_dir, exist_ok=True)

    # 简化JSON数据
    processed_files = simplify_json(
        input_folder=source_dir,
        output_to_folder=True,
        output_folder=target_dir
    )

    return processed_files
```

## 注意事项

1. **文件编码**：所有 JSON 文件使用 UTF-8 编码
2. **文件权限**：确保对输入目录有读权限，对输出目录有写权限
3. **大文件处理**：对于非常大的 JSON 文件，处理可能需要较长时间
4. **内存使用**：工具会将整个 JSON 文件加载到内存中，请确保有足够的内存

## 版本信息

- 当前版本：1.0
- Python 兼容性：3.6+
- 依赖：仅使用 Python 标准库

## 支持

如有问题或建议，请检查：
1. 输入文件格式是否正确
2. 文件路径是否存在
3. 是否有足够的文件权限
4. JSON 文件是否有效

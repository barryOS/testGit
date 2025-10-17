# 快速开始 / Quick Start

## 5分钟上手 / Get Started in 5 Minutes

### 1. 安装 / Install

```bash
pip install -r requirements.txt
```

### 2. 基本使用 / Basic Usage

#### 识别单张图片 / Recognize Single Image

```bash
python main.py -i your_image.jpg -o ./output
```

#### 识别PDF / Recognize PDF

```bash
python main.py -i document.pdf -o ./output --pdf
```

#### 批量处理 / Batch Process

```bash
python main.py -i ./images_folder -o ./output --batch
```

### 3. 常用参数 / Common Options

| 参数 | 说明 | 示例 |
|------|------|------|
| `-i` | 输入文件/目录 | `-i photo.jpg` |
| `-o` | 输出目录 | `-o ./results` |
| `-l` | 语言 (ch/en) | `-l ch` |
| `-f` | 格式 (txt/json/md) | `-f json` |
| `-c` | 置信度阈值 | `-c 0.7` |
| `--pdf` | 处理PDF | `--pdf` |
| `--batch` | 批量处理 | `--batch` |
| `--gpu` | 使用GPU | `--gpu` |
| `--preprocess` | 图像预处理 | `--preprocess` |

### 4. Python代码示例 / Python Code Example

```python
from src.ocr_engine import OCREngine

# 初始化
ocr = OCREngine(lang='ch', use_gpu=False)

# 识别
text, details = ocr.recognize_and_extract('image.jpg')

# 输出
print(text)
```

## 常见问题 / FAQ

### 识别不准确？
尝试: `--preprocess` 参数

### 速度太慢？
尝试: `--gpu` 参数（需要GPU）

### 首次运行慢？
正常，PaddleOCR会下载模型（约几百MB）

## 更多文档 / More Documentation

- 📖 [完整文档 README.md](README.md)
- 📖 [中文文档 README_CN.md](README_CN.md)
- 🔧 [API文档 API.md](API.md)
- 💻 [安装指南 INSTALL.md](INSTALL.md)

## 示例命令 / Example Commands

```bash
# 高质量识别
python main.py -i doc.jpg -o output --preprocess -c 0.8 -f json

# PDF批量处理
python main.py -i ./pdfs -o output --pdf --batch --dpi 400

# 英文识别
python main.py -i english.png -o output -l en

# GPU加速批处理
python main.py -i ./images -o output --batch --gpu
```

开始使用吧！ / Start OCR-ing! 🚀

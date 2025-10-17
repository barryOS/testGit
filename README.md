# 高精度中英文OCR文档识别系统 / High-Accuracy Chinese-English OCR Document Recognition System

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![PaddleOCR](https://img.shields.io/badge/PaddleOCR-2.7+-green.svg)](https://github.com/PaddlePaddle/PaddleOCR)

一个基于PaddleOCR的高精度中英文文档识别系统，支持图片和PDF文档的OCR识别。

A high-accuracy OCR document recognition system based on PaddleOCR, supporting both image and PDF document recognition for Chinese and English.

## ✨ 特性 / Features

- 🎯 **高精度识别** / High Accuracy: 基于PaddleOCR，对中英文文档识别准确率高
- 🖼️ **多格式支持** / Multiple Formats: 支持JPG, PNG, BMP, TIFF等图片格式和PDF文档
- 🔧 **图像预处理** / Image Preprocessing: 内置多种图像预处理功能，提高识别精度
- 📦 **批量处理** / Batch Processing: 支持批量处理整个文件夹的文档
- 💾 **多种输出格式** / Multiple Output Formats: 支持TXT, JSON, Markdown格式输出
- ⚡ **GPU加速** / GPU Acceleration: 支持GPU加速，提高处理速度
- 🌍 **多语言支持** / Multi-language: 支持中文、英文、繁体中文、日文、韩文等

## 📋 系统要求 / Requirements

- Python 3.7+
- PaddlePaddle 2.5.0+
- OpenCV 4.8.0+

## 🚀 快速开始 / Quick Start

### 安装 / Installation

```bash
# 克隆项目
git clone <repository-url>
cd <project-directory>

# 安装依赖
pip install -r requirements.txt
```

### 基本使用 / Basic Usage

#### 1. 识别单张图片 / Recognize Single Image

```bash
python main.py -i /path/to/image.jpg -o ./output
```

#### 2. 识别PDF文档 / Recognize PDF Document

```bash
python main.py -i /path/to/document.pdf -o ./output --pdf
```

#### 3. 批量处理 / Batch Processing

```bash
python main.py -i /path/to/images_folder -o ./output --batch
```

#### 4. 使用图像预处理 / With Image Preprocessing

```bash
python main.py -i /path/to/image.jpg -o ./output --preprocess
```

#### 5. 使用GPU加速 / With GPU Acceleration

```bash
python main.py -i /path/to/image.jpg -o ./output --gpu
```

## 📖 详细用法 / Detailed Usage

### 命令行参数 / Command Line Arguments

```
usage: main.py [-h] -i INPUT [-o OUTPUT] [-l {ch,en,chinese_cht,korean,japan}]
               [-f {txt,json,md}] [-c CONFIDENCE] [--gpu] [--preprocess] [--pdf]
               [--dpi DPI] [--batch] [--log LOG]

optional arguments:
  -h, --help            显示帮助信息 / Show help message
  -i, --input INPUT     输入文件或目录路径 / Input file or directory path
  -o, --output OUTPUT   输出目录路径 (默认: ./output) / Output directory (default: ./output)
  -l, --lang {ch,en,chinese_cht,korean,japan}
                        OCR语言 (默认: ch) / OCR language (default: ch)
  -f, --format {txt,json,md}
                        输出格式 (默认: txt) / Output format (default: txt)
  -c, --confidence CONFIDENCE
                        置信度阈值 (0-1, 默认: 0.5) / Confidence threshold (0-1, default: 0.5)
  --gpu                 使用GPU加速 / Use GPU acceleration
  --preprocess          启用图像预处理 / Enable image preprocessing
  --pdf                 处理PDF文件 / Process PDF files
  --dpi DPI             PDF转图像DPI (默认: 300) / PDF to image DPI (default: 300)
  --batch               批量处理目录中的所有文件 / Batch process all files
  --log LOG             日志文件路径 / Log file path
```

### 示例 / Examples

#### 高质量PDF识别 / High-Quality PDF Recognition

```bash
python main.py -i document.pdf -o ./results --pdf --dpi 400 --confidence 0.7 -f md
```

#### 批量处理并输出JSON / Batch Process with JSON Output

```bash
python main.py -i ./images -o ./results --batch -f json --confidence 0.6
```

#### 英文文档识别 / English Document Recognition

```bash
python main.py -i english_doc.png -o ./results -l en --preprocess
```

## 🏗️ 项目结构 / Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── ocr_engine.py          # OCR核心引擎 / OCR Core Engine
│   ├── image_processor.py     # 图像预处理 / Image Preprocessing
│   ├── pdf_processor.py       # PDF处理 / PDF Processing
│   ├── text_processor.py      # 文本后处理 / Text Post-processing
│   └── utils.py               # 工具函数 / Utility Functions
├── examples/                  # 示例文件 / Example Files
├── tests/                     # 测试文件 / Test Files
├── output/                    # 输出目录 / Output Directory
├── main.py                    # 主程序入口 / Main Entry Point
├── requirements.txt           # 依赖列表 / Dependencies
├── .gitignore
└── README.md
```

## 🔧 核心功能模块 / Core Modules

### OCREngine (ocr_engine.py)

OCR识别核心引擎，基于PaddleOCR实现。

Core OCR recognition engine based on PaddleOCR.

**主要功能 / Main Features:**
- 单张图片识别 / Single image recognition
- 批量识别 / Batch recognition
- 文本提取和置信度过滤 / Text extraction with confidence filtering

### ImageProcessor (image_processor.py)

图像预处理模块，提高OCR识别精度。

Image preprocessing module to improve OCR accuracy.

**预处理功能 / Preprocessing Features:**
- 去噪 / Denoising
- 倾斜矫正 / Deskewing
- 二值化 / Binarization
- 对比度增强 / Contrast enhancement
- 尺寸调整 / Resizing
- 锐化 / Sharpening

### PDFProcessor (pdf_processor.py)

PDF文档处理模块。

PDF document processing module.

**功能 / Features:**
- PDF转图像 / PDF to images conversion
- 分页处理 / Page-by-page processing
- 完整文档文本提取 / Full document text extraction

### TextProcessor (text_processor.py)

文本后处理模块。

Text post-processing module.

**功能 / Features:**
- 文本清理 / Text cleaning
- 去重 / Deduplication
- 按位置排序 / Position-based sorting
- 分行重组 / Line reconstruction
- 统计信息 / Statistics

## 🎨 输出格式 / Output Formats

### TXT格式 / TXT Format

纯文本输出，包含识别的所有文字。

Plain text output with all recognized text.

### JSON格式 / JSON Format

结构化数据输出，包含文本、位置、置信度等详细信息。

Structured data output with text, position, confidence, and more.

```json
{
  "file": "example.jpg",
  "text": "识别的文本内容...",
  "details": [
    {
      "text": "文本块1",
      "confidence": 0.95,
      "position": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    }
  ],
  "statistics": {
    "total_items": 10,
    "average_confidence": 0.92,
    "total_characters": 150
  }
}
```

### Markdown格式 / Markdown Format

Markdown文档输出，包含元数据和格式化的文本内容。

Markdown document output with metadata and formatted text.

## ⚙️ 性能优化建议 / Performance Optimization Tips

1. **使用GPU加速** / Use GPU Acceleration
   - 安装GPU版本的PaddlePaddle
   - 使用`--gpu`参数

2. **调整置信度阈值** / Adjust Confidence Threshold
   - 提高阈值可以过滤低质量结果
   - 推荐值：0.5-0.7

3. **图像预处理** / Image Preprocessing
   - 对于低质量图片使用`--preprocess`
   - 可显著提高识别准确率

4. **PDF DPI设置** / PDF DPI Settings
   - 高质量文档使用400-600 DPI
   - 普通文档使用300 DPI
   - 扫描件可降低至200 DPI

## 🐛 常见问题 / FAQ

### Q: 识别结果不准确怎么办？ / Recognition results are inaccurate?

A: 尝试以下方法：
- 使用`--preprocess`启用图像预处理
- 提高置信度阈值`-c 0.7`
- 确保图片清晰度足够高
- 选择正确的语言参数`-l`

### Q: 处理速度慢？ / Processing is slow?

A: 可以尝试：
- 使用GPU加速`--gpu`
- 降低PDF的DPI设置
- 减小图片尺寸

### Q: 支持哪些图片格式？ / What image formats are supported?

A: 支持常见的图片格式：JPG, JPEG, PNG, BMP, TIFF, TIF

## 📝 开发指南 / Development Guide

### 作为Python模块使用 / Use as Python Module

```python
from src.ocr_engine import OCREngine
from src.image_processor import ImageProcessor
from src.text_processor import TextProcessor

# 初始化OCR引擎
ocr = OCREngine(lang='ch', use_gpu=False)

# 识别图片
full_text, extracted_data = ocr.recognize_and_extract('image.jpg')

# 文本处理
stats = TextProcessor.get_statistics(extracted_data)
print(f"识别了 {stats['total_items']} 个文本块")
print(f"平均置信度: {stats['average_confidence']:.2%}")
print(f"识别文本:\n{full_text}")
```

### 自定义图像预处理 / Custom Image Preprocessing

```python
from src.image_processor import ImageProcessor
import cv2

# 加载并预处理图像
image = ImageProcessor.load_image('input.jpg')
image = ImageProcessor.denoise(image)
image = ImageProcessor.deskew(image)
image = ImageProcessor.enhance_contrast(image)

# 保存预处理结果
ImageProcessor.save_image(image, 'processed.jpg')
```

## 🤝 贡献 / Contributing

欢迎提交Issue和Pull Request！

Issues and Pull Requests are welcome!

## 📄 许可证 / License

MIT License

## 🙏 致谢 / Acknowledgments

本项目基于以下开源项目：

This project is based on the following open-source projects:

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - 百度飞桨OCR工具库
- [OpenCV](https://opencv.org/) - 计算机视觉库
- [pdf2image](https://github.com/Belval/pdf2image) - PDF转图像工具

## 📞 联系方式 / Contact

如有问题或建议，请提交Issue。

For questions or suggestions, please submit an Issue.

---

**注意**: 首次运行时，PaddleOCR会自动下载模型文件，可能需要一些时间。

**Note**: On first run, PaddleOCR will automatically download model files, which may take some time.

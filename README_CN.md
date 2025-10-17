# 高精度中英文OCR文档识别系统

一个功能强大、易于使用的OCR文档识别系统，基于百度飞桨PaddleOCR，专为中英文文档设计。

## 🎯 项目特点

### 高精度识别
- 基于PaddleOCR深度学习模型
- 对中文、英文、数字、符号均有出色表现
- 支持印刷体和部分手写体识别
- 可自定义置信度阈值过滤低质量结果

### 图像预处理
内置多种图像增强技术，提高识别准确率：
- **去噪处理**: 消除图像噪点
- **倾斜矫正**: 自动检测并矫正文档倾斜
- **对比度增强**: 提高文字清晰度
- **二值化处理**: 适用于扫描文档
- **锐化处理**: 增强边缘细节

### PDF支持
- 高质量PDF转图像（可自定义DPI）
- 逐页识别并提取文本
- 保留页码信息
- 支持大型PDF文档

### 批量处理
- 一次处理整个文件夹
- 进度条显示处理状态
- 并行处理提高效率
- 错误容错，单个文件失败不影响整体处理

### 多种输出格式
- **TXT**: 纯文本格式，便于阅读
- **JSON**: 结构化数据，包含位置和置信度信息
- **Markdown**: 带格式的文档，包含元数据

## 📦 安装

### 系统要求
- Python 3.7+
- 2GB以上可用内存
- （可选）NVIDIA GPU用于加速

### 快速安装

```bash
# 1. 克隆项目
git clone <repository-url>
cd <project-directory>

# 2. 安装依赖（CPU版本）
pip install -r requirements.txt

# 3. 验证安装
python main.py --help
```

详细安装说明请查看 [INSTALL.md](INSTALL.md)

## 🚀 使用方法

### 命令行使用

#### 基础示例

```bash
# 识别单张图片
python main.py -i photo.jpg -o ./results

# 识别PDF文档
python main.py -i document.pdf -o ./results --pdf

# 批量处理文件夹
python main.py -i ./images -o ./results --batch
```

#### 高级选项

```bash
# 使用图像预处理提高质量
python main.py -i low_quality.jpg -o ./results --preprocess

# 指定语言（英文）
python main.py -i english.jpg -o ./results -l en

# 设置置信度阈值
python main.py -i photo.jpg -o ./results -c 0.7

# 输出JSON格式
python main.py -i photo.jpg -o ./results -f json

# 高DPI PDF处理
python main.py -i document.pdf -o ./results --pdf --dpi 400

# 使用GPU加速
python main.py -i photo.jpg -o ./results --gpu
```

#### 组合使用

```bash
# 批量处理PDF，启用预处理，输出Markdown
python main.py -i ./pdfs -o ./results --pdf --batch --preprocess -f md -c 0.8

# 处理多个图片，使用GPU，保存日志
python main.py -i ./images -o ./results --batch --gpu --log ./logs/ocr.log
```

### Python API使用

#### 简单示例

```python
from src.ocr_engine import OCREngine

# 初始化OCR引擎
ocr = OCREngine(lang='ch', use_gpu=False)

# 识别图片
text, details = ocr.recognize_and_extract('photo.jpg')

# 打印结果
print("识别文本:")
print(text)

print(f"\n识别了 {len(details)} 个文本块")
```

#### 完整工作流

```python
from src.ocr_engine import OCREngine
from src.image_processor import ImageProcessor
from src.text_processor import TextProcessor
from src.utils import OutputFormatter

# 1. 图像预处理
processed = ImageProcessor.preprocess_for_ocr(
    'input.jpg',
    apply_denoise=True,
    apply_deskew=True,
    enhance_contrast=True
)

# 2. OCR识别
ocr = OCREngine(lang='ch')
result = ocr.recognize_numpy(processed)
extracted = ocr.extract_text(result, confidence_threshold=0.7)

# 3. 文本处理
filtered = TextProcessor.filter_by_confidence(extracted, 0.8)
stats = TextProcessor.get_statistics(filtered)

# 4. 保存结果
full_text = ocr.get_full_text(result)
OutputFormatter.save_as_txt(full_text, 'output.txt')

print(f"平均置信度: {stats['average_confidence']:.2%}")
```

#### 批量处理示例

```python
from src.ocr_engine import OCREngine
from src.utils import FileScanner
from tqdm import tqdm

ocr = OCREngine(lang='ch')

# 扫描所有图片
images = FileScanner.get_image_files('./input_folder')

# 批量处理
for image_path in tqdm(images, desc="处理中"):
    try:
        text, details = ocr.recognize_and_extract(image_path)
        # 处理结果...
    except Exception as e:
        print(f"处理失败 {image_path}: {e}")
```

## 🎨 应用场景

### 1. 文档数字化
- 扫描纸质文档转电子文本
- 旧档案数字化保存
- 书籍内容提取

### 2. 票据识别
- 发票信息提取
- 收据识别
- 证件识别

### 3. 图片文字提取
- 社交媒体图片文字提取
- 截图文字识别
- PPT内容提取

### 4. 批量处理
- 大量文档批处理
- 图书馆资料数字化
- 企业档案管理

## 🔧 性能优化

### 提高识别速度

1. **使用GPU加速**
   ```bash
   python main.py -i image.jpg -o output --gpu
   ```
   速度提升: 3-5倍

2. **批量处理**
   - 一次处理多个文件比单独处理更快
   - 减少模型加载时间

3. **调整图像大小**
   - 过大的图片会降低速度
   - 建议最大尺寸2048x2048

### 提高识别准确率

1. **使用图像预处理**
   ```bash
   python main.py -i image.jpg -o output --preprocess
   ```

2. **调整置信度阈值**
   ```bash
   python main.py -i image.jpg -o output -c 0.7
   ```

3. **选择合适的语言模型**
   ```bash
   # 纯英文文档
   python main.py -i english.jpg -o output -l en
   ```

4. **优化输入图片质量**
   - 确保图片清晰、对比度高
   - 避免模糊、过曝或欠曝
   - 推荐分辨率: 300 DPI以上

### PDF处理优化

```bash
# 高质量文档
python main.py -i doc.pdf -o output --pdf --dpi 400

# 扫描件
python main.py -i scan.pdf -o output --pdf --dpi 300 --preprocess

# 大型PDF（分批处理）
python main.py -i large.pdf -o output --pdf --confidence 0.7
```

## 📊 输出格式说明

### TXT格式
```
这是第一行文本
这是第二行文本
...
```

### JSON格式
```json
{
  "file": "input.jpg",
  "text": "完整文本内容...",
  "details": [
    {
      "text": "文本块内容",
      "confidence": 0.95,
      "position": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    }
  ],
  "statistics": {
    "total_items": 10,
    "average_confidence": 0.92,
    "min_confidence": 0.85,
    "max_confidence": 0.98,
    "total_characters": 150
  }
}
```

### Markdown格式
```markdown
# OCR Recognition Result

## Metadata
- **Source File**: input.jpg
- **Total Items**: 10
- **Average Confidence**: 92.00%
- **Total Characters**: 150

## Content
识别的文本内容...
```

## 🐛 常见问题

### Q1: 识别结果不准确
**解决方案:**
1. 使用 `--preprocess` 参数启用图像预处理
2. 提高输入图片质量
3. 调整置信度阈值 `-c 0.7`
4. 确保选择了正确的语言 `-l ch` 或 `-l en`

### Q2: 处理速度慢
**解决方案:**
1. 使用 GPU 加速 `--gpu`
2. 降低 PDF 的 DPI `--dpi 200`
3. 减小图片尺寸
4. 使用批量处理而非单个处理

### Q3: 内存不足
**解决方案:**
1. 处理大型 PDF 时降低 DPI
2. 减小图片尺寸
3. 分批处理而非一次处理全部

### Q4: 中英文混合识别效果差
**解决方案:**
1. 使用默认的 `ch` 语言模型（支持中英混合）
2. 启用图像预处理
3. 提高置信度阈值

### Q5: 模型下载失败
**解决方案:**
1. 检查网络连接
2. 使用国内镜像安装依赖
3. 手动下载模型文件到 `~/.paddleocr/` 目录

## 📝 更新日志

### v1.0.0 (当前版本)
- ✅ 支持中英文高精度识别
- ✅ 图像预处理功能
- ✅ PDF文档处理
- ✅ 批量处理
- ✅ 多种输出格式
- ✅ GPU加速支持
- ✅ 命令行和API两种使用方式

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📧 联系方式

如有问题请提交 Issue 或参考文档。

## 🙏 致谢

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [OpenCV](https://opencv.org/)
- [pdf2image](https://github.com/Belval/pdf2image)

# API文档 / API Documentation

本文档介绍如何将OCR系统作为Python模块使用。

This document describes how to use the OCR system as a Python module.

## 目录 / Table of Contents

- [OCREngine](#ocrengine) - OCR识别核心引擎
- [ImageProcessor](#imageprocessor) - 图像预处理
- [PDFProcessor](#pdfprocessor) - PDF文档处理
- [TextProcessor](#textprocessor) - 文本后处理
- [Utils](#utils) - 工具函数

---

## OCREngine

OCR识别核心引擎类。

Core OCR recognition engine class.

### 初始化 / Initialization

```python
from src.ocr_engine import OCREngine

ocr = OCREngine(
    use_angle_cls=True,  # 是否使用角度分类 / Use angle classification
    lang='ch',           # 语言: 'ch', 'en', 'chinese_cht', etc.
    use_gpu=False,       # 是否使用GPU / Use GPU
    show_log=False       # 是否显示日志 / Show logs
)
```

### 方法 / Methods

#### recognize_image()

识别单张图片。

Recognize a single image.

```python
result = ocr.recognize_image(
    image_path='path/to/image.jpg',
    cls=True  # 是否进行角度分类 / Perform angle classification
)
```

**返回值 / Returns:** PaddleOCR原始结果格式

#### recognize_and_extract()

识别图片并提取结构化数据。

Recognize image and extract structured data.

```python
full_text, extracted_data = ocr.recognize_and_extract(
    image_path='path/to/image.jpg',
    confidence_threshold=0.5,  # 置信度阈值 / Confidence threshold
    cls=True
)

# full_text: 完整文本字符串
# extracted_data: 列表，每个元素包含text, confidence, position
```

#### batch_recognize()

批量识别多张图片。

Batch recognize multiple images.

```python
results = ocr.batch_recognize(
    image_paths=['image1.jpg', 'image2.jpg'],
    confidence_threshold=0.5,
    cls=True
)

# 返回列表，每个元素包含file, text, details, success
```

#### extract_text()

从PaddleOCR结果中提取文本数据。

Extract text data from PaddleOCR results.

```python
extracted_data = ocr.extract_text(
    result=ocr_result,
    confidence_threshold=0.5
)

# 返回列表: [{'text': str, 'confidence': float, 'position': list}, ...]
```

#### get_full_text()

获取完整的文本字符串。

Get full text string.

```python
full_text = ocr.get_full_text(
    result=ocr_result,
    confidence_threshold=0.5,
    separator='\n'  # 文本分隔符 / Text separator
)
```

---

## ImageProcessor

图像预处理工具类。

Image preprocessing utility class.

### 方法 / Methods

#### load_image()

加载图片。

Load an image.

```python
from src.image_processor import ImageProcessor

image = ImageProcessor.load_image('path/to/image.jpg')
# 返回numpy数组 / Returns numpy array
```

#### preprocess_for_ocr()

一站式图像预处理。

All-in-one image preprocessing.

```python
processed_image = ImageProcessor.preprocess_for_ocr(
    image_path='path/to/image.jpg',
    apply_denoise=True,      # 去噪 / Denoise
    apply_deskew=True,       # 倾斜矫正 / Deskew
    apply_binarize=False,    # 二值化 / Binarize
    enhance_contrast=True,   # 对比度增强 / Enhance contrast
    max_size=2048            # 最大尺寸 / Maximum size
)
```

#### convert_to_grayscale()

转换为灰度图。

Convert to grayscale.

```python
gray_image = ImageProcessor.convert_to_grayscale(image)
```

#### denoise()

图像去噪。

Denoise image.

```python
denoised_image = ImageProcessor.denoise(image, strength=10)
```

#### deskew()

倾斜矫正。

Deskew image.

```python
deskewed_image = ImageProcessor.deskew(image)
```

#### binarize()

二值化处理。

Binarize image.

```python
binary_image = ImageProcessor.binarize(
    image,
    method='adaptive',  # 'adaptive', 'otsu', 或 'simple'
    threshold=127
)
```

#### enhance_contrast()

增强对比度。

Enhance contrast.

```python
enhanced_image = ImageProcessor.enhance_contrast(image, alpha=1.5)
```

#### resize_image()

调整图像大小。

Resize image.

```python
resized_image = ImageProcessor.resize_image(
    image,
    max_width=2048,
    max_height=2048,
    scale=None  # 或使用缩放比例 / Or use scale factor
)
```

#### save_image()

保存图像。

Save image.

```python
ImageProcessor.save_image(image, 'output_path.jpg')
```

---

## PDFProcessor

PDF文档处理类。

PDF document processing class.

### 初始化 / Initialization

```python
from src.pdf_processor import PDFProcessor

pdf_processor = PDFProcessor(dpi=300)  # 设置DPI / Set DPI
```

### 方法 / Methods

#### pdf_to_images()

将PDF转换为图片。

Convert PDF to images.

```python
image_paths = pdf_processor.pdf_to_images(
    pdf_path='document.pdf',
    output_folder='./output',  # 可选 / Optional
    first_page=1,              # 起始页 / First page
    last_page=None             # 结束页 / Last page
)
# 返回图片路径列表 / Returns list of image paths
```

#### process_pdf_with_ocr()

处理PDF并进行OCR识别。

Process PDF with OCR recognition.

```python
results = pdf_processor.process_pdf_with_ocr(
    pdf_path='document.pdf',
    ocr_engine=ocr,            # OCREngine实例
    confidence_threshold=0.5,
    output_folder='./output'
)

# 返回包含所有页面结果的字典
# Returns dictionary with all page results
```

#### get_full_pdf_text()

获取PDF的完整文本。

Get full text from PDF results.

```python
full_text = pdf_processor.get_full_pdf_text(pdf_results)
```

---

## TextProcessor

文本后处理工具类。

Text post-processing utility class.

### 方法 / Methods

#### clean_text()

清理文本。

Clean text.

```python
from src.text_processor import TextProcessor

cleaned_text = TextProcessor.clean_text(text)
```

#### remove_duplicates()

去除重复行。

Remove duplicate lines.

```python
unique_text = TextProcessor.remove_duplicates(text)
```

#### sort_by_position()

按位置排序文本块。

Sort text blocks by position.

```python
sorted_data = TextProcessor.sort_by_position(
    extracted_data,
    sort_direction='vertical'  # 'vertical' 或 'horizontal'
)
```

#### group_by_lines()

将文本块按行分组。

Group text blocks by lines.

```python
lines = TextProcessor.group_by_lines(
    extracted_data,
    threshold=10  # Y坐标差异阈值 / Y-coordinate difference threshold
)
```

#### filter_by_confidence()

按置信度过滤。

Filter by confidence.

```python
filtered_data = TextProcessor.filter_by_confidence(
    extracted_data,
    min_confidence=0.7
)
```

#### get_statistics()

获取统计信息。

Get statistics.

```python
stats = TextProcessor.get_statistics(extracted_data)
# 返回: total_items, average_confidence, min_confidence, 
#      max_confidence, total_characters
```

---

## Utils

工具函数模块。

Utility functions module.

### OutputFormatter

输出格式化工具。

Output formatting utilities.

```python
from src.utils import OutputFormatter

# 保存为文本 / Save as text
OutputFormatter.save_as_txt(text, 'output.txt')

# 保存为JSON / Save as JSON
OutputFormatter.save_as_json(data, 'output.json')

# 保存为Markdown / Save as Markdown
OutputFormatter.save_as_markdown(
    text,
    'output.md',
    title='OCR Result',
    metadata={'key': 'value'}
)

# 创建输出文件名 / Create output filename
output_path = OutputFormatter.create_output_filename(
    input_path='input.jpg',
    output_dir='./output',
    suffix='_ocr',
    extension='txt'
)
```

### FileScanner

文件扫描工具。

File scanning utilities.

```python
from src.utils import FileScanner

# 获取图片文件 / Get image files
image_files = FileScanner.get_image_files(
    directory='./images',
    extensions=['.jpg', '.png']  # 可选 / Optional
)

# 获取PDF文件 / Get PDF files
pdf_files = FileScanner.get_pdf_files(directory='./pdfs')

# 验证文件 / Validate file
is_valid = FileScanner.validate_file(file_path)
```

### setup_logging()

设置日志。

Setup logging.

```python
from src.utils import setup_logging

setup_logging(
    log_file='ocr.log',  # 可选 / Optional
    level=logging.INFO
)
```

---

## 完整示例 / Complete Example

```python
from src.ocr_engine import OCREngine
from src.image_processor import ImageProcessor
from src.text_processor import TextProcessor
from src.utils import OutputFormatter, setup_logging

# 设置日志
setup_logging()

# 初始化OCR引擎
ocr = OCREngine(lang='ch', use_gpu=False)

# 预处理图像
processed_image = ImageProcessor.preprocess_for_ocr(
    'input.jpg',
    apply_denoise=True,
    apply_deskew=True
)

# 保存预处理结果
ImageProcessor.save_image(processed_image, 'processed.jpg')

# 识别文本
full_text, extracted_data = ocr.recognize_and_extract('processed.jpg')

# 过滤低置信度结果
filtered_data = TextProcessor.filter_by_confidence(
    extracted_data,
    min_confidence=0.7
)

# 获取统计信息
stats = TextProcessor.get_statistics(filtered_data)
print(f"识别了 {stats['total_items']} 个文本块")
print(f"平均置信度: {stats['average_confidence']:.2%}")

# 保存结果
OutputFormatter.save_as_txt(full_text, 'output.txt')
OutputFormatter.save_as_json(
    {
        'text': full_text,
        'details': filtered_data,
        'statistics': stats
    },
    'output.json'
)
```

---

## 错误处理 / Error Handling

所有方法在遇到错误时会抛出相应的异常。建议使用try-except进行错误处理：

All methods throw appropriate exceptions on errors. Use try-except for error handling:

```python
try:
    result = ocr.recognize_and_extract('image.jpg')
except FileNotFoundError as e:
    print(f"文件未找到: {e}")
except Exception as e:
    print(f"处理出错: {e}")
```

---

## 性能提示 / Performance Tips

1. **批量处理**: 使用 `batch_recognize()` 而不是循环调用 `recognize_image()`
2. **GPU加速**: 设置 `use_gpu=True` 可以显著提高速度
3. **置信度过滤**: 适当提高 `confidence_threshold` 可以减少后处理工作量
4. **图像预处理**: 仅在必要时使用，会增加处理时间

---

更多信息请参考源代码和示例。

For more information, refer to the source code and examples.

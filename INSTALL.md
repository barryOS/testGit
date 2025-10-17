# 安装指南 / Installation Guide

## 环境要求 / System Requirements

- Python 3.7 或更高版本 / Python 3.7 or higher
- pip (Python包管理器) / pip (Python package manager)
- (可选) CUDA 10.2+ 用于GPU加速 / (Optional) CUDA 10.2+ for GPU acceleration

## 安装步骤 / Installation Steps

### 1. 克隆项目 / Clone Repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. 创建虚拟环境（推荐）/ Create Virtual Environment (Recommended)

#### Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. 安装依赖 / Install Dependencies

#### CPU版本 / CPU Version:

```bash
pip install -r requirements.txt
```

#### GPU版本 / GPU Version (需要CUDA支持 / Requires CUDA):

```bash
# 首先安装GPU版本的PaddlePaddle
python -m pip install paddlepaddle-gpu -i https://mirror.baidu.com/pypi/simple

# 然后安装其他依赖
pip install paddleocr opencv-python Pillow pdf2image numpy tqdm
```

### 4. 验证安装 / Verify Installation

```bash
python -c "from paddleocr import PaddleOCR; print('安装成功 / Installation successful!')"
```

## 额外依赖 / Additional Dependencies

### PDF处理支持 / PDF Processing Support

pdf2image需要poppler-utils支持：

pdf2image requires poppler-utils:

#### Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install poppler-utils
```

#### Mac:

```bash
brew install poppler
```

#### Windows:

1. 从 https://github.com/oschwartz10612/poppler-windows/releases/ 下载poppler
2. 解压并添加bin目录到系统PATH

### OpenCV依赖 / OpenCV Dependencies

如果OpenCV安装失败，尝试：

If OpenCV installation fails, try:

```bash
pip install opencv-python-headless
```

## 常见问题 / Troubleshooting

### 问题1: PaddlePaddle安装失败 / Issue 1: PaddlePaddle Installation Failed

尝试使用国内镜像：

Try using domestic mirror:

```bash
pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
```

### 问题2: 权限错误 / Issue 2: Permission Error

使用--user参数：

Use --user flag:

```bash
pip install --user -r requirements.txt
```

### 问题3: 模型下载慢 / Issue 3: Slow Model Download

首次运行时PaddleOCR会下载模型文件，可能需要较长时间。建议使用稳定的网络连接。

PaddleOCR downloads model files on first run, which may take time. Use a stable network connection.

## 快速测试 / Quick Test

安装完成后，运行示例代码测试：

After installation, run example code to test:

```bash
python examples/quick_start.py
```

或运行单元测试：

Or run unit tests:

```bash
python -m pytest tests/
# 或 / or
python tests/test_ocr_engine.py
```

## 性能优化 / Performance Optimization

### 使用GPU加速 / Use GPU Acceleration

如果有NVIDIA GPU：

If you have an NVIDIA GPU:

1. 安装CUDA Toolkit (10.2+)
2. 安装cuDNN
3. 安装GPU版本的PaddlePaddle
4. 运行时使用`--gpu`参数

### 模型缓存 / Model Caching

PaddleOCR会将下载的模型缓存在：

PaddleOCR caches downloaded models in:

- Linux/Mac: `~/.paddleocr/`
- Windows: `C:\Users\<username>\.paddleocr\`

可以手动清理旧模型释放空间。

You can manually clean old models to free up space.

## 下一步 / Next Steps

安装完成后，请查看：

After installation, check out:

1. [README.md](README.md) - 详细使用文档 / Detailed usage documentation
2. [examples/quick_start.py](examples/quick_start.py) - 示例代码 / Example code
3. 运行 `python main.py --help` 查看所有命令行选项 / Run for all CLI options

## 获取帮助 / Getting Help

如果遇到问题，请：

If you encounter issues:

1. 查看 [PaddleOCR官方文档](https://github.com/PaddlePaddle/PaddleOCR)
2. 提交Issue到项目仓库 / Submit an issue to the repository
3. 检查Python和依赖版本是否符合要求 / Check Python and dependency versions

---

祝使用愉快！/ Happy OCR-ing! 🎉

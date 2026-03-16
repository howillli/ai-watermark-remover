# AI 水印去除工具

🎨 专业的AI图像水印去除工具，使用先进的图像修复技术。

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](README.md) | 简体中文

## ✨ 功能特性

- 🎯 **自动检测**：自动检测常见水印位置（角落、中心）
- ✏️ **手动选择**：通过坐标精确指定水印区域
- 🔧 **多种方法**：修复算法、内容感知填充、基于补丁的去除
- 📦 **批量处理**：一次处理多张图片
- 🎨 **质量保持**：保持原始图像质量
- 📁 **格式支持**：JPG、PNG、WebP、TIFF

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/howillli/ai-watermark-remover.git
cd ai-watermark-remover

# 安装依赖
pip install opencv-python opencv-contrib-python numpy pillow

# 或使用安装脚本
bash install.sh
```

### 基本用法

#### 去除角落水印

```bash
python scripts/remove_watermark.py input.jpg --position topleft
```

#### 去除自定义区域水印

```bash
python scripts/remove_watermark.py input.jpg --area 1500,50,400,100
```

#### 批量去除水印

```bash
python scripts/batch_remove_watermarks.py /path/to/images --position bottomright
```

## 📸 示例展示

### 示例 1：去除"AI生成"水印

**处理前：**

![示例 1 - 带水印](examples/example1_with_watermark.jpg)

**处理后：**

![示例 1 - 已清理](examples/example1_clean.jpg)

**命令：**
```bash
python scripts/remove_watermark.py example1.jpg --position topleft --size medium --method telea --radius 15 --padding 30
```

---

### 示例 2：去除多个水印

**处理前：**

![示例 2 - 带水印](examples/example2_with_watermark.jpg)

**处理后：**

![示例 2 - 已清理](examples/example2_clean.jpg)

**命令：**
```bash
# 步骤 1：去除左上角水印
python scripts/remove_watermark.py example2.jpg --position topleft --method telea --radius 15 --padding 30 --output example2_step1.jpg

# 步骤 2：去除右下角水印
python scripts/remove_watermark.py example2_step1.jpg --position bottomright --method telea --radius 15 --padding 30 --output example2_clean.jpg
```

## 📖 使用指南

### 基于位置的去除

从常见位置去除水印：

```bash
# 右下角（最常见）
python scripts/remove_watermark.py image.jpg --position bottomright

# 左上角
python scripts/remove_watermark.py image.jpg --position topleft

# 中心
python scripts/remove_watermark.py image.jpg --position center
```

**可用位置：**
- `topleft`（左上）、`top`（上）、`topright`（右上）
- `left`（左）、`center`（中心）、`right`（右）
- `bottomleft`（左下）、`bottom`（下）、`bottomright`（右下）

### 基于区域的去除

指定精确坐标（x, y, 宽度, 高度）：

```bash
python scripts/remove_watermark.py image.jpg --area 1500,50,400,100
```

### 交互式选择

可视化选择水印区域：

```bash
python scripts/remove_watermark_interactive.py image.jpg
```

**操作说明：**
- 点击并拖动选择区域
- 按 ENTER 确认
- 按 ESC 取消
- 按 R 重置选择

## 🛠️ 去除方法

### 方法 1：Inpainting（默认）

适用于：文字水印、简单覆盖层

```bash
python scripts/remove_watermark.py image.jpg --position bottomright --method inpaint
```

**优点：** 快速，适合文字  
**缺点：** 可能模糊复杂图案

### 方法 2：Telea（内容感知）

适用于：复杂背景、摄影图像

```bash
python scripts/remove_watermark.py image.jpg --position bottomright --method telea
```

**优点：** 更适合复杂背景  
**缺点：** 处理较慢

### 方法 3：基于补丁

适用于：大型水印、重复图案

```bash
python scripts/remove_watermark.py image.jpg --position bottomright --method patch
```

**优点：** 大面积处理质量最佳  
**缺点：** 处理最慢

## ⚙️ 高级选项

### 调整修复半径

```bash
# 更大的半径适用于更大的水印
python scripts/remove_watermark.py image.jpg --position bottomright --radius 10
```

### 保持图像质量

```bash
# 使用无损输出
python scripts/remove_watermark.py image.jpg --position bottomright --quality 100
```

### 自定义输出位置

```bash
python scripts/remove_watermark.py image.jpg --position bottomright --output clean_image.jpg
```

### 水印大小

```bash
# 对于基于位置的去除，指定水印大小
python scripts/remove_watermark.py image.jpg --position bottomright --size large
```

**可用大小：**
- `small` - 200x60像素
- `medium` - 400x100像素（默认）
- `large` - 600x150像素

## 📊 性能表现

**处理速度**（大约）：
- 小型水印（100x50px）：0.5-1秒
- 中型水印（400x100px）：1-2秒
- 大型水印（800x200px）：3-5秒

**批量处理：**
- 100张图片：约2-5分钟（取决于水印大小）

## 💡 最佳实践建议

1. **使用高分辨率图像**：更好的输入质量 = 更好的输出质量
2. **精确选择**：只选择水印区域，不要包含额外空间
3. **选择正确的方法**：
   - 文字水印 → `inpaint`
   - 照片背景 → `telea`
   - 大面积 → `patch`
4. **调整半径**：对于更大的水印增加半径
5. **检查预览**：批量处理前始终预览

## 🔧 故障排除

### 水印未完全去除

**解决方案：** 增加 `--radius` 或 `--padding`

```bash
python scripts/remove_watermark.py image.jpg --position bottomright --radius 20 --padding 40
```

### 结果模糊

**解决方案：** 使用 `--method telea` 或 `--method patch`

```bash
python scripts/remove_watermark.py image.jpg --position bottomright --method telea
```

### 颜色不匹配

**解决方案：** 增加选择区域以包含更多上下文

```bash
python scripts/remove_watermark.py image.jpg --position bottomright --size large
```

## 📁 项目结构

```
ai-watermark-remover/
├── scripts/
│   ├── remove_watermark.py          # 主要水印去除脚本
│   ├── batch_remove_watermarks.py   # 批量处理脚本
│   ├── remove_watermark_interactive.py  # 交互式选择工具
│   └── create_test_image.py         # 创建带水印的测试图像
├── references/
│   └── ADVANCED_TECHNIQUES.md       # 高级技术文档
├── examples/
│   ├── example1_with_watermark.jpg  # 带水印的示例
│   ├── example1_clean.jpg           # 去除后的示例
│   ├── example2_with_watermark.jpg  # 带多个水印的示例
│   └── example2_clean.jpg           # 去除后的示例
├── install.sh                       # 安装脚本
└── README.md                        # 英文说明文档
```

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建您的特性分支（`git checkout -b feature/AmazingFeature`）
3. 提交您的更改（`git commit -m 'Add some AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 打开一个 Pull Request

## ⚖️ 法律声明

此工具仅用于去除您自己的AI生成图像或您有权修改的图像上的水印。请始终尊重版权和使用权。

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 使用 [OpenCV](https://opencv.org/) 构建
- 修复算法基于 Telea 和 Navier-Stokes 方法
- 灵感来源于对干净AI生成图像的需求

## 📧 联系方式

如有问题或需要支持，请在 GitHub 上提交 issue。

---

**用 ❤️ 为 AI 社区打造**

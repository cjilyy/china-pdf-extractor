# china-pdf-extractor

一个面向中文 PDF 的轻量工具集，聚焦于常见文档（征信报告、财务报表、发票等）的解析与预处理，包括去水印、图像增强、表格/OCR 解析等实用功能。

**核心目标**
- 提供可复用的小工具，快速完成 PDF 预处理与解析
- 保持简单直观的使用方式，便于脚本化与集成

**功能清单**
[x] PDF 去水印
- [ ] OCR/表格解析（规划中）
- [ ] 图像增强与版面分析（规划中）

**快速开始**
- 环境要求：推荐 `Python 3.10+`
- 克隆代码后，可将你的去水印测试代码粘贴到 `scripts/remove_watermark.py`
- 测试文档请放到 `test_files/` 目录，仓库已忽略该目录中文件，不会上传至 GitHub

**目录结构**
- `scripts/`：示例与工具脚本（如 `remove_watermark.py`）
- `test_files/`：本地测试用 PDF/图片文件（已被 Git 忽略）
- `README.md`：项目说明
- `LICENSE`：许可证（MIT）

**使用示例（去水印）**
- 将你的去水印代码粘贴到 `scripts/remove_watermark.py`
- 参考执行（参数仅示例，按你的代码实际修改）：
  - `python scripts/remove_watermark.py --input test_files/input.pdf --output test_files/output.pdf`

**注意事项**
- 请勿将任何真实或敏感数据提交到仓库
- 若处理扫描版 PDF，建议保证较高分辨率与清晰度以提升解析效果

**许可证**
- 本项目采用 MIT License，详情见 `LICENSE`

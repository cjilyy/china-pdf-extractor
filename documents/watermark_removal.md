# PDF 去水印原理说明

本项目当前的去水印实现采用图像级处理思路：将 PDF 页面渲染为位图图像，对浅色（通常为灰色/淡色）的水印进行阈值分割与覆盖，从而得到干净页面，再将处理后的页面重新合成为新的 PDF。

**处理流程**
- 页面渲染：使用 `pdfplumber` 将每一页渲染为图像（位图）
- 灰度化：使用 `OpenCV` 将彩色图像转换为灰度图，以便阈值处理（`scripts/remove_watermark.py:9`）
- 阈值分割：对灰度图执行固定阈值二值化，将较亮区域（可能是浅色水印）分离（`scripts/remove_watermark.py:10`）
- 掩膜反转：反转掩膜以获得需要覆盖的区域（`scripts/remove_watermark.py:11`）
- 覆盖去水印：将掩膜标记的像素置为白色，达到“去水印”的视觉效果（`scripts/remove_watermark.py:12`）
- 合成 PDF：将处理后的各页图像通过 `Pillow` 重新保存为 PDF（`scripts/remove_watermark.py:25–26`）

**关键参数**
- `resolution`：页面渲染分辨率，数值越高，细节越清晰，处理更精确，但文件体积与处理耗时也更大（`scripts/remove_watermark.py:32`）
- `threshold`：灰度阈值，控制“浅色区域”的判定范围；值越低，保留更多原文字；值越高，更激进地覆盖偏亮内容（`scripts/remove_watermark.py:33`）

**适用场景与局限**
- 适用：水印为浅色、半透明文本或图形，且页面背景/正文对比明显
- 局限：
  - 若水印为深色/与正文颜色相近，固定阈值可能无法有效分离
  - 矢量水印（PDF 矢量层）在位图渲染后仍作为像素，无法“结构化删除”；需更复杂的 PDF 对象级处理
  - 对扫描件，背景噪声或阴影可能与水印亮度接近，需更稳健的分割方法

**可能的优化方向**
- 自适应阈值/局部阈值：在不同区域使用不同阈值以适应复杂背景
- 颜色空间分割：在 HSV/LAB 空间中基于色相/明度分离水印
- 形态学操作：结合开闭运算精细化去水印区域边界
- 图像修复（inpainting）：以掩膜为引导进行纹理填充，减少覆盖造成的“白块”痕迹
- PDF 结构级处理：解析 PDF 内容流，定位水印层（如透明度/叠加模式）并移除相应对象

**与脚本的对应关系**
- 去水印函数：`remove_watermark`（`scripts/remove_watermark.py:8–13`）
- 页面处理与合成：`generate_clean_pdf`（`scripts/remove_watermark.py:15–26`）
- CLI 参数与默认路径：`main`（`scripts/remove_watermark.py:28–45`）
  - 默认输入：`test_files/report.pdf`
  - 默认输出：`test_files/clean.pdf`
  - 可选参数：`--resolution`、`--threshold`

**使用建议**
- 从较低阈值开始（如 180–200），按效果逐步调整
- 对扫描件建议提高 `resolution`（如 300）以获得更好的分割与合成质量
- 如遇正文被误覆盖，降低 `threshold` 或改用颜色空间/自适应方法
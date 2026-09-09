# CPC Emblem Construction

使用 [Manim Community](https://www.manim.community/) 实现的**中国共产党党徽几何制法演示**。

本项目是一个单文件 Python / Manim 程序，根据《中国共产党党徽党旗条例》附件所载党徽制法说明，将党徽的几何构造过程转换为可执行、可动画化的 Manim 场景。

项目同时提供：

* 完整的党徽几何构造动画
* 32 × 32 标准方格辅助构造
* 构造点、辅助线、圆与圆弧的逐步展示
* 锤头、锤把、镰刀刀体与镰刀把的分步绘制
* 最终辅助线淡出与完整党徽呈现
* 独立的静态党徽渲染 Scene
* 9:16 竖屏视频输出配置
* 1080 × 1920、60 FPS 输出
* 标准黄色与红色色值定义

> 本项目是独立的技术与教育用途实现，不是中国共产党的官方发布物，也不代表任何官方机构。

---

## Preview

程序将标准制图过程拆分为多个动画步骤，从 32 × 32 方格、对角线和基准点开始，逐步完成锤头、锤把、镰刀刀体及镰刀把的构造，最后移除辅助几何并显示完整党徽。

动画大致按照以下过程展开：

1. 建立 32 × 32 方格并绘制 AC、BD 对角线
2. 取 E、F 等构造点并确定锤把
3. 构造锤头直边
4. 使用圆弧完成锤头曲线
5. 闭合并填充锤头和锤把
6. 构造镰刀外圆弧
7. 构造镰刀下部外圆弧
8. 构造镰刀内侧圆弧
9. 构造内侧四分之一圆弧
10. 完成内弧连接
11. 闭合并填充镰刀刀体
12. 构造镰刀把及端部圆形
13. 淡出全部辅助线，显示最终党徽

每一步均配有简短的中文说明字幕。

---

## Features

### Geometry-based construction

项目没有直接导入现成的 SVG 或位图党徽。

党徽轮廓由程序中的：

* 标准构造点
* 直线
* 圆
* 圆弧
* 多边形
* 几何交点
* 坐标变换

动态生成。

构造坐标使用独立的标准方格坐标系，并通过：

```python
sp((x, y))
```

转换为 Manim 场景坐标。

这样可以将几何定义与实际视频分辨率、Manim 场景坐标系统分离。

### Sampled circular arcs

圆弧并非简单依赖预先绘制的矢量路径，而是根据：

* 圆心
* 起点
* 终点
* 半径
* 角度方向

进行采样，再转换为 Manim `VMobject`。

核心逻辑包括：

```python
angle_screen(...)
arc_points(...)
sampled_arc(...)
```

这也使构造过程可以直接作为动画中的辅助圆弧显示。

### Separate construction and final render

文件包含两个 Scene：

```python
CPCEmblemConstruction
```

用于完整的几何构造动画。

以及：

```python
CPCEmblemStill
```

用于只渲染最终完成的党徽图形。

---

## Requirements

推荐环境：

* Python 3.11+
* Manim Community
* NumPy
* FFmpeg
* 可用的 LaTeX / Manim 相关依赖（取决于本地 Manim 安装方式）

安装 Python 依赖：

```bash
pip install manim numpy
```

具体的 Manim 系统依赖安装方式请参考 Manim Community 官方文档。

---

## Font

默认字体：

```python
CJK_FONT = "PingFang SC"
```

该字体通常可以直接在 macOS 上使用。

如果系统没有 PingFang SC，可以将：

```python
CJK_FONT = "PingFang SC"
```

替换为其他支持中文的字体，例如系统已有的 CJK 字体。

---

## Rendering

假设源码保存为：

```text
cpc_emblem.py
```

### Render the full construction animation

```bash
manim -pqh cpc_emblem.py CPCEmblemConstruction
```

或者使用 Manim 的其他质量选项：

```bash
manim -pql cpc_emblem.py CPCEmblemConstruction
manim -pqm cpc_emblem.py CPCEmblemConstruction
manim -pqh cpc_emblem.py CPCEmblemConstruction
```

源码本身已经配置：

```text
1080 × 1920
60 FPS
9:16
```

因此最终输出面向竖屏展示。

### Render the final emblem only

```bash
manim -pqh cpc_emblem.py CPCEmblemStill
```

如果只需要导出静态 PNG：

```bash
manim -s -qh cpc_emblem.py CPCEmblemStill
```

---

## Colors

源码中定义：

```python
OFFICIAL_YELLOW = ManimColor("#FDCF30")
OFFICIAL_RED = ManimColor("#ED2C25")
```

对应：

```text
Yellow: RGB 253, 207, 48
Red:    RGB 237, 44, 37
```

当前最终党徽使用黄色进行填充。

其他颜色主要用于：

* 网格
* 辅助线
* 构造点
* 构造轮廓
* 字幕
* 动画强调

这些辅助颜色属于本项目的动画视觉设计，不属于党徽本身的标准颜色定义。

---

## Project Structure

本项目有意保持为单文件实现：

```text
.
├── LICENSE
├── NOTICE
├── README.md
└── cpc_emblem.py
```

核心代码无需拆分为多个模块即可阅读、修改和运行。

这种结构也便于：

* 学习几何构造
* 阅读 Manim 动画实现
* 单文件分发
* 快速渲染
* 对照党徽制法研究几何关系

---

## License

本项目的**软件源代码**采用 [MIT License](LICENSE) 授权。

```text
MIT License
Copyright (c) 2026 Eltavine
```

MIT License 适用于本仓库中由项目作者编写的软件实现，包括但不限于：

* Python / Manim 源代码
* 坐标转换逻辑
* 几何构造算法
* 圆弧采样逻辑
* 动画编排
* Scene 实现
* 辅助函数及相关软件结构

你可以在 MIT License 条款允许的范围内使用、复制、修改、合并、发布、分发、再授权或销售本软件的副本。

完整条款请参阅：

```text
LICENSE
```

---

## Important Notice

**MIT License 对本项目软件源代码的授权，不应被理解为对中国共产党党徽、党旗、其标准图案、官方制法规范或相关标志使用权的授权。**

本项目根据公开的党徽制法说明实现几何构造算法，但：

* 软件许可证仅覆盖本项目的软件实现；
* 本项目不授予任何超出作者自身权利范围的权利；
* 本项目不能改变、替代或豁免适用于党徽、党旗及其图案的法律、法规和官方使用规范；
* 使用者应自行确保党徽图形的生成、使用、展示、发布、传播和再利用符合适用的法律法规及相关规定。

特别是，将本项目生成的党徽图形用于：

* 商业用途
* 商标或品牌标识
* 产品包装
* 广告
* 宣传材料
* 网站或应用程序视觉设计
* 二次创作
* 公开传播

时，不应仅依据本仓库的 MIT License 判断其是否可以使用。

有关软件授权与党徽相关内容之间的权利边界，请同时参阅：

```text
NOTICE
```

---

## Source Reference

本项目的几何构造参考：

**《中国共产党党徽党旗条例》及其附件中的党徽制法说明。**

代码中的相关坐标、构造关系和颜色定义用于将该制法转换为可执行的几何动画。

本仓库不替代官方规范。

如本项目的实现、注释、动画说明与现行正式规范存在差异，应以正式发布的规范文本为准。

---

## Disclaimer

This project is an independent software implementation created for technical,
educational, visualization, and geometric-construction purposes.

It is not an official publication of, affiliated with, sponsored by, or
endorsed by the Communist Party of China or any governmental or Party
organization.

The MIT License applies to the software implementation in this repository
only. It does not grant rights concerning the Party emblem, Party flag,
official designs, official specifications, or any regulated use of those
symbols.

Users are responsible for ensuring that their use of generated materials
complies with applicable laws, regulations, and official requirements.

---

## Author

**Eltavine**

GitHub: `@eltavine`

---

## Contributing

Issues and pull requests concerning the software implementation are welcome,
including:

* geometry corrections
* Manim rendering improvements
* animation improvements
* compatibility fixes
* code cleanup
* documentation improvements

Changes to the geometric construction should preferably include a clear
technical basis or reference so that the implementation remains reproducible
and auditable.

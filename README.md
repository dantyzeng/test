# Eight-habitat MAG defense-system analysis

八生境宏基因组组装基因组（MAG）防御系统项目的 GitHub 交付框架。项目覆盖原始宏基因组 reads、MAG 质量控制、GTDB-Tk 分类、DefenseFinder 注释、样本级 RPKM、群落/防御系统比较、移动遗传元件（MGE）分析、Ceres 专题分析和最终图表。

本仓库是轻量级可复现框架，不包含 FASTQ、BAM、MAG FASTA、数据库和大体积中间文件。原始数据和完整计算结果仍保存在本地项目目录；GitHub 中应通过 `metadata/` 中的 manifest 和 accession 找回数据。

## 结果概览

- 8 个生境、25,502 个质量合格 MAG。
- 80 个宏基因组样本（每个生境 10 个样本）的样本级定量比较已形成。
- 统一 DefenseFinder 结果包含 287 类防御系统；重点比较 Ceres、DRT、Cas、RM、AbiE、SoFIC、MazEF、CBASS 和 Retron。
- Ceres 的 MAG 检出比例在冻土最高（654/2,481，26.36%），但这不是细胞丰度或表达量。
- Ceres 核心蛋白分为 CrsA1（6,857 条）和 CrsA2（20 条）；最近邻同宿主门比例为 81.24%，置换检验 `p = 0.0005`。
- 10 kb 防御岛阈值下，Ceres 系统位于防御岛的比例为 1.03%，低于 Cas（4.11%）和 RM（16.62%）。

完整的结果解释、限制和证据文件见 [results/summary.md](results/summary.md)。

## 目录

```text
.
├── README.md
├── LICENSE
├── CITATION.cff
├── environment.yml                 # Conda 环境（Python + R + 常用命令行工具）
├── requirements.txt                 # Python pip 依赖
├── config/config.yaml               # 相对路径、阈值和版本配置
├── docs/
│   ├── workflow.md                  # 从原始数据到最终输出的流程
│   ├── file_formats.md              # 输入/输出文件格式和字段约定
│   ├── dependencies.md              # 软件、数据库和硬件要求
│   └── reproducibility.md           # 复现、审计和数据共享规范
├── metadata/                        # 轻量级样本、MAG 和 accession 清单
├── results/
│   ├── summary.md                   # 当前阶段的结果总结和限制
│   ├── tables/                      # 可提交/可审计的摘要表
│   └── figures/                     # 选定图表的占位目录
└── scripts/
    ├── build_project_summary.py     # 从原始项目目录重建摘要表
    └── run_summary.sh               # 一键运行摘要重建
```

## 快速开始

```bash
git clone <your-repository-url>
cd habitat-MAG-defense
conda env create -f environment.yml
conda activate habitat-mag-defense

# 指向本地完整项目目录
export HABITAT_MAGS_ROOT=/path/to/habitat_MAGs
bash scripts/run_summary.sh
```

完整分析需要原始项目目录中的 MAG、reads、质量评估和 DefenseFinder 结果；本框架只负责组织、记录和重建轻量级摘要。运行大型分析前，请先阅读 [docs/reproducibility.md](docs/reproducibility.md)。

## 关键分析边界

1. MAG 检出率的分母是质量合格 MAG 数，不是样本数、细胞丰度或表达量。
2. RPKM、样本级 prevalence 和稀释曲线需要样本级 mapped-read 计数、特征长度及样本 metadata，不能由 MAG presence/absence 表替代。
3. 生境与 MAG 来源 catalog 部分混杂；生境效应应结合 taxonomy、study/source 和 dispersion 结果解释。
4. 防御岛比例来自 contig 内邻近关系，是 MAG 碎片化条件下的下界，不代表完整染色体上的真实共定位率。
5. Ceres/DRT 的计算结果用于提出可检验候选机制，不等同于表达、抗噬菌体功能或湿实验验证。

## 数据和代码许可

代码和文档按 MIT License 发布。公共数据库、论文补充数据和原始测序数据遵循各自来源的许可与引用要求；请在发布前补充 accession、原始研究 DOI 和数据许可信息。

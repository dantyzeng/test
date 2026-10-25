# 软件和环境要求

## 推荐环境

- Linux x86_64（当前项目在 Ubuntu 20.04/5.15 内核上运行）。
- 16--32 个 CPU 线程用于常规汇总；GTDB-Tk、DefenseFinder、mapping 和 MGE 分析建议 32--256 线程。
- 内存：摘要和绘图至少 16 GB；全量 MAG/DefenseFinder 推荐 64--256 GB。
- 磁盘：原始 reads、MAG、数据库、BAM 和中间文件通常需要数 TB；GitHub 仓库只提交轻量级结果。
- Python 3.10+，R 4.3+，UTF-8 locale。

## 直接依赖

Python 包和 R 包的最低版本见根目录 `requirements.txt` 与 `environment.yml`。主要 Python 包为 numpy、pandas、scipy、scikit-learn、matplotlib、seaborn、openpyxl 和 PyYAML；主要 R 包为 vegan、randomForest、data.table、ggplot2 和 readxl。

## 生物信息软件

| 软件 | 用途 | 项目记录/建议版本 |
|---|---|---|
| FastQC / fastp | reads 质控和过滤 | 0.12 / 0.23+ |
| Bowtie2 / samtools | mapping、BAM、idxstats | 2.5+ / 1.17+ |
| CheckM2 | MAG 完整度/污染度 | 记录数据库版本和模型路径 |
| GTDB-Tk | 分类和系统发育 | 2.4.0，数据库 r220 |
| Prodigal | 基因/蛋白预测 | 2.6+ |
| DefenseFinder | 防御系统注释 | 2.0.1 |
| defense-finder-models | DefenseFinder 模型 | 3.0.0 |
| dRep | 来源 catalog 去冗余 | 必须记录每个 catalog 的参数 |
| CoverM / samtools | abundance/RPKM 汇总 | 按脚本实际版本记录 |
| geNomad / ISEScan / IntegronFinder | MGE 注释 | 记录数据库版本 |
| MAFFT / IQ-TREE / HMMER | 比对、树和 profile | 7.5+ / 2.2+ / 3.3+ |

## 数据库和外部资源

GTDB-Tk 数据库、DefenseFinder models、HMM 数据库和 geNomad 数据库不应提交到 GitHub。发布时提供数据库名称、版本、下载日期、校验和以及安装命令；公共 reads 和补充数据提供 accession/DOI。

## 安装

```bash
conda env create -f environment.yml
conda activate habitat-mag-defense
python -m pip install -r requirements.txt
```

如果所在集群的 Conda channel 没有上述重型工具，可以先建立基础环境，再按项目管理员提供的安装方式安装 GTDB-Tk、CheckM2、DefenseFinder、dRep 和 CoverM；这些工具的数据库不包含在仓库中。建议将最终环境导出为 lockfile，并在 `docs/reproducibility.md` 中记录 `conda list --explicit`、`pip freeze`、`sessionInfo()` 和命令行工具版本。

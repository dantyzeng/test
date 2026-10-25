# 分析流程

## 1. 原始数据和元数据

输入是公共数据库下载的单端或双端宏基因组 reads（`FASTQ/FASTQ.GZ`）、研究来源 metadata、MAG FASTA 和各研究的 accession。每个样本必须在 manifest 中有唯一 `sample`、`habitat`、`study`、`run_accession` 以及 `R1/R2` 路径。公共数据下载记录保存在原始项目的 `quality_analysis/00_meta/public_sources/`。

## 2. Reads 质控和深度标准化

建议顺序：FastQC/fastp 质控 -> 去接头和低质量 reads -> 记录输入/输出碱基数 -> 使用 samtools 对 BAM 做确定性 real-fraction 稀释。当前项目使用 5--10 Gb 目标深度策略；实际参数和样本状态见 `quality_analysis/00_meta/prepare_reads.tsv`。稀释曲线是 reference-catalog recovery，不是从头组装的物种发现曲线。

## 3. MAG 整理和质量控制

为每个生境建立 MAG manifest，保留 `habitat`、`mag_id`、`fasta_path`、`completeness`、`contamination`、`quality_pass` 和 CheckM2 报告路径。原项目同时包含不同研究来源的 MAG catalog，因此应记录 catalog、dRep 参数和去冗余版本。质量筛选阈值必须在配置中显式记录，不能从文件名推断。

## 4. 分类学注释

使用 GTDB-Tk（当前记录为 2.4.0，数据库 r220）对质量合格 MAG 进行 `identify`、`classify_wf`，输出 `*.summary.tsv` 和分类树。统一输出字段为 domain/phylum/class/order/family/genus/species/classification。缺失分类以 `Unclassified` 表示，不要静默删除。

## 5. 基因预测和防御系统注释

对 MAG 进行蛋白预测后运行 DefenseFinder。当前跨生境比较使用 DefenseFinder 2.0.1 和 defense-finder-models 3.0.0。记录系统表、基因表、HMM 命中表和版本日志。`uniform_eight_system_presence_absence.tsv` 是 MAG-level presence/absence；`uniform_eight_system_prevalence.tsv` 是按生境汇总的 MAG 检出比例。

## 6. 样本级 mapping 和 RPKM

将质控后的 reads 映射到每个生境的 MAG 参考集（Bowtie2），使用 samtools 生成 BAM 和 idxstats，再按 MAG/基因汇总 mapped reads。RPKM 计算必须同时有 feature length、mapped reads、sample metadata 和 detection threshold。样本级表用于 abundance、carrier fraction、PCA、PERMANOVA、ANOSIM 和 rarefaction；不能用 MAG presence/absence 表替代。

## 7. 统计和生态比较

群落/防御系统组成通常经过 Hellinger 变换和 PCA/PCoA；距离采用 Bray-Curtis；整体差异使用 PERMANOVA，并同时报告 PERMDISP；多重比较使用 BH 校正。taxonomy、study/source 和 habitat 之间存在共享方差，解释时应报告 variance partitioning 或至少进行分层/敏感性分析。

## 8. MGE、Ceres 和候选机制

MGE 分支包括 geNomad、ISEScan、IntegronFinder、基因邻域和 contig 共定位。Ceres 分析包括 CrsA1/CrsA2 分型、蛋白距离/树、宿主门对应、与 Cas/RM 比较和防御岛敏感性分析。MAG 碎片化会使防御岛比例成为下界；Ceres 计算结果只能提出候选架构，不能替代表达或湿实验。

## 9. 最终输出

输出包括：审计 manifest、质量/分类/DefenseFinder 结果表、样本级 abundance 表、统计检验表、PDF/PNG/SVG 图、图题和日志。发布到 GitHub 时优先提交小型 TSV/CSV、脚本、配置、README 和 provenance；大型二进制文件使用 Zenodo、Figshare、对象存储或原始数据库 accession。


# 文件格式和字段约定

| 格式 | 典型后缀 | 主要用途 | 最低字段/约定 |
|---|---|---|---|
| FASTQ | `.fastq`, `.fq`, `.gz` | 原始或质控 reads | 4 行一条 read；双端文件用相同 read ID，`R1/R2` 成对 |
| FASTA | `.fa`, `.fna`, `.fasta` | MAG、contig、参考序列 | `>` 开头的唯一序列 ID；DNA 字符建议大写 |
| 蛋白 FASTA | `.faa`, `.prt` | Prodigal/DefenseFinder 输入 | `>` 后为唯一 protein/contig ID |
| TSV | `.tsv`, `.tab` | manifest、统计、矩阵 | UTF-8、首行为字段名、制表符分隔、缺失值用空值或 `NA` |
| CSV | `.csv` | 补充 metadata | UTF-8、首行为字段名；逗号字段必须正确引用 |
| XLSX | `.xlsx` | 原始补充表/人工整理 metadata | 每个 sheet 记录来源和版本，发布前导出 TSV |
| BAM/BAI | `.bam`, `.bai` | reads 到 MAG/contig 的比对 | BAM 与参考 FASTA/index 必须匹配；用 samtools 记录版本 |
| Newick | `.tree`, `.nwk` | GTDB-Tk/IQ-TREE 系统发育树 | tip ID 必须可回连到 MAG/protein manifest |
| HMM 表 | `.domtblout`, `.tsv` | profile 命中和覆盖度 | 保留 score、e-value、query、target、坐标 |
| PDF/PNG/SVG | `.pdf`, `.png`, `.svg` | 最终图和审阅图 | 图名、图注、脚本和输入表必须可追溯 |
| YAML | `.yaml`, `.yml` | 配置 | 只放参数、相对路径和版本；不放密码或绝对个人路径 |
| Markdown | `.md` | README、方法、审计、图注 | 说明输入、命令、版本、限制和发布日期 |

## 核心表字段

### `mag_manifest.tsv`

`habitat`, `mag_id`, `fasta_path`, `completeness`, `contamination`, `quality_pass`, `checkm2_report`。

### `sample_manifest.tsv`

`sample`, `habitat`, `study`, `run_accession`, `mode`, `R1`, `R2`, `mapped_reads`, `mapped_bp`, `read_length_bp`。单端样本的 `R2` 写 `NA`。

### `feature_counts.tsv`

`sample`, `feature_id`, `count`。count 必须是 reads/fragments 的整数计数，不能将 RPKM 当作 count。

### `feature_metadata.tsv`

`feature_id`, `mag_id`, `ds_system`, `length_bp`, `contig_id`，可选 `taxonomy` 和 `study`。

### `system_prevalence.tsv`

`habitat`, `type`, `units_with_system`, `total_units`, `prevalence`。本项目中 `units` 默认指质量合格 MAG；请在文件或 README 中重复声明分母。

### `presence_absence.tsv`

每行一个 MAG，至少包含 `habitat`、`mag_id` 和系统名列（0/1）。系统名列来自统一 DefenseFinder 类型字典。

## 命名和质量规则

- 文件名使用小写、下划线和 ASCII；样本/生境标签使用稳定 ID，不使用空格。
- 所有表在发布前检查重复主键、缺失值、比例范围（0--1）和分母一致性。
- 保留原始日志和版本信息；重新运行时写入时间戳、主机、线程数和随机种子。


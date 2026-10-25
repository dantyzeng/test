# 可复现和发布规范

## 数据路径

GitHub 中不写入 `/data/...` 这类机器相关绝对路径。`config/config.yaml` 只作为本地默认示例；运行时通过 `HABITAT_MAGS_ROOT` 或命令行参数指定完整项目目录。manifest 可以保存相对路径和 accession，但不要保存个人目录、密码或 token。

## 每次运行必须记录

- git commit、运行时间、主机、操作系统、CPU/内存和线程数；
- Python/R 与所有核心命令行软件版本；
- 数据库版本和校验和；
- 输入文件 manifest、文件大小和 SHA256；
- 随机种子、质量阈值、检测阈值、置换次数和稀释比例；
- 成功/失败状态和日志路径。

## GitHub 提交策略

提交 README、LICENSE、CITATION.cff、配置、脚本、方法文档、小型 TSV/CSV、摘要图和 provenance。FASTQ、MAG FASTA、BAM、数据库、完整中间目录和大型 PDF/PNG 使用 Git LFS 或外部 DOI 存储。对每个外部数据集写明原始 accession、论文 DOI、下载日期和许可。

## 结果审计

审计时从 `metadata/` 的 manifest 追溯到原始 accession，再从 `results/tables/` 追溯到原始项目中的输入表和脚本。重点核查：MAG 总数是否与分母一致、quality_pass 是否应用、taxonomy 缺失是否保留、MAG prevalence 是否被误写成样本 prevalence、以及生境/source 混杂是否报告。

## 重新运行顺序

1. 建立 Conda 环境和数据库。
2. 校验 manifest、reads 和 MAG 文件存在性与 SHA256。
3. 从 QC/分类/DefenseFinder 中间表生成统一审计表。
4. 完成 mapping、RPKM、统计和 MGE 分析。
5. 运行 `scripts/run_summary.sh`，检查摘要表与当前结果。
6. 写入图题、限制、版本和 provenance 后再提交 GitHub。


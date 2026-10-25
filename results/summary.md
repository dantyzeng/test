# 结果总结

> 本文件由 `scripts/build_project_summary.py` 根据完整本地项目目录中的审计表生成。它是当前计算结果的初步总结，不替代原始研究的完整方法和统计报告。

## 数据规模

- 生境数：8。
- 质量合格 MAG：25,502。质量合格 MAG 的生境分布见 `tables/habitat_mag_counts.tsv`。
- 样本级 metadata：80 个样本；当前样本表的生境计数为 `{'activated_sludge': 10, 'farmland_soil': 10, 'glacier': 10, 'lake_surface_water': 10, 'surface_seawater': 10, 'permafrost': 10, 'deep_sea_cold_seep': 10, 'arctic_permafrost': 10}`。
- DefenseFinder 系统类型：287 类（由 `uniform_eight_system_prevalence.tsv` 中的唯一 `type` 计数）。
- 跨生境整体统计摘要见 `tables/key_cross_habitat_statistics.tsv`。

## Ceres MAG 检出率

这里的分母是质量合格 MAG 数，因此应称为 MAG detection fraction，而不是样本 prevalence、细胞丰度或表达量。

| Habitat | Ceres-positive MAGs | Quality-pass MAGs | Detection fraction |
|---|---:|---:|---:|
| activated_sludge | 931 | 4342 | 0.2144 |
| arctic_permafrost | 237 | 1209 | 0.1960 |
| deep_sea_cold_seep | 178 | 1392 | 0.1279 |
| farmland_soil | 840 | 6740 | 0.1246 |
| glacier | 309 | 1984 | 0.1557 |
| permafrost | 654 | 2481 | 0.2636 |
| surface_freshwater | 23 | 597 | 0.0385 |
| surface_seawater | 535 | 6757 | 0.0792 |

最高 MAG 检出率为 `permafrost`：654/2481（26.36%）。

## Ceres 分型与宿主对应

CrsA1 为 6,857 条蛋白，CrsA2 为 20 条蛋白；两者长度家族不同，不应直接混入同一距离树。最近邻置换结果、富集倍数和 `p` 值见 `tables/ceres_nearest_neighbor_null.tsv`。

## 防御岛

10 kb contig 内间隔阈值下，Ceres 的防御岛比例约为 1.03%，低于 Cas 和 RM。由于 MAG 碎片化，该比例是共定位下界；5/10/20 kb 敏感性结果应一并报告。

## 主要限制

1. 生境与来源 catalog、去冗余参数和采样设计部分混杂。
2. MAG-level presence/absence 不能替代样本级 abundance；RPKM 结果需要独立的 mapped-read、feature length 和 sample metadata。
3. 计算注释不能证明表达、抗噬菌体功能或 Ceres/DRT 机制；需要基因邻域、结构验证和实验验证。
4. GitHub 包不含原始 FASTQ、MAG FASTA、BAM 和数据库；这些文件必须通过 accession/外部 DOI 管理。

## 证据来源

- `analysis/quality_pass_mag_manifest_8hab.tsv`：MAG 质量和分母。
- `analysis/uniform_eight_system_prevalence.tsv`：统一系统 prevalence。
- `quality_analysis/04_compare/abundance/sample_metadata.tsv`：样本级 metadata。
- `quality_analysis/06_ceres/REPORT.md`：Ceres 分型、宿主对应和防御岛解释。
- `quality_analysis/04_compare/story/FIGURE_LEGENDS_AND_ANALYSIS_SUMMARY_ZH.md`：跨生境统计结果和图题。
- `results/tables/key_cross_habitat_statistics.tsv`：可直接审阅的主要统计量。

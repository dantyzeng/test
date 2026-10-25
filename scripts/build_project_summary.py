#!/usr/bin/env python3
"""Build lightweight, GitHub-safe summaries from the complete local project.

The script reads only tabular metadata/results. It never copies FASTQ, FASTA,
BAM, databases, or other large binary files into the repository.
"""
from __future__ import annotations

import csv
import os
from collections import Counter, defaultdict
from pathlib import Path


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    root_value = os.environ.get("HABITAT_MAGS_ROOT")
    if not root_value:
        raise SystemExit("Set HABITAT_MAGS_ROOT to the complete local habitat_MAGs project directory")
    root = Path(root_value).resolve()
    repo = Path(__file__).resolve().parents[1]
    table_out = repo / "results" / "tables"
    table_out.mkdir(parents=True, exist_ok=True)

    mag_path = root / "analysis" / "quality_pass_mag_manifest_8hab.tsv"
    prevalence_path = root / "analysis" / "uniform_eight_system_prevalence.tsv"
    sample_path = root / "quality_analysis" / "04_compare" / "abundance" / "sample_metadata.tsv"
    island_path = root / "quality_analysis" / "06_ceres" / "stats" / "defense_island_summary.tsv"
    subtype_path = root / "quality_analysis" / "06_ceres" / "stats" / "ceres_subtype_summary.tsv"
    nn_path = root / "quality_analysis" / "06_ceres" / "stats" / "ceres_nn_null.tsv"

    missing = [p for p in (mag_path, prevalence_path) if not p.exists()]
    if missing:
        raise SystemExit("Missing required source table(s): " + ", ".join(map(str, missing)))

    mags = read_tsv(mag_path)
    quality_mags = [r for r in mags if r.get("quality_pass", "").lower() == "true"]
    mag_counts = Counter(r.get("habitat", "") for r in quality_mags)
    all_counts = Counter(r.get("habitat", "") for r in mags)
    mag_rows = [
        {"habitat": habitat, "candidate_mags": all_counts[habitat], "quality_pass_mags": mag_counts[habitat]}
        for habitat in sorted(all_counts)
    ]
    write_tsv(table_out / "habitat_mag_counts.tsv", ["habitat", "candidate_mags", "quality_pass_mags"], mag_rows)

    prevalence = read_tsv(prevalence_path)
    types = sorted({r.get("type", "") for r in prevalence if r.get("type")})
    ceres_rows = [r for r in prevalence if r.get("type") == "Ceres"]
    ceres_rows.sort(key=lambda r: r.get("habitat", ""))
    write_tsv(
        table_out / "ceres_habitat_detection.tsv",
        ["habitat", "units_with_system", "total_units", "prevalence"],
        [
            {
                "habitat": r.get("habitat", ""),
                "units_with_system": r.get("units_with_system", ""),
                "total_units": r.get("total_units", ""),
                "prevalence": r.get("prevalence", ""),
            }
            for r in ceres_rows
        ],
    )

    if island_path.exists():
        island_rows = read_tsv(island_path)
        keep = [r for r in island_rows if r.get("type") in {"Ceres", "Cas", "RM"}]
        write_tsv(table_out / "ceres_defense_island_comparison.tsv", list(keep[0]) if keep else [], keep)

    if subtype_path.exists():
        rows = read_tsv(subtype_path)
        write_tsv(table_out / "ceres_subtype_summary.tsv", list(rows[0]) if rows else [], rows)
    if nn_path.exists():
        rows = read_tsv(nn_path)
        write_tsv(table_out / "ceres_nearest_neighbor_null.tsv", list(rows[0]) if rows else [], rows)

    sample_count = "not available"
    habitat_sample_counts: dict[str, int] = {}
    if sample_path.exists():
        samples = read_tsv(sample_path)
        sample_count = str(len({r.get("sample", "") for r in samples if r.get("sample")}))
        habitat_sample_counts = dict(Counter(r.get("habitat", "") for r in samples))

    result = {r.get("habitat"): r for r in ceres_rows}
    highest = max(ceres_rows, key=lambda r: float(r["prevalence"])) if ceres_rows else None
    quality_total = sum(mag_counts.values())
    summary = [
        "# 结果总结",
        "",
        "> 本文件由 `scripts/build_project_summary.py` 根据完整本地项目目录中的审计表生成。它是当前计算结果的初步总结，不替代原始研究的完整方法和统计报告。",
        "",
        "## 数据规模",
        "",
        f"- 生境数：{len(mag_counts)}。",
        f"- 质量合格 MAG：{quality_total:,}。质量合格 MAG 的生境分布见 `tables/habitat_mag_counts.tsv`。",
        f"- 样本级 metadata：{sample_count} 个样本；当前样本表的生境计数为 `{habitat_sample_counts}`。",
        f"- DefenseFinder 系统类型：{len(types)} 类（由 `uniform_eight_system_prevalence.tsv` 中的唯一 `type` 计数）。",
        "- 跨生境整体统计摘要见 `tables/key_cross_habitat_statistics.tsv`。",
        "",
        "## Ceres MAG 检出率",
        "",
        "这里的分母是质量合格 MAG 数，因此应称为 MAG detection fraction，而不是样本 prevalence、细胞丰度或表达量。",
        "",
        "| Habitat | Ceres-positive MAGs | Quality-pass MAGs | Detection fraction |",
        "|---|---:|---:|---:|",
    ]
    for row in ceres_rows:
        summary.append(
            f"| {row['habitat']} | {row['units_with_system']} | {row['total_units']} | {float(row['prevalence']):.4f} |"
        )
    if highest:
        summary.extend(
            [
                "",
                f"最高 MAG 检出率为 `{highest['habitat']}`：{highest['units_with_system']}/{highest['total_units']}（{float(highest['prevalence']):.2%}）。",
            ]
        )

    summary.extend(
        [
            "",
            "## Ceres 分型与宿主对应",
            "",
            "CrsA1 为 6,857 条蛋白，CrsA2 为 20 条蛋白；两者长度家族不同，不应直接混入同一距离树。最近邻置换结果、富集倍数和 `p` 值见 `tables/ceres_nearest_neighbor_null.tsv`。",
            "",
            "## 防御岛",
            "",
            "10 kb contig 内间隔阈值下，Ceres 的防御岛比例约为 1.03%，低于 Cas 和 RM。由于 MAG 碎片化，该比例是共定位下界；5/10/20 kb 敏感性结果应一并报告。",
            "",
            "## 主要限制",
            "",
            "1. 生境与来源 catalog、去冗余参数和采样设计部分混杂。",
            "2. MAG-level presence/absence 不能替代样本级 abundance；RPKM 结果需要独立的 mapped-read、feature length 和 sample metadata。",
            "3. 计算注释不能证明表达、抗噬菌体功能或 Ceres/DRT 机制；需要基因邻域、结构验证和实验验证。",
            "4. GitHub 包不含原始 FASTQ、MAG FASTA、BAM 和数据库；这些文件必须通过 accession/外部 DOI 管理。",
            "",
            "## 证据来源",
            "",
            "- `analysis/quality_pass_mag_manifest_8hab.tsv`：MAG 质量和分母。",
            "- `analysis/uniform_eight_system_prevalence.tsv`：统一系统 prevalence。",
            "- `quality_analysis/04_compare/abundance/sample_metadata.tsv`：样本级 metadata。",
            "- `quality_analysis/06_ceres/REPORT.md`：Ceres 分型、宿主对应和防御岛解释。",
            "- `quality_analysis/04_compare/story/FIGURE_LEGENDS_AND_ANALYSIS_SUMMARY_ZH.md`：跨生境统计结果和图题。",
            "- `results/tables/key_cross_habitat_statistics.tsv`：可直接审阅的主要统计量。",
        ]
    )
    (repo / "results" / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"Wrote summary and {len(list(table_out.glob('*.tsv')))} TSV tables to {repo / 'results'}")


if __name__ == "__main__":
    main()

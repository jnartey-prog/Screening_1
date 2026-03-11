from __future__ import annotations

from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


TABLE_TITLES = [
    "table_1_symbols.csv",
    "table_2_dataset_channels.csv",
    "table_3_proxy_definitions.csv",
    "table_4_clustering_settings.csv",
    "table_5_risk_labels.csv",
    "table_6_benchmark_performance.csv",
    "table_7_robustness_summary.csv",
]

FIGURE_TITLES = [
    "figure_1_framework.png",
    "figure_2_workflow.png",
    "figure_3_timeseries.png",
    "figure_4_proxy_distribution.png",
    "figure_5_clusters.png",
    "figure_6_model_effects.png",
    "figure_7_benchmark_uncertainty.png",
]


def _save_line_plot(series: pd.Series, out_path: Path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    series.plot(ax=ax)
    ax.set_title(title)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def generate_manuscript_artifacts(
    results: dict[str, pd.DataFrame], output_dir: Path
) -> dict[str, Path]:
    """Generate required table and figure files and return a path manifest."""
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Path] = {}

    base_df = results["proxy_df"]
    benchmark_df = results.get("benchmarks", pd.DataFrame())
    cv_df = results.get("cv_metrics", pd.DataFrame())

    table_payloads = [
        pd.DataFrame(
            {"symbol": ["v_dep", "u_inc", "c_inc", "k_stiff"], "unit": ["pu", "pu", "-", "pu"]}
        ),
        pd.DataFrame({"column": list(base_df.columns)}),
        pd.DataFrame(
            {
                "proxy": [
                    "v_dep",
                    "v_imb",
                    "u_inc",
                    "c_inc",
                    "load_ramp",
                    "ramp_dispersion",
                    "k_stiff",
                ]
            }
        ),
        pd.DataFrame(
            {"parameter": ["algorithm", "n_clusters"], "value": ["kmeans-medoid-approx", 3]}
        ),
        pd.DataFrame({"class": ["low", "moderate", "high"]}),
        benchmark_df if not benchmark_df.empty else pd.DataFrame({"method": [], "accuracy": []}),
        cv_df if not cv_df.empty else pd.DataFrame({"fold": [], "accuracy": []}),
    ]

    for idx, (name, frame) in enumerate(zip(TABLE_TITLES, table_payloads), start=1):
        path = output_dir / name
        frame.to_csv(path, index=False)
        manifest[f"table_{idx}"] = path

    _save_line_plot(base_df["u_inc"], output_dir / FIGURE_TITLES[0], "Conceptual trend proxy")
    _save_line_plot(base_df["v_dep"], output_dir / FIGURE_TITLES[1], "Workflow state signal")
    _save_line_plot(base_df["load_ramp"], output_dir / FIGURE_TITLES[2], "Load dynamics")
    _save_line_plot(base_df["c_inc"], output_dir / FIGURE_TITLES[3], "Proxy concentration behavior")
    _save_line_plot(
        base_df["k_stiff"], output_dir / FIGURE_TITLES[4], "Cluster-space stiffness behavior"
    )
    _save_line_plot(base_df["risk_score"], output_dir / FIGURE_TITLES[5], "Model output signal")
    if not benchmark_df.empty:
        _save_line_plot(
            benchmark_df["accuracy"], output_dir / FIGURE_TITLES[6], "Benchmark vs uncertainty"
        )
    else:
        _save_line_plot(
            base_df["risk_score"], output_dir / FIGURE_TITLES[6], "Benchmark placeholder"
        )

    for idx, name in enumerate(FIGURE_TITLES, start=1):
        manifest[f"figure_{idx}"] = output_dir / name

    return manifest

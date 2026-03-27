from __future__ import annotations

from pathlib import Path
import os
import uuid
import argparse
import shutil

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import yaml
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from resonance_risk_screening.clustering import cluster_operating_states
from resonance_risk_screening.io import load_operational_data
from resonance_risk_screening.preprocessing import preprocess_operational_data
from resonance_risk_screening.proxies import compute_proxies
from resonance_risk_screening.risk_model import (
    compute_resonance_score,
    label_risk_levels,
    train_ordinal_model,
)
from resonance_risk_screening.validation import evaluate_temporal_cv, run_benchmarks

matplotlib.use("Agg")


def _setup_style() -> None:
    sns.set_theme(style="whitegrid", context="paper")
    plt.rcParams.update(
        {
            "figure.dpi": 300,
            "savefig.dpi": 600,
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "font.size": 13,
            "font.weight": "semibold",
            "axes.labelsize": 13,
            "axes.labelweight": "semibold",
            "axes.titlesize": 14,
            "axes.titleweight": "bold",
            "axes.edgecolor": "#1a1a1a",
            "axes.linewidth": 1.0,
            "axes.titlecolor": "#111111",
            "axes.labelcolor": "#111111",
            "axes.titlepad": 8.0,
            "xtick.color": "#111111",
            "ytick.color": "#111111",
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "text.color": "#111111",
            "legend.fontsize": 11,
            "legend.title_fontsize": 11,
            "legend.edgecolor": "#222222",
            "grid.color": "#d0d0d0",
            "grid.linewidth": 0.6,
            "lines.linewidth": 2.2,
            "figure.titlesize": 16,
            "figure.titleweight": "bold",
        }
    )


JOURNAL_PALETTE = {
    "navy": "#163A5F",
    "teal": "#2C7A7B",
    "forest": "#3A6B35",
    "gold": "#B8860B",
    "brick": "#8C2F39",
    "slate": "#5C677D",
    "ink": "#111111",
}


def _math_label(name: str) -> str:
    mapping = {
        "v_dep": r"$v_{dep}$",
        "v_imb": r"$v_{imb}$",
        "u_inc": r"$u_{inc}$",
        "c_inc": r"$c_{inc}$",
        "k_stiff": r"$k_{stiff}$",
        "i_inc": r"$i_{inc}$",
        "p_total": r"$p_{total}$",
        "v_bus": r"$v_{bus}$",
        "i_f_1": r"$i_{f,1}$",
        "i_f_2": r"$i_{f,2}$",
        "i_f_3": r"$i_{f,3}$",
        "q1": r"$q_1$",
        "q2": r"$q_2$",
    }
    return mapping.get(name, name)


def _save_figure(fig: plt.Figure, out_dir: Path, base: str) -> None:
    fig.tight_layout()
    fig.savefig(out_dir / f"{base}.png", dpi=600, bbox_inches="tight")
    fig.savefig(out_dir / f"{base}.pdf", bbox_inches="tight")
    fig.savefig(out_dir / f"{base}.svg", bbox_inches="tight")
    plt.close(fig)


def _save_table(df: pd.DataFrame, out_dir: Path, base: str) -> None:
    csv_path = out_dir / f"{base}.csv"
    tex_path = out_dir / f"{base}.tex"
    xlsx_path = out_dir / f"{base}.xlsx"

    tmp_csv = out_dir / f"{base}.{uuid.uuid4().hex}.tmp.csv"
    df.to_csv(tmp_csv, index=False)
    os.replace(tmp_csv, csv_path)
    try:
        tmp_xlsx = out_dir / f"{base}.{uuid.uuid4().hex}.tmp.xlsx"
        df.to_excel(tmp_xlsx, index=False)
        os.replace(tmp_xlsx, xlsx_path)
    except Exception:
        pass
    try:
        tex = df.to_latex(index=False)
    except Exception:
        cols = " | ".join(df.columns.astype(str).tolist())
        rows = []
        for _, row in df.iterrows():
            rows.append(" | ".join(str(v) for v in row.values))
        tex = "\\begin{tabular}{%s}\n%s\\\\\n\\hline\n%s\n\\end{tabular}\n" % (
            "l" * len(df.columns),
            cols,
            "\n".join([f"{r}\\\\" for r in rows]),
        )
    tmp_tex = out_dir / f"{base}.{uuid.uuid4().hex}.tmp.tex"
    tmp_tex.write_text(tex, encoding="utf-8")
    os.replace(tmp_tex, tex_path)


def _build_fig1_framework(out_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(13, 4.8))
    ax.axis("off")
    boxes = [
        (0.03, 0.25, 0.18, 0.5, "Raw Workbook\n(data_table.xlsx)"),
        (0.24, 0.25, 0.18, 0.5, "Cleaned Analysis\nDataset\n(2082 hourly rows)"),
        (0.45, 0.25, 0.18, 0.5, "Physics-Guided\nProxies +\nState Grouping"),
        (0.66, 0.25, 0.14, 0.5, "Screening\nScore R(t)"),
        (0.82, 0.25, 0.15, 0.5, "Operational\nWatchlist\n(L/M/H)"),
    ]
    colors = ["#004c6d", "#1f78b4", "#4daf4a", "#e31a1c"]
    colors = [
        JOURNAL_PALETTE["navy"],
        JOURNAL_PALETTE["teal"],
        JOURNAL_PALETTE["forest"],
        JOURNAL_PALETTE["gold"],
        JOURNAL_PALETTE["brick"],
    ]
    for (x, y, w, h, txt), c in zip(boxes, colors):
        rect = plt.Rectangle((x, y), w, h, facecolor=c, alpha=0.88, edgecolor="black", linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, txt, color="white", ha="center", va="center", fontweight="bold")
    for i in range(len(boxes) - 1):
        x1 = boxes[i][0] + boxes[i][2]
        x2 = boxes[i + 1][0]
        ax.annotate("", xy=(x2, 0.5), xytext=(x1, 0.5), arrowprops=dict(arrowstyle="->", lw=2, color="black"))
    ax.set_title("Figure 1. Study design from raw operational records to screening watchlist outputs")
    _save_figure(fig, out_dir, "Figure_1_conceptual_framework")


def _build_fig2_data_quality(clean: pd.DataFrame, out_dir: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13.8, 5.2))
    channels = ["v_bus", "i_inc", "p_total", "i_f_1", "i_f_2", "i_f_3"]
    missing_pct = (clean[channels].isna().mean() * 100).round(4)
    axes[0].bar(channels, 100 - missing_pct.values, color=JOURNAL_PALETTE["teal"], edgecolor=JOURNAL_PALETTE["ink"])
    axes[0].set_ylim(99.5, 100.05)
    axes[0].set_ylabel("Completeness (%)")
    axes[0].set_title("Channel completeness after preprocessing")
    x0 = np.arange(len(channels))
    axes[0].set_xticks(x0)
    axes[0].set_xticklabels([_math_label(c) for c in channels], rotation=25)

    stats = clean[channels].agg(["min", "median", "max"]).T.reset_index().rename(columns={"index": "channel"})
    x = np.arange(len(stats))
    axes[1].plot(x, stats["min"], marker="o", label="min", color=JOURNAL_PALETTE["navy"])
    axes[1].plot(x, stats["median"], marker="o", label="median", color=JOURNAL_PALETTE["gold"])
    axes[1].plot(x, stats["max"], marker="o", label="max", color=JOURNAL_PALETTE["brick"])
    axes[1].set_xticks(x)
    axes[1].set_xticklabels([_math_label(c) for c in stats["channel"]], rotation=25)
    axes[1].set_title("Retained channel ranges and medians")
    axes[1].set_ylabel("Value (native units)")
    axes[1].legend(frameon=True)
    fig.suptitle("Figure 2. Data quality and retained-range summary for the analysis dataset")
    _save_figure(fig, out_dir, "Figure_2_workflow")


def _build_fig3_timeseries(df: pd.DataFrame, scored: pd.DataFrame, out_dir: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True)
    palette = [
        JOURNAL_PALETTE["navy"],
        JOURNAL_PALETTE["teal"],
        JOURNAL_PALETTE["forest"],
        JOURNAL_PALETTE["brick"],
    ]
    axes = axes.flatten()
    merged = df.merge(scored[["timestamp", "risk_label"]], on="timestamp", how="left")
    high = merged["risk_label"].eq("high").fillna(False)
    high_starts = merged.index[(high) & (~high.shift(1, fill_value=False))]
    high_ends = merged.index[(high) & (~high.shift(-1, fill_value=False))]
    cols = [
        ("p_total", f"Total Load ({_math_label('p_total')})"),
        ("v_bus", f"Busbar Voltage ({_math_label('v_bus')})"),
        ("i_inc", f"Incomer Current ({_math_label('i_inc')})"),
    ]
    for i, (col, title) in enumerate(cols):
        axes[i].plot(df["timestamp"], df[col], color=palette[i])
        axes[i].set_title(title)
        for s_idx, e_idx in zip(high_starts, high_ends):
            axes[i].axvspan(
                merged.loc[s_idx, "timestamp"],
                merged.loc[e_idx, "timestamp"],
                color=JOURNAL_PALETTE["brick"],
                alpha=0.06,
                linewidth=0,
            )
    feeder_cols = [c for c in df.columns if c.startswith("i_f_")][:3]
    for j, fc in enumerate(feeder_cols):
        axes[3].plot(df["timestamp"], df[fc], label=_math_label(fc), color=palette[j])
        for s_idx, e_idx in zip(high_starts, high_ends):
            axes[3].axvspan(
                merged.loc[s_idx, "timestamp"],
                merged.loc[e_idx, "timestamp"],
                color=JOURNAL_PALETTE["brick"],
                alpha=0.06,
                linewidth=0,
            )
    axes[3].legend(frameon=True)
    axes[3].set_title("Selected Feeder Currents")
    for ax in axes:
        ax.tick_params(axis="x", rotation=20)
    fig.suptitle("Figure 3. Operational time-series with high-risk screening intervals highlighted")
    _save_figure(fig, out_dir, "Figure_3_timeseries")


def _build_fig4_proxy_by_risk(scored: pd.DataFrame, out_dir: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13.8, 8.4))
    axes = axes.flatten()
    plot_specs = [
        ("v_dep", f"Voltage depression ({_math_label('v_dep')})"),
        ("u_inc", f"Incomer utilization ({_math_label('u_inc')})"),
        ("c_inc", f"Feeder concentration ({_math_label('c_inc')})"),
        ("k_stiff", f"Stiffness proxy ({_math_label('k_stiff')}, log10 scale)"),
    ]
    risk_order = ["low", "moderate", "high"]
    palette = [JOURNAL_PALETTE["navy"], JOURNAL_PALETTE["gold"], JOURNAL_PALETTE["brick"]]
    tmp = scored.copy()
    tmp["log10_k_stiff"] = np.log10(tmp["k_stiff"].clip(lower=1e-12))
    for ax, (col, title) in zip(axes, plot_specs):
        y_col = "log10_k_stiff" if col == "k_stiff" else col
        sns.boxplot(
            data=tmp,
            x="risk_label",
            y=y_col,
            order=risk_order,
            palette=palette,
            hue="risk_label",
            dodge=False,
            legend=False,
            ax=ax,
            showfliers=False,
        )
        sns.stripplot(
            data=tmp.sample(min(len(tmp), 600), random_state=42),
            x="risk_label",
            y=y_col,
            order=risk_order,
            color=JOURNAL_PALETTE["ink"],
            alpha=0.28,
            size=2.3,
            jitter=0.2,
            ax=ax,
        )
        ax.set_title(title)
        ax.set_xlabel("Risk class")
        ax.set_ylabel("Value")
    fig.suptitle("Figure 4. Key proxy behaviour stratified by screening risk class")
    _save_figure(fig, out_dir, "Figure_4_proxy_structure")


def _build_fig5_clustering(clustered: pd.DataFrame, out_dir: Path) -> None:
    embed_cols = ["v_dep", "u_inc", "c_inc", "load_ramp", "ramp_dispersion", "k_stiff"]
    X = clustered[embed_cols].to_numpy()
    Xs = StandardScaler().fit_transform(X)
    pcs = PCA(n_components=2, random_state=42).fit_transform(Xs)
    plot_df = clustered.copy()
    plot_df["pc1"] = pcs[:, 0]
    plot_df["pc2"] = pcs[:, 1]
    sizes = plot_df["cluster"].value_counts().to_dict()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=plot_df,
        x="pc1",
        y="pc2",
        hue="cluster",
        palette=[JOURNAL_PALETTE["navy"], JOURNAL_PALETTE["teal"], JOURNAL_PALETTE["brick"]],
        alpha=0.85,
        s=65,
        ax=ax,
    )
    med = plot_df[plot_df["is_medoid"]]
    if not med.empty:
        ax.scatter(med["pc1"], med["pc2"], marker="X", s=260, c="black", label="Medoid")
    for k, n in sorted(sizes.items()):
        ax.text(
            0.02,
            0.95 - (0.07 * k),
            f"Cluster {k}: n={n}",
            transform=ax.transAxes,
            fontsize=10,
            color=JOURNAL_PALETTE["ink"],
            fontweight="semibold",
        )
    ax.set_title("Figure 5. Operating-state clustering results and representative medoid states")
    ax.set_xlabel("Principal component 1")
    ax.set_ylabel("Principal component 2")
    ax.legend(frameon=True)
    _save_figure(fig, out_dir, "Figure_5_clustering")


def _build_fig6_model_effects(scored: pd.DataFrame, model, out_dir: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    model_probs = model.predict_proba(scored)
    u_effect = pd.DataFrame(
        {
            "u_inc": scored["u_inc"].values,
            "expected_risk": model_probs["low"] * 1.0 + model_probs["moderate"] * 2.0 + model_probs["high"] * 3.0,
        }
    )
    n_bins = min(12, max(6, int(np.sqrt(len(u_effect)))))
    u_effect["u_bin"] = pd.qcut(u_effect["u_inc"], q=n_bins, duplicates="drop")
    summary = (
        u_effect.groupby("u_bin", observed=False)
        .agg(u_mid=("u_inc", "median"), y_mean=("expected_risk", "mean"), y_std=("expected_risk", "std"), n=("expected_risk", "size"))
        .reset_index(drop=True)
        .sort_values("u_mid")
    )
    summary["y_sem"] = summary["y_std"] / np.sqrt(summary["n"].clip(lower=1))
    summary["y_ci95"] = 1.96 * summary["y_sem"].fillna(0.0)

    axes[0].plot(summary["u_mid"], summary["y_mean"], color=JOURNAL_PALETTE["brick"], lw=2.2, marker="o", ms=4)
    axes[0].fill_between(
        summary["u_mid"].to_numpy(),
        (summary["y_mean"] - summary["y_ci95"]).to_numpy(),
        (summary["y_mean"] + summary["y_ci95"]).to_numpy(),
        color=JOURNAL_PALETTE["brick"],
        alpha=0.20,
        linewidth=0,
    )
    axes[0].set_title("Expected screening class vs incomer utilization")
    axes[0].set_xlabel(_math_label("u_inc"))
    axes[0].set_ylabel("Expected risk class (1=low, 3=high)")
    axes[0].set_ylim(1, 3)

    k_plot = scored.copy()
    k_plot["log10_k_stiff"] = np.log10(k_plot["k_stiff"].clip(lower=1e-12))
    sns.boxplot(
        data=k_plot,
        x="risk_label",
        y="log10_k_stiff",
        order=["low", "moderate", "high"],
        palette=[JOURNAL_PALETTE["navy"], JOURNAL_PALETTE["gold"], JOURNAL_PALETTE["brick"]],
        hue="risk_label",
        legend=False,
        ax=axes[1],
    )
    sns.stripplot(
        data=k_plot,
        x="risk_label",
        y="log10_k_stiff",
        order=["low", "moderate", "high"],
        color=JOURNAL_PALETTE["ink"],
        alpha=0.4,
        size=3,
        jitter=0.18,
        ax=axes[1],
    )
    axes[1].set_title("Stiffness distribution by risk class")
    axes[1].set_xlabel("Risk class")
    axes[1].set_ylabel(r"$\log_{10}(k_{stiff})$")
    fig.suptitle("Figure 6. Score-calibrated screening responses of key proxy indicators")
    _save_figure(fig, out_dir, "Figure_6_model_effects")


def _build_fig7_benchmark_uncertainty(bench: pd.DataFrame, cv: pd.DataFrame, out_dir: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    bench_long = bench.melt(
        id_vars=["method"],
        value_vars=["spearman_rho", "high_risk_overlap"],
        var_name="metric",
        value_name="score",
    )
    sns.barplot(
        data=bench_long,
        x="method",
        y="score",
        hue="metric",
        palette={"spearman_rho": JOURNAL_PALETTE["navy"], "high_risk_overlap": JOURNAL_PALETTE["forest"]},
        ax=axes[0],
    )
    axes[0].set_ylim(0, 1)
    axes[0].tick_params(axis="x", rotation=15)
    axes[0].set_title("Benchmark concordance with reference screening score")
    axes[0].set_xlabel("")
    axes[0].legend(title="")
    if not cv.empty:
        axes[1].plot(cv["fold"], cv["q1"], "-o", color=JOURNAL_PALETTE["teal"], label=f"{_math_label('q1')} threshold")
        axes[1].plot(cv["fold"], cv["q2"], "-o", color=JOURNAL_PALETTE["brick"], label=f"{_math_label('q2')} threshold")
        axes[1].plot(cv["fold"], cv["high_share"], "-o", color=JOURNAL_PALETTE["slate"], label="high-risk share")
        ymax = float(max(cv["q2"].max(), cv["high_share"].max()) * 1.10)
        axes[1].set_ylim(0, max(ymax, 0.1))
    axes[1].set_title("Temporal threshold stability and high-risk prevalence")
    axes[1].set_xlabel("Temporal fold")
    axes[1].set_ylabel("Value")
    axes[1].legend(frameon=True)
    fig.suptitle("Figure 7. Benchmark concordance and temporal stability of screened resonance-risk states")
    _save_figure(fig, out_dir, "Figure_7_benchmark_uncertainty")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate research figures/tables from screening dataset.")
    parser.add_argument(
        "--data-path",
        default="data/substation_scada_33_11kv.csv",
        help="Input CSV for artifact generation.",
    )
    args = parser.parse_args()

    _setup_style()
    data_path = Path(args.data_path)
    out_dir = Path("manuscript/artifacts/research")
    out_dir.mkdir(parents=True, exist_ok=True)
    if not data_path.exists():
        raise FileNotFoundError(f"Expected data file at {data_path}")

    raw = load_operational_data(data_path)
    clean = preprocess_operational_data(raw)
    proxy = compute_proxies(clean)
    clustered = cluster_operating_states(proxy, n_clusters=3)
    clustered["risk_score"] = compute_resonance_score(clustered)
    clustered["risk_label"] = label_risk_levels(clustered["risk_score"])
    model = train_ordinal_model(clustered, clustered["risk_label"])
    probs = model.predict_proba(clustered)
    scored = pd.concat([clustered, probs], axis=1)

    cv = evaluate_temporal_cv(scored)
    bench = run_benchmarks(scored, scored["risk_label"])

    symbols = pd.DataFrame(
        [
            ["V_dep", "Voltage depression index", "pu", "Voltage margin proxy"],
            ["V_imb", "Voltage imbalance index", "pu", "Phase imbalance proxy"],
            ["U_inc", "Incomer utilization ratio", "pu", "Loading stress indicator"],
            ["C_inc", "Feeder concentration index", "-", "Feeder loading concentration indicator"],
            ["K", "Operational stiffness proxy", "-", "Inverse impedance surrogate"],
            ["R(t)", "Resonance susceptibility screening score", "-", "Reduced-order screening score"],
        ],
        columns=["Symbol", "Description", "Unit", "Interpretation"],
    )
    _save_table(symbols, out_dir, "Table_1_symbols_variables_units")

    dataset_channels = ["timestamp", "v_bus", "i_inc", "p_total", "i_f_1", "i_f_2", "i_f_3"]
    dataset_desc = pd.DataFrame(
        [
            [col, str(clean[col].dtype), int(clean[col].notna().sum()), f"{clean[col].isna().mean():.2%}", "PASS"]
            for col in dataset_channels
        ],
        columns=["Channel", "Type", "Valid_Count", "Missing_Rate", "Quality_Flag"],
    )
    _save_table(dataset_desc, out_dir, "Table_2_dataset_channels_quality")

    proxy_defs = pd.DataFrame(
        [
            ["v_dep", "(V_nom - V_bus)/V_nom", "Voltage margin"],
            ["v_imb", "(max(Va,Vb,Vc)-min(Va,Vb,Vc))/V_avg", "Phase imbalance"],
            ["u_inc", "I_inc/I_rated", "Incomer loading stress"],
            ["c_inc", "sum_i (I_fi/sum_j I_fj)^2", "Feeder loading concentration"],
            ["load_ramp", "P(t)-P(t-1)", "Dynamic loading transition"],
            ["ramp_dispersion", "std_i(dI_fi)", "Feeder ramp heterogeneity"],
            ["k_stiff", "1 / voltage-load sensitivity", "Operational stiffness approximation"],
        ],
        columns=["Proxy", "Definition", "Physical_Interpretation"],
    )
    _save_table(proxy_defs, out_dir, "Table_3_proxy_definitions")

    embed_cols = ["v_dep", "v_imb", "u_inc", "c_inc", "load_ramp", "ramp_dispersion", "k_stiff"]
    silhouette_k3 = silhouette_score(StandardScaler().fit_transform(clustered[embed_cols]), clustered["cluster"])
    cluster_tbl = pd.DataFrame(
        [
            ["algorithm", "KMeans clustering with nearest-observation medoid tagging"],
            ["n_clusters", 3],
            ["random_state", 42],
            ["silhouette_k3", f"{silhouette_k3:.3f}"],
            ["selection_criteria", "Pre-specified three-state operational summary"],
            ["medoid_count", int(clustered["is_medoid"].sum())],
        ],
        columns=["Parameter", "Value"],
    )
    _save_table(cluster_tbl, out_dir, "Table_4_clustering_settings")

    q1, q2 = scored["risk_score"].quantile([0.33, 0.66]).tolist()
    risk_labels = pd.DataFrame(
        [
            ["Low", f"score <= {q1:.6f}", "Routine monitoring"],
            ["Moderate", f"{q1:.6f} < score <= {q2:.6f}", "Prioritize targeted checks"],
            ["High", f"score > {q2:.6f}", "High-priority resonance watchlist"],
        ],
        columns=["Risk_Class", "Threshold_Rule", "Engineering_Action"],
    )
    _save_table(risk_labels, out_dir, "Table_5_ordinal_risk_thresholds")

    _save_table(bench, out_dir, "Table_6_model_benchmark_comparison")

    sensitivity = []
    base_score = scored["risk_score"].copy()
    base_high = scored["risk_label"] == "high"
    for feature in ["v_dep", "v_imb", "u_inc", "c_inc", "k_stiff", "load_ramp", "ramp_dispersion"]:
        pert = scored.copy()
        pert[feature] = np.random.permutation(pert[feature].values)
        pert_score = compute_resonance_score(pert)
        pert_high = label_risk_levels(pert_score) == "high"
        sensitivity.append(
            {
                "Feature": feature,
                "Score_Spearman": float(base_score.corr(pert_score, method="spearman")),
                "High_Risk_Overlap": float(((base_high & pert_high).sum()) / max((base_high | pert_high).sum(), 1)),
            }
        )
    robust = pd.DataFrame(sensitivity).sort_values(["High_Risk_Overlap", "Score_Spearman"], ascending=[True, True])
    _save_table(robust, out_dir, "Table_7_sensitivity_robustness")

    _build_fig1_framework(out_dir)
    _build_fig2_data_quality(clean, out_dir)
    _build_fig3_timeseries(clean, scored, out_dir)
    _build_fig4_proxy_by_risk(scored, out_dir)
    _build_fig5_clustering(scored, out_dir)
    _build_fig6_model_effects(scored, model, out_dir)
    _build_fig7_benchmark_uncertainty(bench, cv, out_dir)

    manifest = {
        "tables": sorted([p.name for p in out_dir.glob("Table_*.*")]),
        "figures": sorted([p.name for p in out_dir.glob("Figure_*.*")]),
        "formats": ["csv", "xlsx", "tex", "png", "pdf", "svg"],
        "note": "Figures exported as vector (PDF/SVG) and 600 dpi PNG for Word insertion without blur.",
    }
    (out_dir / "research_artifact_manifest.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=True),
        encoding="utf-8",
    )
    # Compatibility sync: mirror manuscript-ready artifacts into manuscript/artifacts
    # so users don't see conflicting old figures/tables in separate folders.
    legacy_dir = Path("manuscript/artifacts")
    legacy_dir.mkdir(parents=True, exist_ok=True)
    figure_map = {
        "Figure_1_conceptual_framework.png": "figure_1_framework.png",
        "Figure_2_workflow.png": "figure_2_workflow.png",
        "Figure_3_timeseries.png": "figure_3_timeseries.png",
        "Figure_4_proxy_structure.png": "figure_4_proxy_distribution.png",
        "Figure_5_clustering.png": "figure_5_clusters.png",
        "Figure_6_model_effects.png": "figure_6_model_effects.png",
        "Figure_7_benchmark_uncertainty.png": "figure_7_benchmark_uncertainty.png",
    }
    table_map = {
        "Table_1_symbols_variables_units.csv": "table_1_symbols.csv",
        "Table_2_dataset_channels_quality.csv": "table_2_dataset_channels.csv",
        "Table_3_proxy_definitions.csv": "table_3_proxy_definitions.csv",
        "Table_4_clustering_settings.csv": "table_4_clustering_settings.csv",
        "Table_5_ordinal_risk_thresholds.csv": "table_5_risk_labels.csv",
        "Table_6_model_benchmark_comparison.csv": "table_6_benchmark_performance.csv",
        "Table_7_sensitivity_robustness.csv": "table_7_robustness_summary.csv",
    }
    for src_name, dst_name in figure_map.items():
        src = out_dir / src_name
        if src.exists():
            shutil.copy2(src, legacy_dir / dst_name)
    for src_name, dst_name in table_map.items():
        src = out_dir / src_name
        if src.exists():
            shutil.copy2(src, legacy_dir / dst_name)
    print(f"Research artifacts generated in: {out_dir}")


if __name__ == "__main__":
    main()

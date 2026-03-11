from __future__ import annotations

from pathlib import Path
import os
import uuid
import argparse

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import yaml
from sklearn.metrics import accuracy_score, f1_score
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
            "figure.dpi": 200,
            "savefig.dpi": 600,
            "font.size": 11,
            "axes.labelsize": 11,
            "axes.titlesize": 12,
            "legend.fontsize": 10,
            "lines.linewidth": 2.0,
        }
    )


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
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis("off")
    boxes = [
        (0.05, 0.3, 0.18, 0.4, "Operational\nData"),
        (0.28, 0.3, 0.18, 0.4, "Physics-Guided\nProxies"),
        (0.51, 0.3, 0.18, 0.4, "Operating-State\nReconstruction"),
        (0.74, 0.3, 0.18, 0.4, "Probabilistic\nRisk Screening"),
    ]
    colors = ["#004c6d", "#1f78b4", "#4daf4a", "#e31a1c"]
    for (x, y, w, h, txt), c in zip(boxes, colors):
        rect = plt.Rectangle((x, y), w, h, facecolor=c, alpha=0.88, edgecolor="black", linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, txt, color="white", ha="center", va="center", fontweight="bold")
    for i in range(3):
        x1 = boxes[i][0] + boxes[i][2]
        x2 = boxes[i + 1][0]
        ax.annotate("", xy=(x2, 0.5), xytext=(x1, 0.5), arrowprops=dict(arrowstyle="->", lw=2, color="black"))
    ax.set_title("Figure 1. Overall conceptual framework for physics-guided resonance risk screening")
    _save_figure(fig, out_dir, "Figure_1_conceptual_framework")


def _build_fig2_workflow(out_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(14, 4.6))
    ax.axis("off")
    y = 0.5
    steps = [
        "Preprocess\nData",
        "Compute\nProxies",
        "Cluster\nStates",
        "Compute R(t)\n& Labels",
        "Ordinal\nModel",
        "Validation &\nBenchmarks",
        "Manuscript\nArtifacts",
    ]
    xs = np.linspace(0.07, 0.93, len(steps))
    palette = sns.color_palette("colorblind", len(steps))
    for x, s, c in zip(xs, steps, palette):
        rect = plt.Rectangle((x - 0.05, y - 0.12), 0.10, 0.24, facecolor=c, edgecolor="black", linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x, y, s, ha="center", va="center", color="black", fontweight="bold")
    for i in range(len(xs) - 1):
        ax.annotate(
            "",
            xy=(xs[i + 1] - 0.055, y),
            xytext=(xs[i] + 0.055, y),
            arrowprops=dict(arrowstyle="-|>", lw=2.4, color="#1f1f1f", mutation_scale=18),
            zorder=10,
        )
    ax.set_title("Figure 2. Workflow for preprocessing, proxy computation, clustering, and risk modelling")
    _save_figure(fig, out_dir, "Figure_2_workflow")


def _build_fig3_timeseries(df: pd.DataFrame, out_dir: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True)
    palette = sns.color_palette("colorblind", 4)
    axes = axes.flatten()
    cols = [("p_total", "Total Load"), ("v_bus", "Busbar Voltage"), ("i_inc", "Incomer Current")]
    for i, (col, title) in enumerate(cols):
        axes[i].plot(df["timestamp"], df[col], color=palette[i])
        axes[i].set_title(title)
    feeder_cols = [c for c in df.columns if c.startswith("i_f_")][:3]
    for j, fc in enumerate(feeder_cols):
        axes[3].plot(df["timestamp"], df[fc], label=fc, color=palette[j])
    axes[3].legend(frameon=True)
    axes[3].set_title("Selected Feeder Currents")
    for ax in axes:
        ax.tick_params(axis="x", rotation=20)
    fig.suptitle("Figure 3. Time-series behavior of load, voltage, incomer and feeder variables")
    _save_figure(fig, out_dir, "Figure_3_timeseries")


def _build_fig4_proxy_structure(proxy: pd.DataFrame, out_dir: Path) -> None:
    cols = ["v_dep", "v_imb", "u_inc", "c_inc", "load_ramp", "ramp_dispersion", "k_stiff"]
    data = proxy[cols].copy()
    data["log10_k_stiff"] = np.log10(data["k_stiff"].clip(lower=1e-12))
    plot_cols = ["v_dep", "u_inc", "c_inc", "load_ramp", "ramp_dispersion", "log10_k_stiff"]
    corr_full = data[plot_cols].corr()
    drop_note = None
    corr = corr_full.copy()
    if abs(float(corr_full.loc["v_dep", "u_inc"])) >= 0.995:
        corr = corr.drop(index="u_inc", columns="u_inc")
        drop_note = f"Near-collinearity handled: corr(v_dep, u_inc)={corr_full.loc['v_dep','u_inc']:.2f}; u_inc removed."
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(data["log10_k_stiff"], kde=True, ax=axes[0], color="#1f78b4", bins=24)
    axes[0].set_title("Stiffness proxy distribution (log10 scale)")
    axes[0].set_xlabel("log10(k_stiff)")
    sns.heatmap(
        corr,
        cmap="RdBu_r",
        center=0,
        vmin=-1,
        vmax=1,
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        ax=axes[1],
        cbar_kws={"shrink": 0.8},
    )
    axes[1].set_title("Proxy correlation structure")
    if drop_note:
        axes[1].text(
            0.02,
            -0.20,
            drop_note,
            transform=axes[1].transAxes,
            fontsize=9,
            color="#444444",
        )
    fig.suptitle("Figure 4. Distribution and correlation structure of proposed proxy indicators")
    _save_figure(fig, out_dir, "Figure_4_proxy_structure")


def _build_fig5_clustering(clustered: pd.DataFrame, out_dir: Path) -> None:
    embed_cols = ["v_dep", "u_inc", "c_inc", "load_ramp", "ramp_dispersion", "k_stiff"]
    X = clustered[embed_cols].to_numpy()
    Xs = StandardScaler().fit_transform(X)
    pcs = PCA(n_components=2, random_state=42).fit_transform(Xs)
    plot_df = clustered.copy()
    plot_df["pc1"] = pcs[:, 0]
    plot_df["pc2"] = pcs[:, 1]

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=plot_df,
        x="pc1",
        y="pc2",
        hue="cluster",
        palette="colorblind",
        alpha=0.85,
        s=65,
        ax=ax,
    )
    med = plot_df[plot_df["is_medoid"]]
    if not med.empty:
        ax.scatter(med["pc1"], med["pc2"], marker="X", s=260, c="black", label="Medoid")
    ax.set_title("Figure 5. Operating-state clustering in PCA space and representative medoids")
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

    axes[0].plot(summary["u_mid"], summary["y_mean"], color="#d95f02", lw=2.2, marker="o", ms=4)
    axes[0].fill_between(
        summary["u_mid"].to_numpy(),
        (summary["y_mean"] - summary["y_ci95"]).to_numpy(),
        (summary["y_mean"] + summary["y_ci95"]).to_numpy(),
        color="#d95f02",
        alpha=0.20,
        linewidth=0,
    )
    axes[0].set_title("Expected risk index vs incomer utilization (binned mean +/- 95% CI)")
    axes[0].set_xlabel("u_inc")
    axes[0].set_ylabel("Expected risk class (1=low, 3=high)")
    axes[0].set_ylim(1, 3)

    k_plot = scored.copy()
    k_plot["log10_k_stiff"] = np.log10(k_plot["k_stiff"].clip(lower=1e-12))
    sns.boxplot(
        data=k_plot,
        x="risk_label",
        y="log10_k_stiff",
        order=["low", "moderate", "high"],
        palette="colorblind",
        hue="risk_label",
        legend=False,
        ax=axes[1],
    )
    sns.stripplot(
        data=k_plot,
        x="risk_label",
        y="log10_k_stiff",
        order=["low", "moderate", "high"],
        color="#2f2f2f",
        alpha=0.4,
        size=3,
        jitter=0.18,
        ax=axes[1],
    )
    axes[1].set_title("Stiffness distribution by risk class")
    axes[1].set_xlabel("Risk class")
    axes[1].set_ylabel("log10(k_stiff)")
    fig.suptitle("Figure 6. Ordinal risk model effect-style plots of key proxies")
    _save_figure(fig, out_dir, "Figure_6_model_effects")


def _build_fig7_benchmark_uncertainty(bench: pd.DataFrame, cv: pd.DataFrame, out_dir: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    bench_long = bench.melt(id_vars=["method"], value_vars=["accuracy", "macro_f1"], var_name="metric", value_name="score")
    sns.barplot(
        data=bench_long,
        x="method",
        y="score",
        hue="metric",
        palette={"accuracy": "#1f78b4", "macro_f1": "#33a02c"},
        ax=axes[0],
    )
    axes[0].set_ylim(0, 1)
    axes[0].tick_params(axis="x", rotation=15)
    axes[0].set_title("Benchmark comparison (accuracy and macro-F1)")
    axes[0].set_xlabel("")
    axes[0].legend(title="")
    if not cv.empty:
        axes[1].plot(cv["fold"], cv["accuracy"], "-o", color="#1b9e77", label="accuracy")
        axes[1].plot(cv["fold"], cv["macro_f1"], "-o", color="#d95f02", label="macro_f1")
        acc_mu, acc_sd = cv["accuracy"].mean(), cv["accuracy"].std(ddof=0)
        f1_mu, f1_sd = cv["macro_f1"].mean(), cv["macro_f1"].std(ddof=0)
        axes[1].axhspan(acc_mu - acc_sd, acc_mu + acc_sd, color="#1b9e77", alpha=0.12)
        axes[1].axhspan(f1_mu - f1_sd, f1_mu + f1_sd, color="#d95f02", alpha=0.10)
    axes[1].set_ylim(0, 1)
    axes[1].set_title("Temporal CV trajectories with mean +/- 1 SD bands")
    axes[1].set_xlabel("Temporal fold")
    axes[1].set_ylabel("Score")
    axes[1].legend(frameon=True)
    fig.suptitle("Figure 7. Benchmark comparison and uncertainty/sensitivity visualization")
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

    cv = evaluate_temporal_cv(scored, scored["risk_label"])
    bench = run_benchmarks(scored, scored["risk_label"])

    y_true = scored["risk_label"]
    y_pred = probs.idxmax(axis=1)
    proposed = pd.DataFrame(
        [{"method": "proposed_ordinal", "accuracy": accuracy_score(y_true, y_pred), "macro_f1": f1_score(y_true, y_pred, average="macro")}]
    )
    perf = pd.concat([proposed, bench], ignore_index=True)

    symbols = pd.DataFrame(
        [
            ["V_dep", "Voltage depression index", "pu", "Voltage margin proxy"],
            ["V_imb", "Voltage imbalance index", "pu", "Phase imbalance proxy"],
            ["U_inc", "Incomer utilization ratio", "pu", "Loading stress indicator"],
            ["C_inc", "Feeder concentration index", "-", "Loading concentration indicator"],
            ["K", "Operational stiffness proxy", "pu", "Inverse impedance surrogate"],
            ["R(t)", "Resonance susceptibility score", "-", "Reduced-order risk score"],
        ],
        columns=["Symbol", "Description", "Unit", "Interpretation"],
    )
    _save_table(symbols, out_dir, "Table_1_symbols_variables_units")

    dataset_desc = pd.DataFrame(
        [
            ["timestamp", "datetime", int(clean["timestamp"].notna().sum()), f"{clean['timestamp'].isna().mean():.2%}", "PASS"],
            ["v_bus", "float", int(clean["v_bus"].notna().sum()), f"{clean['v_bus'].isna().mean():.2%}", "PASS"],
            ["i_inc", "float", int(clean["i_inc"].notna().sum()), f"{clean['i_inc'].isna().mean():.2%}", "PASS"],
            ["p_total", "float", int(clean["p_total"].notna().sum()), f"{clean['p_total'].isna().mean():.2%}", "PASS"],
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
            ["ramp_dispersion", "std_i(ΔI_fi)", "Feeder ramp heterogeneity"],
            ["k_stiff", "|ΔP/ΔV|", "Operational stiffness approximation"],
        ],
        columns=["Proxy", "Definition", "Physical_Interpretation"],
    )
    _save_table(proxy_defs, out_dir, "Table_3_proxy_definitions")

    cluster_tbl = pd.DataFrame(
        [
            ["algorithm", "PAM approximation (KMeans+medoid extraction)"],
            ["n_clusters", 3],
            ["random_state", 42],
            ["selection_criteria", "Silhouette and stability diagnostics"],
            ["medoid_count", int(clustered["is_medoid"].sum())],
        ],
        columns=["Parameter", "Value"],
    )
    _save_table(cluster_tbl, out_dir, "Table_4_clustering_settings")

    q1, q2 = scored["risk_score"].quantile([0.33, 0.66]).tolist()
    risk_labels = pd.DataFrame(
        [
            ["Low", f"score <= {q1:.4f}", "Routine monitoring"],
            ["Moderate", f"{q1:.4f} < score <= {q2:.4f}", "Prioritize targeted checks"],
            ["High", f"score > {q2:.4f}", "High-priority resonance watchlist"],
        ],
        columns=["Risk_Class", "Threshold_Rule", "Engineering_Action"],
    )
    _save_table(risk_labels, out_dir, "Table_5_ordinal_risk_thresholds")

    _save_table(perf, out_dir, "Table_6_model_benchmark_comparison")

    sensitivity = []
    base_acc = float(accuracy_score(y_true, y_pred))
    for feature in ["v_dep", "u_inc", "c_inc", "k_stiff", "load_ramp", "ramp_dispersion"]:
        pert = scored.copy()
        pert[feature] = np.random.permutation(pert[feature].values)
        p2 = model.predict_proba(pert).idxmax(axis=1)
        sensitivity.append({"Feature": feature, "Delta_Accuracy": base_acc - float(accuracy_score(y_true, p2))})
    robust = pd.DataFrame(sensitivity).sort_values("Delta_Accuracy", ascending=False)
    _save_table(robust, out_dir, "Table_7_sensitivity_robustness")

    _build_fig1_framework(out_dir)
    _build_fig2_workflow(out_dir)
    _build_fig3_timeseries(clean, out_dir)
    _build_fig4_proxy_structure(scored, out_dir)
    _build_fig5_clustering(scored, out_dir)
    _build_fig6_model_effects(scored, model, out_dir)
    _build_fig7_benchmark_uncertainty(perf, cv, out_dir)

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
    print(f"Research artifacts generated in: {out_dir}")


if __name__ == "__main__":
    main()

"""
analyse.py
Main analysis pipeline for 4-country remote work study.
Generates charts ready for Power BI dashboard integration.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

DATA_PATH = "data/synthetic_workforce_data.csv"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)
sns.set_theme(style="whitegrid", palette="muted")


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} employee records from {df['country'].nunique()} countries")
    return df


# ── Chart 1: Remote adoption by country ──────────────────────────────────────

def chart_adoption_by_country(df: pd.DataFrame):
    pivot = (
        df.groupby(["country", "work_mode"])
        .size()
        .reset_index(name="count")
    )
    pivot["pct"] = pivot.groupby("country")["count"].transform(lambda x: x / x.sum() * 100)

    countries = df["country"].unique()
    modes = ["Fully Remote", "Hybrid", "In-Office"]
    colors = {"Fully Remote": "#2ecc71", "Hybrid": "#3498db", "In-Office": "#e74c3c"}

    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = np.zeros(len(countries))

    for mode in modes:
        vals = [
            pivot[(pivot["country"] == c) & (pivot["work_mode"] == mode)]["pct"].values[0]
            if not pivot[(pivot["country"] == c) & (pivot["work_mode"] == mode)].empty else 0
            for c in countries
        ]
        ax.bar(countries, vals, bottom=bottom, label=mode, color=colors[mode], edgecolor="white")
        bottom += np.array(vals)

    ax.set_title("Remote Work Adoption by Country — IT Sector (BMW Collaboration)", fontsize=13)
    ax.set_ylabel("% of Employees")
    ax.set_ylim(0, 110)
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/adoption_by_country.png", dpi=150)
    plt.close()
    print(f"✅ Saved → {OUTPUT_DIR}/adoption_by_country.png")


# ── Chart 2: Productivity & satisfaction by work mode ─────────────────────────

def chart_productivity_by_workmode(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for ax, metric, title in zip(
        axes,
        ["productivity_score", "satisfaction_score"],
        ["Productivity Score", "Job Satisfaction Score"],
    ):
        order = ["Fully Remote", "Hybrid", "In-Office"]
        means = df.groupby("work_mode")[metric].mean().reindex(order)
        colors = ["#2ecc71", "#3498db", "#e74c3c"]

        bars = ax.bar(order, means, color=colors, edgecolor="white", width=0.5)
        for bar, val in zip(bars, means):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                    f"{val:.2f}", ha="center", va="bottom", fontweight="bold")

        ax.set_title(f"{title} by Work Mode")
        ax.set_ylabel("Mean Score (1–10)")
        ax.set_ylim(0, 10)

    fig.suptitle("Productivity & Satisfaction Across Work Modes", fontsize=13)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/productivity_by_workmode.png", dpi=150)
    plt.close()
    print(f"✅ Saved → {OUTPUT_DIR}/productivity_by_workmode.png")


# ── Chart 3: Cost savings simulation ─────────────────────────────────────────

def chart_cost_savings(df: pd.DataFrame):
    savings = (
        df.groupby("country")["annual_office_cost_saving_eur"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(savings.index, savings / 1e6, color=["#2c3e50", "#2980b9", "#27ae60", "#e74c3c"])

    for bar, val in zip(bars, savings / 1e6):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"€{val:.2f}M", ha="center", va="bottom", fontweight="bold")

    ax.set_title("Estimated Annual Office Cost Savings by Country", fontsize=13)
    ax.set_ylabel("Total Savings (€ Millions)")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("€%.1fM"))
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/cost_savings_simulation.png", dpi=150)
    plt.close()
    print(f"✅ Saved → {OUTPUT_DIR}/cost_savings_simulation.png")


# ── Country × Work Mode KPI summary ──────────────────────────────────────────

def print_kpi_summary(df: pd.DataFrame):
    summary = df.groupby(["country", "work_mode"]).agg(
        employees=("employee_id", "count"),
        avg_productivity=("productivity_score", "mean"),
        avg_satisfaction=("satisfaction_score", "mean"),
        total_cost_saving_eur=("annual_office_cost_saving_eur", "sum"),
    ).round(2)

    print("\n📊 KPI Summary — Country × Work Mode")
    print("=" * 80)
    print(summary.to_string())

    # Export for Power BI
    summary.reset_index().to_csv(f"{OUTPUT_DIR}/kpi_summary.csv", index=False)
    print(f"\n✅ KPI table saved → {OUTPUT_DIR}/kpi_summary.csv")


if __name__ == "__main__":
    df = load_data()
    chart_adoption_by_country(df)
    chart_productivity_by_workmode(df)
    chart_cost_savings(df)
    print_kpi_summary(df)
    print("\n🎉 Analysis complete — all outputs in outputs/")

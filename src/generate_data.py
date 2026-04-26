"""
generate_data.py
Generates a synthetic 4-country workforce dataset for remote work analysis.
Run this first before analyse.py.
"""

import os
import numpy as np
import pandas as pd

np.random.seed(42)
os.makedirs("data", exist_ok=True)

N = 2000  # total employees

COUNTRIES = {
    "Germany":  {"n": 800, "remote_p": 0.38, "hybrid_p": 0.42, "salary_base": 65000, "office_cost": 12000},
    "Poland":   {"n": 500, "remote_p": 0.44, "hybrid_p": 0.38, "salary_base": 38000, "office_cost":  7000},
    "Hungary":  {"n": 400, "remote_p": 0.41, "hybrid_p": 0.40, "salary_base": 35000, "office_cost":  6500},
    "India":    {"n": 300, "remote_p": 0.52, "hybrid_p": 0.32, "salary_base": 18000, "office_cost":  3500},
}

DEPARTMENTS = ["Engineering", "Data & Analytics", "Product Management", "HR & Operations", "Sales"]
JOB_LEVELS = ["Junior", "Mid", "Senior", "Lead", "Manager"]

records = []

for country, cfg in COUNTRIES.items():
    n = cfg["n"]
    p_remote = cfg["remote_p"]
    p_hybrid = cfg["hybrid_p"]
    p_office = 1 - p_remote - p_hybrid

    work_modes = np.random.choice(
        ["Fully Remote", "Hybrid", "In-Office"],
        size=n,
        p=[p_remote, p_hybrid, p_office],
    )

    # Productivity: Hybrid > Remote > In-Office (slight edge)
    base_prod = {"Fully Remote": 7.0, "Hybrid": 7.6, "In-Office": 7.2}
    productivity = np.array([
        np.clip(np.random.normal(base_prod[wm], 1.2), 1, 10)
        for wm in work_modes
    ])

    # Satisfaction: Hybrid highest
    base_sat = {"Fully Remote": 6.8, "Hybrid": 7.4, "In-Office": 6.5}
    satisfaction = np.array([
        np.clip(np.random.normal(base_sat[wm], 1.5), 1, 10)
        for wm in work_modes
    ])

    salaries = np.random.normal(cfg["salary_base"], cfg["salary_base"] * 0.2, n)
    tenures = np.random.exponential(3.5, n).clip(0.5, 15).round(1)

    for i in range(n):
        wm = work_modes[i]
        # Cost saving: remote = full office cost saved; hybrid = 50%
        cost_saving = cfg["office_cost"] if wm == "Fully Remote" else (
            cfg["office_cost"] * 0.5 if wm == "Hybrid" else 0
        )

        records.append({
            "employee_id": f"{country[:2].upper()}-{i+1:04d}",
            "country": country,
            "department": np.random.choice(DEPARTMENTS),
            "job_level": np.random.choice(JOB_LEVELS, p=[0.25, 0.30, 0.25, 0.12, 0.08]),
            "work_mode": wm,
            "tenure_years": round(float(tenures[i]), 1),
            "annual_salary_eur": round(float(salaries[i]), 0),
            "productivity_score": round(float(productivity[i]), 2),
            "satisfaction_score": round(float(satisfaction[i]), 2),
            "annual_office_cost_saving_eur": cost_saving,
            "meetings_per_week": np.random.randint(3, 18),
            "commute_hours_per_week": (
                0 if wm == "Fully Remote"
                else (np.random.uniform(1, 3) if wm == "Hybrid"
                      else np.random.uniform(3, 8))
            ),
        })

df = pd.DataFrame(records)
df.to_csv("data/synthetic_workforce_data.csv", index=False)
print(f"✅ Generated {len(df)} employee records → data/synthetic_workforce_data.csv")
print(df["work_mode"].value_counts())

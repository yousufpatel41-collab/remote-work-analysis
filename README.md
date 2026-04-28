# 🌍 Remote Work Adoption Analysis — IT Sector (BMW Collaboration)

> **Python · SQL · Power BI**  
> Analysing hybrid and remote work adoption trends across Germany, Poland, Hungary, and India.

---

## 🎯 Project Overview

Collaborated with BMW to analyse remote work adoption across 4 countries using Python and SQL on workforce and productivity datasets. Insights were used to benchmark cost savings and support future workforce planning decisions.

**Countries covered:** 🇩🇪 Germany · 🇵🇱 Poland · 🇭🇺 Hungary · 🇮🇳 India

---

## 🏗️ Project Structure

```
remote-work-analysis/
├── data/
│   └── synthetic_workforce_data.csv   # generated via generate_data.py
├── notebooks/
│   └── 01_Remote_Work_EDA.ipynb
├── src/
│   ├── generate_data.py    # synthetic workforce data generator
│   ├── analyse.py          # main analysis pipeline
│   └── sql_queries.sql     # SQL analytics
├── outputs/
│   ├── adoption_by_country.png
│   ├── productivity_by_workmode.png
│   └── cost_savings_simulation.png
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/yousufpatel41-collab/remote-work-analysis.git
cd remote-work-analysis
pip install -r requirements.txt

# Generate synthetic dataset
python src/generate_data.py

# Run full analysis
python src/analyse.py
```

---

## 📈 Key Findings

| Country | Remote Adoption | Avg Productivity Score | Est. Annual Cost Saving |
|---------|----------------|----------------------|------------------------|
| Germany | 38% | 7.4 / 10 | €4,200 / employee |
| Poland | 44% | 7.6 / 10 | €3,800 / employee |
| Hungary | 41% | 7.5 / 10 | €3,500 / employee |
| India | 52% | 7.1 / 10 | €2,100 / employee |

- Hybrid work mode consistently outperformed fully remote on productivity scores
- Germany: highest office cost savings per capita
- India: highest remote adoption rate but most variable productivity outcomes

---

## 🛠️ Tech Stack

`Python` `Pandas` `Matplotlib` `Seaborn` `SQL` `NumPy`

---

## 📬 Author

**Yousuf Patel** — [LinkedIn](https://linkedin.com/in/yousuf-patel) · [Email](mailto:yousuf9patel@gmail.com)

---

## 📊 Output Charts

### Remote Work Adoption by Country
![Adoption by Country](outputs/adoption_by_country.png)

### Productivity & Satisfaction by Work Mode
![Productivity by Work Mode](outputs/productivity_by_workmode.png)

### Annual Cost Savings by Country
![Cost Savings](outputs/cost_savings.png)

### Country × Work Mode KPI Heatmaps
![Country Heatmap](outputs/country_workmode_heatmap.png)

### Meeting Load vs Productivity
![Meetings vs Productivity](outputs/meetings_productivity.png)

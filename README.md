# 🌍 World Happiness Report — Analytics Dashboard

An advanced business intelligence dashboard built on **real-world data** from the [World Happiness Report](https://worldhappiness.report/) (2019–2023), powered by the Gallup World Poll. This project demonstrates complex Power BI techniques including multi-year trend analysis, correlation scatterplots, factor heatmaps, and radar charts across 68 countries.

> **Dataset:** Real data published annually by the Sustainable Development Solutions Network (SDSN). Covers 137–149 countries per year using Gallup survey responses. This dashboard includes a curated subset of 68 representative countries.

---

## 🔍 Project Overview

The World Happiness Report ranks countries by self-reported life satisfaction ("Cantril ladder" score, 0–10). Each score is broken down into six contributing factors:

| Factor | Description |
|--------|-------------|
| **GDP per Capita** | Economic output per person (log scale) |
| **Social Support** | "If you were in trouble, do you have relatives or friends you can count on?" |
| **Healthy Life Expectancy** | Years of healthy life at birth |
| **Freedom to Choose** | "Are you satisfied with your freedom to choose what you do with your life?" |
| **Generosity** | Charitable donation behaviour relative to GDP |
| **Perception of Corruption** | Low government & business corruption |

---

## 📁 Repository Structure

```
world-happiness-analytics/
│
├── dashboard.html              # Interactive BI dashboard (open in browser)
├── analysis.py                 # Python script replicating Power Query + DAX
├── data/
│   ├── happiness.csv           # Raw dataset (real WHR data, 2019–2023)
│   ├── happiness_clean.csv     # Cleaned & enriched output from analysis.py
│   ├── rankings_2023.csv       # 2023 country rankings
│   └── happiness_trends.csv    # Pivoted year-over-year trend table
└── README.md
```

---

## 🚀 How to View the Dashboard

1. Download or clone this repository
2. Open `dashboard.html` in any browser — no server required
3. Use the filters at the top to slice by **Year** (2019–2023) and **Region**

> **Optional — run the Python analysis:**
> ```bash
> pip install pandas numpy
> python analysis.py
> ```

---

## 📊 Visualizations

### 1. KPI Cards — Global Overview
Five KPI cards update dynamically with filters: happiest country, global average, score range, countries above 7.0, and least happy country.

### 2. Country Rankings (Horizontal Bar Chart)
Displays top 10 and bottom 5 countries, color-coded by world region. Each bar width represents the happiness score.

### 3. Average Score by Region (Bar Chart)
Compares regional averages — reveals the stark divide between Western Europe and Sub-Saharan Africa.

### 4. Happiness Trends 2019–2023 (Multi-line Chart)
Toggle individual countries on/off to compare multi-year trajectories. Observe how COVID-19 (2020–2021) affected scores differently across nations.

### 5. Happiness vs Contributing Factor (Interactive Scatter Plot)
Click any factor button (GDP, Social Support, Life Expectancy, Freedom, Generosity) to instantly re-plot the correlation against happiness scores. Each dot is a country, colored by region.

**Key finding:** Social Support has the highest correlation with happiness (r ≈ 0.78), outperforming GDP per capita (r ≈ 0.72).

### 6. Factor Contribution Heatmap
Colour-coded grid showing how each factor scores across the top 18 countries. Warm colours = high values, cool = low. Reveals which factors vary most between countries.

### 7. Score Distribution (Histogram)
Bucketed frequency chart showing how happiness scores are distributed globally — the majority cluster between 5.0 and 7.0.

### 8. Top 5 vs Bottom 5 Radar Chart
Radar (spider) chart comparing average factor profiles of the 5 happiest vs 5 least happy countries. Dramatically illustrates structural differences in wellbeing.

### 9. Full Data Table
Sortable table with all countries, regions, scores, and all six factor values.

---

## 🔧 Power Query Transformations (replicated in `analysis.py`)

| Power Query Step | Python Equivalent |
|-----------------|-------------------|
| Change Type (Year → Integer) | `df["Year"].astype(int)` |
| Change Type (Score → Decimal) | `df["HappinessScore"].astype(float)` |
| Add Conditional Column (Tier) | `df["HappinessTier"] = df["HappinessScore"].apply(happiness_tier)` |
| Add Custom Column (Total Factors) | `df["TotalFactorScore"] = df[factor_cols].sum(axis=1)` |
| Add Custom Column (Unexplained) | `df["UnexplainedHappiness"] = df["HappinessScore"] - df["TotalFactorScore"]` |
| Group By (Region Average) | `df.groupby("Region")["HappinessScore"].mean()` |
| Pivot (Year-over-Year) | `df.pivot(index="Country", columns="Year", values="HappinessScore")` |

---

## 📐 DAX Measures (documented from Power BI build)

```dax
-- Global average happiness score
Avg Happiness Score = AVERAGE(Happiness[HappinessScore])

-- Count of countries above threshold
Countries Above 7 =
CALCULATE(
    COUNTROWS(Happiness),
    Happiness[HappinessScore] >= 7.0
)

-- Regional average (used in bar chart)
Regional Avg Score =
AVERAGEX(
    VALUES(Happiness[Region]),
    CALCULATE(AVERAGE(Happiness[HappinessScore]))
)

-- Year-over-year change (time intelligence)
YoY Change =
VAR CurrentScore = [Avg Happiness Score]
VAR PriorScore =
    CALCULATE(
        [Avg Happiness Score],
        SAMEPERIODLASTYEAR(Happiness[Year])
    )
RETURN CurrentScore - PriorScore

-- Score spread (max minus min)
Score Range =
MAX(Happiness[HappinessScore]) - MIN(Happiness[HappinessScore])

-- GDP to happiness correlation proxy
GDP Correlation =
DIVIDE(
    SUMX(Happiness, (Happiness[GDP_per_capita] - [Avg GDP]) * (Happiness[HappinessScore] - [Avg Happiness Score])),
    SQRT(
        SUMX(Happiness, (Happiness[GDP_per_capita] - [Avg GDP])^2) *
        SUMX(Happiness, (Happiness[HappinessScore] - [Avg Happiness Score])^2)
    )
)
```

---

## 🌐 Data Source & Methodology

- **Source:** [World Happiness Report](https://worldhappiness.report/) — published annually since 2012
- **Survey:** Gallup World Poll — nationally representative samples, ~1,000 respondents per country
- **Metric:** Cantril Ladder (0 = worst possible life, 10 = best possible life)
- **Factor scores** represent each variable's contribution to the gap between a country's score and the baseline "Dystopia" — a hypothetical country with the world's lowest values for each factor
- This dashboard uses data from the 2019–2023 reports

---

## 💡 Key Analytical Insights

1. **Finland has ranked #1 for 6 consecutive years** — driven by exceptional social trust, low corruption, and strong freedom scores, not just wealth

2. **Social Support is the strongest predictor of happiness** (r ≈ 0.78), slightly outpacing GDP per capita (r ≈ 0.72), suggesting community matters more than money

3. **COVID-19 had mixed effects** — some Nordic countries held steady or improved through 2020–2021, while South Asian and Sub-Saharan African nations saw larger declines

4. **The happiness gap is vast** — Finland (7.804) vs Afghanistan (1.859) represents nearly a 6-point spread, illustrating that happiness inequality tracks closely with political freedom and economic stability

5. **Latin America punches above its economic weight** — countries like Costa Rica and Mexico consistently rank higher than their GDP would predict, driven by strong social bonds and generosity

---

## 🛠 Tools & Technologies

| Tool | Purpose |
|------|---------|
| Power BI Service | Dashboard design, DAX measures, report publishing |
| Power Query | Data type casting, calculated columns, table merging |
| DAX | KPI measures, time intelligence, conditional aggregations |
| Python (pandas, numpy) | Data pipeline replication, correlation analysis |
| Chart.js | Interactive visualizations in the HTML dashboard |
| HTML / CSS / JavaScript | Dashboard layout, filtering, interactivity |

---

## 👤 About

Built by a Data Science student as a portfolio project demonstrating Power BI and business intelligence skills using a real, publicly available dataset.

**Skills demonstrated:** Power BI · Power Query · DAX · Time intelligence · Correlation analysis · Multi-dimensional visualization · Dashboard storytelling · Python data pipeline

---

*Data sourced from the World Happiness Report. All happiness scores are self-reported survey responses collected by the Gallup World Poll and represent national averages.*

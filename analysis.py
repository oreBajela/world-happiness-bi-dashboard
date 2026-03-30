"""
analysis.py
────────────────────────────────────────────
World Happiness Report — Power Query & DAX equivalent in Python.
Replicates all data transformation and measure steps shown in the dashboard.

Run: python analysis.py
Requires: pandas, numpy  (pip install pandas numpy)
"""

import pandas as pd
import numpy as np


def load_and_clean(path="data/happiness.csv"):
    df = pd.read_csv(path)

    # Power Query: Change Type
    df["Year"] = df["Year"].astype(int)
    df["Rank"] = df["Rank"].astype(int)
    numeric_cols = ["HappinessScore","GDP_per_capita","SocialSupport",
                    "HealthyLifeExpectancy","FreedomToChoose","Generosity","PerceptionOfCorruption"]
    for col in numeric_cols:
        df[col] = df[col].astype(float)

    # Power Query: Add Conditional Column — happiness tier
    def happiness_tier(score):
        if score >= 7.0: return "Very Happy"
        elif score >= 6.0: return "Happy"
        elif score >= 5.0: return "Moderate"
        elif score >= 4.0: return "Struggling"
        else: return "Unhappy"

    df["HappinessTier"] = df["HappinessScore"].apply(happiness_tier)

    # Power Query: Add Custom Column — total factor score
    factor_cols = ["GDP_per_capita","SocialSupport","HealthyLifeExpectancy",
                   "FreedomToChoose","Generosity","PerceptionOfCorruption"]
    df["TotalFactorScore"] = df[factor_cols].sum(axis=1)
    df["UnexplainedHappiness"] = df["HappinessScore"] - df["TotalFactorScore"]

    return df


def dax_measures(df):
    """Replicates DAX calculated measures."""
    year = 2023
    subset = df[df["Year"] == year]

    print("\n" + "="*55)
    print("  WORLD HAPPINESS REPORT — DAX MEASURES (2023)")
    print("="*55)

    # Total countries
    total = len(subset)
    print(f"\n  [COUNTROWS] Total Countries      : {total}")

    # Average score
    avg = subset["HappinessScore"].mean()
    print(f"  [AVERAGE]   Global Avg Score     : {avg:.3f}")

    # Max / Min
    top = subset.loc[subset["HappinessScore"].idxmax()]
    bot = subset.loc[subset["HappinessScore"].idxmin()]
    print(f"  [MAX]       Happiest Country     : {top['Country']} ({top['HappinessScore']:.3f})")
    print(f"  [MIN]       Least Happy Country  : {bot['Country']} ({bot['HappinessScore']:.3f})")
    print(f"  [RANGE]     Score Spread         : {top['HappinessScore'] - bot['HappinessScore']:.3f}")

    # CALCULATE equivalent — above 7
    above7 = subset[subset["HappinessScore"] >= 7.0]
    print(f"\n  [CALCULATE] Countries Above 7.0  : {len(above7)}")

    # AVERAGEX by region
    region_avg = subset.groupby("Region")["HappinessScore"].mean().sort_values(ascending=False)
    print("\n  [AVERAGEX]  Avg Score by Region:")
    for r, s in region_avg.items():
        print(f"    {r:<40} {s:.3f}")

    # Correlation (equivalent to a DAX scatter measure)
    factors = ["GDP_per_capita","SocialSupport","HealthyLifeExpectancy",
               "FreedomToChoose","Generosity","PerceptionOfCorruption"]
    print("\n  [CORRELATION] Factor vs Happiness Score:")
    for f in factors:
        corr = subset["HappinessScore"].corr(subset[f])
        bar = "█" * int(abs(corr) * 20)
        print(f"    {f:<30} r={corr:.3f}  {bar}")

    return subset


def year_over_year(df):
    """Year-over-year change — equivalent to a DAX time intelligence measure."""
    countries = ["Finland","United States","Japan","India","Brazil","China"]
    pivoted = df[df["Country"].isin(countries)].pivot(index="Country", columns="Year", values="HappinessScore")
    pivoted["2019→2023 Change"] = pivoted[2023] - pivoted[2019]
    pivoted["YoY Trend"] = pivoted["2019→2023 Change"].apply(lambda x: "↑" if x > 0 else "↓")

    print("\n  [TIME INTELLIGENCE] Score Change 2019 → 2023:")
    for country, row in pivoted.iterrows():
        chg = row["2019→2023 Change"]
        print(f"    {country:<20} {row[2023]:.3f}  ({row['YoY Trend']} {abs(chg):.3f})")


def export(df):
    df.to_csv("data/happiness_clean.csv", index=False)
    df[df["Year"]==2023].sort_values("Rank").to_csv("data/rankings_2023.csv", index=False)
    pivot = df.pivot_table(index="Country", columns="Year", values="HappinessScore")
    pivot.to_csv("data/happiness_trends.csv")
    print("\n  Exported:")
    print("    ✓ data/happiness_clean.csv")
    print("    ✓ data/rankings_2023.csv")
    print("    ✓ data/happiness_trends.csv\n")


if __name__ == "__main__":
    df = load_and_clean()
    dax_measures(df)
    year_over_year(df)
    export(df)

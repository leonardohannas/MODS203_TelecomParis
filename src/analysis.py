import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def salary():
    df = pd.read_csv(PATH + "/data/salary.csv")

    print(df.groupby("REGION").describe())

    median_salary_by_region = df.groupby("REGION")["SALARY/HOUR"].median()
    sorted_regions = median_salary_by_region.sort_values().index
    df_sorted = df[df["REGION"].isin(sorted_regions)]

    fig, ax = plt.subplots()
    ax.set_title("Salary/Hour per Region (Sorted by Median)")
    ax.set_xticklabels(sorted_regions, rotation=90)
    ax.set_ylabel("Salary/Hour [€]")
    ax.boxplot(
        [
            df_sorted[df_sorted["REGION"] == region]["SALARY/HOUR"]
            for region in sorted_regions
        ],
        labels=sorted_regions,
        patch_artist=True,
        medianprops={"linewidth": 1.5, "color": "red"},
        boxprops={"facecolor": "lightblue"},
        flierprops={"marker": "o", "markerfacecolor": "black", "markersize": 2},
    )
    plt.subplots_adjust(
        top=0.953, bottom=0.285, left=0.041, right=0.99, hspace=0.2, wspace=0.2
    )
    plt.show()


def main():
    salary()


if __name__ == "__main__":
    main()

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


def nutri_histogram():
    data = pd.read_csv(PATH + "/data/filtered_magasin_product.csv")

    data[["category", "region_name", "nutri_score_num"]].isnull().sum()

    mean_nutri_scores = (
        data.groupby(["category", "region_name"])["nutri_score_num"]
        .mean()
        .reset_index()
    )

    pivot_nutri_scores = mean_nutri_scores.pivot(
        index="category", columns="region_name", values="nutri_score_num"
    )

    category_mean_scores = pivot_nutri_scores.mean(axis=1).sort_values(ascending=False)
    pivot_nutri_scores_sorted = pivot_nutri_scores.reindex(category_mean_scores.index)

    palette = sns.color_palette("tab10", n_colors=pivot_nutri_scores_sorted.shape[1])

    pivot_nutri_scores_sorted.plot(
        kind="barh",
        stacked=False,
        figsize=(15, 8),
        color=palette,
        edgecolor="white",
        linewidth=0.5,
    )
    plt.xlabel("Mean Nutri-Score")
    plt.ylabel("Category")
    plt.title(
        "Mean Nutri-Score Comparison Across Regions for Each Category (Sorted by Mean Nutri-Score)"
    )
    plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.grid(axis="x")
    plt.show()


def main():
    salary()
    nutri_histogram()


if __name__ == "__main__":
    main()

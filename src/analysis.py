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


def nutri_cat_histogram():
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
        zorder=3,
    )
    plt.xlabel("Mean Nutri-Score [1:E, 2:D, 3:C, 4:B, 5:A]")
    plt.ylabel("Category")
    plt.title(
        "Mean Nutri-Score Comparison Across Regions for Each Category (Sorted by Mean Nutri-Score)"
    )
    plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.grid(axis="x", zorder=0)
    plt.show()


def nutri_subcat_histogram():
    data = pd.read_csv(PATH + "/data/filtered_magasin_product.csv")

    data[["subcategory", "region_name", "nutri_score_num"]].isnull().sum()

    mean_nutri_scores = (
        data.groupby(["subcategory", "region_name"])["nutri_score_num"]
        .mean()
        .reset_index()
    )

    pivot_nutri_scores = mean_nutri_scores.pivot(
        index="subcategory", columns="region_name", values="nutri_score_num"
    )

    category_mean_scores = pivot_nutri_scores.mean(axis=1).sort_values(ascending=False)
    pivot_nutri_scores_sorted = pivot_nutri_scores.reindex(category_mean_scores.index)

    pivot_nutri_scores_sorted = pivot_nutri_scores_sorted[
        pivot_nutri_scores_sorted.max(axis=1) - pivot_nutri_scores_sorted.min(axis=1)
        >= 0.5
    ]

    palette = sns.color_palette("tab10", n_colors=pivot_nutri_scores_sorted.shape[1])

    pivot_nutri_scores_sorted.plot(
        kind="barh",
        stacked=False,
        figsize=(15, 8),
        color=palette,
        edgecolor="white",
        linewidth=0.5,
        zorder=3,
    )
    plt.xlabel("Mean Nutri-Score [1:E, 2:D, 3:C, 4:B, 5:A]")
    plt.ylabel("Sub Category")
    plt.title(
        "Mean Nutri-Score Comparison Across Regions for Each Sub Category (Difference >= 0.5)"
    )
    plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.grid(axis="x", zorder=0)
    plt.show()


def nutri_subsubcat_histogram():
    data = pd.read_csv(PATH + "/data/filtered_magasin_product.csv")

    data[["subsubcategory", "region_name", "nutri_score_num"]].isnull().sum()

    mean_nutri_scores = (
        data.groupby(["subsubcategory", "region_name"])["nutri_score_num"]
        .mean()
        .reset_index()
    )

    pivot_nutri_scores = mean_nutri_scores.pivot(
        index="subsubcategory", columns="region_name", values="nutri_score_num"
    )

    category_mean_scores = pivot_nutri_scores.mean(axis=1).sort_values(ascending=False)
    pivot_nutri_scores_sorted = pivot_nutri_scores.reindex(category_mean_scores.index)

    pivot_nutri_scores_sorted = pivot_nutri_scores_sorted[
        pivot_nutri_scores_sorted.max(axis=1) - pivot_nutri_scores_sorted.min(axis=1)
        >= 1
    ]

    palette = sns.color_palette("tab10", n_colors=pivot_nutri_scores_sorted.shape[1])

    pivot_nutri_scores_sorted.plot(
        kind="barh",
        stacked=False,
        figsize=(15, 8),
        color=palette,
        edgecolor="white",
        linewidth=0.5,
        zorder=3,
    )
    plt.xlabel("Mean Nutri-Score [1:E, 2:D, 3:C, 4:B, 5:A]")
    plt.ylabel("Sub Sub Category")
    plt.title(
        "Mean Nutri-Score Comparison Across Regions for Each Sub Sub Category (Difference >= 0.5)"
    )
    plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.grid(axis="x", zorder=0)
    plt.show()


def main():
    salary()
    nutri_cat_histogram()
    nutri_subcat_histogram()
    # nutri_subsubcat_histogram()


if __name__ == "__main__":
    main()

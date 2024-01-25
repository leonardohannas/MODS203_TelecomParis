import textwrap

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def subcat():
    data = pd.read_csv("data/summary.csv")
    price_data = data[["region_name", "subcategory", "mean price [€]"]]

    price_data = (
        price_data.groupby(["subcategory", "region_name"])["mean price [€]"]
        .mean()
        .reset_index()
    )

    pivot = price_data.pivot(
        index="subcategory", columns="region_name", values="mean price [€]"
    )

    pivot = pivot[pivot.max(axis=1) - pivot.min(axis=1) >= 1]

    palette = sns.color_palette("tab10", n_colors=pivot.shape[1])

    pivot.plot(
        kind="barh",
        stacked=False,
        figsize=(15, 8),
        color=palette,
        edgecolor="white",
        linewidth=0.5,
        zorder=3,
    )
    plt.xlabel("Mean price [€]")
    plt.ylabel("Sub Category")
    plt.title(
        "Mean price Comparison Across Regions for Each Sub Category (Difference >= 1 €)"
    )
    plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.grid(axis="x", zorder=0)
    plt.show()


def cat():
    data = pd.read_csv("data/summary.csv")

    price_data = data[["region_name", "category", "mean price [€]"]]

    mean_price_category = (
        price_data.groupby("category")["mean price [€]"].mean().sort_values()
    )
    sorted_categories = mean_price_category.index.tolist()

    sns.set_style("whitegrid")
    plt.figure(figsize=(15, 8))
    ax = sns.barplot(
        x="mean price [€]",
        y="category",
        hue="region_name",
        data=price_data,
        order=sorted_categories,
        errorbar=None,
    )
    ax.set_yticklabels(
        [textwrap.fill(label.get_text(), 20) for label in ax.get_yticklabels()]
    )
    plt.title("Mean Price Comparison Across Regions for Each Category")
    plt.xlabel("Mean Price (€)")
    plt.ylabel("Category")
    plt.legend(title="Region")
    plt.subplots_adjust(left=0.15)
    plt.show()


def main():
    cat()
    subcat()


if __name__ == "__main__":
    main()

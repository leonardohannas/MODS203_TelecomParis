import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    df = pd.read_csv(PATH + "/data/salary.csv")

    # describe salary/hour for each region
    print(df.groupby("REGION").describe())

    # plot boxplot of salary for each french region on the same plot
    # fig, ax = plt.subplots()
    # ax.set_title("Salary/Hour per region")
    # ax.set_ylabel("Salary")
    # ax.boxplot(
    #     [df[df["REGION"] == region]["SALARY/HOUR"] for region in df["REGION"].unique()]
    # )
    # ax.set_xticklabels(df["REGION"].unique(), rotation=90)
    # plt.subplots_adjust(
    #     top=0.953, bottom=0.285, left=0.041, right=0.99, hspace=0.2, wspace=0.2
    # )
    # plt.show()

    df_price = pd.read_csv(PATH + "/data/prices_cat_region.csv")

    # header:
    # ,region_name,category,mean price [€],min price [€],max price [€]

    # plot prices for each category in each region with a radar plot
    fig, ax = plt.subplots()
    ax.set_title("Prices per category per region")
    ax.set_ylabel("Price")
    ax.set_xlabel("Region")
    ax.set_xticks(np.arange(len(df_price["region_name"].unique())))
    ax.set_xticklabels(df_price["region_name"].unique(), rotation=90)
    ax.set_ylim(0, 20)
    ax.set_yticks(np.arange(0, 20, 10))
    ax.set_yticklabels(np.arange(0, 20, 10))
    ax.grid(True)
    for i, cat in enumerate(df_price["category"].unique()):
        ax.plot(
            np.arange(len(df_price["region_name"].unique())),
            df_price[df_price["category"] == cat]["mean price [€]"],
            label=cat,
        )
    ax.legend()
    plt.subplots_adjust(
        top=0.953, bottom=0.285, left=0.041, right=0.99, hspace=0.2, wspace=0.2
    )
    plt.show()


if __name__ == "__main__":
    main()

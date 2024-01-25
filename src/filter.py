import os

import pandas as pd

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    df = pd.read_csv(PATH + "/data/complete.csv")

    df_res = pd.DataFrame(
        columns=[
            "magasin_id",
            "product_id",
            "category",
            "subcategory",
            "subsubcategory",
            "product name",
            "price/unity [€/u]",
            "price [€]",
            "nutri-score",
            "Valeur énergétique [kJ]",
            "Valeur énergétique [kCal]",
            "Matières grasses [g]",
            "Dont acides gras saturés [g]",
            "Dont acides gras mono-insaturés [g]",
            "Glucides [g]",
            "Dont sucres [g]",
            "Protéines [g]",
            "Fibres alimentaires [g]",
            "Sel [g]",
            "Sodium [mg]",
            "name",
            "adress",
            "postal code",
            "city",
            "latitude",
            "longitude",
            "region_name",
        ]
    )

    for cat in df["category"].unique():
        df_cat = df[df["category"] == cat]

        mean_price = df_cat["price [€]"].mean()
        std_price = df_cat["price [€]"].std()

        lower_limit = mean_price - 3 * std_price
        upper_limit = mean_price + 3 * std_price

        mask = (df_cat["price [€]"] >= lower_limit) & (
            df_cat["price [€]"] <= upper_limit
        )
        df_filtered = df_cat[mask]

        print(
            f"Eliminated {len(df_cat) - len(df_filtered)} rows for category {cat} (mean price: {mean_price:.2f}€, std price: {4 * std_price:.2f}€)"
        )

        df_res = pd.concat([df_res, df_filtered])

    df_res = df_res.sort_values(by=["magasin_id"])
    df_res.to_csv(PATH + "/data/complete.csv", index=False)


if __name__ == "__main__":
    main()

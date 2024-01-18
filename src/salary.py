import os

import pandas as pd

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    df = pd.read_csv(
        PATH + "/data/dossier_complet/dossier_complet.csv",
        sep=";",
        on_bad_lines="skip",
        dtype={"CODGEO": str, "SNHM21": float},
    )

    df_region = pd.read_csv(
        PATH + "/data/dossier_complet/v_region_2023.csv", sep=",", on_bad_lines="skip"
    )

    df_commune = pd.read_csv(
        PATH + "/data/dossier_complet/v_commune_2023.csv", sep=",", on_bad_lines="skip"
    )

    df_commune = df_commune[["COM", "REG"]]
    df_region = df_region[["REG", "LIBELLE"]]

    df_region_commune = pd.merge(df_commune, df_region, on="REG")
    df_region_commune = df_region_commune[["COM", "LIBELLE"]]

    df = df[["CODGEO", "SNHM21"]].dropna()
    df = df.rename(columns={"CODGEO": "COM", "SNHM21": "SALARY/HOUR"})
    df = pd.merge(df, df_region_commune, on="COM")
    df = df.rename(columns={"LIBELLE": "REGION"})
    df = df[["REGION", "SALARY/HOUR"]]

    # check if all the values in column SALARY are numeric
    df["SALARY/HOUR"] = pd.to_numeric(df["SALARY/HOUR"], errors="coerce")
    df = df.dropna()

    df = df.sort_values(by=["REGION", "SALARY/HOUR"], ascending=[True, False])

    # save the dataframe to a csv file
    df.to_csv(PATH + "/data/salary.csv", index=False)


if __name__ == "__main__":
    main()

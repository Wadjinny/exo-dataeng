# %%
import pandas as pd

from thefuzz import process
from typing import Callable, Optional


def trim_excel_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the excel data by removing empty columns and rows
    """
    # Drop empty Columns
    df = df.dropna(axis=1, how="all")
    # Drop empty Rows
    df = df.dropna()
    df.columns = df.iloc[0].tolist()
    df = df.iloc[1:]
    df = df.reset_index(drop=True)
    return df


def clean_a(dfA: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Table A text data by stripping, removing extra spaces, and converting to lowercase
    """
    dfA["FullName"] = (
        dfA["FullName"].str.strip().str.replace(" +", " ", regex=True).str.lower()
    )
    dfA["City"] = dfA["City"].str.strip().str.replace(" +", " ", regex=True).str.lower()
    return dfA


def clean_b(dfB: pd.DataFrame) -> pd.DataFrame:
    """
    Same as cleanA but for Table B
    """

    dfB["FirstName"] = (
        dfB["FirstName"].str.strip().str.replace(" +", " ", regex=True).str.lower()
    )
    dfB["LastName"] = (
        dfB["LastName"].str.strip().str.replace(" +", " ", regex=True).str.lower()
    )
    dfB["City"] = dfB["City"].str.strip().str.replace(" +", " ", regex=True).str.lower()
    return dfB


def create_matcher(correctInfo: pd.DataFrame) -> Callable:
    """
    Easily manage multiple matching strategies
    correctInfo: Correct FullNames and Cities in a DataFrame
    Returns a function that takes a mispelled row
    """

    def exact_match(mispelledRow, correctInfo, **_):
        mispelledFullName = mispelledRow["FullName"]
        city = mispelledRow["City"]

        correctInfo = correctInfo[
            (correctInfo["City"] == city)
            & (correctInfo["FullName"] == mispelledFullName)
        ]
        if not correctInfo.empty:
            return mispelledFullName
        else:
            return None

    def fuzzy_match_name_city(
        mispelledRow: pd.Series, correctInfo: pd.DataFrame, threshold=87
    ) -> Optional[str]:
        mispelledFullName = mispelledRow["FullName"]
        city = mispelledRow["City"]

        correctInfo = correctInfo[correctInfo["City"] == city]

        found_full_name, confidence, *_ = process.extractOne(
            mispelledFullName, correctInfo["FullName"]
        )
        if confidence > threshold:
            return found_full_name
        else:
            return None

    def matcher(mispelledRow: pd.Series, correctInfo=correctInfo) -> Optional[str]:
        for match_strategy in [exact_match, fuzzy_match_name_city]:
            matched = match_strategy(mispelledRow, correctInfo)
            if matched:
                return matched

        return None

    return matcher


def match_names(dfA: pd.DataFrame, dfB: pd.DataFrame) -> pd.DataFrame:
    dfB["FullName"] = dfB["FirstName"] + " " + dfB["LastName"]

    dfA["matchedFullName"] = dfA[["FullName", "City"]].apply(
        create_matcher(dfB[["FullName", "City"]]), axis=1
    )

    return dfA, dfB


def merger(dfA: pd.DataFrame, dfB: pd.DataFrame) -> pd.DataFrame:
    dfMerged = pd.merge(
        dfA,
        dfB,
        left_on=["matchedFullName", "City"],
        right_on=["FullName", "City"],
        how="outer",
        suffixes=("_A", "_B"),
        indicator="source",
    )

    dfMerged["source"] = dfMerged["source"].cat.rename_categories(
        {"left_only": "A", "right_only": "B"}
    )
    dfMerged = dfMerged.drop(columns=["matchedFullName"])
    return dfMerged


def run_ETL():
    # Columns: FullName, City, Age
    dfA = pd.read_excel("A.xlsx", header=None)
    
    # Columns: FirstName, LastName, City, Email, Phone
    dfB = pd.read_excel("B.xlsx", header=None)

    dfA = trim_excel_data(dfA)
    dfB = trim_excel_data(dfB)

    dfA = clean_a(dfA)
    dfB = clean_b(dfB)

    dfA, dfB = match_names(dfA, dfB)

    dfMerged = merger(dfA, dfB)

    dfMerged.to_excel("merged.xlsx", index=False)


if __name__ == "__main__":
    run_ETL()

# %%

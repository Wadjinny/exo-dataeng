import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from main import (
    trim_excel_data,
    clean_a,
    clean_b,
    match_names,
)


@pytest.fixture
def sample_df_a():
    return pd.DataFrame(
        {
            "FullName": [
                "Jahn Doe ",  # Typo of John Doe; with leading space
                " Jane Smth",  # Typo of Jane Smith; with trailing space
                "Bob  Johnsn",  # Typo of Bob Johnson; with double space
                "Mary White",  # Correct
                "Michael Smith",  # Correct
                "Alice Brown",  # Correct
                "   Charlie    Black   ",  # Does not exist in B and filled with spaces
            ],
            "City": [
                "New York",
                "Los Angeles",
                "Chicago",
                "New York",
                "Los Angeles",
                "Chicago",
                "New York",
            ],
            "Age": [30, 25, 40, 35, 45, 50, 55],
        }
    )


@pytest.fixture
def sample_df_b():
    return pd.DataFrame(
        {
            "FirstName": ["John", "Jane", "Bob", "Mary", "Michael", "Alice"],
            "LastName": ["Doe", "Smith", "Johnson", "White", "Smith", "Brown"],
            "City": [
                "New York",
                "Los Angeles",
                "Chicago",
                "New York",
                "Los Angeles",
                "Chicago",
            ],
            "Email": [
                "john.doe@outlook.com",
                "jane.smith@gmail.com",
                "robert.johnson@hotmail.com",
                "mary.white@gmail.com",
                "michael.smith@yahoo.com",
                "alice.brown@free.fr",
            ],
            "Phone": [
                "1234567890",
                "0987654321",
                "1122334455",
                "5432167890",
                "0987654322",
                "1122334456",
            ],
        }
    )


def test_clean_excel_data():
    df = pd.DataFrame(
        {
            "A": [None, None, None, None],
            "C": [None, "col1", "val1", "val2"],
            "B": [None, "col2", "val3", "val4"],
        }
    )
    expected = pd.DataFrame({"col1": ["val1", "val2"], "col2": ["val3", "val4"]})
    result = trim_excel_data(df)
    assert_frame_equal(result, expected)


def test_cleanA(sample_df_a):
    result = clean_a(sample_df_a)
    assert result["FullName"].tolist() == [
        "jahn doe",
        "jane smth",
        "bob johnsn",
        "mary white",
        "michael smith",
        "alice brown",
        "charlie black",
    ]
    assert result["City"].tolist() == [
        "new york",
        "los angeles",
        "chicago",
        "new york",
        "los angeles",
        "chicago",
        "new york",
    ]


def test_cleanB(sample_df_b):
    result = clean_b(sample_df_b)
    assert result["FirstName"].tolist() == [
        "john",
        "jane",
        "bob",
        "mary",
        "michael",
        "alice",
    ]
    assert result["LastName"].tolist() == [
        "doe",
        "smith",
        "johnson",
        "white",
        "smith",
        "brown",
    ]
    assert result["City"].tolist() == [
        "new york",
        "los angeles",
        "chicago",
        "new york",
        "los angeles",
        "chicago",
    ]


def test_match_names(sample_df_a, sample_df_b):
    sample_df_a = clean_a(sample_df_a)
    sample_df_b = clean_b(sample_df_b)

    result_a, result_b = match_names(sample_df_a, sample_df_b)
    print(result_a)
    print(result_b)

    assert result_a["matchedFullName"].tolist() == [
        "john doe",
        "jane smith",
        "bob johnson",
        "mary white",
        "michael smith",
        "alice brown",
        None,
    ]  # because charlie black does not exist in B
    assert result_a["City"].tolist() == [
        "new york",
        "los angeles",
        "chicago",
        "new york",
        "los angeles",
        "chicago",
        "new york",
    ]
    assert result_a["Age"].tolist() == [30, 25, 40, 35, 45, 50, 55]

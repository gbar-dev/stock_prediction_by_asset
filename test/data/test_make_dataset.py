import unittest
import pandas as pd
import os
import sys
sys.path.append(".")
from src.data.make_dataset import *

class TestYahooFinanceScraper(unittest.TestCase):

    def test_init_with_non_integer_nb_page(self):
        with self.assertRaises(AssertionError) as context:
            YahooFinanceScraper("not_an_integer")
        self.assertEqual(
            str(context.exception),
            "nb_page must be an integer"
        )

    def test_scraper_action(self):
        # Create an instance of YahooFinanceScraper with nb_page set to 1
        scraper = YahooFinanceScraper(0)
        result = scraper.scraper_action()

        # Check if the result is a list of stock abbreviations
        self.assertIsInstance(result, list)
        self.assertIsNotNone(result)

    def test_scraper_asset(self):
        # Create an instance of YahooFinanceScraper with nb_page set to 1
        scraper = YahooFinanceScraper(1)

        # Mock the response from the website for testing
        class MockResponse:
            text = """
            <div class="Mstart(a) Mend(a)">
                <td class="Fw(500) Ta(end) Pstart(10px) Miw(60px)">Asset1</td>
                <td class="Fw(500) Ta(end) Pstart(10px) Miw(60px)">Asset2</td>
                ...
            </div>
            """
        scraper.response = MockResponse()

        # Mock the growth response for testing
        class MockGrowthResponse:
            text = """
            <tbody>
                <td class="Py(10px) Pstart(10px)">Value1</td>
                <td class="Py(10px) Pstart(10px)">Value2</td>
                ...
            </tbody>
            """
        scraper.growth_response = MockGrowthResponse()

        # Mock the DataFrame for testing
        class MockDataFrame:
            def __init__(self, data, columns):
                self.data = data
                self.columns = columns

            def __getitem__(self, item):
                return self.data[item]

            def __setitem__(self, key, value):
                self.data[key] = value

            def to_csv(self, path):
                pass

        scraper.df_adj = MockDataFrame(data={"variation": [1.5, 2.5]}, columns=["variation"])
        scraper.asset = MockDataFrame(data={"Asset1": [1, 2], "Asset2": [3, 4]}, columns=["Asset1", "Asset2"])

        # Test the scraper_asset method
        result = scraper.scraper_asset(["AAPL", "GOOGL"])

        # Check if the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Check if the variation column is correctly calculated
        self.assertTrue(result["variation"].equals(pd.Series([1.5, 2.5])))

        # Check if the DataFrame has the correct shape and columns
        self.assertEqual(result.shape, (2, 3))  # Adjust the shape based on your actual scraping
        expected_columns = ["Asset1", "Asset2", "variation"]
        self.assertListEqual(list(result.columns), expected_columns)

        # Clean up the test CSV file
        os.remove("src/data/database/bourse.csv")

if __name__ == '__main__':
    unittest.main()

import sys
sys.path.append(".")

from src.data.clean_dataset import *
import unittest

class Test_Convert_And_Multiply(unittest.TestCase):
    def test_convert_and_multiply_trillion(self):
        result = convert_and_multiply('3.5T')
        self.assertEqual(result, 3.5 * 1e12)

    def test_convert_and_multiply_billion(self):
        result = convert_and_multiply('2.2B')
        self.assertEqual(result, 2.2 * 1e9)

    def test_convert_and_multiply_million(self):
        result = convert_and_multiply('500M')
        self.assertEqual(result, 500 * 1e6)

    def test_convert_and_multiply_thousand(self):
        result = convert_and_multiply('75k')
        self.assertEqual(result, 75 * 1e3)

    def test_convert_and_multiply_percentage(self):
        result = convert_and_multiply('25%')
        self.assertEqual(result, 25)

    def test_convert_and_multiply_plain_value(self):
        result = convert_and_multiply('123')
        self.assertEqual(result, 123.0)

    def test_convert_and_multiply_none(self):
        result = convert_and_multiply(None)
        self.assertIsNone(result)

    def test_convert_and_multiply_str(self):
        result = convert_and_multiply("str")
        self.assertIsNone(result)



class TestPreprocessingFunction(unittest.TestCase):
    def setUp(self):
        # Create a sample CSV file for testing
        self.data_path = "test_bourse.csv"
        data = {
            "Cap": ["Large", "Mid", "Small"],
            "Value": ["100M", "50B", "25M"],
            "P/E_N-1": [10, 15, 20],
            "variation": ["2.5%", "1.5B", "3.0M"]
        }
        df = pd.DataFrame(data)
        df.to_csv(self.data_path, index=False)

    def tearDown(self):
        # Clean up the sample CSV file after testing
        os.remove(self.data_path)

    def test_preprocessing(self):
        preprocessed_data, variation_column = Preprocessing(self.data_path)

        # Check if the output is a tuple of DataFrames
        self.assertIsInstance(preprocessed_data, pd.DataFrame)
        self.assertIsInstance(variation_column, pd.Series)

        # Check if the 'variation' column is correctly processed
        self.assertTrue(variation_column.equals(pd.Series([0.025, 1.5e9, 3.0e6])))

        # Check if the DataFrame has the correct shape and columns
        self.assertEqual(preprocessed_data.shape, (3, 3))  # Adjust the shape based on your actual preprocessing
        expected_columns = ["Cap", "Value", "P/E_N-1"]
        self.assertListEqual(list(preprocessed_data.columns), expected_columns)

        # Add more specific checks based on your preprocessing steps

if __name__ == '__main__':
    unittest.main()
if __name__ == '__main__':
    unittest.main()
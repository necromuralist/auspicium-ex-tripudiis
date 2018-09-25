"""This holds things to help with the data from the `Competitive Data Science Kaggle Competition <https://www.kaggle.com/c/competitive-data-science-final-project/data>`_ 
"""
# python standard library
from pathlib import Path
import os

# from pypi
from dotenv import load_dotenv
import pandas


class DataPaths:
    """Holds the paths to the data from the kaggle site"""
    def __init__(self):
        self._root = None
        self._sales_training_data = None
        self._test_data = None
        self._item_categories = None
        self._items = None
        self._shops = None
        self._sample_submission = None
        return

    @property
    def root(self):
        """path to the root of the contest data"""
        if self._root is None:
            # this assumes you have a .env file somewhere in the repository
            load_dotenv()
            self._root = Path(os.environ.get("contest_data_root"))
        return self._root

    @property
    def sales_training_data(self):
        """path to the gzipped sales data for training"""
        if self._sales_training_data is None:
            self._sales_training_data = self.root.joinpath("sales_train.csv.gz")
        return self._sales_training_data

    @property
    def test_data(self):
        """gzipped testing data"""
        if self._test_data is None:
            self._test_data = self.root.joinpath("test.csv.gz")
        return self._test_data

    @property
    def item_categories(self):
        """information about the product categories"""
        if self._item_categories is None:
            self._item_categories = self.root.joinpath("item_categories.csv")
        return self._item_categories

    @property
    def items(self):
        """information about the products"""
        if self._items is None:
            self._items = self.root.joinpath("items.csv")
        return self._items

    @property
    def shops(self):
        """information about the shops"""
        if self._shops is None:
            self._shops = self.root.joinpath("shops.csv")
        return self._shops

    @property
    def sample_submission(self):
        """A gzipped example of what you should submit"""
        if self._sample_submission is None:
            self._sample_submission = self.root.joinpath("sample_submission.csv.gz")
        return self._sample_submission


class Data:
    """pandas data-frames for the sets"""
    def __init__(self):
        self._paths = None
        self._sales_training_data = None
        self._test_data = None
        self._product_categories = None
        self._products = None
        self._shops = None
        self._sample_submission = None
        return

    @property
    def paths(self):
        """paths object with the paths to the files"""
        if self._paths is None:
            self._paths = DataPaths()
        return self._paths

    @property
    def sales_training_data(self):
        """training data with the sales"""
        if self._sales_training_data is None:
            self._sales_training_data = pandas.read_csv(self.paths.sales_training_data)
        return self._sales_training_data

    @property
    def test_data(self):
        """The test-data set for submission"""
        if self._test_data is None:
            self._test_data = pandas.read_csv(self.paths.test_data)
        return self._test_data

    @property
    def product_categories(self):
        """supplemental product category data"""
        if self._item_categories is None:
            self._item_categories = pandas.read_csv(self.paths.item_categories)
        return self._item_categories

    @property
    def products(self):
        """extra information about the products"""
        if self._products is None:
            self._products = pandas.read_csv(self.paths.items)
        return self._products

    @property
    def shops(self):
        """extra data for the shops"""
        if self._shops is None:
            self._shops = pandas.read_csv(self.paths.shops)
        return self._shops

    @property
    def sample_submission(self):
        """an example of what you should submit"""
        if self._sample_submission is None:
            self._sample_submission = pandas.read_csv(self.paths.sample_submission)
        return self._sample_submission

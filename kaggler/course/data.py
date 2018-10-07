"""This holds things to help with the data from the `Competitive Data Science Kaggle Competition <https://www.kaggle.com/c/competitive-data-science-final-project/data>`_ 
"""
# python standard library
from pathlib import Path
import os

# from pypi
from dotenv import load_dotenv
import pandas

# this project
from kaggler.errors import ConfigurationError


class Configuration:
    """Some string settings"""
    contest_data = "contest_data_root"


class DataPaths:
    """Holds the paths to the data from the kaggle site

    Args:
     debug: emit messages
    """
    def __init__(self, debug: bool=False,
                 root_folder:str=Configuration.contest_data) -> None:
        self.debug = debug
        self.root_folder = root_folder
        self._root = None
        self._sales_training_data = None
        self._test_data = None
        self._item_categories = None
        self._items = None
        self._shops = None
        self._sample_submission = None
        return

    def emit(self, message: str) -> None:
        """prints the message if debug is True"""
        if self.debug:
            print(message)
        return

    @property
    def root(self) -> Path:
        """path to the root of the contest data"""
        if self._root is None:
            # this assumes you have a .env file somewhere in the repository
            load_dotenv()
            root = os.environ.get(self.root_folder)
            if not root:
                raise ConfigurationError(
                    "no '{}' in"
                    " .env or environment (set it)".format(self.root_folder))
            self._root = Path(root).expanduser()
            self.emit("Root: {}".format(self._root))
            self.check_its_there(self._root)
        return self._root

    @property
    def sales_training_data(self):
        """path to the gzipped sales data for training"""
        if self._sales_training_data is None:
            self._sales_training_data = self.root.joinpath("sales_train.csv.gz")
            self.check_its_there(self._sales_training_data)
        return self._sales_training_data

    @property
    def test_data(self):
        """gzipped testing data"""
        if self._test_data is None:
            self._test_data = self.root.joinpath("test.csv.gz")
            self.check_its_there(self._test_data)
        return self._test_data

    @property
    def item_categories(self):
        """information about the product categories"""
        if self._item_categories is None:
            self._item_categories = self.root.joinpath("item_categories.csv")
            self.check_its_there(self._item_categories)
        return self._item_categories

    @property
    def items(self):
        """information about the products"""
        if self._items is None:
            self._items = self.root.joinpath("items.csv")
            self.check_its_there(self.items)
        return self._items

    @property
    def shops(self):
        """information about the shops"""
        if self._shops is None:
            self._shops = self.root.joinpath("shops.csv")
            self.check_its_there(self._shops)
        return self._shops

    @property
    def sample_submission(self):
        """A gzipped example of what you should submit"""
        if self._sample_submission is None:
            self._sample_submission = self.root.joinpath("sample_submission.csv.gz")
            self.check_its_there(self._sample_submission)
        return self._sample_submission

    def check_its_there(self, path: Path):
        """Checks that file or folder exists

        Args:
         path (pathlib.path): check it exists

        Raises:
         ConfigurationError: the expected path doesn't exist
        """
        if not path.exists():
            raise ConfigurationError("'{}' doesn't exist".format(path))        
        return


class Data:
    """pandas data-frames for the sets

    Args: 
     debug (bool): if true, emit more noise
    """
    def __init__(self, debug: bool=False) -> None:
        self.debug = debug
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
            self._paths = DataPaths(self.debug)
        return self._paths

    @property
    def sales_training_data(self):
        """training data with the sales"""
        if self._sales_training_data is None:
            self._sales_training_data = pandas.read_csv(
                self.paths.sales_training_data)
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

if __name__ == "__main__":
    p = DataPaths()
    p.sales_training_data

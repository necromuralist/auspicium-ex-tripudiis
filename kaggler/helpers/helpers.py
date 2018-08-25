# python standard library
import os
import pickle
# from pypi
from tabulate import tabulate


class Helpers:
    """Helper functions"""
    pickle_target = os.path.expanduser("~/projects/kaggle-competitions/pickles/")
    pickle_target_string = pickle_target + "{}.pkl"

    @staticmethod
    def print_head(frame, showindex=False):
        """prints the head of the given data frame

        Args:
         frame (pandas.DataFrame): data frame to print as a table
         showindex (bool): whether to print the index
        """
        print(tabulate(frame.head(), headers="keys", tablefmt="orgtbl",
                       showindex=showindex))
        return

    @staticmethod
    def print_table(data, showindex=True):
        """print the data

        Args:
         data: some kind of data-frame
        """
        print(tabulate(data, headers="keys", tablefmt="orgtbl",
                       showindex=showindex))
        return

    @staticmethod
    def pickle_it(thing, name=None):
        """save the object to a pickle in the data folder

        Args:
         thing: object to pickle
         name: thing to call the pickle
        """
        name = name if name is not None else thing.__name__
        with open(
                os.path.join(
                    Helpers.pickle_target_string.format(name)),
                "wb") as pickler:
            pickle.dump(thing, pickler)
        return

    @staticmethod
    def unpickle(name):
        """loads the pickled object from the data folder
    
        Args:
         name: name of the pickle without the folder or extension
    
        Returns:
         object: the un-pickled object
        """
        with open(Helpers.pickle_target_string.format(name),
                  "rb") as unpickler:
            unpickled = pickle.load(unpickler)
        return unpickled

    @staticmethod
    def exists(name):
        """checks if the thing is already a pickle

        Args:
         name: name of the pickle without folder or extension

        Returns:
         bool: True if the pickle exists
        """
        return os.path.isfile(Helpers.pickle_target_string.format(name))


class DataSource:
    """Strings for the files

    Args:
     directory: path to the data-folder
    """
    def __init__(self, directory="~/projects/kaggle-competitions/data/"):
        self._directory = None
        self.directory = directory
        self._file_names = None
        self._paths = None
        self._file_name_paths = None
        return

    @property
    def directory(self):
        """The path to the data"""
        return self._directory

    @directory.setter
    def directory(self, path):
        """expands the user and saves the path

        Args:
         path (str): path to the data folder
        """
        self._directory = os.path.expanduser(path)
        if not os.path.exists(self._directory):
            raise Exception(
                "This file doesn't exist: {}".format(self._directory))
        return

    @property
    def file_names(self):
        """list of file names in the data directory"""
        if self._file_names is None:
            self._file_names = os.listdir(self.directory)
        return self._file_names

    @property
    def paths(self):
        """list of paths to the file names"""
        if self._paths is None:
            self._paths = [os.path.join(self.directory, name)
                    for name in self.file_names]
        return self._paths

    @property
    def file_name_paths(self):
        """dict of name: path"""
        if self._file_name_paths is None:
            self._file_name_paths = {
                name.split('.')[0]: self.paths[index]
                for index, name in enumerate(self.file_names)}
        return self._file_name_paths
    
    def set_attributes(self):
        """attaches the file names to this object"""
        for name in self.file_names:
            setattr(self, name.split('.')[0], name)
        return


class DataNames:
    """thing with the data-file-names (without extensions) as attributes"""
    training = "sales_train"
    items = "items"
    item_categories = "item_categories"
    shops = "shops"


class DataKeys:
    """Column names/keys for the data."""
    item_category = "item_category_id"
    shop = "shop_id"
    item = "item_id"
    date = "date"
    date_block = "date_block_num"
    price = "item_price"
    day_count = "item_cnt_day"
    month_count = 'item_count_month'
    name = "item_name"
    day = "day"
    month = "month"
    year = "year"

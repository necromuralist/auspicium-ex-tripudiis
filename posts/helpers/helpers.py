import pickle
from tabulate import tabulate
class Helpers:
    """Helper functions"""
    pickle_target = "../pickles/"
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
    
        Args;
         name: name of the pickle without the folder or extension
    
        Returns:
         object: the un-pickled object
        """
        with open(Helpers.pickle_target_string.format(name),
                  "rb") as unpickler:
            unpickled = pickle.load(unpickler)
        return unpickled

class DataSource:
    """Strings for the files"""
    directory = "../data/"

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

class Pickles:
    """Holder of the pickle names"""
    super_set = "training_data"
    grouped = "grouped_months_data"
    x_train = "x_train"
    x_test = "x_test"
    y_train = "y_train"
    y_test = "y_test"
    train_test = "train_test"

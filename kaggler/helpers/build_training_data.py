import os

import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

import pandas
from sklearn.model_selection import train_test_split

from kaggler.helpers.helpers import (
    DataKeys,
    DataNames,
    DataSource,
    Helpers,
)

class Pickles:
    """Holder of the pickle names"""
    super_set = "training_data"
    grouped = "grouped_months_data"
    x_train = "x_train"
    x_test = "x_test"
    y_train = "y_train"
    y_test = "y_test"
    train_test = "train_test"

class SuperSet:
    """Creates the super-set of data"""
    def __init__(self):
        self._data_sources = None
        self._data = None
        return

    @property
    def data_sources(self):
        """string-values for the data sources"""
        if self._data_sources is None:
            self._data_sources = DataSource()
            self._data_sources.set_attributes()
        return self._data_sources

    @property
    def data(self):
        """the super-set"""
        if self._data is None:
            self._data = pandas.read_csv(
                self.data_sources.file_name_paths[DataNames.training])
        return self._data

class Items:
    """sale items data"""
    def __init__(self):
        self._data = None
        self._data_sources = None
        return

    @property
    def data_sources(self):
        """a Data-Source object"""
        if self._data_sources is None:
            self._data_sources = DataSource()
        return self._data_sources
        
    @property
    def data(self):
        """dataframe of sale items"""
        if self._data is None:
            self._data = pandas.read_csv(
                self.data_sources.file_name_paths[DataNames.items])
        return self._data


class SuperDuper:
    """super set with item counts"""
    def __init__(self):
        self._data = None
        self._super_set = None
        self._items = None
        return

    @property
    def super_set(self):
        """super-set of data"""
        if self._super_set is None:
            self._super_set = SuperSet().data
        return self._super_set

    @property
    def items(self):
        """sale-items data"""
        if self._items is None:
            self._items = Items().data
        return self._items

    @property
    def data(self):
        """super set with sale items"""
        if self._data is None:
            self._data = self.super_set.merge(self.items,
                                              on=DataKeys.item,
                                              how="left")
        
            assert len(self.data) == len(self.super_set)
        return self._data


class SuperDates:
    """Super-set with dates split out"""
    def __init__(self):
        self._super_duper = None
        self._date_expression = None
        self._dates = None
        self._data = None
        return

    @property
    def super_duper(self):
        """A super-duper data set"""
        if self._super_duper is None:
            self._super_duper = SuperDuper().data
        return self._super_duper

    @property
    def date_expression(self):
        """regular expression to parse the dates"""
        if self._date_expression is None:
            self._date_expression = (r'(?P<{}>\d{{2}})\.'
                                     '(?P<{}>\d{{2}})\.'
                                     '(?P<{}>\d{{4}})').format(
                                         DataKeys.day,
                                         DataKeys.month,
                                         DataKeys.year)
        return self._date_expression

    @property
    def dates(self):
        """dataframe of dates"""
        if self._dates is None:
            self._dates = self.super_duper.date.str.extract(
                self.date_expression)
        return self._dates

    @property
    def data(self):
        """data set with date columns"""
        if self._data is None:
            self._data = pandas.concat(
                (self.super_duper, self.dates),
                axis='columns')
        return self._data

class SuperClean:
    """The super-set data with extra columns removed"""
    def __init__(self, drop=[DataKeys.date, DataKeys.name, DataKeys.day]):
        self.drop = drop
        self._super_set = None
        self._data = None
        return

    @property
    def super_set(self):
        """the super-set data"""
        if self._super_set is None:
            self._super_set = SuperDates().data
        return self._super_set

    @property
    def data(self):
        """The cleaned data"""
        if self._data is None:
            self._data = self.super_set.drop(self.drop, axis="columns")
        return self._data

    def save(self):
        """Saves the data as a pickle"""
        Helpers.pickle_it(self.data, Pickles.super_set)
        return


class Grouper:
    """Data Grouped by month, shop, item"""
    def __init__(self):
        self._cleaned = None
        self._grouper = None
        self._data = None
        return

    @property
    def cleaned(self):
        """cleaned super-set"""
        if self._cleaned is None:
            self._cleaned = SuperClean().data
        return self._cleaned

    @property
    def grouper(self):
        """goups the data by columns"""
        if self._grouper is None:
            self._grouper = self.cleaned[[DataKeys.date_block, DataKeys.shop,
                                          DataKeys.item,
                                          DataKeys.day_count]].copy()
        return self._grouper

    @property
    def data(self):
        """the summed group-data"""
        if self._data is None:
            self._data = self.grouper.groupby([DataKeys.date_block,
                                               DataKeys.shop,
                                               DataKeys.item]).sum()
        return self._data


class Chunked:
    """Data set chunked-up to the months"""
    def __init__(self):
        self._grouped = None
        self._data = None
        return

    @property
    def grouped(self):
        """grouped data"""
        if self._grouped is None:
            self._grouped = Grouper().data
        return self._grouped

    @property
    def data(self):
        """The chunked data with the counts renamed"""
        if self._data is None:
            self._data =  self.grouped.reset_index()
            self._data.rename(
                columns={DataKeys.day_count: DataKeys.month_count},
                inplace=True)
        return self._data

class SuperGroup:
    """Super Set grouped

    Args:
     groups: list of columns to form the groups
    """
    def __init__(self, groups=[DataKeys.date_block,
                               DataKeys.shop,
                               DataKeys.item]):
        self.groups = groups
        self._super_set = None
        self._data = None
        return

    @property
    def super_set(self):
        """cleaned super set of data"""
        if self._super_set is None:
            self._super_set = SuperClean().data
        return self._super_set

    @property
    def data(self):
        """the super group data"""
        if self._data is None:
            self._data = self.super_set.groupby(self.groups).last()
            self._data = self._data.reset_index()
        return self._data

class MergeChunked:
    """merge the super-set and the chunked data"""
    def __init__(self):
        self._chunked = None
        self._super_group = None
        self._data = None
        return

    @property
    def chunked(self):
        if self._chunked is None:
            self._chunked = Chunked().data
        return self._chunked

    @property
    def super_group(self):
        if self._super_group is None:
            self._super_group = SuperGroup().data
        return self._super_group

    @property
    def data(self):
        if self._data is None:
            self._data = self.chunked.merge(self.super_group,
                        on=[DataKeys.date_block,
                            DataKeys.shop,
                            DataKeys.item],
                        how="left")
            self._data.drop([DataKeys.day_count], axis="columns")
        return self._data

    def __call__(self):
        """save the data as a pickle"""
        Helpers.pickle_it(self.data, Pickles.grouped)
        return




class TrainValidation:
    """Makes the training and validation sets

    Args:
     test_size: fraction of data to use as validaiton data
     seed: random seed
    """
    def __init__(self, test_size=0.2, seed=2018):
        self.test_size = test_size
        self.seed = seed
        self._target = None
        self._features = None
        self._chunked = None
        self._x_train = None
        self._x_test = None
        self._y_train = None
        self._y_test = None
        return

    @property
    def chunked(self):
        """the data chunked by month"""
        if self._chunked is None:
            self._chunked = MergeChunked().data
        return self._chunked

    @property
    def target(self):
        """the target data"""
        if self._target is None:
            self._target = self.chunked[DataKeys.month_count].copy()
        return self._target

    @property
    def features(self):
        """The feature data"""
        if self._features is None:
            self._features = self.chunked[
                self.chunked.columns[
                    ~self.chunked.columns.isin([DataKeys.month_count,
                                                DataKeys.day_count])]].copy()
        return self._features

    @property
    def x_train(self):
        if self._x_train is None:
            self.split()
        return self._x_train

    @property
    def x_test(self):
        if self._x_test is None:
            self.split()
        return self._x_test

    @property
    def y_train(self):
        if self._y_train is None:
            self.split()
        return self._y_train

    @property
    def y_test(self):
        if self._y_test is None:
            self.split()
        return self._y_test

    def split(self):
        self._x_train, self._x_test, self._y_train, self._y_test = train_test_split(
            self.features,
            self.target,
            test_size=self.test_size,
            random_state=self.seed
        )
        return

    def __call__(self):
        """stores the data-files"""
        Helpers.pickle_it(self.x_train, Pickles.x_train)
        Helpers.pickle_it(self.x_test, Pickles.x_test)
        Helpers.pickle_it(self.y_train, Pickles.y_train)
        Helpers.pickle_it(self.y_test, Pickles.y_test)
        return

    def check(self):
        """checks the columns for the data"""
        assert DataKeys.month_count not in self.features.columns, "Features has target"
        assert DataKeys.month_count not in self.x_train.columns, "x_train has target"
        assert DataKeys.month_count not in self.x_test.columns, "x_test has target"
        assert DataKeys.day_count not in self.features.columns, "Features has day count"
        assert DataKeys.day_count not in self.x_train.columns, "x_train has day count"
        assert DataKeys.day_count not in self.x_test.columns, "x_test has day count"
        assert self.target.name == DataKeys.month_count, "Target not month count"
        assert self.y_test.name == DataKeys.month_count, "y-test not month count"
        assert self.y_train.name == DataKeys.month_count, "y-train not month count"
        return

if __name__ == "__main__":
    data = TrainValidation()
    data()
    data.check()

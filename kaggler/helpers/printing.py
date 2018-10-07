"""These are helpers to output the data-frames"""
# from pypi
from tabulate import tabulate

def print_table(frame, headers="keys", showindex=False):
    """Prints an org-mode table

    Args:
     frame: the data to print
     headers: list of table to headers to use instead of coulmns
     showindex (bool): whether to print the index
    """
    print(tabulate(frame, headers=headers, tablefmt="orgtbl",
                   showindex=showindex))
    return

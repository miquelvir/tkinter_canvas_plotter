"""
custom errors of the package
"""


class InvalidDatasetError(ValueError):
    """ the provided dataset is invalid (due to a dimension consistency problem) """
    pass

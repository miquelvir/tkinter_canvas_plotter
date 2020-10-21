"""
custom errors of the package
"""


class GraphError(ValueError):
    """ base class for all errors of the package """
    pass


class InvalidDatasetError(GraphError):
    """ the provided dataset is invalid (due to a dimension consistency problem) """
    pass

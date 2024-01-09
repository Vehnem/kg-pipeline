###Datasource Adapter###

from abc import ABC

class DataSourceAdapter(ABC):
    """abstract class for datasource adapters"""

    def __init__(self, datasource):
        self.datasource = datasource

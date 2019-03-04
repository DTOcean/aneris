
from copy import deepcopy

from aneris.boundary import DataDefinition, Structure

import pandas as pd

class SeriesData(Structure):

    '''Structure represented in a series of some sort'''

    def get_data(self, raw, meta_data):

        series = pd.Series(raw)

        return series

    def get_value(self, data):

        return data.copy()


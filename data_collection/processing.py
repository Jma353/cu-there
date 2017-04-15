# Data processing tools
# This file contains two classes:
# (1) TrainTestSplit: an object containing training and testing data
# (2) JsonLoader: an object that yields TrainTestSplit instances for various ML models using data from a JSON file

class TrainTestSplit(object):
    """ Class containing training and testing data (acts like a struct) """
    _train = None
    _test = None

    def __init__(self, train, test):
        self._train = train
        self._test = test

    def get_train(self):
        return self._train

    def get_test(self):
        return self._test

class JsonLoader(object):
    """ Class for loading consolidated event data
    (JSON) into a format easily usable by the models in predictive_models.py """

    _dict = {}

    def __init__(self):
        self._dict = {}

    def __init__(self, filename):
        self.load_data(self, filename)

    def load_data(self, filename):
        self._dict = json.loads(filename)

    def time_model_data(self):
        """ Returns a TrainTestSplit for TimeModel. """
        train = []
        test = []
        return TrainTestSplit(train, test)

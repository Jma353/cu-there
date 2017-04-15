# Predictive models for event attendance

import numpy as np

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

class Model(object):
    """ Base (abstract) class for a machine learning model. """
    sklearn_model = None

    def train(self, train_set):
        """ Trains the sklearn_model object.

        The parameter train_set takes the form (X, y) where X
        is a matrix of independent variable values and y is a vector of
        dependent variable values. """

    def test(self, test_set):
        """ Evaluates the model on a test set.

        The parameter test_set contains a matrix of independent variables.
        The output is a vector of dependent variable values. """
        pass

class TimeModel(Model):
    """ Predicts event attendance based on event time.
        Attempts to fit time-attendance relationship to a polynomial of degree 2
        (with roots at the lowest-attendance times and vertex at the
        highest-attendance time). """

    def train(self, train_set):
        """ Polynomial interpolation of degree 2 (quadratic regression). """
        self.sklearn_model = make_pipeline(PolynomialFeatures(2), Ridge())
        X, y = train_set[:, 0], train_set[:, 1]
        X = X.reshape(-1, 1)
        results = self.sklearn_model.fit(X, y)
        return results

    def test(self, test_set):
        """ Output of quadratic regression model. """
        if not self.sklearn_model:
            raise Exception("Model has not been trained yet.")
        return self.sklearn_model.predict(test_set)

    def summary(self):
        return self.sklearn_model.summary()

    def __init__(self):
        self.sklearn_model = None

class LatLongModel(Model):
    """ Predicts event attendance based on latitude and longitude.
    See `latlong_regression.md` for a detailed description of this model. """
    pass

class DescriptionModel(Model):
    """ Predicts event attendance based on textual description features."""
    pass

class EventModel(Model):
    """ Model that combines outputs of DescriptionModel, TimeModel,
    and LatLongModel into a single attendance number. """
    pass

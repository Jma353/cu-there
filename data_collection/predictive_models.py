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
        self.sklearn_model = make_pipeline(PolynomialFeatures(3), Ridge())
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

class VenueModel(object):
    """ Ranks the venues by highest average attendance.
        Usage:

        v = VenueModel()
        v.add_venues(events)
        venues_to_events = v.top_k(20)
        # Do stuff with events in venues_to_events

    """

    def __init__(self):
        self._venues_to_avgs = {}
        self._events = []

    def add_venues(self, events):
        """ Adds venue data (for computing top venues) """
        self._events = events
        venues_to_sums = {}
        venues_to_lens = {}
        for event in events:
            venue_id = event["venue"]["id"]
            if venue_id in venues_to_sums:
                venues_to_sums[event["venue"]["id"]] += event["stats"]["attending"]
                venues_to_lens[event["venue"]["id"]] += 1
            else:
                venues_to_sums[event["venue"]["id"]] = event["stats"]["attending"]
                venues_to_lens[event["venue"]["id"]] = 1
        for venue_id in venues_to_sums:
            self._venues_to_avgs[venue_id] = (venues_to_sums[venue_id]*1.0)/venues_to_lens[venue_id]

    def top_k(self, k=10):
        """ Returns the top k venues with the events present at them. Format:

        [
            {"venue id 1": [ /* highest-attendance venue */
                <event 1>,
                <event 2>,
                ...
            ]},
            {"venue id 2": [ /* second-highest-attendance venue */
                <event 1>,
                <event 2>
            ]}
        ]
        """
        top_venues = sorted(venues_to_sums.keys(), key=venues_to_sums.get, reverse=True)
        result = []
        for venue_id in top_venues:
            entry = []
            for event in self._events:
                if event["venue"]["id"] == venue_id:
                    entry.append(event)
            result.append({venue_id: entry})
        return result


class DescriptionModel(Model):
    """ Predicts event attendance based on textual description features."""
    pass

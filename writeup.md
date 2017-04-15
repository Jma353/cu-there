# CU There: Machine Learning Writeup

This document outlines the machine learning system for CU There.

The goal of the system is to provide recommendations of times and locations (given as latitude and longitude) for an event on the Cornell campus given a textual description of the event.

## Data Pipeline

The data pipeline (from event JSON to recommendations based on a textual description) is as follows:

### Data Preprocessing

The file `processing.py` will contain functions for converting data in the raw JSON event format into numpy matrices that can be used in the machine learning model. This is done by converting the JSON to dictionaries using `json.loads` and extracting relevant dictionary entries. These functions will be stored under the class `JsonLoader`.

### Machine Learning Model: Training Phase

The machine learning model (called `EventModel` in the codebase) is complex due to the wildly varying nature of the predictors: time is numerical, latitude and longitude is geospatial, and description is textual.

Because of this, we subdivide this model into several smaller learning models whose results are averaged to produce a final estimate. These models are:

* `predictive_models.TimeModel` - quadratic regression model responsible for predicting event attendance based on time
* `predictive_models.LatLongModel` - responsible for predicting attendance based on latitude and longitude
* `predictive_models.DescriptionModel` - text-based regression model responsible for predicting attendance based on description

Using the `JsonLoader` class, we load the event data and convert it into a set of training data usable by the machine learning models. We then train each model on this data using the `.train()` method of each model class.

### Machine Learning Model: Testing Phase

The user enters the description of their event into the frontend. The description is then fed into the pre-trained model via the backsolver, which yields pairs of times and locations that (when combined with the description) yield the highest attendance. More details on this in the "backsolver" section.

## Regression Models

Specific details about each regression model are listed below.

### Time of Day

This is a simple polynomial regression model of degree 2. Time of day (represented as an hour in decimal; e.g. `8.5` is `8:30 AM` and `21.2` is `9:12 PM`) is the independent variable. Attendance is the dependent variable.

Quadratic regression is used because the relationship between time and attendance intuitively follows a "bell curve" with a peak around mid-day. A concave-down quadratic function with a root early in the day and a root later in the day should accurately model this relationship.

### Latitude-Longitude

The approach below consists of a "patchwork" of regression models distributed in space. Each point in space up to a certain granularity is mapped to a quadratic regression model (with a bell-shaped "peak" like the one described above) that most accurately predicts the attendance of an event on this point. This creates a discontinuous function in 3D space with "peaks" in various locations that are known to have high attendance. New points in the test set are evaluated using the regression model that is nearest to the point.

#### Pre-processing

* Transform (lat, long) into scaled-down variable centered at 0.
	* Make the center of the event search (constants.LATITUDE, constants.LONGITUDE) the origin (0, 0).
	* Place lat's and long's onto this coordinate plane, multiplying units by some factor of 10 for scaling purposes (for now let's make it 100).

#### Training model

* Sort events in decreasing order of attendance (highest first).
* Create empty mapping of (lat, long) pairs to regression models, with a small-enough granularity - for now let's say 0.1.
* Go down the sorted list of events, and:
	* Perform 3D quadratic regression on attendance vs. (lat, long) within a small radius of the event.
	* Take each point within this radius, using the granularity given above.
		* If there is no model mapped to this point in the mapping described above, associate the point with this model.
		* If there is a model already mapped to the point, check the R^2 values of the already-mapped model and the new model. If the R^2 of the new model is higher, update the mapping (associating the point with the new model).

#### Testing model (making predictions)

* Round the point to the nearest value for which we have a mapping.
* Check the model associated with the point in the mapping. Evaluate the model on the point.

### Textual Description

TBD

## Ensemble (EventModel)

The `EventModel` takes the predictions of each of the three smaller models (`DescriptionModel`, `LatLongModel`, and `TimeModel`) and averages them to produce an overall attendance prediction.

## Backsolver

The machine learning model described above takes in three parameters (time, location, and description) and gives an estimate of attendance. The goal of our system is related but different: we're given a description and are asked to find time and location such that attendance is maximized. We can use our model as a tool to solve this optimization problem through a "backsolving" or "guess-and-check" process.

We take the description as fixed. For all locations, for all times, we run the machine learning model and take note of the output. As this is done, we keep track of the 5 pairs that yield the highest attendance according to our model. We then return these 5 pairs, sorted in decreasing order of attendance, as the output of the system.

This process takes _O(|L| |T|)_ time where _L_ is the set of locations and _T_ is the set of times (for example, every 15 minute block in a 24-hour day), since we iterate through all pairs.

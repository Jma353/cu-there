# Lat-Long Regression for Event Attendance

## Pre-processing

* Transform (lat, long) into scaled-down variable centered at 0.
	* Make the center of the event search (constants.LATITUDE, constants.LONGITUDE) the origin (0, 0).
	* Place lat's and long's onto this coordinate plane, multiplying units by some factor of 10 for scaling purposes (for now let's make it 100).

## Training model

* Sort events in decreasing order of attendance (highest first).
* Create empty mapping of (lat, long) pairs to regression models, with a small-enough granularity - for now let's say 0.1.
* Go down the sorted list of events, and:
	* Perform 3D quadratic regression on attendance vs. (lat, long) within a small radius of the event.
	* Take each point within this radius, using the granularity given above.
		* If there is no model mapped to this point in the mapping described above, associate the point with this model.
		* If there is a model already mapped to the point, check the R^2 values of the already-mapped model and the new model. If the R^2 of the new model is higher, update the mapping (associating the point with the new model).

## Testing model (making predictions)

* Round the point to the nearest value of the given granularity.
* Check the model associated with the point in the mapping. Evaluate the model on the point.

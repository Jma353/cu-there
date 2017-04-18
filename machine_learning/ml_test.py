from processing import JsonLoader
from predictive_models import TimeModel
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score

def test_time_model():
  """ Manual test of time ML model. Plots predictions of attendance vs. time. """
  j = JsonLoader("../results/1491923869-consolidation.json")
  data = j.time_model_data()
  t = TimeModel()
  t.train(data)

  print "R^2:"
  preds = []
  for time in data[:,0]:
      preds.append(t.test(time))
  print r2_score(data[:,1], preds)

  predictions = []
  for i in xrange(0, 24*4):
      predictions.append(t.test(i/4.0))


  fig = plt.figure()
  plt.plot([i/4.0 for i in xrange(0, 24*4)], predictions)
  plt.scatter(data[:,0], data[:, 1], )
  fig.suptitle("Event Attendance vs. Time")
  plt.xlabel("Time of Day (Hours)")
  plt.ylabel("Predicted Attendance")
  axes = plt.gca()
  axes.set_xlim([0, 24])
  plt.show()

test_time_model()

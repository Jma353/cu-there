# Code for testing the accuracy of our models (not part of the app itself)

from processing import JsonLoader

def test_time_model(json_file):
    loader = JsonLoader(json_file)
    data = loader.time_model_data()
    train_set, test_set = data.get_train(), data.get_test()
    tm = TimeModel()
    tm.train(train_set)
    output = tm.test(test_set)
    # TODO: accuracy

from app.preprocessing.preprocess import Preprocess
import dill

preprocessed = Preprocess()
dill.dump(preprocessed, open('preprocessed.p', 'wb'))

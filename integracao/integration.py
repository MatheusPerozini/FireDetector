import OpenCVImage
import pickle

with open('modelBayess.pkl', 'rb') as f:
    bayessModel = pickle.load(f)


# coding: utf-8

import pickle


def load_data(path):
    f = open(path, 'rb')
    data = pickle.load(f)
    f.close()
    return data



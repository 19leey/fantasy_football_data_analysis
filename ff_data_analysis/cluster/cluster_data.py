# -*- encoding: utf-8 -*-
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np


#TODO: modularize and clean up


def cluster_overall_test(data_frame):
    slices = {}
    new_label = 0
    for slice in range(1, 4):
        if slice is 1:
            data_frame_slice = data_frame[data_frame.Rank <= 50].reset_index(drop=True)
            k = 10
        elif slice is 2:
            data_frame_slice = data_frame[np.logical_and(data_frame.Rank > 50, data_frame.Rank <= 125)].reset_index(drop=True)
            k = 9
        elif slice is 3:
            data_frame_slice = data_frame[data_frame.Rank > 125].reset_index(drop=True)
            k = 8

        x = data_frame_slice['Avg'].values
        y = data_frame_slice['Rank'].values
        X = np.array(list(zip(x, y)))

        kmeans = KMeans(n_clusters=k)
        kmeans = kmeans.fit(X)
        labels = kmeans.predict(X)
        centroids = kmeans.cluster_centers_
        labels = kmeans.labels_

        label_indexes = {}
        for index, label in zip(range(len(data_frame_slice)), labels):
            label_indexes[label] = index

        start = 0
        for label in label_indexes:
            end = (label_indexes[label] + 1)
            labels[start:end] = new_label
            start = end
            new_label += 1

        data_frame_slice = data_frame_slice.join(pd.DataFrame({'Tiers' : list(labels)}))
        slices[slice] = data_frame_slice

    return slices

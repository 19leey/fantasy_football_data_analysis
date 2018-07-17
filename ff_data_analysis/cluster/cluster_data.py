# -*- encoding: utf-8 -*-
from ff_data_analysis.generator import generate_csv as gen
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np


def get_position_k_values(position):
    if position is 'qb':
        return 8
    elif position is 'rb':
        return 10
    elif position is 'wr':
        return 10
    elif position is 'te':
        return 8
    elif position is 'k':
        return 5
    elif position is 'dst':
        return 5


def get_position_cutoffs(position):
    if position is 'qb':
        return 50
    elif position is 'rb':
        return 75
    elif position is 'wr':
        return 75
    elif position is 'te':
        return 50
    elif position is 'k':
        return 25
    elif position is 'dst':
        return 25


def cluster_overall_rankings(data_frame):
    slices = {}
    new_label = 0
    data_frame = data_frame[data_frame.Rank <= 250]
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

        X = np.array(list(zip(data_frame_slice['Avg'].values, data_frame_slice['Rank'].values)))
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
    gen.write_clustered_consensus_rankings(slices)
    return slices


def cluster_position_rankings(data_frame, position):
    data_frame = data_frame[data_frame.Rank <= get_position_cutoffs(position)].reset_index(drop=True)
    X = np.array(list(zip(data_frame['Avg'].values, data_frame['Rank'].values)))
    kmeans = KMeans(n_clusters=get_position_k_values(position))
    kmeans = kmeans.fit(X)
    labels = kmeans.predict(X)
    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    label_indexes = {}
    for index, label in zip(range(len(data_frame)), labels):
        label_indexes[label] = index
        
    start = 0
    for label, new_label in zip(label_indexes, range(0, get_position_k_values(position))):
        end = (label_indexes[label] + 1)
        labels[start:end] = new_label
        start = end
        new_label += 1

    data_frame = data_frame.join(pd.DataFrame({'Tiers' : list(labels)}))
    gen.write_clustered_consensus_rankings(data_frame, position)
    return data_frame

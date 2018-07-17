# -*- encoding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import pandas as pd


def draw_cluster_plot(data_frame):
    colors = ['g.', 'r.', 'b.', 'y.', 'c.', 'm.', 'k.', 'g.']

    for _, row in data_frame.iterrows():
        plt.plot(row['Avg'], row['Rank'], colors[row['Tiers']], markersize = 10)
    plt.show()

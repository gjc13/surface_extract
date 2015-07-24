#!/usr/bin/python2.7

__author__ = 'gjc'

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from numpy import array


def random_noise_box_dots(origin, xvec, yvec, zvec, numpoints, scale=0.01):
    return random_box_dots(origin, xvec, yvec, zvec, numpoints)\
        + np.random.normal(0, scale, (numpoints, 3))


def random_box_dots(origin, xvec, yvec, zvec, numpoints):
    scales = np.random.rand(numpoints, 3)
    points = np.zeros((numpoints, 3))
    for i, row in enumerate(scales):
        points[i] = row[0]*xvec + row[1]*yvec + row[2]*zvec
    points = points + origin
    return points


def get_simulated_data():
    points = random_noise_box_dots(
        array([0, 0, 0]),
        array([0.05, 0, 0]),
        array([0, 0, 0.6]),
        array([0, 0, 0]),
        200)
    points = np.append(points, random_noise_box_dots(
        array([0.95, 0, 0]),
        array([0.05, 0, 0]),
        array([0, 0, 0.6]),
        array([0, 0, 0]),
        200), axis=0)
    points = np.append(points, random_noise_box_dots(
        array([0, 0, 0.1]),
        array([1, 0, 0]),
        array([0, 0.3, 0]),
        array([0, 0, 0]),
        2000), axis=0)
    points = np.append(points, random_noise_box_dots(
        array([0, 0, 0.4]),
        array([1, 0, 0]),
        array([0, 0.3, 0]),
        array([0, 0, 0]),
        2000), axis=0)
    return points


if __name__ == '__main__':
    fig = plt.figure()
    axis = fig.add_subplot(111, projection='3d')
    box_points = random_box_dots(array([-1, -1, 0]),
                                 array([2, 0, 0]),
                                 array([0, 2, 0]),
                                 array([0, 0, 1]),
                                 2000)
    box_points2 = random_box_dots(array([5, 5, 5]),
                                  array([1, 0, 0]),
                                  array([0, 1, 0]),
                                  array([0, 0, 6]),
                                  2000)
    box_points = np.append(box_points, box_points2, axis=0)
    example_points = get_simulated_data()
    axis.scatter(example_points[:, 0], example_points[:, 1], example_points[:, 2])
    plt.show()


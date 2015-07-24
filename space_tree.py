#!/usr/bin/python2.7

__author__ = 'gjc'


from math import fabs


class SpaceTree:
    # scope: (xmin, xmax, ymin, ymax, zmin, zmax)
    def __init__(self, scope, node_id=0, min_grid_size=0.03, root=None):
        self._xmin = scope[0]
        self._xmax = scope[1]
        self._ymin = scope[2]
        self._ymax = scope[3]
        self._zmin = scope[4]
        self._zmax = scope[5]
        if root is None:
            self.__root = self
        else:
            self.__root = root
        self.id = node_id
        self._min_tree_grid_size = min_grid_size
        self.__minsize = min(fabs(self._xmin - self._xmax),
                             fabs(self._ymin - self._ymax),
                             fabs(self._zmin - self._zmax))
        self.__xmiddle = (self._xmin+self._xmax)/2
        self.__ymiddle = (self._ymin+self._ymax)/2
        self.__zmiddle = (self._zmin+self._zmax)/2
        self._child_nodes = None
        self.is_leaf = self.__minsize < min_grid_size
        self.points = []
        self.surrounding_nodes = {}
        self.__build_surrounding_nodes()

    def add_point(self, point):
        if self.is_leaf:
            self.points.append(point)
            return
        if self._child_nodes is None:
            self.__add_child_nodes()
        child_node_id = (point[0] >= self.__xmiddle) << 2 | \
            (point[1] >= self.__ymiddle) << 1 | \
            (point[2] >= self.__zmiddle)
        self._child_nodes[child_node_id].add_point(point)

    def __add_child_nodes(self):
        if self.is_leaf:
            return
        self._child_nodes = [
            SpaceTree((self._xmin, self.__xmiddle, self._ymin, self.__ymiddle, self._zmin, self.__zmiddle),
                      self.id*8+1, self._min_tree_grid_size, self.__root),
            SpaceTree((self._xmin, self.__xmiddle, self._ymin, self.__ymiddle, self.__zmiddle, self._zmax),
                      self.id*8+2, self._min_tree_grid_size, self.__root),
            SpaceTree((self._xmin, self.__xmiddle, self.__ymiddle, self._ymax, self._zmin, self.__zmiddle),
                      self.id*8+3, self._min_tree_grid_size, self.__root),
            SpaceTree((self._xmin, self.__xmiddle, self.__ymiddle, self._ymax, self.__zmiddle, self._zmax),
                      self.id*8+4, self._min_tree_grid_size, self.__root),
            SpaceTree((self.__xmiddle, self._xmax, self._ymin, self.__ymiddle, self._zmin, self.__zmiddle),
                      self.id*8+5, self._min_tree_grid_size, self.__root),
            SpaceTree((self.__xmiddle, self._xmax, self._ymin, self.__ymiddle, self.__zmiddle, self._zmax),
                      self.id*8+6, self._min_tree_grid_size, self.__root),
            SpaceTree((self.__xmiddle, self._xmax, self.__ymiddle, self._ymax, self._zmin, self.__zmiddle),
                      self.id*8+7, self._min_tree_grid_size, self.__root),
            SpaceTree((self.__xmiddle, self._xmax, self.__ymiddle, self._ymax, self.__zmiddle, self._zmax),
                      self.id*8+8, self._min_tree_grid_size, self.__root),
        ]

    def __build_surrounding_nodes(self):
        xstart = self._xmin - 2*self._xmax
        xend = self._xmin
        xstep = self._xmax - self._xmin
        for i in range(0, 3):
            ystart = self._ymin - 2*self._ymax
            yend = self._ymin
            ystep = self._ymax - self._ymin
            for j in range(0, 3):
                zstart = self._zmin - 2*self._zmax
                zend = self._zmin
                zstep = self._zmax - self._zmin
                for k in range(0, 3):
                    if i != 1 or j != 1 or k != 1:
                        surrounding_id = i << 4 | j << 2 | k
                        self.surrounding_nodes[surrounding_id] = self.__root.__get_node_range(
                            xstart, xend, ystart, yend, zstart, zend)
                    zstart = zstart + zstep
                    zend = zend + zstep
                ystart = ystart + ystep
                yend = yend + ystep
            xstart = xstart + xstep
            xend = xend + xstep

    def __get_node_range(self, xmin, xmax, ymin, ymax, zmin, zmax):
        if xmax < self._xmin or xmin > self._xmax or \
           ymax < self._ymin or ymin > self._ymax or \
           zmax < self._zmin or zmin > self._zmax:
            return None
        if xmax < self._xmin or xmin > self._xmax or \
           ymax < self._ymin or ymin > self._ymax or \
           zmax < self._zmin or zmin > self._zmax:
            return self
        if self._child_nodes is None:
            return None
        for child_node in self._child_nodes:
            node = child_node.__get_node_range(xmin, xmax, ymin, ymax, zmin, zmax)
            if node is not None:
                return node
        return None


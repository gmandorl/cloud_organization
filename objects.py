import numpy as np



class Pairs:

    def __init__(self, pairlist):
        self.pairlist = pairlist
        if pairlist:
            self.partner1, self.partner2 = zip(*pairlist)
        else:
            self.partner1, self.partner2 = [], []

    def __len__(self):
        return len(self.pairlist)

    def distance_regionprops(self):
        """The distance in units of pixels between two centroids of cloud-objects found by skm.regionprops."""

        dist_x = np.array([c.centroid[1] for c in self.partner1]) - \
                 np.array([c.centroid[1] for c in self.partner2])
        dist_y = np.array([c.centroid[0] for c in self.partner1]) - \
                 np.array([c.centroid[0] for c in self.partner2])
        return np.sqrt(dist_x**2 + dist_y**2)

    def distance_shapely(self):
        """The shortest distance in units of pixels between edges of cloud-objects given by shapely.MultiPolygon."""

        return np.array([self.pairlist[i][0].distance(self.pairlist[i][1]) for i in range(len(self.pairlist))])

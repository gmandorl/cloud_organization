import numpy as np



class Pairs:

    def __init__(self, region_pairs, poly_pairs):
        self.region_pairs = region_pairs
        self.poly_pairs = poly_pairs

        if region_pairs:
            self.partner1, self.partner2 = zip(*region_pairs)
        else:
            self.partner1, self.partner2 = [], []

        self.destances_regions = self.compute_distance_regions()
        self.destances_polys = self.compute_distance_polys()

    def __len__(self):
        return len(self.region_pairs)


    def compute_distance_regions(self):
        """The distance in units of pixels between two centroids of cloud-objects found by skm.regionprops."""

        dist_x = np.array([c.centroid[1] for c in self.partner1]) - \
                 np.array([c.centroid[1] for c in self.partner2])
        dist_y = np.array([c.centroid[0] for c in self.partner1]) - \
                 np.array([c.centroid[0] for c in self.partner2])
        return np.sqrt(dist_x**2 + dist_y**2)


    def compute_distance_polys(self):
        """The shortest distance in units of pixels between edges of cloud-objects given by shapely.MultiPolygon."""

        return np.array([self.poly_pairs[i][0].distance(self.poly_pairs[i][1]) for i in range(len(self.poly_pairs))])




    def get_distance_regions(self):
        return self.destances_regions

    def get_distance_polys(self):
        return self.destances_polys



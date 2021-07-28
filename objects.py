import numpy as np
#import scipy as sp
import skimage.measure as skm
import shapely.geometry as spg
#import shapely.ops as spo
import timeit
import math

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable




def gen_shortlist(start, inlist):
    """Iterator items starting at 'start', not 0."""
    for j in range(start, len(inlist)):
        yield inlist[j]


def gen_tuplelist(inlist):
    """Tuples of all possible unique pairs in an iterator. For one element only in iterator, yields tuple with two
    times the same item."""
    #print ("\ninlist \n ", inlist , "\n\n")
    if len(inlist) == 1:
        yield inlist[0], inlist[0]
    else:
        for i, item1 in enumerate(inlist):
            #print ("inlist.area ", item1.area )
            for item2 in gen_shortlist(start=i + 1, inlist=inlist):
                yield item1, item2


def gen_tuplelist2(L1, L2):
    """Tuples of all possible unique pairs in an iterator. For one element only in iterator, yields tuple with two
    times the same item. This function defines also the order in which all the pairs are computed hereafter"""

    if len(L1) != len(L2) :
        raise ValueError('Not the same number of regions and polygons')

    for n in range(len(L1)) :
        for m in range(n+1, len(L1)) :
            yield L1[n], L1[m]




def get_objects(sky_scene) :

    labeled = skm.label(sky_scene, background=0 )#, connectivity=1)
    objects = skm.regionprops(labeled)

    #ax = plt.subplot(111)
    #im = ax.imshow(np.flipud(labeled[30:40,500:520]))
    #divider = make_axes_locatable(ax)
    #cax = divider.append_axes("right", size="5%", pad=0.05)
    #plt.colorbar(im, cax=cax), plt.show()

    polys = []
    for o in objects:
        layout = o.image.astype(int)
        bounds = o.bbox
        y_length = bounds[2] - bounds[0]
        x_length = bounds[3] - bounds[1]
        # prepare bed to put layout in
        bed = np.zeros(shape=(y_length + 2, x_length + 2))
        bed[1:-1, 1:-1] = layout
        # get the contour needed for shapely
        contour = skm.find_contours(bed, level=0.5, fully_connected='high')
        # increase coordinates to get placement inside of original input array right
        contour[0][:, 0] += bounds[0]  # increase y-values
        contour[0][:, 1] += bounds[1]  # increase x-values
        # sugar coating needed for shapely (contour only consists of 1 object...anyways)
        coordinates = [tuple(c)  for c in contour[0]]

        m_poly = spg.Polygon(coordinates)
        #print(m_poly.centroid, m_poly.area, m_poly.length, "\n\n")
        polys.append(m_poly)


    return objects, polys



class Pairs:

    def __init__(self, sky_scene):
        self.list_regions, self.list_polys = get_objects(sky_scene)

        self.region_pairs  = list(gen_tuplelist2(self.list_regions, self.list_polys))
        self.poly_pairs = list(gen_tuplelist2(self.list_polys, self.list_polys))

        if self.region_pairs:
            self.partner1, self.partner2 = zip(*self.region_pairs)
        else:
            self.partner1, self.partner2 = [], []

        self.destances_regions = self.compute_distance_regions()
        self.destances_polys = self.compute_distance_polys()



    def __len__(self) :
        return len(self.partner1)


    def compute_distance_regions(self) :
        """The distance in units of pixels between two centroids of cloud-objects found by skm.regionprops."""

        dist_x = np.array([c.centroid[1] for c in self.partner1]) - \
                 np.array([c.centroid[1] for c in self.partner2])
        dist_y = np.array([c.centroid[0] for c in self.partner1]) - \
                 np.array([c.centroid[0] for c in self.partner2])
        return np.sqrt(dist_x**2 + dist_y**2)


    def correct_distance(self, i) :
        """Distance is not well implemented in shapely.geometry. In particular there are case where it is zeros
        The following function corrects those cases"""
        print("\n --- i --- ", i)
        #print("self.partner1[i].coords", self.partner1[i].coords)
        r1_xy = np.array(self.partner1[i].coords)
        r2_xy = np.array(self.partner2[i].coords)
        deltaX = r1_xy[:,0] - r2_xy[:,0][:,None]
        deltaY = r1_xy[:,1] - r2_xy[:,1][:,None]
        return math.sqrt(np.amin(deltaX**2 + deltaY**2)) - 1



    def compute_distance_polys(self):
        """The shortest distance in units of pixels between edges of cloud-objects given by shapely.MultiPolygon."""
        distances = np.array([self.poly_pairs[i][0].distance(self.poly_pairs[i][1]) for i in range(len(self.poly_pairs))])
        for i in np.where(distances==0)[0] :
            print ("index ",i)
            distances[i] = self.correct_distance(i)
        return distances


    def compute_distance_regions_2Darray (self, diagonal_values = 0) :
        dist_x = np.array([c.centroid[1] for c in self.list_regions]) - np.array([c.centroid[1] for c in self.list_regions])[:,None]
        dist_y = np.array([c.centroid[0] for c in self.list_regions]) - np.array([c.centroid[0] for c in self.list_regions])[:,None]
        distances =  np.sqrt(dist_x**2 + dist_y**2)
        """ diagonal have all zeros. Therefore the min() over rows and columns are zeros
        fill_diagonal function set the diagonal to a high value"""
        np.fill_diagonal(distances, diagonal_values)
        return distances



    def get_distance_regions(self) :
        return self.destances_regions

    def get_distance_polys(self) :
        return self.destances_polys

    def get_number_of_regions(self) :
        return len(self.list_regions)


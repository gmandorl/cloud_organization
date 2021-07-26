import xarray as xr
import numpy as np
import datetime
#import functools
#import math as m
import timeit
import skimage.measure as skm
#import scipy as sp
import shapely.geometry as spg
import shapely.ops as spo


import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable

from objects import Pairs
import metrics




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


def get_objects(sky_scene) :

    labeled = skm.label(sky_scene, background=0)  # , connectivity=1)
    objects = skm.regionprops(labeled)

    #ax = plt.subplot(111)
    #im = ax.imshow(np.flipud(labeled))
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



def run_metrics( file_name="") :

    excl_var= ['EPScld', 'Pcld', 'frac_Rain', 'frac_Lay', 'Psurf', 'Tsurf', 'frac_mlow', 'DZ_mlow', 'DZtopCIRS_mlow', 'Ztop_mlow', 'RR_mlow', 'Ptropo', 'cldtyp', 'frac_cldtyp', 'Ptropo', 'RR_Cb', 'RR_Ci', 'RR_thCi', 'DZ_Cb', 'DZ_Ci', 'DZ_thCi', 'DZtopCIRS_Cb', 'DZtopCIRS_Ci', 'DZtopCIRS_thCi', 'EPS_scen', 'MultiLayer', 'P_scen', 'Ztop_Cb', 'Ztop_Ci', 'Ztop_thCi', 'cldtypinHL', 'count_cld', 'frac_Cb', 'frac_Ci', 'frac_cldtypinHL', 'frac_scen', 'frac_thCi', 'landfrac']
    ds = xr.open_dataset(file_name, decode_times=False, drop_variables=excl_var)

    sky_scene = np.where((ds.variables["RainRate"]>0.)*(ds.variables["scen"]==1), 1, 0)
    sky_scene = np.nan_to_num(sky_scene, nan=0.)
    total_number_of_pixels = sky_scene.shape[0]*sky_scene.shape[1]

    list_regions, list_polys = get_objects(sky_scene)


    print ("total_number_of_pixels : ", sky_scene.shape[0], sky_scene.shape[1], total_number_of_pixels)
    #print ("list_regions : ", len(list_regions) ,"\n", list_regions)
    #print ("list_polys : ", len(list_polys) ,"\n", list_polys)

    #all_s_pairs = [Pairs(pairlist=list(gen_tuplelist(cloudlist))) for cloudlist in props_s]
    all_pairs = Pairs(region_pairs=list(gen_tuplelist(list_regions)), poly_pairs=list(gen_tuplelist(list_polys)))

    #print ("all_pairs : ", all_pairs)

    #iorg = metrics.i_org(pairs=all_pairs, objects=list_regions, total_number_of_pixels = total_number_of_pixels)
    iorg = metrics.i_org(pairs=all_pairs, objects=list_regions, total_number_of_pixels = 9841.)

    rom = 6.25 * metrics.radar_organisation_metric(all_pairs)


    fileTXT = open("txt_files/info_"+str(datetime.datetime.now().strftime('%y%m%d_%H%M%S'))+".txt","w")
    fileTXT.write("file name: \t" + file_name + "\n")
    fileTXT.write("rom: \t" + str(rom) + "\n")
    fileTXT.write("iorg: \t" + str(iorg) + "\n\n")
    fileTXT.close()








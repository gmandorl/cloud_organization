import functools
import numpy as np
import scipy as sp
import math
import timeit


#######################################################################################
######################################### I_org #######################################
#######################################################################################

def i_org(all_pairs, total_number_of_pixels = 1):
    """I_org according to [Tompkins et al. 2017]"""

    start = timeit.default_timer()
    objects = all_pairs.list_regions

    if len(all_pairs.partner1) == 0 :
        return np.nan
    if len(all_pairs) == 1:
        if all_pairs.partner1 == all_pairs.partner2:
            return np.nan

    #print("\n\n i_org 00 \n")

    distances = np.array(all_pairs.get_distance_regions())
    #print ("distances ", distances)
    dist_min = []
    print("before")
    dist_min = np.amin(all_pairs.compute_distance_regions_2Darray(diagonal_values = total_number_of_pixels), axis=1)
    print("after")
    #dist_min2 = np.amin(all_pairs.compute_distance_regions_2Darray(diagonal_values = total_number_of_pixels), axis=1)
    allDist = []
    #allDist2 = all_pairs.compute_distance_regions_2Darray(diagonal_values = total_number_of_pixels)
    #print("\n\n i_org 0 \n")

    #faster = True
    #if faster:
        #for cloud in objects:
            ##print("HERE - ", timeit.default_timer() - start)
            ##print("\n\n i_org  \n", cloud, cloud.area, cloud.centroid[0], cloud.centroid[1], len(all_pairs.partner1))
            #dist_min.append(np.array([distances[i] for i, pair in enumerate(all_pairs.region_pairs) if cloud in pair]).min())
            ##allDist.append([distances[i] for i, pair in enumerate(all_pairs.region_pairs) if cloud in pair])
            ##dist_min2 = all_pairs.compute_distance_regions_2Darray.min()
    #else:
        ## maybe faster
        #for cloud in objects:
            #pair_in = np.isin(np.array(all_pairs.region_pairs), cloud, assume_unique=True)
            #pair_one = pair_in[:, 0] + pair_in[:, 1]
            #dist_min.append(distances[pair_one].min())
    #print("\n\n i_org 1 \n")

    #print ("\nCOMPARISON: ---------------- ", len(dist_min), dist_min2.shape)


    #print(allDist)
    #print(allDist2, "\n\n")

    #for n in range(len(dist_min)) :
        #print(dist_min[n] - dist_min2[n])


    # the theoretical Weibull-distribution for n particles
    u_dist_min, u_dist_min_counts = np.unique(dist_min, return_counts=True)
    lamda = all_pairs.get_number_of_regions() / float(total_number_of_pixels)  # one radar scan contains 9841 pixels
    weib_cdf = 1 - np.exp(- lamda * math.pi * u_dist_min**2)
    #print("\n\n i_org 2 \n")

    #print("\n\n i_org \n\n", dist_min, "\n\n", u_dist_min, "\n\n", u_dist_min_counts, "\n\n", lamda, "\n\n", weib_cdf)

    # the CDF from the actual data
    data_cdf = np.cumsum(u_dist_min_counts / np.sum(u_dist_min_counts))
    #print("\n\n data_cdf \n", type(data_cdf), data_cdf)
    #print("\n\n i_org 3 \n")

    # compute the integral between Weibull CDF and data CDF
    weib_cdf = np.append(0, weib_cdf   )
    weib_cdf = np.append(   weib_cdf, 1)
    data_cdf = np.append(0, data_cdf   )
    data_cdf = np.append(   data_cdf, 1)
    #print("\n\n i_org 4 \n")
    #print("\n\n da integrare \n", weib_cdf, data_cdf)
    return sp.integrate.trapz(data_cdf, weib_cdf)



#######################################################################################
######################################### ROME ########################################
#######################################################################################

def _radar_organisation_metric(in_func):
    """ROME according to [Retsch et al. 2020]"""

    @functools.wraps(in_func)
    def wrapper(all_pairs, elliptic=False):
        if len(all_pairs.partner1) == 0 :
            return np.nan

        area_1 = np.float64(np.array([c.area for c in all_pairs.partner1]))
        area_2 = np.float64(np.array([c.area for c in all_pairs.partner2]))
        if elliptic:
            ma_mi_1, ma_mi_2 = in_func(all_pairs)
            area_1 *= ma_mi_1
            area_2 *= ma_mi_2

        large_area = np.maximum(area_1, area_2)
        small_area = np.minimum(area_1, area_2)

        if len(all_pairs) == 1:
            if all_pairs.partner1 == all_pairs.partner2:
                return area_1.item()

        return np.mean(large_area + np.minimum(small_area, (small_area / all_pairs.get_distance_polys())**2))

    return wrapper


@_radar_organisation_metric
def radar_organisation_metric():
    pass


@_radar_organisation_metric
def elliptic_shape_organisation(all_pairs):
    """Ratio of objects major to minor axis given by the region properties. To modify existing metric."""
    major, minor = [], []
    for c in all_pairs.partner1:
        major.append(c.major_axis_length)
        minor.append(c.minor_axis_length)
    ma, mi = np.array(major), np.array(minor)
    ma += 1. #np.where(ma == 0., 1., ma) # non conserva le gerarchie, dovremmo mettere semplicemente +1
    mi += 1. #np.where(mi == 0., 1., mi)
    ma_mi_1 = ma / mi
    major, minor = [], []
    for c in all_pairs.partner2:
        major.append(c.major_axis_length)
        minor.append(c.minor_axis_length)
    ma, mi = np.array(major), np.array(minor)
    ma += 1. # np.where(ma == 0., 1., ma)
    mi += 1. # np.where(mi == 0., 1., mi)
    ma_mi_2 = ma / mi
    return ma_mi_1, ma_mi_2




#######################################################################################
######################################### COP  ########################################
#######################################################################################

def conv_org_pot(all_pairs):
    """The Convective Organisation Potential according to [White et al. 2018]"""
    if len(all_pairs.partner1) == 0 :
        return np.nan
    if len(all_pairs) == 1:
        if all_pairs.partner1 == all_pairs.partner2:
            return np.nan
    diameter_1 = np.array([c.equivalent_diameter for c in all_pairs.partner1])
    diameter_2 = np.array([c.equivalent_diameter for c in all_pairs.partner2])
    v = np.array(0.5 * (diameter_1 + diameter_2) / all_pairs.get_distance_regions())
    return np.sum(v) / len(all_pairs.partner1)





#######################################################################################
######################################### SCAI ########################################
#######################################################################################

def simple_convective_aggregation_metric(all_pairs, total_number_of_pixels = 1):
    """SCAI according to [Tobin et al. 2013]"""
    if len(all_pairs.partner1) == 0:
        return np.nan
    if len(all_pairs) == 1:
        if all_pairs.partner1 == all_pairs.partner2:
            return np.nan

    #n_max = 6844  # 117**2 / 2
    d_0 = np.exp(np.log(all_pairs.get_distance_regions()).sum() / len(all_pairs))
    l = 117
    #return all_pairs.get_number_of_regions() / n_max * d_0 / l * 1000
    return all_pairs.get_number_of_regions() / (total_number_of_pixels**1.5) * d_0 * 1000






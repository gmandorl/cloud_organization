import functools
import numpy as np
import scipy as sp
import math



def i_org(pairs, objects, total_number_of_pixels = 1):
    """I_org according to [Tompkins et al. 2017]"""
    if not pairs.region_pairs:
        return np.nan
    if len(pairs) == 1:
        if pairs.partner1 == pairs.partner2:
            return np.nan

    #print("\n\n i_org 00 \n")

    distances = np.array(pairs.get_distance_regions())
    dist_min = []
    #print("\n\n i_org 0 \n")

    faster = True
    if faster:
        for cloud in objects:
            #print("\n\n i_org  \n", cloud, len(pairs.region_pairs))
            dist_min.append(np.array([distances[i] for i, pair in enumerate(pairs.region_pairs) if cloud in pair]).min())
    else:
        # maybe faster
        for cloud in objects:
            pair_in = np.isin(np.array(pairs.region_pairs), cloud, assume_unique=True)
            pair_one = pair_in[:, 0] + pair_in[:, 1]
            dist_min.append(distances[pair_one].min())
    #print("\n\n i_org 1 \n")

    # the theoretical Weibull-distribution for n particles
    u_dist_min, u_dist_min_counts = np.unique(dist_min, return_counts=True)
    lamda = len(objects) / float(total_number_of_pixels)  # one radar scan contains 9841 pixels
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
    cdf_integral = sp.integrate.cumtrapz(data_cdf, weib_cdf, initial=0)
    return cdf_integral[-1]  # ---- equivalent to return sp.integrate.trapz(data_cdf, weib_cdf)



def _radar_organisation_metric(in_func):
    """Decorator for metric ROM."""

    @functools.wraps(in_func)
    def wrapper(all_pairs, elliptic=False):
        if not all_pairs.region_pairs:
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
    """Ratio of objects major to minor axis given by the .regionprop properties. To modify existing metric."""
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




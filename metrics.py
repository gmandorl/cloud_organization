import numpy as np
import scipy as sp
import math



def i_org(pairs, objects, total_number_of_pixels = 1):
    """I_org according to [Tompkins et al. 2017]"""
    if not pairs.pairlist:
        return np.nan
    if len(pairs) == 1:
        if pairs.partner1 == pairs.partner2:
            return np.nan

    print("\n\n i_org 00 \n")

    distances = np.array(pairs.distance_regionprops())
    dist_min = []
    print("\n\n i_org 0 \n")

    faster = True
    if faster:
        for cloud in objects:
            print("\n\n i_org  \n", cloud, len(pairs.pairlist))
            dist_min.append(np.array([distances[i] for i, pair in enumerate(pairs.pairlist) if cloud in pair]).min())
    else:
        # maybe faster
        for cloud in objects:
            pair_in = np.isin(np.array(pairs.pairlist), cloud, assume_unique=True)
            pair_one = pair_in[:, 0] + pair_in[:, 1]
            dist_min.append(distances[pair_one].min())
    print("\n\n i_org 1 \n")

    # the theoretical Weibull-distribution for n particles
    u_dist_min, u_dist_min_counts = np.unique(dist_min, return_counts=True)
    lamda = len(objects) / float(total_number_of_pixels)  # one radar scan contains 9841 pixels
    weib_cdf = 1 - np.exp(- lamda * math.pi * u_dist_min**2)
    print("\n\n i_org 2 \n")

    #print("\n\n i_org \n\n", dist_min, "\n\n", u_dist_min, "\n\n", u_dist_min_counts, "\n\n", lamda, "\n\n", weib_cdf)

    # the CDF from the actual data
    data_cdf = np.cumsum(u_dist_min_counts / np.sum(u_dist_min_counts))
    #print("\n\n data_cdf \n", type(data_cdf), data_cdf)
    print("\n\n i_org 3 \n")

    # compute the integral between Weibull CDF and data CDF
    weib_cdf = np.append(0, weib_cdf   )
    weib_cdf = np.append(   weib_cdf, 1)
    data_cdf = np.append(0, data_cdf   )
    data_cdf = np.append(   data_cdf, 1)
    print("\n\n i_org 4 \n")
    #print("\n\n da integrare \n", weib_cdf, data_cdf)
    cdf_integral = sp.integrate.cumtrapz(data_cdf, weib_cdf, initial=0)
    return cdf_integral[-1]  # ---- equivalent to return sp.integrate.trapz(data_cdf, weib_cdf)

import xarray as xr
import numpy as np
import datetime
import functools
import math as m
#import matplotlib.pyplot as plt
import timeit
import skimage.measure as skm
import scipy as sp
import shapely.geometry as spg
import shapely.ops as spo




def run_metrics( file_name="") :

    excl_var= ['EPScld', 'Pcld', 'frac_Rain', 'frac_Lay', 'Psurf', 'Tsurf', 'frac_mlow', 'DZ_mlow', 'DZtopCIRS_mlow', 'Ztop_mlow', 'RR_mlow', 'Ptropo', 'cldtyp', 'frac_cldtyp', 'Ptropo', 'RR_Cb', 'RR_Ci', 'RR_thCi', 'DZ_Cb', 'DZ_Ci', 'DZ_thCi', 'DZtopCIRS_Cb', 'DZtopCIRS_Ci', 'DZtopCIRS_thCi', 'EPS_scen', 'MultiLayer', 'P_scen', 'Ztop_Cb', 'Ztop_Ci', 'Ztop_thCi', 'cldtypinHL', 'count_cld', 'frac_Cb', 'frac_Ci', 'frac_cldtypinHL', 'frac_scen', 'frac_thCi', 'landfrac']
    ds = xr.open_dataset(file_name, decode_times=False, drop_variables=excl_var)







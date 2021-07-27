import xarray as xr
import numpy as np
import datetime
import timeit


from objects import Pairs
import metrics






def run_metrics( file_name="") :



    excl_var= ['EPScld', 'Pcld', 'frac_Rain', 'frac_Lay', 'Psurf', 'Tsurf', 'frac_mlow', 'DZ_mlow', 'DZtopCIRS_mlow', 'Ztop_mlow', 'RR_mlow', 'Ptropo', 'cldtyp', 'frac_cldtyp', 'Ptropo', 'RR_Cb', 'RR_Ci', 'RR_thCi', 'DZ_Cb', 'DZ_Ci', 'DZ_thCi', 'DZtopCIRS_Cb', 'DZtopCIRS_Ci', 'DZtopCIRS_thCi', 'EPS_scen', 'MultiLayer', 'P_scen', 'Ztop_Cb', 'Ztop_Ci', 'Ztop_thCi', 'cldtypinHL', 'count_cld', 'frac_Cb', 'frac_Ci', 'frac_cldtypinHL', 'frac_scen', 'frac_thCi', 'landfrac']
    ds = xr.open_dataset(file_name, decode_times=False, drop_variables=excl_var)

    sky_scene = np.where((ds.variables["RainRate"]>0.)*(ds.variables["scen"]==1), 1, 0)
    sky_scene = np.nan_to_num(sky_scene, nan=0.)
    total_number_of_pixels = sky_scene.shape[0]*sky_scene.shape[1]

    #list_regions, list_polys = get_objects(sky_scene)



    print ("total_number_of_pixels : ", sky_scene.shape[0], sky_scene.shape[1], total_number_of_pixels)
    #print ("list_regions : ", len(list_regions) ,"\n", list_regions)
    #print ("list_polys : ", len(list_polys) ,"\n", list_polys)

    #all_s_pairs = [Pairs(pairlist=list(gen_tuplelist(cloudlist))) for cloudlist in props_s]
    #all_pairs = Pairs(region_pairs=list(gen_tuplelist(list_regions)), poly_pairs=list(gen_tuplelist(list_polys)))
    all_pairs = Pairs(sky_scene)

    #------------------ METRICS ---------------------

    #iorg    = metrics.i_org(all_pairs, total_number_of_pixels = 9841.)
    iorg    = metrics.i_org(all_pairs, total_number_of_pixels)
    rom     = 6.25 * metrics.radar_organisation_metric(all_pairs)
    rom_el  = 6.25 * metrics.elliptic_shape_organisation(all_pairs, elliptic = True)
    scai    = metrics.simple_convective_aggregation_metric(all_pairs, total_number_of_pixels)
    cop     = metrics.conv_org_pot(all_pairs)

    #-------------- OTHER PROPERTIES ----------------

    cloud_number = all_pairs.get_number_of_regions()
    total_area = np.array([c.area for c in all_pairs.list_regions]).sum()
    cloud_max_area = np.array([c.area for c in all_pairs.list_regions]).max()

    fileTXT = open("txt_files3/info_"+str(datetime.datetime.now().strftime('%y%m%d_%H%M%S'))+".txt","w")
    fileTXT.write("file name: \t" + file_name + "\n")
    fileTXT.write("rom: \t" + str(rom) + "\n")
    fileTXT.write("iorg: \t" + str(iorg) + "\n")
    fileTXT.write("COP: \t" + str(cop) + "\n")
    fileTXT.write("SCAI: \t" + str(scai) + "\n\n")
    fileTXT.close()

    #print("metrics: ", iorg, rom, rom_el, scai, cop, cloud_number, total_area, cloud_max_area)

    ds_m = xr.Dataset({'cop':       (("time"), np.ones(1)*cop),
                       'rom_el':    (("time"), np.ones(1)*rom_el),
                       'rom':       (("time"), np.ones(1)*rom),
                       'iorg':      (("time"), np.ones(1)*iorg),
                       'scai':      (("time"), np.ones(1)*scai),
                       #'rom_el': rom_el,
                       #'rom': rom,
                       #'iorg': iorg,
                       #'scai': scai,
                       'cloud_number':      (("time"), np.ones(1)*cloud_number),
                       'total_area':        (("time"), np.ones(1)*total_area),
                       'cloud_max_area':    (("time"), np.ones(1)*cloud_max_area),
                       },
                     #coords={"time": [datetime.datetime(2008, 1, 3)],}
                     coords={"time": [datetime.datetime.now()],}
    )


    return ds_m






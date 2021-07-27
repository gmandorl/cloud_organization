import timeit
from run_metrics import *
import argparse

parser = argparse.ArgumentParser()
#parser.add_argument("model", help="model to plot")
parser.add_argument("-o", "--outfolder",default="output",help="fgure output folder folder")
#parser.print_help()
args = parser.parse_args()


if __name__ == '__main__':
    # c = Client()
    start = timeit.default_timer()

    ds_m = []
    #ds_m.append(run_metrics( file_name ="/home/gmandorli/firstProject/clds_AIRS-ERAI_vertical_0130AM_20080103_smallsmallSLICE.nc"))
    #ds_m.append(run_metrics( file_name ="/home/gmandorli/firstProject/clds_AIRS-ERAI_vertical_0130AM_20080103_smallSLICE.nc"))
    #ds_m.append(run_metrics( file_name ="/home/gmandorli/firstProject/clds_AIRS-ERAI_vertical_0130AM_20080103_tinySLICE.nc"))
    #ds_m.append(run_metrics( file_name ="/home/gmandorli/firstProject/clds_AIRS-ERAI_vertical_0130AM_20080103_SLICE.nc"))
    ds_m.append(run_metrics("/bdd/ARA/GEWEX_CA_ftp/deep_learning/results_phase2/2008/01/clds_AIRS-ERAI_vertical_0130AM_20080103.nc"))
    #ds_m.append(run_metrics("/bdd/ARA/GEWEX_CA_ftp/deep_learning/results_phase2/2016/01/clds_AIRS-ERAI_vertical_0130AM_20160117.nc"))

    #list_of_files = []
    #path = "/bdd/ARA/GEWEX_CA_ftp/deep_learning/results_phase2/2008/01/clds_AIRS-ERAI_vertical_0130AM_200801"
    #for n in range(1,2) :
        #f = path+("0" if n<10 else "")+str(n)+".nc"
        #list_of_files.append(f)
        #ds_m.append(run_metrics( file_name = f))

    #for f in list_of_files : ds_m.append(run_metrics( file_name = f))


    ds_m = xr.merge(ds_m)
    ds_m.to_netcdf(args.outfolder+'/test.nc')

    stop = timeit.default_timer()
    print('This script needed {} seconds.'.format(stop-start))


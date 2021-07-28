import timeit
from run_metrics import *
import argparse
import subprocess
import glob



parser = argparse.ArgumentParser()
#parser.add_argument("model", help="model to plot")
parser.add_argument("-o", "--outfolder",default="output",help="fgure output folder folder")
#parser.print_help()
args = parser.parse_args()


def find_date(file_name_str, time) :
    date_str = file_name_str.split("_")[-1]
    date_str = date_str.split(".")[0]
    return datetime.datetime.strptime(date_str+time, '%Y%m%d%I%M%p')


def get_list_of_files_and_date (path       = "/bdd/ARA/GEWEX_CA_ftp/deep_learning/results_phase2/",
                                f_name     = "clds_AIRS-ERAI_vertical",
                                time       = "0130AM",
                                first_date = "01/01/2008",
                                last_date  = "10/01/2008"
                               ) :

    file_names = glob.glob(path + '*/*/' + f_name + '_' + time + '*.nc')
    first_date = datetime.datetime.strptime(first_date, '%d/%m/%Y')
    last_date  = datetime.datetime.strptime(last_date,  '%d/%m/%Y')

    inputs = []
    for fname in file_names :
        date = find_date(fname, time)
        if date >= first_date and date <= last_date :
            inputs.append({"name": fname, "date": date})

    return inputs






if __name__ == '__main__':
    # c = Client()
    start = timeit.default_timer()

    ds_m = []
    #ds_m.append(run_metrics( file_name ="/home/gmandorli/firstProject/clds_AIRS-ERAI_vertical_0130AM_20080103_smallsmallSLICE.nc"))
    #ds_m.append(run_metrics( file_name ="/home/gmandorli/firstProject/clds_AIRS-ERAI_vertical_0130AM_20080103_smallSLICE.nc"))
    #ds_m.append(run_metrics( file_name ="/home/gmandorli/firstProject/clds_AIRS-ERAI_vertical_0130AM_20080103_tinySLICE.nc"))
    #ds_m.append(run_metrics( file_name ="/home/gmandorli/firstProject/clds_AIRS-ERAI_vertical_0130AM_20080103_SLICE.nc"))
    #ds_m.append(run_metrics("/bdd/ARA/GEWEX_CA_ftp/deep_learning/results_phase2/2008/01/clds_AIRS-ERAI_vertical_0130AM_20080103.nc"))
    #ds_m.append(run_metrics("/bdd/ARA/GEWEX_CA_ftp/deep_learning/results_phase2/2016/01/clds_AIRS-ERAI_vertical_0130AM_20160117.nc"))

    inputs = get_list_of_files_and_date()
    for n in range(len(inputs)) :
        print (inputs[n])
        ds_m.append(run_metrics( file_name = inputs[n]["name"], data_LT = inputs[n]["date"]))




    ds_m = xr.merge(ds_m)
    ds_m.to_netcdf(args.outfolder+'/test.nc')

    stop = timeit.default_timer()
    print('This script needed {} seconds.'.format(stop-start))


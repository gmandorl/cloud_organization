import timeit
from run_metrics import run_metrics



if __name__ == '__main__':
    # c = Client()
    start = timeit.default_timer()

    run_metrics( file_name ="/home/gmandorli/firstProject/clds_AIRS-ERAI_vertical_0130AM_20080103_smallsmallSLICE.nc")
    #run_metrics( file_name ="/home/gmandorli/firstProject/clds_AIRS-ERAI_vertical_0130AM_20080103_smallSLICE.nc")

    stop = timeit.default_timer()
    print('This script needed {} seconds.'.format(stop-start))


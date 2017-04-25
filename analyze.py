from scipy import stats
import numpy as np

my_data = np.genfromtxt('data/GLB.Ts+dSST.csv', delimiter=',', skip_header=2)

base_year = 1880
start_year = 1950
end_year =   2016

years = np.array(range(start_year - base_year,end_year - base_year + 1))
# I think 13 is the annual average column...
annual_averaged_anomoly = my_data[start_year - base_year:end_year - base_year + 1][:,13]


# Basically copied from the second answer here:
# https://stackoverflow.com/questions/36400419/how-to-calculate-the-99-confidence-interval-for-the-slope-in-a-linear-regressio
# Not the best answer, but uses only numpy/scipy.
def calc_ci(x, y, n_stds):
    slope,intercept,r_value,p_value,std_err = stats.linregress(x,y)
    confidence_interval = [slope-n_stds*std_err,slope+n_stds*std_err]
    return confidence_interval

if __name__=='__main__':
    # If n were large enough, 1.96 would correspond to a 95% CI
    # However, n is pretty small here.
    # Following comments in the SO post mentioned above, the following URL
    # http://www.graphpad.com/guides/prism/6/statistics/index.htm?confidence_intervals.htm
    # suggests for n ~ 50 as here, a value of 2 is probably more appropriate.
    # Basically only pay attention to the most significant digit.
    n_stds = 2
    ci = calc_ci(years, annual_averaged_anomoly, n_stds)
    print "Slope: ", (ci[0] + ci[1]) / 2
    print "CI: ", ci


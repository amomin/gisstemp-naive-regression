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
    # n is not very large here, say roughly n ~ 50
    # But n_stds=2 still gives a roughly a 95% confidence interval so
    # good enough for our purposes.
    # FWIW n_std = 3 would still easily exclude 0.
    n_stds = 2
    ci = calc_ci(years, annual_averaged_anomoly, n_stds)
    print "Slope: ", (ci[0] + ci[1]) / 2
    print "CI: ", ci

from scipy import stats
from termcolor import colored
import numpy as np
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--start", dest="start_year", type='int', default=1950,
                  help="Start year for slope window", metavar="START")
parser.add_option("-e", "--end", dest="end_year", type='int', default=2016,
                  help="End year for slope window", metavar="END")
parser.add_option("-w", "--window", type='int', dest="window", default=None,
                  help="Specify a window")

(options, args) = parser.parse_args()
# Turn options Values into dictionary.
options = vars(options)
print options, args

my_data = np.genfromtxt('data/GLB.Ts+dSST.csv', delimiter=',', skip_header=2)

base_year = 1880

# Basically copied from the second answer here:
# https://stackoverflow.com/questions/36400419/how-to-calculate-the-99-confidence-interval-for-the-slope-in-a-linear-regressio
# Not the best answer, but uses only numpy/scipy.
def calc_ci(x, y, n_stds):
    slope,intercept,r_value,p_value,std_err = stats.linregress(x,y)
    confidence_interval = [slope-n_stds*std_err,slope+n_stds*std_err]
    return confidence_interval

if __name__=='__main__':
    start_year = int(options['start_year'])
    end_year = int(options['end_year'])
    window = end_year - start_year
    if options['window'] != None and options['window'] < end_year - start_year:
        window = options['window']        
        

    for i in range(start_year, end_year - window + 1):
        j = i + window

        years = np.array(range(i - base_year,j - base_year + 1))
        # I think 13 is the annual average column...
        annual_averaged_anomoly = my_data[i - base_year:j - base_year + 1][:,13]
        # n is not very large here, say roughly n ~ 50
        # But n_stds=2 still gives a roughly a 95% confidence interval so
        # good enough for our purposes.
        # FWIW n_std = 3 would still easily exclude 0.
        n_stds = 2
        ci = calc_ci(years, annual_averaged_anomoly, n_stds)

        print "Years: %d to %d" % (i, j)
        print "\tSlope:", colored("%.02f" % (100*(ci[0] + ci[1]) / 2), 'red'), \
              "degrees C per century"
        print "\tCI: [%.02f C/100y, %.02f C/100y]" % (100*ci[0], 100*ci[1])

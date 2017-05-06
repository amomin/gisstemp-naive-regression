from scipy import stats
import numpy as np

def calc_ci(x, y, n_stds):
    slope,intercept,r_value,p_value,std_err = stats.linregress(x,y)
    confidence_interval = [slope-n_stds*std_err,slope+n_stds*std_err]
    return confidence_interval

N = 100
c = 0.0

s = 1880
base_temp = -0.5
dCpC = 1.6
l = 50
noise = 1.5

for i in range(0,N):
    xs = np.array(range(s, s+l))
    ys = np.array([base_temp] * l) + \
         (dCpC / 100.0) * np.array(range(0, l)) + \
         noise * np.random.rand(1, l)

    ci = calc_ci(xs, ys, 2)
    if ci[0] < 0 and ci[1] > 0:
        c += 1

print "Increase by %.02f degC/Cent, %d year intervals %d times, noise=%.02f" \
      % (dCpC, l, N, noise)
print "Fraction of times 0 is in the CI:", c / N

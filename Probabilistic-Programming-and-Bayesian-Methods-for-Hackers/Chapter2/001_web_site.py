import pymc as pm
from IPython.core.pylabtools import figsize
from matplotlib import pyplot as plt

p = pm.Uniform('p', lower=0, upper=1)

p_ture = 0.05 # unknown in reality
N = 1500

# sample N Bernoulli random variables from Ber(0.05)
# each random variable has a 0.05 chance of being a 1.
# this is the data-generation step
occurrences = pm.rbernoulli(p_ture, N)

print occurrences
print occurrences.sum()

print "What is the observed frequency in Group A? %.4f" % occurrences.mean()
print "Does this equal the true frequency? %s" % (occurrences.mean() == p_ture)

# include the boservations, which are Bernoulli
obs = pm.Bernoulli('obs', p, value=occurrences, observed=True)

mcmc = pm.MCMC([p,obs])
mcmc.sample(18000, 1000)

figsize(12.5, 4)
plt.title("Posterior distribution of $p_A$, the true effectiveness of site A")
plt.vlines(p_ture, 0, 90, linestyle="--", label="true $p_A$ (unknown)")
plt.hist(mcmc.trace('p')[:], bins=25, histtype="stepfilled", normed=True)
plt.legend()
plt.show()
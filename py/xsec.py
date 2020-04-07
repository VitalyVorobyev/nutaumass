#! /usr/bin/env python

""" e+e- -> tau+ tau- cross section tools """

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

mtau = 1776.86
mpip = 139.57061
me = 0.5
alpha = 1 / 137

gev_to_mb = 0.389379  # 1 hbar^2 * c^2 * GeV^{-2} = 0.389379 mb
sigma0 = 4 * np.pi * alpha**2 / 3. * 10**12 * gev_to_mb

def velocity(s, m=mtau):
    """ """
    return np.sqrt(1-4*m**2/s)

def xsec_tree_level(x, bias=0):
    """ Lower oeder QED calculation """
    f = np.zeros(x.shape)
    mask = x > (2*mtau + bias)
    s = (x - bias)[mask]**2
    v = velocity(s)
    f[mask] = sigma0 * 0.5 * v * (3-v**2) / s
    return f

def convolve(x, s, sigma=3, pdf=stats.norm.pdf):
    """ Discrete convolution with Gaussian resolution """
    return np.dot(s, pdf(x.reshape(1,-1) - x.reshape(-1,1), scale=sigma)) * (x[1] - x[0])

def approx(x, thr, zero, a0, a1, pow):
    """ """
    f = np.zeros(x.shape)
    mask = x > 2*mtau + thr
    xi = (x - 2*mtau - thr)[mask]
    f[mask] = zero + (a0*xi + a1*xi**2) * xi**pow
    return f

def main():
    """ Unit test """
    print(f'{0.25 * sigma0 * 10**-6} nb / [E(GeV)]^2')
    plt.figure(figsize=(6,6))

    sqrts = np.linspace(2*mtau-20, 2*mtau+30, 500)
    s = xsec_tree_level(sqrts)
    plt.plot(sqrts, s, label='Born xsec')
    plt.plot(sqrts, convolve(sqrts, s), label='Born with beam energy spread')
    plt.xlim((2*mtau-6, 2*mtau+12))
    plt.ylim((0., 1.))
    plt.legend(loc='best')
    plt.grid()
    plt.tight_layout()
    plt.show()
    

if __name__ == '__main__':
    main()

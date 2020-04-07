#! /usr/bin/env python

""" Phase-space Monte-Carlo event generator """

import numpy as np
import matplotlib.pyplot as plt
import phasespace as phsp

mtau = 1776.86
mpip = 139.57061

def masses_3pi(mnu):
    """ Masses """
    return (mtau, [mpip, mpip, mpip, mnu])

def generate_tau_decay(mo, chs, n):
    """ returns (weights, particles) """
    return phsp.nbody_decay(mo, chs).generate(n_events=n)

def random_unit_vector():
    """ """
    pass

def boost_matrix(boost_vector):
    """ ___       Boost matrix                                ___
        |  g         -g*b*nx         -g*b*ny        -g*b*nz     |
        | -g*b*nx  1+(g-1)*nx^2      (g-1)*nx*ny    (g-1)*nx*nz |
        | -g*b*ny    (g-1)*ny*nx   1+(g-1)*ny^2     (g-1)*ny*nz |
        | -g*b*nz    (g-1)*nz*nx     (g-1)*nz*ny  1+(g-1)*nz^2  |
        ___                                                   ___
    """
    pass

def boost(events, boosts):
    """ """
    pass

def boost_to_lab_frame(events, sqrts, sigma):
    """ Events in tau frame to lab frame
        sqrts = sqrt(s), with the Mandelstam variable s
        sigma - Gaussian beam energy spread
    """
    N = events['p_0'].shape[0]
    debeam = sigma*np.random.randn(N)
    

def main():
    """ Unit test """
    mtau, mchs = masses_3pi(0.)
    weights, particles = generate_tau_decay(mtau, mchs, 10**3)
    print(weights)
    print(particles)

if __name__ == '__main__':
    main()

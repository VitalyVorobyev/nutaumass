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

def generate(mo, chs, n):
    """ returns (weights, particles) """
    return phsp.nbody_decay(mo, chs).generate(n_events=n)

def 

def gen_tautau(s, m_nu):
    """ e+e- -> tau+ tau- decay """
    pip1 = phsp.GenParticle('pi+_tau+_1', mpip)
    pip2 = phsp.GenParticle('pi+_tau+_1', mpip)
    kaon = phsp.GenParticle('K+', KAON_MASS)
    kstar = phsp.GenParticle('K*', KSTARZ_MASS).set_children(pion, kaon)
    gamma = phsp.GenParticle('gamma', 0)
    bz = GenParticle('B0', B0_MASS).set_children(kstar, gamma)

weights, particles = bz.generate(n_events=1000)

def main():
    """ Unit test """
    mtau, mchs = masses_3pi(0.)
    weights, particles = generate(mtau, mchs, 10**3)
    print(weights)
    print(particles)

if __name__ == '__main__':
    main()

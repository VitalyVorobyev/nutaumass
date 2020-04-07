#! /usr/bin/env python

""" e+e- -> tau+ tau- cross section tools """

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Slider

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
    mask = x > 2*mtau + bias
    s = (x - bias)[mask]**2
    v = velocity(s)
    f[mask] = sigma0 * 0.5 * v * (3-v**2) / s
    return f

def approx(x, zero, a0, a1, pow, bias=0):
    """ """
    f = np.zeros(x.shape)
    mask = x > 2*mtau + bias
    xi = (x - 2*mtau - bias)[mask]
    f[mask] = zero + (a0*xi + a1*xi**2) * xi**pow
    return f

def run():
    """ """
    fname='xsec.png'

    ithr = 0.395
    izero = 0.120
    ia1, ia2 = 0.1162, -5.641
    ipow = -0.154
    ia2 *= 10**-3

    fig, ax = plt.subplots(figsize=(6,6))
    image = mpimg.imread(fname)
    ax.imshow(image, extent=[3552, 3562, 0.0, 0.7], aspect=10)
    sqrts = np.linspace(2*mtau, 2*mtau+8, 250)
    born, = plt.plot(sqrts, xsec_tree_level(sqrts, ithr))
    appr, = plt.plot(sqrts, approx(sqrts, izero, ia1, ia2, ipow, ithr))
    plt.ylim((0., 0.7))
    plt.tight_layout()
    plt.grid()

    plt.subplots_adjust(left=0.1, bottom=0.25)

    axcolor = 'lightgoldenrodyellow'
    axpo = plt.axes([0.15, 0.23, 0.65, 0.03], facecolor=axcolor)
    axth = plt.axes([0.15, 0.18, 0.65, 0.03], facecolor=axcolor)
    axze = plt.axes([0.15, 0.13, 0.65, 0.03], facecolor=axcolor)
    axa1 = plt.axes([0.15, 0.08, 0.65, 0.03], facecolor=axcolor)
    axa2 = plt.axes([0.15, 0.03, 0.65, 0.03], facecolor=axcolor)

    spo = Slider(axpo, 'power', -5, 5,     valinit=ipow,  valfmt='%1.3f')
    sth = Slider(axth, 'thr', -0.50, 0.50, valinit=ithr,  valfmt='%1.3f')
    sze = Slider(axze, 'zero', 0.00, 0.15, valinit=izero, valfmt='%1.3f')
    sa1 = Slider(axa1, 'a1',  -0.1, 0.2,   valinit=ia1,   valfmt='%1.4f')
    sa2 = Slider(axa2, r'a2 ($10^{-3}$)',  -10, 10, valinit=ia2*10**3,   valfmt='%1.3f')

    def update(val):
        ithr, izero, ia1, ia2, ipow = [x.val for x in [sth, sze, sa1, sa2, spo]]
        ia2 *= 10**-3
        born.set_ydata(xsec_tree_level(sqrts, ithr))
        appr.set_ydata(approx(sqrts, izero, ia1, ia2, ipow, ithr))
        fig.canvas.draw_idle()

    sth.on_changed(update)
    sze.on_changed(update)
    sa1.on_changed(update)
    sa2.on_changed(update)
    spo.on_changed(update)

    plt.show()

def main():
    """ Unit test """
    print(f'{gev_to_mb * sigma0 * 0.25 * 10**-6} nb / [E(GeV)]^2')
    run()

if __name__ == '__main__':
    main()

import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate

def make_plots():
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    for trans,lam in zip(transmission_list,tlam_list):
        ax1.plot(lam,trans,color='DodgerBlue',alpha=0.6)
    for emis in emission_list:
        ax2.plot(lamda_list,emis,color='FireBrick',alpha=0.6)
    plt.xlim(6450,7000)
    plt.ylim(0,1)
    ax1.set_ylabel('Transmission %')
    ax1.set_xlabel('Wavelength [Angst]')
    ax2.set_ylabel('Emission [Normalized]')
    plt.show()


line_list = [6548.,6563.,6584.]
line_str_list = [0.3,0.7,1.0]
lamda_list = np.arange(6450,7000,1)
line_width = 4
redshift = 0.05
emission_list = []
for line,lstr in zip(line_list,line_str_list):
    emis = lstr * np.exp( - (lamda_list - (line * (1. + redshift)))**2 / (line_width**2))
    emission_list.append(emis)

emission_list /= np.max(emission_list)

filter_list = ['CTIO.6520-76.dat','CTIO.6563-78.dat','CTIO.6606-75.dat','CTIO.6649-76.dat','CTIO.6693-76.dat','CTIO.6737-76.dat','CTIO.6781-78.dat','CTIO.6826-78.dat','CTIO.6871-78.dat']
filter_short = {'CTIO.6520-76.dat':'6520-76','CTIO.6563-78.dat':'6563-78','CTIO.6606-75.dat':'6606-75','CTIO.6649-76.dat':'6649-76','CTIO.6693-76.dat':'6693-76','CTIO.6737-76.dat':'6737-76','CTIO.6781-78.dat':'6781-78','CTIO.6826-78.dat':'6826-78','CTIO.6871-78.dat':'6871-78'}
filter_direc = 'Filters/'
transmission_list = []
for fltr in filter_list:
    lam,trans = np.loadtxt(filter_direc+fltr,unpack=True)
    f = interpolate.interp1d(lam,trans,bounds_error=False,fill_value=0.)
    full_trans = f(lamda_list)
    transmission_list.append(full_trans)


if True:
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    for trans in transmission_list:
        ax1.plot(lamda_list,trans,color='DodgerBlue',alpha=0.6)
    for emis in emission_list:
        ax2.plot(lamda_list,emis,color='FireBrick',alpha=0.6)
    plt.xlim(6450,7000)
    plt.ylim(0,1)
    ax1.set_ylabel('Transmission %')
    ax1.set_xlabel('Wavelength [Angst]')
    ax2.set_ylabel('Emission [Normalized]')
    plt.show()



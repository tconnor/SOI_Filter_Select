import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate

def make_plots(transmission_list,emission_list,lamda_list,galname):
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
    plt.savefig('allfilters_'+galname+'.png',dpi=100)

def make_select_plots(transmission_list,emission_list,lamda_list,galname,on_idx,off_idx,filter_list,filter_short):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.fill_between(lamda_list,transmission_list[on_idx],color='DarkSeaGreen',alpha=0.6)
    ax1.fill_between(lamda_list,transmission_list[off_idx],color='DodgerBlue',alpha=0.6)
    for emis in emission_list:
        ax2.plot(lamda_list,emis,color='FireBrick',alpha=0.6)
    plt.xlim(6450,7000)
    plt.ylim(0,1)
    ax1.set_ylabel('Transmission %')
    ax1.set_xlabel('Wavelength [Angst]')
    ax2.set_ylabel('Emission [Normalized]')
    ax1.text(6500,0.8,filter_short[filter_list[on_idx]],color='DarkSeaGreen')
    ax1.text(6500,0.725,filter_short[filter_list[off_idx]],color='DodgerBlue')
    plt.savefig('selectfilters_'+galname+'.png',dpi=100)

def make_transmission_curves(filter_list,filter_direc,lamda_list):
    transmission_list = []
    for fltr in filter_list:
        lam,trans = np.loadtxt(filter_direc+fltr,unpack=True)
        f = interpolate.interp1d(lam,trans,bounds_error=False,fill_value=0.)
        full_trans = f(lamda_list)
        transmission_list.append(full_trans)
    return transmission_list

def make_emission_curves(line_list,line_str_list,line_width,lamda_list,redshift):
    emission_list = []
    for line,lstr in zip(line_list,line_str_list):
        emis = lstr * np.exp( - (lamda_list - (line * (1. + redshift)))**2 / (line_width**2))
        emission_list.append(emis)
    emission_list /= np.max(emission_list)
    return emission_list

def run_galaxy(line_pars,filter_pars,galname,redshift,max_through,lamda_list):
    line_list,line_str_list,line_width = line_pars
    filter_list,filter_short,filter_direc = filter_pars
    emission_list = make_emission_curves(line_list,line_str_list,line_width,lamda_list,redshift)
    transmission_list = make_transmission_curves(filter_list,filter_direc,lamda_list)
    make_plots(transmission_list,emission_list,lamda_list,galname)
    throughput_list = []
    off_throughput_list = []
    for trans in transmission_list:
        throughput = np.sum(trans * emission_list)
        throughput_list.append(throughput)
        if throughput > max_through:
            off_throughput_list.append(0)
        else:
            off_throughput_list.append(throughput)
    on_idx = throughput_list.index(max(throughput_list))
    off_idx = off_throughput_list.index(max(off_throughput_list))
    make_select_plots(transmission_list,emission_list,lamda_list,galname,on_idx,off_idx,filter_list,filter_short)
    return



def main(catfile):
    filter_list = ['CTIO.6520-76.dat','CTIO.6563-78.dat','CTIO.6606-75.dat','CTIO.6649-76.dat','CTIO.6693-76.dat','CTIO.6737-76.dat','CTIO.6781-78.dat','CTIO.6826-78.dat','CTIO.6871-78.dat']
    filter_short = {'CTIO.6520-76.dat':'6520-76','CTIO.6563-78.dat':'6563-78','CTIO.6606-75.dat':'6606-75','CTIO.6649-76.dat':'6649-76','CTIO.6693-76.dat':'6693-76','CTIO.6737-76.dat':'6737-76','CTIO.6781-78.dat':'6781-78','CTIO.6826-78.dat':'6826-78','CTIO.6871-78.dat':'6871-78'}
    filter_direc = 'Filters/'

    line_list = [6548.,6563.,6584.]
    line_str_list = [0.3,0.7,0.9]
    line_width = 4
    line_pars = [line_list,line_str_list,line_width]
    filter_pars = [filter_list,filter_short,filter_direc]
    lamda_list = np.arange(6450,7000,1)
    max_through = 0.5
    with open(catfile,'r') as fl:
        for line in fl:
            galname,redshift = line.split(',')
            redshift = float(redshift)
            run_galaxy(line_pars,filter_pars,galname,redshift,max_through,lamda_list)

if __name__ == '__main__':
    main('sample_list.cat')

#!/usr/bin/env python

#Freja Eilsø Storm
#Inspiration from Mia Harring Hansen

import numpy as np
import copy
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter,MaxNLocator
from matplotlib import rcParams
from subprocess import Popen, PIPE
plt.rcParams.update(plt.rcParamsDefault)

def shell(cmd, shell=False):
    """ 
    runs the shell command cmd
    """
    if shell:
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    
    else:
        cmd = cmd.split()
        p = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    output, err = p.communicate()
    
    return output.decode('utf-8')

def align_yaxis(ax1, ax2):
    """Align zeros of the two axes, zooming them out by same ratio"""
    axes = (ax1, ax2)
    extrema = [ax.get_ylim() for ax in axes]
    tops = [extr[1] / (extr[1] - extr[0]) for extr in extrema]
    # Ensure that plots (intervals) are ordered bottom to top:
    if tops[0] > tops[1]:
        axes, extrema, tops = [list(reversed(l)) for l in (axes, extrema, tops)]

    # How much would the plot overflow if we kept current zoom levels?
    tot_span = tops[1] + 1 - tops[0]

    b_new_t = extrema[0][0] + tot_span * (extrema[0][1] - extrema[0][0])
    t_new_b = extrema[1][1] - tot_span * (extrema[1][1] - extrema[1][0])
    axes[0].set_ylim(extrema[0][0], b_new_t)
    axes[1].set_ylim(t_new_b, extrema[1][1])


def readfile(f):
    """
    read the data-file is it was exported before hand
    """

    x = []
    y = []
    with open(f, 'r') as my_file:
        for l in my_file:
            row = l.split(',')
            
            x.append(float(row[0]))
            y.append(float(row[1]))
    return x,y

def oscillator_plot(ax,l,f,i,lambda_start, lambda_end,colorlist,lab):
    """
    plots the stick spectrum of the oscillator strengths
    """
    if colorlist != []:
        tableau20 = colors(colorlist)
    else:
        tableau20 = colors() 
   
    ax2 = ax.twinx()
    align_yaxis(ax,ax2)
    ax2.set_ylim([0,1.1])
    ax2.grid(None)
    if i == 0:
    #setup
        ax2.set_xlim([lambda_start,lambda_end])
        ax2.yaxis.set_tick_params(which='major', labelsize=14, direction='out')
    else:
        ax2.set_yticklabels([])

    if 'VAC' in lab:
        ax2.bar(l,f,2,color = tableau20[i],hatch='-')
    else:
        ax2.bar(l,f,2,color = tableau20[i])
    
    


def plot_setup(ax):
    """
    set up the "nice" uv-vis layout
    """
    ax.tick_params(axis = 'both', which = 'major', length = 8)
    ax.tick_params(axis = 'both', which = 'minor', length = 4)

    ax.get_xaxis().set_tick_params(direction='out', width=1)
    ax.get_yaxis().set_tick_params(direction='out', width=1)

    majorLocator = MultipleLocator(100)
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(20)
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)

    
    ax.yaxis.set_major_locator(MultipleLocator(2.5))
    #ax.yaxis.set_major_locator(MultipleLocator(0.2))
    #ax.yaxis.set_major_formatter(majorFormatter)
    ax.yaxis.set_minor_locator(MultipleLocator(0.5))

#    fm = mpl.font_manager
#    fm.get_cachedir()
#    font = 'arial'
#    rcParams['font.family'] = [font]
    ax.legend(loc="upper right",fontsize=28)
    legend = ax.legend(frameon = 1)
    frame = legend.get_frame()
    frame.set_color('white')
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14) 
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(14) 

def colors(colorlist=[]):
    if colorlist != []:
        tableau20 = copy.copy(colorlist)
        for i in range(len(tableau20)):
            r, g, b = tableau20[i]
            tableau20[i] = (r / 255., g / 255., b / 255.)
    else :
#	These are the "Tableau 20" colors as RGB.
        tableau20 = [(255,0,0),(0,0,255), (255,125,0), (128,128,0), (200,200,0),(0, 255, 0), (0,128,128), (0,0,128), (128,0,128),(255,0,255), (43, 0,0), (140, 86, 75), (196, 156, 148),(227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),(188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)] 
#	     Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
        for i in range(len(tableau20)):    
            r, g, b = tableau20[i]    
            tableau20[i] = (r / 255., g / 255., b / 255.)
    return tableau20

def plotter(ax,j,x,y,lab,colorlist, ymax_old=1):
    """
    plot the data
    """
    if colorlist != []:
        tableau20 = colors(colorlist)
    else:
        tableau20 = colors() 

    ymax = max(y)

    if 'VAC' in lab:
        ax.plot(x,y,color=tableau20[j],linewidth=2.0,linestyle='--',label=lab,alpha=1.0)
    else :
        #ax.plot(x,y/ymax,color=tableau20[j],linewidth=2.0,label=lab,alpha=1.0)
        ax.plot(x,y,color=tableau20[j],linewidth=2.0,label=lab,alpha=1.0)
    #ax.plot(x,y,color=tableau20[j],linewidth=2.0,label=lab,alpha=1.0)
    
    if ymax < ymax_old:
        ymax = ymax_old
    ymax_old = ymax
     
    ax.set_ylim([0,ymax_old])
    #ax.set_ylim([0,1.0])
    ax.set_xlim([min(x),max(x)])
    return ymax

def uvvis(t,l,f):
    """
    adds a gaussian distribution on top of the calculated oscillator strengths
    t; x-axis range
    l; list of calculated transition energies
    f; calculated oscillator strengths

    for each value on the x-axis, the contribution to the absorption from each calculated transition energy is summed up
    http://gaussian.com/uvvisplot/
    k = transformation constant

    """

    #l = l[:25]
    #f = f[:25]
    ###CONSTANTS####
    NA=6.02214199*10**23 #avogadros number
    c=299792458 #speed of light
    e=1.60217662*10**(-19) #electron charge
    me=9.10938*10**(-31) #electron mass
    pi=math.pi
    epsvac=8.8541878176*10**(-12)
    ### 
    sigmaeV=0.3
    sigmacm=sigmaeV*8065.544
    ### 

    k=(NA*e**2)/(np.log(10)*2*me*c**2*epsvac)*np.sqrt(np.log(2)/pi)*10**(-1)

    lambda1=np.zeros(len(l))
    lambda_tot=np.zeros(len(t))
    for x in range(1,len(t)):
        for i in range(0,len(l)):
            lambda1[i]=(k/sigmacm)*f[i]*np.exp(-4*np.log(2)*((1/t[x]-1/l[i])/(10**(-7)*sigmacm))**2)
        lambda_tot[x]=sum(lambda1)
    return np.array(lambda_tot)*10**-4

def iteration(N_datafiles, N_subplots):
    """
    divides the number of plots as equal as possible among subplots
    """

    it = N_datafiles / N_subplots
    rest = N_datafiles % N_subplots
    list_iteration = [int(it) for i in range(N_subplots)]
    counter = 0
    for i in range(rest):
        list_iteration[counter] += 1
        counter += 1
    return list_iteration


def main():
    
    import argparse
    import sys 
    import os

    parser = argparse.ArgumentParser()
    
    parser.add_argument('-s','--no_of_subplots',type=int,help='the desired number of subplots')    
    parser.add_argument('-o','--output',help='the extention of the outputfilei. DEFAULT .log') 
    parser.add_argument('-e','--experimental',help='data file with experimental data in csv')
    parser.add_argument('-ls','--lambda_start',type=int,help='starting value of x axis')
    parser.add_argument('-le','--lambda_end',type=int,help='ending value of x axis')
    parser.add_argument('-f','--oscillator',type=bool,help='request plot with oscillator strength stick plot. Call with "true"')
    parser.add_argument('-pdf','--filename',help='set the name of the .pdf file the plot is saved to')
    parser.add_argument('-c','--colorlist',nargs='+',help='list of RGB colors eq. -c "254,0,251" "91,228,62" "15,0,62"')

    args = parser.parse_args() 
    

    if args.no_of_subplots:
        print("# of subplots {}".format(args.no_of_subplots))
        subplot_no = args.no_of_subplots
    else :
        subplot_no = 1

    if args.output:
        ext = args.output
    else :
        ext = ".log"
    
    if args.experimental:
        experimental=True
        experimental_data = args.experimental
    else:
        experimental=False
    if args.lambda_start:
        lambda_start = args.lambda_start
    else:
        lambda_start = 200
    
    if args.lambda_end:
        lambda_end = args.lambda_end
    else:
        lambda_end = 850

    if args.oscillator:
        osc_plot = True
    else :
        osc_plot = False

    if args.filename:
        filename=args.filename
    else :
        filename='test'
    filename += '.pdf'

    if args.colorlist:
        colorlist = args.colorlist
        colorlist = [sublist.split(',') for sublist in colorlist]
        for i in range(len(colorlist)):
            for j in range(len(colorlist[i])):
                colorlist[i][j] = int(colorlist[i][j])
                
    else:
        colorlist = []
    
    files = [filename for filename in os.listdir('.') if filename.endswith(ext)]
    files.sort()
    print(files)
    #number of points on x-axis
    ymax_old = 1. 
    N=500
    t=np.linspace(lambda_start, lambda_end, N, endpoint=True)
     
    if subplot_no == 4:
        fig,axarr= plt.subplots(2,2,figsize=(10,8),sharey=True,sharex = True)
        axarr = [j for i in axarr for j in i]
    elif subplot_no == 1:
        fig,axarr= plt.subplots(subplot_no,figsize=(10,8))
    else :
        fig,axarr= plt.subplots(subplot_no,figsize=(10,8),sharey=True, sharex = True)
    
    
    counter = 0
    if subplot_no > 1:
        for index, it in enumerate(iteration(len(files),subplot_no)):
            if experimental:
                l,f = readfile(experimental_data) 
                plotter(axarr[index],1,l,f,'EXP',colorlist,ymax_old)  
            
            for curve in range(it):
                normal = shell('grep "Normal termination" '+ files[counter],shell=True)
                if normal != '':
                    excitation_data = shell('grep "Excited" '+files[counter], shell=True).split('\n')
                    excitation_data  = [k for i in excitation_data[1:-1] for k in i.split(' ') if k != '']
                    
                    l = excitation_data[6::10]
                    l = [float(k) for k in l]
                
                    f = excitation_data[8::10]
                    f = [float(k.split('f=')[1]) for k in f]
                    s = uvvis(t,l,f)
                
                else:
                    continue
                
                lab = files[counter].split('.')[0]
                lab = lab.split('_')[1]
                ymax_old = plotter(axarr[index],counter,t,s,lab,colorlist,ymax_old)        
               
                if osc_plot:
                    print(curve)
                    oscillator_plot(axarr[index],l,f,counter,lambda_start,lambda_end,colorlist,lab)
   
                with open(files[counter]+'data.csv','w') as f:
                    for i in range(len(s)):
                        f.write("{},{} \n".format(t[i],s[i]))
                counter += 1
            plot_setup(axarr[index])

    else :
        for index, it in enumerate(iteration(len(files),subplot_no)):
            if experimental:
                l,f = readfile(experimental_data) 
                plotter(axarr,1,l,f,'EXP',colorlist,ymax_old)  
            
            for curve in range(it):
                normal = shell('grep  "Normal termination" '+ files[counter],shell=True)
                if normal != '':
                    excitation_data = shell('grep "Excited" '+files[counter], shell=True).split('\n')
                    excitation_data  = [k for i in excitation_data[1:-1] for k in i.split(' ') if k != '']
                    l = excitation_data[6::10]
                    l = [float(k) for k in l]
                    f = excitation_data[8::10]
                    f = [float(k.split('f=')[1]) for k in f]
                    
                    #limit number of excited statenks
                    l = l[:25]
                    f = f[:25]

                    s = uvvis(t,l,f)
                else:
                    continue
                
                lab = files[counter].split('_')[0]
                lab = lab.split('-')[-1]
                #lab = lab.replace('M',r'$\beta$',1)
                ymax_old = plotter(axarr,counter,t,s,lab,colorlist,ymax_old)
                
                if osc_plot:
                    oscillator_plot(axarr,l,f,counter,lambda_start,lambda_end,colorlist,lab)

                with open(files[counter]+'data.csv','w') as f:
                    for i in range(len(s)):
                        f.write("{},{} \n".format(t[i],s[i]))
                counter += 1
            plot_setup(axarr)
                

    

    fig.subplots_adjust(hspace=0.1,bottom=0.2)
    fig.text(0.5, 0.1, r'$\lambda$ (nm)', fontsize=22, ha='center', va='center')
    fig.text(0.04, 0.5, r'$\epsilon$ (10$^4$ M$^{-1}$ cm$^{-1}$)', fontsize=22, ha='center', va='center', rotation='vertical')
    #fig.text(0.04, 0.5, r'Normalized Absorption (a.u.)', fontsize=22, ha='center', va='center', rotation='vertical')
    if osc_plot:
        fig.text(0.97, 0.5, 'Oscillator Strength', fontsize=22, ha='center', va='center', rotation=270)
    plt.savefig(filename)

if __name__=="__main__":
    plt.style.use('seaborn')
    #plt.grid(False)
    plt.tight_layout()
    main()

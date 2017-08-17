import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import os
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from scipy.interpolate import splrep, sproot, splev


def fwhm(x, y, k=10):
    """
    Determine full-with-half-maximum of a peaked set of points, x and y.

    Assumes that there is only one peak present in the datasset.  The function
    uses a spline interpolation of order k.
    """

    class MultiplePeaks(Exception): pass
    class NoPeaksFound(Exception): pass

    half_max = np.amax(y)/2.0
    s = splrep(x, y - half_max)
    roots = sproot(s)

    if len(roots) > 2:
        raise MultiplePeaks("The dataset appears to have multiple peaks, and "
                "thus the FWHM can't be determined.")
    elif len(roots) < 2:
        raise NoPeaksFound("No proper peaks were found in the data set; likely "
                "the dataset is flat (e.g. all zeros).")
    else:
        return roots, abs(roots[1] - roots[0])


def uvvis(t,l,f):
    ###CONSTANTS####
    NA=6.02214199*10**23 #avogadros number
    c=299792458 #speed of light
    e=1.60217662*10**(-19) #electron charge
    me=9.10938*10**(-31) #electron mass
    pi=math.pi
    epsvac=8.8541878176*10**(-12)
    ###
    sigmaeV=0.4
    sigmacm=sigmaeV*8065.544
    ###

    k=(NA*e**2)/(np.log(10)*2*me*c**2*epsvac)*np.sqrt(np.log(2)/pi)*10**(-1)

    lambda1=np.zeros(len(l))
    lambda_tot=np.zeros(len(t))
    for x in range(1,len(t)):
        for i in range(0,len(l)):
            lambda1[i]=(k/sigmacm)*f[i]*np.exp(-4*np.log(2)*((1/t[x]-1/l[i])/(10**(-7)*sigmacm))**2)
        lambda_tot[x]=sum(lambda1)
    return lambda_tot

def readfile(f):
    tom = []
    l = []
    f = []
    with open(files[i],'r') as my_file:
        next(my_file)
        for line in my_file:
            row=line.split()
            tom.append(float(row[0]))
            l.append(float(row[1]))
            f.append(float(row[2]))
        #f = f[:25]
        #l = l[:25]
    return tom,l,f
    
def plot(x,y,ax,fig,box=[0.85,0.85],i=0,lambda_start=250, lambda_end=750,ymax_old = 1000):
    #legend_list = ['SubPc', 'SubPc(TP)','SubPc(TP)$_2$','SubPc(TP)$_3$'] 
    print (files[i].split('_',3)[0].rsplit(',',1)[0])
    #lab = legend_list[i]
    lab = input('Enter legend: ') or files[i].split('_',3)[0].rsplit('.',1)[0]
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    #write the maximum absorption
    for n in range(len(y)):
        if y[-(n+1)] > y[-(n+2)]:
            txt = str(int(t[-(n+1)]))
            print ('adding text')
   #         plt.annotate(txt,(t[-(n+1)]-10,uv[-(n+1)]+400))
            break        
    ax.plot(x,y,color = tableau20[i],lw=1.5, label = lab +' '+ txt)
    #plt.legend()
    #if i ==6:
    #    fig.text(box[0],box[1]-(float(3)/28.0),lab + r' $\lambda_{max} $ ' + txt, fontsize=10, color = tableau20[i])
    #else :
    fig.text(box[0],box[1]-(float(i%4)/28.0),lab + r' $\lambda_{max} $ ' + txt,fontsize=10, color = tableau20[i])
    ymax = max(y)+2000
    print (ymax_old, ymax)
    if ymax < ymax_old:
        ymax = ymax_old
    ymax_old = ymax
    print (ymax_old)
    
    ax.set_xlim([lambda_start,lambda_end])
    ax.set_ylim([0,120000])
    #ax.get_xaxis().set_tick_params(direction='out', width=1)
    #ax.get_yaxis().set_tick_params(direction='out', width=1)
    
    majorLocator = MultipleLocator(50)
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(25000)
        
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    
    #ax.xaxis.set_minor_locator(minorLocator)
    ax.yaxis.set_minor_locator(minorLocator)

    ax.grid(color='black', which='minor', axis='y', linestyle='--', alpha = 0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    return ymax_old

def oscillator_plot(ax,l,f,i,lambda_start,lambda_end):
    ax2 = ax.twinx()
    ax2.spines["top"].set_visible(False)
    #ax2.spines["right"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.bar(l,f,2,color = tableau20[i])
    plt.xlim([lambda_start,lambda_end])
    plt.ylim(0,1)




#user input for plot
#title = input('Enter plot title: ') or "title"
name = input('Enter filename: ') or "test"    

#create list of relevant file names
files = [filename for filename in os.listdir('.') if filename.endswith('.txt')]
files.sort()
print (files)

# These are the "Tableau 20" colors as RGB.
tableau20 = [(200,135,202), (146,210,200), (246,100,100), (255,176,102),
             (76, 143, 0), (70, 170, 255), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)] 
 
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)




#number of points on x-axis
N=500
lambda_start = 220
lambda_end = 900
t=np.linspace(lambda_start, lambda_end, N, endpoint=True)
#y-axis parameters


ymax_old = 1000

#fig,(ax1,ax2) = plt.subplots(2,sharey=True, sharex = True)


sigma_list = []
for i in range(len(files)):
    if len(files) <= 7:
        if i%11==0:
            fig,ax1 = plt.subplots()
        #ax = plt.subplot(111)
        h,l,f = readfile(files[i])
        uv = uvvis(t,l,f)
        #roots, value = fwhm(t[160:],uv[160:])
        ymax_old = plot(t,uv,ax1,fig,box=[0.7,0.85],i=i,lambda_start=lambda_start, lambda_end=lambda_end,ymax_old=ymax_old)
        #for n in range(len(uv)):
        #    if uv[n+1]-uv[n] <=0.00000001:
        #        print ('possible t',n)
        #maxint = np.amax(uv[160:])
        #end_value = (maxint/ymax_old)*0.5
        #sigma_list.append(value)
        #ax1.axvspan(roots[0],roots[1],end_value-0.005,end_value,facecolor=tableau20[i],alpha=0.5)        
        
    elif len(files) <= 11 :
        if i <= 3:
            if (i)%20==0:
                fig,(ax1,ax2) = plt.subplots(2,1,figsize=(10,4),sharey=True, sharex = True)
            h,l,f = readfile(files[i])
            uv = uvvis(t,l,f)
            #ax =  plt.subplot(211)
            print ('plot')
            ymax_old = plot(t,uv,ax1,fig,i=i,lambda_start=lambda_start,box =[0.8,0.85],lambda_end=lambda_end,ymax_old=ymax_old)
            
        else :
            h,l,f = readfile(files[i])
            uv = uvvis(t,l,f)
            #ax = plt.subplot(212)
            print ('plot')
            ymax_old = plot(t,uv,ax2,fig,i=i,lambda_start=lambda_start,lambda_end=lambda_end,box = [0.8,0.45],ymax_old=ymax_old)
    
       
    elif len(files) <= 25 :
       
        if i <= 4:  
            if i % 11 ==0:
                 fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,figsize=(10,4),sharey=True, sharex = True)
            h,l,f = readfile(files[i])
            uv = uvvis(t,l,f)
            #ax = plt.subplot(221)
            ymax_old = plot(t,uv,ax1,fig,[0.45,0.85],i,lambda_start,lambda_end,ymax_old)
        elif i <= 9 :
            h,l,f = readfile(files[i])
            uv = uvvis(t,l,f)
            #ax =  plt.subplot(222)
            ymax_old = plot(t,uv,ax2,fig,i=i,lambda_start=lambda_start,lambda_end=lambda_end,ymax_old=ymax_old)
        elif i <= 14 :
            h,l,f = readfile(files[i])
            uv = uvvis(t,l,f)
            #ax = plt.subplot(223)
            ymax_old = plot(t,uv,ax3,fig,[0.45,0.45],i,lambda_start,lambda_end,ymax_old)
        elif i <= len(files)-1:
            h,l,f = readfile(files[i])
            uv = uvvis(t,l,f)
            #ax = plt.subplot(224)
            ymax_old = plot(t,uv,ax4,fig,[0.85,0.45],i,lambda_start,lambda_end,ymax_old)


#Add labels collectively for subplots
#plt.margins(0.1)
plt.subplots_adjust(left=0.2,bottom=0.15)
#fig.text(0.5,0.95,title, fontsize=20, ha='center', va='center')
fig.text(0.5, 0.06, 'Wavelength (nm)', fontsize=15, ha='center', va='center')
fig.text(0.15, 0.5, r'$\varepsilon$ L mol$^{-1}$ cm$^{-1}$', fontsize=15, ha='center', va='center', rotation='vertical')


plt.savefig(name + '.pdf', format='PDF')

print(sigma_list)

for i in range(len(files)):
    if len(files) <= 5:
        h,l,f = readfile(files[i])
        oscillator_plot(ax1,l,f,i,lambda_start,lambda_end)
        
    elif len(files) <= 11 :
        if i <= 3:
            h,l,f = readfile(files[i])
            oscillator_plot(ax1,l,f,i,lambda_start,lambda_end)
        else :
            h,l,f = readfile(files[i])
            oscillator_plot(ax2,l,f,i,lambda_start,lambda_end)
    
    elif len(files) <= 25 :
       
        if i <= 4:  
            h,l,f = readfile(files[i])
            oscillator_plot(ax1,l,f,i,lambda_start,lambda_end)
        elif i <= 9 :
            h,l,f = readfile(files[i])
            oscillator_plot(ax2,l,f,i,lambda_start,lambda_end)
        elif i <= 14 :
            h,l,f = readfile(files[i])
            oscillator_plot(ax3,l,f,i,lambda_start,lambda_end)
        elif i <= len(files)-1:
            h,l,f = readfile(files[i])
            oscillator_plot(ax4,l,f,i,lambda_start,lambda_end)


plt.savefig(name + '2.pdf', format = 'PDF')

plt.clf()

"""
# Add the oscillator strength bars
ax2 = ax.twinx()
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2.spines["left"].set_visible(False)
for i in range(len(files)):
    h,l,f = readfile(files[i])
    uv = uvvis(t,l,f)
    ax2.bar(l,f,2,color = tableau20[i])
    plt.xlim([lambda_start,lambda_end])
    plt.ylim(0,1)
plt.savefig(name + '2.png')

plt.clf()

ax = plt.subplot(111)
plt.margins(0.2)
plt.subplots_adjust(bottom=0.15,hspace=0.5)
#plt.show()
fig.text(0.5,0.95,title, fontsize=20, ha='center', va='center')
fig.text(0.5, 0.06, 'Wavelength (nm)', fontsize=17, ha='center', va='center')
fig.text(0.02, 0.5, r'$\varepsilon$ (L/(mol cm))', fontsize=17, ha='center',
        va='center', rotation='vertical')

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
for i in range(len(files)):
    h,l,f = readfile(files[i])
    #print len(f)
    uv = uvvis(t,l,f)
    lab = files[i].split('_uv_data.txt',1)[0]
    fig.text(0.7,0.85-(float(i)/30.0),lab,fontsize=10,color = tableau20[i])
    ax.bar(l,f,0.3,color = tableau20[i])
    plt.xlim([lambda_start,lambda_end])
    plt.ylim(0,1)
plt.savefig(name + 'osc.png')
"""

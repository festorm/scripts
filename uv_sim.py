import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import os
from matplotlib.ticker import MultipleLocator

fig = plt.figure()
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

#user input for plot
title = raw_input('Enter plot title: ') or "title"
name = raw_input('Enter filename: ') or "test"


def uvvis(t,l,f):
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

#create list of relevant file names
files = [filename for filename in os.listdir('.') if filename.endswith('.txt')]
files.sort()
print files
# These are the "Tableau 20" colors as RGB.
tableau20 = [(196, 13, 111), (36, 13, 111), (36, 218, 111), (210, 70, 43),    
             (76, 143, 0), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229), (158, 200, 229)] 
    
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)


#number of points on x-axis
N=500
t=np.linspace(200, 650, N, endpoint=True)
ymax_old = 1000

for i in range(len(files)):
    """
    if len(files) <= 5 :
        ax = plt.subplot(111)
        lab = files[i].split('_uv_data.txt',1)[0]
        h,l,f = readfile(files[i])
        uv = uvvis(t,l,f)
        print len(uv)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.plot(t,uv,color = tableau20[i])
        fig.text(0.7,0.85-(float(i)/30.0),lab, fontsize=10, color = tableau20[i])
        ymax = max(uv)+2000

        if ymax < ymax_old:
            ymax = ymax_old
        ymax_old = ymax
        
        plt.xlim([200,650])
        plt.ylim([0,1.0*10**5])
        plt.grid(color='black', which='major', axis='y', linestyle='--', alpha = 0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
       
    elif len(files) <= 10 :
        if i <= 3:
            lab = files[i].split('_uv_data.txt',1)[0]
            h,l,f = readfile(files[i])
            uv = uvvis(t,l,f)

            plt.subplot(211)
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            plt.plot(t,uv,color = tableau20[i])
            fig.text(0.7,0.85-(float(i)/30.0),lab, fontsize=10, color = tableau20[i])
            ymax = max(uv)+2000

            if ymax < ymax_old:
                ymax = ymax_old
            ymax_old = ymax
            
            plt.xlim([200,650])
            plt.ylim(0,1.0*10**5)
            ax = plt.subplot(211)
            plt.grid(color='black', which='major', axis='y', linestyle='--', alpha = 0.3)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.spines["left"].set_visible(False)
        else :
            lab = files[i].split('_uv_data.txt',1)[0]
            print lab
            h,l,f = readfile(files[i])
            uv = uvvis(t,l,f)
        ymax = max(uv)+2000

            if ymax < ymax_old:
                ymax = ymax_old
            ymax_old = ymax
            plt.xlim([200,650])
            plt.ylim(0,1.0*10**5)
            plt.subplot(212)
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            plt.plot(t,uv,color = tableau20[i])
            fig.text(0.7,0.55-(float(i)/30.0),lab, fontsize=10, color = tableau20[i])
            ax = plt.subplot(212)
            plt.grid(color='black', which='major', axis='y', linestyle='--', alpha = 0.3)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.spines["left"].set_visible(False)
    """
    if len(files) <= 25 :
            if i <= 4:                   
                lab = files[i].split('_uv_data.txt',1)[0]

                h,l,f = readfile(files[i])
                uv = uvvis(t,l,f)
                print l[0]
                plt.subplot(221)
                #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
                plt.plot(t,uv,color = tableau20[i])
                #fig.text(0.7,0.85-(float(i)/30.0),lab, fontsize=10, color = tableau20[i])
                ymax = max(uv)+2000

                if ymax < ymax_old:
                    ymax = ymax_old
                ymax_old = ymax
                
                plt.xlim([200,550])
                plt.ylim(0,1.0*10**5)
                ax = plt.subplot(221)
                plt.grid(color='black', which='major', axis='y', linestyle='--', alpha = 0.3)
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["bottom"].set_visible(False)
                ax.spines["left"].set_visible(False)
            elif i <= 9 :
                lab = files[i].split('_uv_data.txt',1)[0]
                h,l,f = readfile(files[i])
                print l[0]
                uv = uvvis(t,l,f)
                ymax = max(uv)+2000

                if ymax < ymax_old:
                    ymax = ymax_old
                ymax_old = ymax
                plt.xlim([200,550])
                plt.ylim(0,1.0*10**5)
                plt.subplot(222)
                plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
                plt.plot(t,uv,color = tableau20[i])
                #fig.text(0.7,0.55-(float(i)/30.0),lab, fontsize=10, color = tableau20[i])
                ax = plt.subplot(222)
                plt.grid(color='black', which='major', axis='y', linestyle='--', alpha = 0.3)
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["bottom"].set_visible(False)
                ax.spines["left"].set_visible(False)
            elif i <= 14 :
                lab = files[i].split('_uv_data.txt',1)[0]
                h,l,f = readfile(files[i])
                print l[0]
                uv = uvvis(t,l,f)
                ymax = max(uv)+2000

                if ymax < ymax_old:
                    ymax = ymax_old
                ymax_old = ymax
                
                plt.xlim([200,550])
                plt.ylim(0,1.0*10**5)
                plt.subplot(223)
                plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
                plt.plot(t,uv,color = tableau20[i])
                #fig.text(0.7,0.55-(float(i)/30.0),lab, fontsize=10, color = tableau20[i])
                ax = plt.subplot(223)
                plt.grid(color='black', which='major', axis='y', linestyle='--', alpha = 0.3)
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["bottom"].set_visible(False)
                ax.spines["left"].set_visible(False)
            else :
                lab = files[i].split('_uv_data.txt',1)[0]
                h,l,f = readfile(files[i])
                print l[0]
                uv = uvvis(t,l,f)
                ymax = max(uv)+2000

                if ymax < ymax_old:
                    ymax = ymax_old
                ymax_old = ymax
                
                plt.xlim([200,550])
                plt.ylim(0,1.0*10**5)
                plt.subplot(224)
                plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
                plt.plot(t,uv,color = tableau20[i])
                #fig.text(0.7,0.55-(float(i)/30.0),lab, fontsize=10, color = tableau20[i])
                ax = plt.subplot(224)
                plt.grid(color='black', which='major', axis='y', linestyle='--', alpha = 0.3)
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["bottom"].set_visible(False)
                ax.spines["left"].set_visible(False)


#Trying to make the plot look nice
#create horizontal lines to guide the eye
#for y in range(-800,900,100):
#    plt.axhline(y,linestyle= "--", lw=0.5,color="black", alpha=0.3)
#remove y ticks
#plt.tick_params(axis="both", which="both", bottom="off", top="off",labelbottom="on", left="off", right="off", labelleft="on")

#change font on axis
#plt.yticks(fontsize=14)
#plt.xticks(fontsize=14)

#plt.legend(loc='center right', bbox_to_anchor=(1,0.7))
#plt.legend()
plt.margins(0.2)
plt.subplots_adjust(bottom=0.15,hspace=0.5)
#plt.show()
fig.text(0.5,0.95,title, fontsize=20, ha='center', va='center')
fig.text(0.5, 0.06, 'Wavelength (nm)', fontsize=17, ha='center', va='center')
fig.text(0.02, 0.5, r'$\varepsilon$ (L/(mol cm))', fontsize=17, ha='center', va='center', rotation='vertical')


plt.savefig(name + '.png')
ax2 = ax.twinx()
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2.spines["left"].set_visible(False)
for i in range(len(files)):
    h,l,f = readfile(files[i])
    uv = uvvis(t,l,f)
    ax2.bar(l,f,2,color = tableau20[i])
    plt.xlim([200,650])
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
    fig.text(0.7,0.85-(float(i)/30.0),lab,             fontsize=10,color = tableau20[i])
    ax.bar(l,f,0.3,color = tableau20[i])
    plt.xlim([200,350])
    plt.ylim(0,1)
plt.savefig(name + 'osc.png')


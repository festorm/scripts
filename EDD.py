#! /usr/bin/env python

import numpy
import copy
import math
import matplotlib.pyplot as plt 
from subprocess import Popen, PIPE

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

def homo_lumo(filename):
    """
    Identify the orbital number of the HOMO and LUMO orbital
    """
    alpha_beta = shell('grep alpha electrons ' + str(filename), shell=True).split(' ')
    alpha_beta = [k for k in alpha_beta if k != '']

    homo1 = alpha_beta[1]
    homo2 = alpha_beta[4] 
    if homo1 >= homo2:
        homo = homo1
    else:
        homo = homo2

    lumo = int(homo) + 1

    return int(homo),int(lumo)

def create_states(filename):
    """
    Create a dictionary with all the excitations
    Each dictionary element is a dictionary in it self with the information of the state
    """
    excited_state = shell('sed -n "/Excitation energies and oscillator strengths/,/Population analysis/p" ' + str(filename),shell=True).split('\n')
    excited_state = [k for k in excited_state if k != '']
    excited_state = excited_state[2:-3]
    excited_state.append(' ')
 
    all_states = {}
    
    counter = 0
    for i in excited_state:
        string = [k for k in i.split(' ') if k != '']
        if 'Excited' in string:
            state = {}
            from_orb = []
            to_orb = []
            coef = []
            transitions = []
            state['level'] = int(string[2].strip(':'))
            state['eV'] = string[4]
            state['nm'] = string[6]
            state['f'] = string[8].split('=')[1]
        else:
            for i in string:
                if '>' in i:
                    from_orb.append(int(string[0]))
                    if string[1] != '->':
                        to_orb.append(int(string[1].split('>')[1]))
                        coefficient = (2*float(string[2])**2.0)*100.0
                    else:
                        to_orb.append(int(string[2]))
                        coefficient = (2*float(string[3])**2.0)*100.0
                    coef.append(coefficient)
        if string == []:
            state['transitions'] = [[from_orb[i],to_orb[i],coef[i]] for i in range(len(to_orb))]
            all_states[str(counter)] = state

            counter += 1
    return all_states

def write_excitation_data(all_states):   
    """
    create a SI latex table of all the excitations including the orbitals participating and the contribution from each orbital
    """
    with open('Excitation_data.txt','w') as f:
        for i in range(len(all_states)):
            f.write('{:20s} & {:10s} & {:20s} {:5s} \n'.format('Excited State','eV','Osc. Strength','\\\\'))
            f.write('{:2d} & {:.4f} & {:.4f} {:5s} \n'.format(all_states[str(i)]['level'],float(all_states[str(i)]['eV']),float(all_states[str(i)]['f']),'\\\\'))
            f.write('{:10s} & {:10s} & {:10s} {:5s} \n'.format('From Orb.','To Orb', 'Coef','\\\\'))
            for j in range(len(all_states[str(i)]['transitions'])):
                #print(all_states[str(i)]['transitions'][j][2])
                f.write('{:3d} & {:3d} & {:.3f} {:5s} \n'.format(all_states[str(i)]['transitions'][j][0],all_states[str(i)]['transitions'][j][1],all_states[str(i)]['transitions'][j][2],'\\\\'))

def create_edd_cube(all_states,i,formchk):
    """
    Creating a .sh script that use the gaussian utilities to create the electron density difference plots of all the orbitals in a given transition
    """

    before_mos = []
    after_mos = []
    with open('EDD_cube' + str(i + 1)+'.sh','w') as f:
        for j in range(len(all_states[str(i)]['transitions'])):

            from_orb = all_states[str(i)]['transitions'][j][0] 
            to_orb = all_states[str(i)]['transitions'][j][1]
            coef = all_states[str(i)]['transitions'][j][2]
            before_mos.append(from_orb)
            after_mos.append(to_orb)
            for m in from_orb,to_orb:
                f.write('if [ ! -e "mo'+str(m)+'.cub" ] \n'
                        'then \n'
                        'echo Creating the cube of MO ' + str(m) + '\n' 
                        'cubegen 0 MO='+str(m)+' '+formchk+ ' mo'+str(m)+
                        '.cub -2 h \n'
                        'fi \n \n')
                        #creates the .cube file of the mo using 1 cpu, the coarse grid including the header
                
                f.write('if [ ! -e "sq'+str(m) + '.cub" ] \n then \n'
                        'echo Squaring the cube of MO ' + str(m) + '\n')
                #read the cubman introduction at : http://gaussian.com/cubman/
                f.write('echo sq > tmp.txt \n'
                        'echo '+ 'mo'+str(m) + '.cub >> tmp.txt \n'
                        'echo y  >> tmp.txt \n'
                        'echo sq'+str(m) + '.cub >> tmp.txt \n'
                        'echo y  >> tmp.txt\n'
                        'cat tmp.txt | cubman > tmp2.txt \n'
                        'fi \n \n')

                f.write('echo Scaling MO ' + str(m) + ' by ' + str(coef) + '\n'
                        'echo sc > tmp.txt \n'
                        'echo sq'+str(m)+'.cub >> tmp.txt \n'
                        'echo y >> tmp.txt \n'
                        'echo sc'+str(m)+'.cub >> tmp.txt \n'
                        'echo y >> tmp.txt \n'
                        'echo '+ str(coef) + '>> tmp.txt\n'
                        'cat tmp.txt | cubman > tmp2.txt \n')
            

        f.write('echo Adding the before cubes ' + ",".join(map(str,before_mos)) + '\n'
                'mv sc'+str(all_states[str(i)]['transitions'][0][0])+'.cub'
                ' before.cub \n')
        f.write('echo Adding the after cubes ' + ",".join(map(str,after_mos)) + '\n'
                'mv sc'+str(all_states[str(i)]['transitions'][0][1])+'.cub'
                ' after.cub \n')
        
        for k in all_states[str(i)]['transitions'][1:]:
            print(k[0],k[1],k[2])

            f.write('echo a > tmp.txt \n'
                    'echo sc'+str(k[0])+'.cub >> tmp.txt\n'
                    'echo y >> tmp.txt \n'
                    'echo before.cub >> tmp.txt \n' 
                    'echo y >> tmp.txt \n'
                    'echo bef.cub >> tmp.txt \n'
                    'echo y >> tmp.txt \n'
                    'cat tmp.txt | cubman > tmp2.txt \n'
                    'mv bef.cub before.cub \n\n')
            
            f.write('echo a > tmp.txt \n'
                    'echo sc'+str(k[1])+'.cub >> tmp.txt\n'
                    'echo y >> tmp.txt \n'
                    'echo after.cub >> tmp.txt \n' 
                    'echo y >> tmp.txt \n'
                    'echo aft.cub >> tmp.txt \n'
                    'echo y >> tmp.txt \n'
                    'cat tmp.txt | cubman > tmp2.txt \n'
                    'mv aft.cub after.cub \n\n')
            

        f.write('echo Substracting the before from the after cubes \n'
                'echo su > tmp.txt \n'
                'echo before.cub >> tmp.txt \n'
                'echo y >> tmp.txt \n'
                'echo after.cub >> tmp.txt \n'
                'echo y >> tmp.txt \n'
                'echo trans'+str(i+1)+'.cub >> tmp.txt \n'
                'echo y >> tmp.txt \n'
                'cat tmp.txt | cubman > tmp2.txt \n\n')

if __name__=="__main__":

    import sys

    filename = sys.argv[1]
    i = int(sys.argv[2]) - 1
    formchk = sys.argv[3]
    
    homo,lumo = homo_lumo(filename)
    all_states = create_states(filename)
    print(all_states['0'])
    #create_edd_cube(all_states,i,formchk)

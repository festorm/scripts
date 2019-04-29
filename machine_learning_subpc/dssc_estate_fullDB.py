#!/home/koerstz/anaconda3/envs/rdkit-env/bin/python
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.EState import Fingerprinter
from rdkit.Chem.EState import EStateIndices 
from rdkit.Chem.EState import AtomTypes 

from numpy import linalg as la
from multiprocessing import Pool

import pandas as pd
from subprocess import Popen, PIPE
import os
import numpy as np
import pickle

dssc = pd.read_pickle("dssc_no_br_db.pkl")
num_processes = 8

#https://stackoverflow.com/questions/40357434/pandas-df-iterrow-parallelization
chunks = np.array_split(dssc, num_processes)

def finger_print(chunk):
    """
    Create a dictionary with the e-state fingerprint for the molecule in mol (rdkit mol)

    Input:
    mol; rdkit mol object
    name; structure name
    e_opt; energy gap (target)
    """
    if AtomTypes.esPatterns is None:
            AtomTypes.BuildPatts()

    name_list = [name for name,_ in AtomTypes.esPatterns]
    df = pd.DataFrame(columns=['name','smiles']+name_list)

    for row_index,row in chunk.iterrows():
        name = (row["name"])
        smiles = (row["smiles"])

        mol = Chem.MolFromSmiles(smiles)
        try:

            types = AtomTypes.TypeAtoms(mol)
            es = EStateIndices(mol)
            counts, sums = Fingerprinter.FingerprintMol(mol)

            if AtomTypes.esPatterns is None:
                AtomTypes.BuildPatts()

            name_list = [name for name,_ in AtomTypes.esPatterns]

            data={'name':name,'smiles':smiles}
            data2 = {k: v for k,v in zip(name_list,sums)}

            data.update(data2)
            df = df.append(data,ignore_index=True)

        except AttributeError:
            print(i,formula)
        continue
    return df

pool = Pool(processes=num_processes)

df = pd.concat(pool.map(finger_print,chunks))
pool.close()
pool.join()

df.to_pickle("estate_from_smile_no_br_full.pkl")


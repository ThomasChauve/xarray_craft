import xarray as xr
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import ipywidgets as widgets
import scipy
import datetime
import skimage
import matscipy.elasticity

from IPython import get_ipython
if get_ipython().__class__.__name__=='ZMQInteractiveShell':
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm

@xr.register_dataset_accessor("craft")

class craft(object):
    '''
    This is a classe to work on aita data in xarray environnement.
    
    .. note:: xarray does not support heritage from xr.DataArray may be the day it support it, we could move to it
    '''
    
    def __init__(self, xarray_obj):
        '''
        Constructor for aita. 
        
        The xarray_obj should contained at least :
        1. orientation : DataArray that is compatiblmultiplese with uvec structure
        2. quality : DataArray of dim (m,n,1)
        
        It can contained :
        1. micro : DataArray of dim (m,n,1)
        2. grainId : DataArray of dim (m,n,1)
        
        :param xarray_obj:
        :type xarray_obj: xr.Dataset
        '''
        self._obj = xarray_obj 
    pass

    def strain_energy(self):
        '''
        Strain energy map compute as : w=1/2*e_ij*s_ij (Einstein notation)
        https://fr.wikipedia.org/wiki/%C3%89nergie_%C3%A9lastique
        https://meefi.pedagogie.ec-nantes.fr/MEF/MIAS/treillis/doc/Cours-MMC-RDM-chapII.pdf
        '''
        tmp=self._obj.strain*self._obj.stress
        
        return 1/2*(np.sum(tmp,axis=-1)+np.sum(tmp[...,3::],axis=-1))
    
    def elastic_strain(self,S=np.array([[103,-42.9,-23.2,0,0,0],[-42.9,103,-23.2,0,0,0],[-23.2,-23.2,84.4,0,0,0],[0,0,0,331.8,0,0],[0,0,0,0,331.8,0],[0,0,0,0,0,292.0]])*10**-6):
        '''
        Compute elastic_strain
        '''
        eo=self._obj.orientation.uvecs.bunge_euler()
        ss=self._obj.stress.shape
        res=self._obj.copy()
        res[...]=0
        
        for t in range(ss[0]):
            for i in tqdm(range(ss[1])):
                for j in tqdm(range(ss[2])):
                    mp1=np.matrix([[np.cos(eo[i,j,0]),np.sin(eo[i,j,0]),0],
                                   [-np.sin(eo[i,j,0]),np.cos(eo[i,j,0]),0],
                                   [0,0,1]])

                    mp=np.matrix([[1,0,0],
                                   [0,np.cos(eo[i,j,1]),np.sin(eo[i,j,1])],
                                   [0,-np.sin(eo[i,j,1]),np.cos(eo[i,j,1])]])
                    
                    mr=mp1*mp
                    Sl=np.matrix(matscipy.elasticity.rotate_elastic_constants(S,mr))
                    tmp=np.array(self._obj.stress[t,i,j,:])
                    lstress=np.transpose(np.matrix([tmp[0],tmp[1],tmp[2],tmp[5],tmp[4],tmp[3]]))
                    tmp2=np.array(Sl*lstress)
                    res[t,i,j,0]=tmp[0]
                    res[t,i,j,1]=tmp[1]
                    res[t,i,j,2]=tmp[2]
                    res[t,i,j,3]=tmp[5]/2
                    res[t,i,j,4]=tmp[4]/2
                    res[t,i,j,5]=tmp[3]/2
                    
                    
                    
            return res
        
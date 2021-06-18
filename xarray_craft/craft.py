import xarray as xr
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import ipywidgets as widgets
import scipy
import datetime
import skimage

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
        1. orientation : DataArray that is compatible with uvec structure
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
        
        return 1/2*(np.sum(tmp,axis=-1)+np.sum(tmp[:,:,3::],axis=-1))
        
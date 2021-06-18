'''
This is an object to take care of unit vector
'''
from xarrayuvecs.uniform_dist import unidist
import xarrayuvecs.lut2d as lut2d

import datetime
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from sklearn.neighbors import KernelDensity
import scipy

@xr.register_dataarray_accessor("gamma")

class gamma(object):
    '''
    This is a classe to work on unit vector in xarray environnement that respect the -1 symmetry (i.e. u is equivalent to -u)
    
    .. note:: xarray does not support heritage from xr.DataArray may be the day it support it, we could move to it
    '''
    
    def __init__(self, xarray_obj):
        '''
        Constructor for uvec. The univ vector u should be pass as azimuth and colatitude in radian
        Colatitude : angle between u-vector and z vector [0 pi/2]
        Azimuth : angle between the projection of u-vector in xOy plan and x-vector [0 2pi]
        
        :param xarray_obj: dimention should be (n,m,2), xarray_obj[n,m,0]=azimuth , xarray_obj[n,m,1]=colatitude
        :type xarray_obj: xr.DataArray
        '''
        self._obj = xarray_obj 
    pass

    def gamma_activity(self,plane='ba'):
        '''
        :param plane: relative activity of 'ba' for basal, 'pr' for prismatic, 'py' for pyramidal
        :type plane: str
        :return: relative basal activity map
        :rtype: im2d.image2d
        '''
        nn=np.linalg.norm(np.float128(self._obj),axis=-1)
        
        if plane=='ba':
            res=np.linalg.norm(np.float128(self._obj)[...,0:3],axis=-1)/nn
        elif plane=='pr':
            res=np.linalg.norm(np.float128(self._obj)[...,3:6],axis=-1)/nn
        elif plane=='py':
            res=np.linalg.norm(np.float128(self._obj)[...,6:12],axis=-1)/nn
            
        return xr.DataArray(res,dims=self._obj.coords.dims[0:-1])
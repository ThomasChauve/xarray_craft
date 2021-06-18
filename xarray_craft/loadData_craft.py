import xarray as xr
import os
import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy

import xarrayaita.loadData_aita as lda


def craft1time_2d(adr_data,time):
    '''
    Function to load the data from craft
    
    The input file should be in the adr_data folder and the output file should be in adr_data/output folder.
    It must contained at least '*strain.vtk', '*stress.vtk', '*gamma.vtk'
    
    :param adr_data: path to the simulation
    :type adr_data: str
    :param time: time as written in the output file
    :type micro_adress: str
    
    .. note:: to open the vtk file you vtk_plit install from craft. It will be nice to find a better solution
    '''
    data_name=os.listdir(adr_data)
    
    adr_graindId=[data_name[i][-4::] for i in range(len(data_name))].index('.vtk')
    adr_phase=[data_name[i][-6::] for i in range(len(data_name))].index('.phase')
    
    ds=lda.craft_input(adr_data+data_name[adr_graindId],adr_data+data_name[adr_phase])
    
    tmp=adr_data+'output/'
    
    tmp_split='vtk_split '+tmp+'*'+time+'_gamma.vtk'
    os.system(tmp_split)
    tmp_split='vtk_split '+tmp+'*'+time+'_strain.vtk'
    os.system(tmp_split)
    tmp_split='vtk_split '+tmp+'*'+time+'_stress.vtk'
    os.system(tmp_split)
    
    data_name_cr=os.listdir(tmp)
    
    wanted_data=[time+'_strain11.vtk',time+'_strain22.vtk',time+'_strain33.vtk',time+'_strain12.vtk',time+'_strain13.vtk',time+'_strain23.vtk',
                 time+'_stress11.vtk',time+'_stress22.vtk',time+'_stress33.vtk',time+'_stress12.vtk',time+'_stress13.vtk',time+'_stress23.vtk',
                 time+'_gamma01.vtk',time+'_gamma02.vtk',time+'_gamma03.vtk',time+'_gamma04.vtk',time+'_gamma05.vtk',time+'_gamma06.vtk',time+'_gamma07.vtk',time+'_gamma08.vtk',time+'_gamma09.vtk',time+'_gamma10.vtk',time+'_gamma11.vtk',time+'_gamma12.vtk']
    
    
    strain=[]
    stress=[]
    gamma=[]
    reader = vtk.vtkDataSetReader()
    for j in range(len(wanted_data)):
        for k in range(len(data_name_cr)):
            if (data_name_cr[k][len(data_name_cr[k])-len(wanted_data[j]):]==wanted_data[j]):
                nb=k
                break
        reader.SetFileName(tmp+data_name_cr[nb])
        print(data_name_cr[nb])
        reader.Update()
        ug  = reader.GetOutput()
        if j in range(6):
            strain.append(vtk_to_numpy(ug.GetPointData().GetScalars()).reshape((ug.GetDimensions()[0:2][::-1])))
        elif j in range(12):
            stress.append(vtk_to_numpy(ug.GetPointData().GetScalars()).reshape((ug.GetDimensions()[0:2][::-1])))
        elif j in range(24):
            gamma.append(vtk_to_numpy(ug.GetPointData().GetScalars()).reshape((ug.GetDimensions()[0:2][::-1])))

    
    ds['strain']=xr.DataArray(np.expand_dims(np.dstack(strain),axis=0),dims=('time','y','x','sT'))
    ds['stress']=xr.DataArray(np.expand_dims(np.dstack(stress),axis=0),dims=('time','y','x','sT'))
    ds['gamma']=xr.DataArray(np.expand_dims(np.dstack(gamma),axis=0),dims=('time','y','x','g'))
    
    ds.attrs['simu_time']=time
    
    os.system('rm '+tmp+'*strain1*.vtk '+tmp+'*strain2*.vtk '+tmp+'*stress1*.vtk '+tmp+'*stress2*.vtk '+tmp+'*33.vtk '+tmp+'*gamma0*.vtk '+tmp+'*gamma1*.vtk '+tmp+'*rotation1.vtk '+tmp+'*rotation2.vtk '+tmp+'*rotation3.vtk' )
    
    
    return ds
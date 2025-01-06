from mapping import *

min_samples_size = 605

from scipy import interpolate
import numpy as np

def resample_with_spline(data, new_length=min_samples_size):
    old_indices = np.linspace(0, len(data) - 1, num=len(data))
    new_indices = np.linspace(0, len(data) - 1, num=new_length)
    tck = interpolate.splrep(old_indices, data, s=0)
    return interpolate.splev(new_indices, tck, der=0)

def raw_data(sample):
    print('raw_data')
    #print(sample)
    old_RwristX = sample["Rwrist"]["x"]
    RwristX = resample_with_spline(sample["Rwrist"]["x"])

    RwristY = resample_with_spline(sample["Rwrist"]["y"])
    RwristZ = resample_with_spline(sample["Rwrist"]["z"])
    Rwrist = [RwristX, RwristY, RwristZ]

    RelbowX = resample_with_spline(sample["Relbow"]["x"][:min_samples_size])
    RelbowY = resample_with_spline(sample["Relbow"]["y"][:min_samples_size])
    RelbowZ = resample_with_spline(sample["Relbow"]["z"][:min_samples_size])
    Relbow = [RelbowX, RelbowY, RelbowZ]

    RshoulderX = resample_with_spline(sample["Rshoulder"]["x"])
    RshoulderY = resample_with_spline(sample["Rshoulder"]["y"])
    RshoulderZ = resample_with_spline(sample["Rshoulder"]["z"])
    Rshoulder = [RshoulderX, RshoulderY, RshoulderZ]

    return [Rwrist, Relbow, Rshoulder]

def preprocess_data(sample,mode='train'):
    r_data = raw_data(sample)
    #print('r_data',r_data)
    #flatten the sample
    flatten = []
    for bp in r_data:
        for xyz in bp:
            flatten.extend(xyz)
    #print('preprocess_data_sample',flatten)
    return flatten
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 17:54:30 2014

@author: Mathew Topper
"""

#import pprint
#import matplotlib.pylab as plt

import numpy as np
import pandas as pd

from .distribution import gaussiandistribution

class SPT(object):
    
    def __init__(self):
    
        self.raw = {}
        self.normalised = {}

    def read(self, SPTFileName):
    
        '''
        Import Datawell .spt ascii file. Outputs structure SPT. 
        Tom Davey
        Jul 2011
        Modified into a class structure by M.B.R. Topper May 2012
        Converted to Python Dec 2014
        
        *.SPT Data Text File   
         
        System File plus Spectrum File
          
        All numbers are decimal.
          
        The System File is a list of 12 CrLf separated quantities as follows:
          
        Transmission Index                (-)
        Significant WaveHeight Hs(m0)     (cm)
        Zero-Upcross Period Tz            (s)
        Maximum PSD1 Smax                 (m2/Hz)
        Reference Temperature             (°C)
        Sea Surface Temperature           (°C)
        Battery Status                    (0-7)
        Vertical Accelerometer Offset     (m/s2)
        X Accelerometer Offset            (m/s2)
        Y Accelerometer Offset            (m/s2)
        Compass Heading                   (°, 0=North)
        Magnetic Field Inclination        (°)
        
        The Spectrum File is a list of 64 frequency records in a table as
        follows:
        
        Frequency (Hz) | Normalized PSD (-) | Direction (°) | Spread (°) |
        Skewness (-) | Kurtosis (-)
        ''' 
    
#       Open the file
        with open(SPTFileName, 'r') as fid:
            
            sptlines = fid.readlines()
    
#       Get the top 12 lines
        self.raw['tranIndex'] = float(sptlines.pop(0))
        self.raw['Hm0'] = float(sptlines.pop(0))
        self.raw['Tz'] = float(sptlines.pop(0))
        self.raw['Smax'] = float(sptlines.pop(0))
        self.raw['refTemp'] = float(sptlines.pop(0))
        self.raw['seaTemp'] = float(sptlines.pop(0))
        self.raw['batteryStatus'] = float(sptlines.pop(0))
        self.raw['vertOffset'] = float(sptlines.pop(0))
        self.raw['xOffset'] = float(sptlines.pop(0))
        self.raw['yOffset'] = float(sptlines.pop(0))
    
#       Get the record and strip the degree symbol if its there
        line = sptlines.pop(0)
        line = ''.join(e for e in line if e.isalnum())
        self.raw['compassHeading'] = float(line)
    
#       Get the record and strip the degree symbol if its there
        line = sptlines.pop(0)
        line = ''.join(e for e in line if e.isalnum())
        self.raw['magFieldInclination'] = float(line)

#       Read the remainder of the file to get the tabulated data.
        data = pd.DataFrame(columns=('Frequency',
                                     'Normalized PSD',
                                     'Direction',
                                     'Spread',
                                     'Skewness',
                                     'Kurtosis'
                                     ))

        for i, line in enumerate(sptlines):
            
            dataline = [float(x) for x in line.split(',')]
            data.loc[i] = dataline
            
        # Fix the data type of the frame
        data = data.astype(float)
            
        self.raw['data'] = data
        self.normalised = {}

    def make_normalised(self):
        
        self.normalised = {}
        
        # Rename the variables as it's not very clear
        data = self.raw['data']            
        
        self.normalised['bearingsDegrees'] = data['Direction'].values
        self.normalised['spreadingDegrees'] = data['Spread'].values
        self.normalised['skewness'] = data['Skewness'].values
        self.normalised['kurtosis'] = data['Kurtosis'].values

        # Get the frequencies
        frequencies = data['Frequency'].values
        
        # Scale up the PSD using the normalisation value
        PSD1D = data['Normalized PSD'] * self.raw['Smax']
        
        # Add info to the spectrum class
        self.normalised['frequencies'] = frequencies
        self.normalised['PSD1D'] = PSD1D
        
        # Get Hm0
        Hm0 = self.raw['Hm0'] / 100.
        
        self.normalised['Hm0'] = Hm0
        
        # Copy Tz
        self.normalised['Tz'] = self.raw['Tz']

            
    def add_distribution(self, intervalDegrees):

        intervalRadians = np.radians(intervalDegrees)
        bearingsRadians = np.radians(self.normalised['bearingsDegrees'])
        spreadingRadians = np.radians(self.normalised['spreadingDegrees'])
        PSD = self.normalised['PSD1D']

        spreadBearingsRadians, spreadPSD = \
                        gaussiandistribution( intervalRadians,
                                              PSD,
                                              bearingsRadians,
                                              spreadingRadians )
                                              
         # Get the frequency spread too
        spreadFrequency, _ = np.meshgrid( self.normalised['frequencies'],
                                          spreadPSD[:,1] )
                                    
                                    
        # Load up the results
        self.normalised['distributedFrequency']       = spreadFrequency
        self.normalised['distributedPSD']             = spreadPSD
        self.normalised['distributedBearingsRadians'] = spreadBearingsRadians
        self.normalised['distributedBearingsDegrees'] = \
                                        np.degrees(spreadBearingsRadians)
   
#if __name__ == '__main__':
#    
#    test = SPT()
#    test.read('test_spectrum_30min.spt')
#    
#    df = test.raw['data']
#    pprint.pprint(df.ix[df['Normalized PSD'].idxmax()])
#    
#    test.make_normalised()
#    
#    PSD1D = test.normalised['PSD1D']
#    freqs = test.normalised['frequencies']
#    
#    plt.plot(freqs, PSD1D)
#    plt.show()
    
#    test.add_distribution(10)
#    spreadFrequency = test.normalised['distributedFrequency']
#    spreadBearingsDegrees = test.normalised['distributedBearingsDegrees']
#    spreadPSD = test.normalised['distributedPSD']
#                    
#    z_min, z_max = -np.abs(spreadPSD).max(), np.abs(spreadPSD).max()
#    
#    plt.pcolor(spreadFrequency, spreadBearingsDegrees, spreadPSD,
#               cmap='RdBu', vmin=z_min, vmax=z_max)
#    plt.show()

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 18:36:39 2014

@author: Mathew Topper
"""

import numpy as np

def gaussiandistribution( intervalRadians,
                          PSD,
                          bearingsRadians,
                          spreadingRadians ):

    '''
    Function to apply directionality to 1D frequency and power spectral 
    density (freq, psd) information using directionality and spreading 
    (direc, spread). It does this by fitting a guassian distribution to each
    frquency bin.
    '''
    
    # OK, this needs to be done in RADIANS! Check if arrays too
    PSD = np.array(PSD)
    bearingsRadians = np.array(bearingsRadians)
    spreadingRadians = np.array(spreadingRadians)
    
    # Calculate the number of interations in the for loop.
    loopIterations = np.floor(2. * np.pi / intervalRadians)
    
    # Preallocate the new arrays
    spreadBearingsRadians = np.zeros([loopIterations, len(bearingsRadians)])
    GuassianDistribution = np.zeros([loopIterations, len(bearingsRadians)])
    
    # Prep the new directions
    centredDirections = np.arange(-np.pi, np.pi, intervalRadians)
    
    for newBearingCounter, shift in enumerate(centredDirections):
    
        # Distance from the mean direction for the given direction
        delta = bearingsRadians + shift
    
        # Guassian Equation with spreading as standard deviation
        top = -(delta-bearingsRadians) ** 2
        bottomleft = 2. * spreadingRadians ** 2
        bottomright = spreadingRadians * np.sqrt(2*np.pi)
        newBearings = np.exp( top / (bottomleft * bottomright) )
                                          
        GuassianDistribution[newBearingCounter, :] = newBearings
        spreadBearingsRadians[newBearingCounter, :] = delta
    
    # Create a matrix of repeated psd. The centredDirections is used to 
    # create the right number of rows
    mfactor, _ = np.meshgrid( PSD, centredDirections )
    
    spreadpsd = mfactor * GuassianDistribution
    
    # Fix any negative or over 2pi directions and fix
    lowIndex = np.nonzero(spreadBearingsRadians < 0.)
    
    spreadBearingsRadians[lowIndex] = spreadBearingsRadians[lowIndex] + \
                                                                    2 * np.pi
    
    highIndex = np.nonzero(spreadBearingsRadians > 2 * np.pi)
    
    spreadBearingsRadians[highIndex] = spreadBearingsRadians[highIndex] - \
                                                                    2 * np.pi
    
    # Sort the output
    sortedOutputs = sortmatricesbyaxis([spreadBearingsRadians, spreadpsd])
                                                                  
    spreadBearingsRadians = sortedOutputs[0]
    spreadpsd = sortedOutputs[1]
                    
    # Scale to the old PSD
    freqLength = spreadpsd.shape[1]
    
    # Generate a 1D PSD
    newPSD = np.zeros([freqLength])
    
    for i in xrange(freqLength):
        
        # An extra direction is required
        longDirs = np.zeros([spreadpsd.shape[0] + 1])
        
        longDirs[:-1] = spreadBearingsRadians[:,i]
        longDirs[-1] = spreadBearingsRadians[0,i] + 2 * np.pi
    
        # A matching PSD value must be provided too
        PSD2DSize = spreadpsd.shape
        newPSD2D = np.zeros([PSD2DSize[0] + 1, PSD2DSize[1]])
        
        newPSD2D[:-1,:] = spreadpsd
        newPSD2D[-1,:] = spreadpsd[0,:]
    
        newPSD[i] = np.trapz(newPSD2D[:, i], longDirs)
            
    PSDDiff = newPSD / PSD
    
    for i in xrange(freqLength):
        
        # An extra direction is required
        spreadpsd[:, i] = spreadpsd[:, i] / PSDDiff[i]
        
    return spreadBearingsRadians, spreadpsd
    
def sortmatricesbyaxis( sortMatrices, sort_axis=0 ):
                                        
    '''Sort the first matrix in sortMatrices by the given sort_axis.
    Then apply that sorting to any additional matricies in the list.'''
    
    # Sort the primary matrix and record the indices
    sortMatrix = sortMatrices.pop(0)
    
    sortIndices = np.argsort(sortMatrix, axis=sort_axis)
    advancedIncides = list(np.ix_(*[np.arange(x) for x in sortMatrix.shape]))
    advancedIncides[sort_axis] = sortIndices
    
    # Add primary matrix to the output list
    primarySorted = sortMatrix[advancedIncides]
    sortedMatrices = [primarySorted]
    
    # For each additional matrix sort it using the indexes derived by the sort
    # of the primary matrix.
    for additionalMatrix in sortMatrices:
        
        additionalSorted = additionalMatrix[advancedIncides]
        
        sortedMatrices.append(additionalSorted)
        
    return sortedMatrices
    
def test_sortmatricesbycolumn():
    
    '''Turn this into a proper test'''
    
    a = np.random.randint(0,100,(3,3))
    b = np.random.randint(0,100,(3,3))
    print a
    print b
    result = sortmatricesbyaxis([a,b])
    print result[0]
    print result[1]
    
def test_gaussiandistribution():
    
    bearing = np.radians(180)
    spreading = np.radians(30)
    
    intervalRadians = np.radians(10)
    PSD = [1]*5
    bearingsRadians = [bearing]*5
    spreadingRadians = [spreading]*5
    
    spreadBearingsRadians, spreadpsd = \
             gaussiandistribution( intervalRadians,
                                   PSD,
                                   bearingsRadians,
                                   spreadingRadians )

    test = np.trapz(spreadpsd[:,1], spreadBearingsRadians[:,1])
    print "Error in PSD of {0:.3f}%".format((test - 1) * 100)
    
if __name__ == '__main__':
    
#    test_sortmatricesbycolumn()
    test_gaussiandistribution()
    


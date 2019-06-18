

def generateDefault():
    ############# solver.inp file gen #############
    # f = open("solver.inp", "a+")
    f = open("fileTest.txt", "a+")
    fileContent = ["Density: ", "Viscosity: ", " ", "Number of Timesteps: ", "Time Step Size: ", " ", "Number of Timesteps between Restarts: ", \
     "Number of Force Surfaces: ", "Surface ID's for Force Calculation: ", "Force Calculation Method: ", "Print Average Solution: ", \
     "Print Error Indicators: ", " ", "Time Varying Boundary Conditions From File: ", " ", "Step Construction: ", " ", \
     "Number of Resistance Surfaces: ", "List of Resistance Surfaces: ", "Resistance Values: ", " ", "Pressure Coupling: ", \
     "Number of Coupled Surfaces: ", " ", "Backflow Stabilization Coefficient: ", "Residual Control: ", "Residual Criteria: ", "Minimum Required Iterations: ", \
     "svLS Type: ", "Number of Krylov Vectors per GMRES Sweep: ", "Number of Solves per Left-hand-side Formation: ", "Tolerance on Momentum Equations: ", \
     "Tolerance on Continuity Equations: ", "Tolerance on svLS NS Solver: ", "Maximum Number of Iterations for svLS NS Solver: ", "Maximum Number of Iterations for svLS Momentum Loop: ", \
     "Maximum Number of Iterations for svLS Continuity Loop: ", "Time Integration Rule: ", "Time Integration Rho Infinity: ", "Flow Advection Form: ", \
     "Quadrature Rule on Interior: ", "Quadrature Rule on Boundary: "]

    defaultFile = ["1.06", "0.04", " ", "100", "0.0004", " ", "10", "1", "1", "Velocity Based", "True", "False", " ", "True", " ", "1 2 3 4", " ", \
     "1", "3", "16000", " ", "Implicit", "1", " ", "0.2", "True", "0.01", "3", "NS", "100", "1", "0.05", "0.4", "0.4", "1", "2", "400", "Second Order", \
     "0.5", "Convective", "2", "3"]
    index1 = 0
    index2 = 0
    for txt in range(len(fileContent)):
        f.write(fileContent[index1] + defaultFile[index1] + "\n")
        index1 += 1
    f.close()
    ############# .svpre file gen #############
    # pre = open("cylinderSim.svpre", "a+")
    pre = open("cylinderSim.txt", "a+")
    preContent = ["mesh_and_adjncy_vtu mesh-complete/mesh-complete.mesh.vtu", "set_surface_id_vtp mesh-complete/mesh-complete.exterior.vtp 1", \
    "set_surface_id_vtp mesh-complete/mesh-surfaces/cap_segment1.vtp 2", "set_surface_id_vtp mesh-complete/mesh-surfaces/cap_segment1_2.vtp 3", \
    "fluid_density 1.06", "fluid_viscosity 0.04", "initial_pressure 0", "initial_velocity 0.0001 0.0001 0.0001", \
    "prescribed_velocities_vtp mesh-complete/mesh-surfaces/cap_segment1.vtp", "bct_analytical_shape parabolic", "bct_period 1.0", \
    "bct_point_number 2", "bct_fourier_mode_number 1", "bct_create mesh-complete/mesh-surfaces/cap_segment1.vtp cap_segment1.flow", \
    "bct_write_dat bct.dat", "bct_write_vtp bct.vtp", "pressure_vtp mesh-complete/mesh-surfaces/cap_segment1_2.vtp 0", \
    "noslip_vtp mesh-complete/walls_combined.vtp", "write_geombc geombc.dat.1", "write_restart restart.0.1"]
    for newTxt in range(len(preContent)):
        pre.write(preContent[index2] + "\n")
        index2 += 1
    ############# Alter files #############
    userInp = raw_input('Would you like to alter either file? \n')
    if userInp == 'yes' or userInp == 'y' or userInp == "Yes":
        fileInp = raw_input("Enter the name of the file you'd like to change: [the solver.inp,  cylinderSim.svpre] \n")
        if (fileInp == 'solver.inp'):
            with open('/Users/tobiasjacobson/Documents/Atom/preScripting/fileTest.txt') as pr:
                content = pr.readlines()
                for thing in content:
                    sys.stdout.write(thing)
                alterFile = raw_input("Which line will you change?\n")
                addFile = raw_input("What will you replace it with?\n")
                fin = open("fileTest.txt")
                fout = open("fileTest1.txt", "wt")
                for line in fin:
                    fout.write( line.replace(alterFile, addFile) )
                fin.close()
                fout.close()
                os.remove('/Users/tobiasjacobson/Documents/Atom/preScripting/fileTest.txt')
        elif (fileInp == 'cylinderSim.svpre'):
            print('')
        else:
            print('Not a valid file')
    pre.close()

###############################
#             Main            #
###############################

import os
import fileinput
import sys
# os.remove('/Users/tobiasjacobson/Documents/Atom/preScripting/cylinderSim.txt')
# os.remove('/Users/tobiasjacobson/Documents/Atom/preScripting/fileTest.txt')
# Moving from root directory
os.chdir('/Users/tobiasjacobson/Documents/Atom/preScripting')
generateDefault()

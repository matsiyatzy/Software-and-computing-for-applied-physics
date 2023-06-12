import numpy as np
import scipy.spatial as spsa
'''
    The functions in this file is heavily based on the work done by 
    Kjetil A. Johannessen and Abdullah Abdulhaque at NTNU that provided 
    a very similar code to use in the course TMA4220.
'''

def generate_mesh(num_nodes):
    '''
        Generates a finite element mesh with N nodes of the unite circle.
        ----------------
        Inputs: 
            num_nodes (int): Number of nodes in the finite element mesh
        ----------------
        Outputs:
            
       ----------------
        Raises:
            ValueError:
                
        ----------------
        Long description: 
            The function generates a mesh of the unit circle by splitting it up in triangles.
            Number of nodes in the mesh is given by the input N. The function returns ...
    '''


    # Getting data about circle.
    outwards_circles, radii_of_circles, dof_in_circles, starting_angle_for_circles = circle_data(num_nodes)

    # Generating the nodal points.
    #p = nodal_points(pass)

    

    # Generating the boundary elements.
   # edge = FreeBoundary(N,alpha)

    pass

#--------------------------------------------

def circle_data(num_nodes):
    '''
        Calculate data related to circles based on the given number of degrees of freedom (N).
        It is called from the function generate_mesh().
        ----------------
        Input:
        - num_nodes (int): Number of degrees of freedom desired for the circles.
        ----------------
        Returns:
        - outward_circles (int): Number of outward circles, excluding the origin.
        - radii_of_circles (ndarray): Array of radii for the different circles.
        - dof_in_circles (ndarray): Array containing the number of degrees of freedom in each circle.
        - starting_angle_for_circles (ndarray): Array of starting angles for each circle.
        ----------------
        Raises:
            No need to test the input, as it is the same input as for its "parent function", 
            aka the function it is called in.
        ----------------
        Long description:
            The function computes the number of outward circles, the radii, the number of degrees of freedom,
            and the starting angles for each circle based on the given number of degrees of freedom (num_nodes).
    '''
    
    # Number of outward circles,excluding the origin.
    outward_circles = int(np.floor(np.sqrt(num_nodes / np.pi)))

    # Radius of the different circles.
    radii_of_circles = np.linspace(0, 1, outward_circles + 1)

    # Number of DOF in each circle.
    dof_in_circles_temp = np.floor((2 * np.pi * outward_circles) * radii_of_circles)
    dof_in_circles = np.zeros(len(dof_in_circles_temp), dtype=int)
    for i in range(len(dof_in_circles_temp)):
        dof_in_circles[i] = int(dof_in_circles_temp[i])

    # Fine-tuning to get the right amount of DOF.
    dof_in_circles[0] = 1
    i = 1
    while sum(dof_in_circles) > num_nodes:
        if dof_in_circles[i] > 0:
            dof_in_circles[i] -= 1
        i += 1
        if sum(dof_in_circles[1:outward_circles]) == 0:
            i = outward_circles
        elif i > outward_circles:
            i = 1

    while sum(dof_in_circles) < num_nodes:
        dof_in_circles[-1] += 1

    # Creating the starting angle.
    starting_angle_for_circles = np.pi / dof_in_circles
    starting_angle_for_circles[0::2] = 0

    return outward_circles, radii_of_circles, dof_in_circles, starting_angle_for_circles

#--------------------------------------------

#...

import numpy as np
import scipy.spatial as spsa


def generate_mesh(N):
    '''
        Generates a finite element mesh with N nodes of the unite circle.
        ----------------
        Inputs: 
            N: Number of nodes in the finite element mesh
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
    a, b = circle_data(N)

    # Generating the nodal points.
    p = nodal_points()

    

    # Generating the boundary elements.
    edge = FreeBoundary(N,alpha)

    return p


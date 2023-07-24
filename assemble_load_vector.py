import numpy as np
import inspect

import numerical_integration as numint


def zero_func(x, y):
    '''
        This is the zero function.
        ----------------
        Inputs: 
            - x (ndarray): array of x-coordinates/inputs
            - y (ndarray): array of y-coordinates/inputs
        ----------------
        Outputs:
            - ndarray of len(x) zeros
       ----------------
        Raises:
            - ValueError: if x and y have different size
        ----------------
        Long description: 
            A simple implementation that returns the zero function from two inputs x and y.
            This is used as the default parameter for the right hand side of the PDE.
    '''
    if (len(x) != len(y)):
        raise ValueError ("x and y must have the same size")
    return np.zeros(len(x))

def elemental_load_vector(nodal_points, element, right_hand_side = zero_func):
    '''¨
        Function that creates the local 3x1 load vector.
        ----------------
        Inputs: 
            nodal_points: The list of all nodes in the unit circle mesh
            element: The given element to calculate the local elemental matrix on.
                     It is a list/array of 3 indices.
            right_hand_side: the function on the right hand side of the original poisson equation
        ----------------
        Returns: 
            elemental_load: 3x1 vector being the elemental load vector on the given element
        ----------------
        Raises:
            ValueError: If the right_hand_side function cannot input 2 arguments
        ----------------
        Long description:
            This function takes in an element in the large unit circle mesh and calculates
            the points corresponding to this element. Then, calculate the local basis functions
            for these points. Lastly, calculate the effect on the local load from
            these basis functions.
    '''
    signature = inspect.signature(right_hand_side)
    parameters = signature.parameters
    if (not len(parameters) == 2):
        raise ValueError ("The right hand side needs to be able to accept two inputs")

    # Find the nodal points giving the vertices of the triangular element
    p1 = nodal_points[element[0]]
    p2 = nodal_points[element[1]]
    p3 = nodal_points[element[2]]

    # Matrix to determine coeffs in local basis functions
    M = np.column_stack([[1, 1, 1], [p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]]])

    # Find coeffs for local basis functions
    C_1 = np.linalg.solve(M, [1, 0, 0])
    C_2 = np.linalg.solve(M, [0, 1, 0])
    C_3 = np.linalg.solve(M, [0, 0, 1])

    # Full coefficient matrix for local basis function
    C = np.array([C_1, C_2, C_3])

    # Create empty local load vector
    Fh_k = np.zeros(3)
    for alpha in range(3):
        # Create local basis function H = c + c_x*c + c_y*y
        H = lambda x, y : C[alpha,0] + C[alpha,1] * x + C[alpha,2] * y
        # Generate right hand side of the integral
        Hf = lambda x, y : H(x, y) * right_hand_side(x, y)
        Fh_k[alpha] = numint.gaussian_quadrature_2D(p1, p2, p3, 4, Hf)
    return Fh_k

#----------------------------------------------------------------------------------------

def load_vector(num_nodes, nodal_points, elements, right_hand_side = zero_func):
    '''
        This function assembles the whole load vector F. 
        ----------------
        Inputs:
            num_nodes (int): Total number of nodes in the finite element mesh
            nodal_points: List/numpy array of all nodal points in the mesh
            elements: List/numpy array where every element is a vector with 3 elements
                      which gives the index in the nodal_points array of which nodes
                      makes up element i
            right_hand_side: the function on the right hand side of the original poisson equation
        ----------------
        Output:
           load_vector: A num_nodes long vector that is the load
                              vector for the whole system
        ----------------
        Raises:
            -
        ----------------
        Long description:
            This function uses the mesh of the unit circle and the helping function 
            elemental_load_vector() to assemble the full load vector of
            the system.
    '''
    # Initialize load vector as a vector of zeros
    F = np.zeros(num_nodes)
    num_elemenents = len(elements)

    for k in range(num_elemenents):
        Fh_k = elemental_load_vector(nodal_points, elements[k], right_hand_side)
        for alpha in range(3):
            # Local to global map
            i = elements[k, alpha]
            F[i] += Fh_k[alpha]
    return F

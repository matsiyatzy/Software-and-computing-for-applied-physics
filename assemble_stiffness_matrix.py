import numpy as np


def elemental_stiffness_matrix(nodal_points, element):
    '''¨
        Function that creates the local 3x3 elemental matrices.
        ----------------
        Inputs: 
            nodal_points: The list of all nodes in the unit circle mesh
            element: The given element to calculate the local elemental matrix on.
                     It is a list/array of 3 indices.
        ----------------
        Returns: 
            elemental_matrix: 3x3 matrix being the elemental matrix on the given element
        ----------------
        Raises:

        ----------------
        Long description:
            This function takes in an element in the large unit circle mesh and calculates
            the points corresponding to this element. Then, calculate the local basis functions
            for these points. Lastly, calculate the effect on the local elemental matrix from
            these basis functions.
    '''
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

    print(C)

    # Create empty local elemental matrix
    A_k = np.zeros((3, 3))

    # Calculate the area of a triangle given by (p1, p2, p3)
    area = 1/2 * np.abs(p1[0]*(p2[1] - p3[1]) + p2[0]*(p3[1]-p1[1]) + p3[0]*(p1[1]-p2[1]))

    # Assemble local elemental matrix - follows the theory pdf
    for alpha in range(3):
        for beta in range(3):
            # A^k_{alpha, beta} = area(triangle) * (c_x,alpha * c_x,beta + c_y, alpha * c_y, beta)
            A_k[alpha,beta] = area * (C[alpha,1] * C[beta,1] + C[alpha,2] * C[beta,2])
    return A_k

#----------------------------------------------------------------------------------------

def stiffness_matrix(num_nodes, nodal_points, elements):
    pass

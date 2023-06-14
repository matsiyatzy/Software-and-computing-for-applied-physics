import numpy as np
import matplotlib.pyplot as plt

import assemble_load_vector as loadvec
import assemble_stiffness_matrix as stiffmat
import generate_mesh as mesh

def solver(num_nodes, right_hand_side = loadvec.zero_func):
    '''
        This function uses other implemented functions and imposes the boundary conditions.
        In short words, this function is used to solve the whole system, 
        nabla^2 u(x, y) = -f(x, y)
        ----------------
        Inputs:
            num_nodes (int): Total number of nodes in the finite element mesh
            right_hand_side: the function on the right hand side of the original poisson equation (f(x, y))
        ----------------
        Output:
            sol: A vector of length num_nodes that is the solution to the poisson problem 
            nodal_points: the nodal_points we get from the mesh generation
        ----------------
        Raises:
            -
        ----------------
        Long description:
            This function uses the mesh of the unit circle to build the stiffness matrix
            and load vector. Then, the homogeneous dirichlet boundary conditions are imposed
            by removing the rows and columns corresponding to boundary elements in the
            stiffness matrix (as we already know the value here). 
    '''
    # Generate mesh
    nodal_points, elements, boundary_edges = mesh.generate_mesh(num_nodes)

    # Assemble stiffness matrix
    A = stiffmat.stiffness_matrix(num_nodes, nodal_points, elements)

    # Assemble load vector
    F = loadvec.load_vector(num_nodes, nodal_points, elements, right_hand_side)

    # Impose boundary conditions by removing boundary nodes from A and F
    edge_nodes = np.unique(boundary_edges).astype(int)
    
    A = np.delete(A, edge_nodes, axis = 0)
    A = np.delete(A, edge_nodes, axis = 1)
    F = np.delete(F, edge_nodes)

    # Solve linear system
    solution_temp = np.linalg.solve(A, F)

    # Get the full solution by adding zeros on boundary again
    sol = np.zeros(num_nodes)
    sol[:len(solution_temp)] = solution_temp

    # Return the solution, and nodal_points + elements for plotting
    return sol, nodal_points

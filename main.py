import numpy as np

import solver
import generate_mesh as mesh
import plotting


def right_hand_side_f(x, y):
    '''
        This function gives the right hand side of the Poisson problem.
        ----------------
        Inputs:
            - x (ndarray): array of x-coordinates/inputs
            - y (ndarray): array of y-coordinates/inputs
        ----------------
        Output:
            - ndarray of the value of f (the right hand side) at each pair (x, y)
        ----------------
        Raises:
            - ValueError: if x and y have different sizes
        ----------------
        Long description:
            This function gives the right hand side of the Poisson problem,
            nabla^2 u(x, y) = -f(x, y),
            where f(x, y) is given by this function.
    '''
    if (len(x) != len(y)):
        raise ValueError ("x and y must have the same size")
    return 1 - x**2 - y**2

#----------------------------------------------------------------------------------------

def run_program(num_nodes = 1000, plot_exact = False, exact_sol = np.zeros(10)):
    '''
        This function runs the whole solver program.
        ----------------
        Inputs:
            num_nodes (int): Total number of nodes in the finite element mesh
            plot_exact (bool): Flag to indicate whether or not you want to plot
                               the exact solution. If this is true, an exact sol
                               must be provided.
            exact_sol (ndarray): The exact solution to the given problem, on the same format
                                 as numerical_sol. This must be provided if plot_exact = True.
                                 If you don't have the exact solution on vector form, but only
                                 as a python function, the exact solution can be found by
                                 exact_sol = exact_function(nodal_points[:, 0], nodal_points[:, 1]).
                                 Just comment out the line in this function to use it.
        ----------------
        Output:
            -
        ----------------
        Raises:
            -
        ----------------
        Long description:
            This function runs the whole program which solves the 2D poisson problem
            nabla^2 u(x, y) = -f(x, y),
            where f is given at the top of this file. The input variable num_nodes
            gives the total number of nodes in the FEM mesh. 

    '''
    # Find numerical solution and mesh
    sol, nodal_points, elements, boundary_edges = solver.solver(num_nodes, right_hand_side_f)

    # Comment out the below line if you only have exact solution on function form
    # exact_sol = exact_func(nodal_points[:, 0], nodal_points[:, 1])

    # Plot mesh
    print(f"The finite element mesh given by the provided {num_nodes} nodes: ")
    plotting.plot_unit_circle_mesh(nodal_points, elements, boundary_edges)


    # Plot solution
    if (plot_exact):
        plotting.plot_solution(nodal_points, sol, True, exact_sol)
    else:
        plotting.plot_solution(nodal_points, sol)


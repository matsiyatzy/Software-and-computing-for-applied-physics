import numpy as np

import solver
import plotting

import sys


#----------------------------------------------------------------------------------------

def run_program(args):
    '''
        This function runs the whole solver program.
        ----------------
        Inputs:
            args: Command line input. The first input is:
                num_nodes: Total number of nodes in the finite element mesh
                function: a python function written in text-form without spaces
                          for example: x**2+y**2+1 <- this can be written into 
                          the command line
                verbose: true/false whether or not you want the prints during the run (default True)
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
    def right_hand_side_f(x, y):
        '''
            This function gives the right hand side of the Poisson problem. 
            This function comes from the command line.
            ----------------
            Inputs:
                - x (ndarray): array of x-coordinates/inputs
                - y (ndarray): array of y-coordinates/inputs
            ----------------
            Output:
                - ndarray of the value of f (the right hand side) at each pair (x, y)
            ----------------
            Raises:
               
            ----------------
            Long description:
                This function gives the right hand side of the Poisson problem,
                nabla^2 u(x, y) = -f(x, y),
                where f(x, y) is given by this function.
        '''
        function = args[1]
        func_val = eval(function)

        return func_val
    
    verbose = True
    if len(args) > 2:
        verbose_arg = args[2]
        if (verbose_arg == "False" or verbose_arg == "false"):
            verbose = False

    # Find numerical solution and mesh
    num_nodes = int(args[0])
    if (verbose):
        print("Running the solver...")
    sol, nodal_points, elements, boundary_edges = solver.solver(num_nodes, right_hand_side_f)

    # Plot mesh
    if (verbose):
        print(f"The finite element mesh given by the provided {num_nodes} nodes: ")
    plotting.plot_unit_circle_mesh(nodal_points, elements, boundary_edges)


    # Plot solution
    if (verbose):
        print("Here is the numerical solution of the poisson equation: ")
    plotting.plot_solution(nodal_points, sol)

#----------------------------------------------------------------------------------------

if __name__ == "__main__":
    args = sys.argv[1:]
    run_program(args)
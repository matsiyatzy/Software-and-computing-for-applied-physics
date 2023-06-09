import matplotlib.pyplot as plt
import numpy as np

def plot_unit_circle_mesh(nodal_points, elements, boundary_edges):
    '''
        This function plots the mesh of the unit circle.
        ----------------
        Inputs: 
            nodal_points (ndarray): List of all nodal points in the mesh
            elements (ndarray): List where each element is a list of size 3. This
                                list indicates by index which of the nodal points
                                that make up the element
            boundary_edges (ndarray): List where each element is a list of size 2.
                                      This list indicates by index which two nodal
                                      points makes up the endpoints of the edge.
        ----------------
        Outputs:
            None, but shows a plot of the meshed unit circle
       ----------------
        Raises:
            -
        ----------------
        Long description: 
            This function uses all three outputs from the generate_mesh() function in
            generate_mesh.py to make a plot of the unit circle with the corresponding
            finite element mesh.
    '''
    # Assure that elements and boundary edges are represented as ints
    elements = elements.astype(int)
    boundary_edges = boundary_edges.astype(int)

    # Represent nodal points as a long list
    x = nodal_points[:, 0].flatten()
    y = nodal_points[:, 1].flatten()

    # Find total number of nodes
    num_nodes = len(nodal_points)

    # Plot interior elements
    plt.plot(x[elements.T], y[elements.T], color = "red")

    # Plot boundary edges
    plt.plot(x[boundary_edges.T], y[boundary_edges.T], color = "black")

    # Give a title to the plot
    plt.title(f"Plot of the unit mesh with num_nodes = {num_nodes}")
    plt.show()

#----------------------------------------------------------------------------------------

def plot_solution(nodal_points, numerical_sol, plot_exact = False, exact_sol = np.zeros(10)):
    '''
        Function that plots the solution of the 2D poisson problem
        ----------------
        Inputs: 
            nodal_points (ndarray): List of all nodal points in the mesh
            numerical_sol (ndarray): The numerical solution received from the 
                                     solver() function. Given as an len(nodal_points) array
            plot_exact (bool): Flag to indicate whether or not this function should also
                               plot the exact solution to the given problem. If this is true, 
                               an exact solution must also be provided. 
            exact_sol (ndarray): The exact solution to the given problem, on the same format
                                 as numerical_sol. This must be provided if plot_exact = True.
        ----------------
        Outputs:
            None, but plots a solution to the 2D poisson problem, and if provided, also the
            exact solution.
       ----------------
        Raises:
            ValueError: if plot_exact = True, but exact_sol is not provided
        ----------------
        Long description: 
            This function takes the numerical solution of the 2D poisson problem provided
            by the function solver.solver() and plots it. If the user wants, and have access
            to the exact solution, this can also be plotted together with the error.
    '''
    num_nodes = len(nodal_points)

    if (plot_exact):
        if len(exact_sol != len(numerical_sol)):
            raise ValueError ("Exact solution and numerical solution are of different size")

    if (plot_exact):

        fig = plt.figure(figsize=(18, 6))
        fig.suptitle(f"num_nodes = {num_nodes}", size = 22)
        
        ax1 = fig.add_subplot(1, 3, 1, projection="3d")
        ax1.plot_trisurf(nodal_points[:, 0], nodal_points[:, 1], numerical_sol, linewidth=0.2)
        ax1.set_title("Numerical solution")
        
        ax2 = fig.add_subplot(1, 3, 2, projection="3d")
        ax2.plot_trisurf(nodal_points[:, 0], nodal_points[:, 1], exact_sol, linewidth=0.2)
        ax2.set_title("Exact")
        
        ax3 = fig.add_subplot(1, 3, 3, projection="3d")
        ax3.plot_trisurf(nodal_points[:, 0], nodal_points[:, 1], np.abs(numerical_sol - exact_sol), linewidth=0.2)
        ax3.set_title("|Error|")

        plt.show()

    else:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.plot_trisurf(nodal_points[:, 0], nodal_points[:, 1], numerical_sol, linewidth=0.2)
        ax.set_title(f"Numerical solution with num_nodes = {num_nodes}")
        plt.show()
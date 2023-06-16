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
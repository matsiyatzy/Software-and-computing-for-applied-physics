import pytest
import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st

import numerical_integration as numint
import generate_mesh as gm
import assemble_stiffness_matrix as stiffness
import assemble_load_vector as load


# Tests from numerical_integration.py
#----------------------------------------------------------------------------------------

def test_gaussian_quadrature_2d_simple():
    '''
        Test that the gaussian_quadrature_2d function can evaluate a simple integral
        on a simple domain. In this case the function g(x, y) = x+y on the triangle
        given by the points (0, 0), (1, 0) and (0, 1).
        Which is int_0^1 int_0^1 x+y dxdy = 1/3
    '''

    def g(x, y):
        return x+y

    p1 = np.array([0, 0])
    p2 = np.array([0, 1])
    p3 = np.array([1, 0])

    exact = 1/3

    numerical_value = numint.gaussian_quadrature_2D(p1, p2, p3, 4, g)
    assert np.abs(numerical_value-exact) < 0.01

#----------------------------------------------------------------------------------------

def test_gaussian_quadrature_2d_advanced():
    '''
        Test that the gaussian_quadrature_2d function can evaluate a tougher integral
        on a non-trivial domain. In this case the function g(x, y) = log(x+y) on the triangle
        given by the points (1, 0), (3, 1) and (3, 2).
        Which is int_0^1 int_0^1 log(x+y) dxdy approx 1.16541
    '''

    def g(x, y):
        return np.log(x+y)

    p1 = np.array([1, 0])
    p2 = np.array([3, 1])
    p3 = np.array([3, 2])

    exact = 1.16541

    numerical_value = numint.gaussian_quadrature_2D(p1, p2, p3, 4, g)

    assert np.abs(numerical_value - exact) < 0.01

#----------------------------------------------------------------------------------------

# Tests from generate_mesh.py
#----------------------------------------------------------------------------------------

@given(num_nodes = st.integers(4, 1000))
def test_circle_data_outwards_circle(num_nodes):
    '''
        Test that the outward_circle argument from the function circle_data
        is at it should. It should be an integer larger than 0.
    '''
    outwards_circles, _, _, _ = gm.circle_data(num_nodes)

    assert isinstance(outwards_circles, int), "Number of outward circles should be an integer"
    assert outwards_circles > 0, "There should be a positive number of outwards circles" 

#----------------------------------------------------------------------------------------

@given(num_nodes = st.integers(4, 1000))
def test_circle_data_radii_of_circles(num_nodes):
    '''
        Test that the radii_of_circles argument from the function circle_data()
        is at it should. The variable should be a np.ndarray. The first element
        is the radius of the origin (that sounds weird but well well) should be 0,
        and the radius of the last circle should be 1 (as the unit circle has radius 1)
    '''
    _, radii_of_circles, _, _ = gm.circle_data(num_nodes)

    assert isinstance(radii_of_circles, np.ndarray), "The radii of the circles should be a np.array"
    assert radii_of_circles[0] == 0, "Radius of the origin must be 0"
    assert radii_of_circles[-1] == 1, "Radius of the last circle must be 1"

#----------------------------------------------------------------------------------------

@given(num_nodes = st.integers(4, 1000))
def test_circle_data_dof_in_circles(num_nodes):
    '''
        Test that the dof_in_circles argument from the function circle_data()
        is at it should. The variable should be a np.ndarray and the total
        sum of all elements should be equal to num_nodes.
    '''
    _, _, dof_in_circles, _ = gm.circle_data(num_nodes)

    assert isinstance(dof_in_circles, np.ndarray), "The dof in each circle should be a np.array"
    assert np.sum(dof_in_circles) == num_nodes, "The total degrees of freedom should equal num of nodes"
    
#----------------------------------------------------------------------------------------

@given(num_nodes = st.integers(4, 1000))
def test_circle_data_starting_angle_for_circles(num_nodes):
    '''
        Test that the starting_angles_for_circles argument from the function circle_data()
        is at it should. The variable should be a np.ndarray and all elements
        should have a value between 0 and 2 pi. 
    '''
    _, _, _, starting_angles = gm.circle_data(num_nodes)

    assert isinstance(starting_angles, np.ndarray), "The atarting angles list should be a np.array"
    for i in range(len(starting_angles)):
        assert starting_angles[i] < 2*np.pi, "Starting angle must be smaller than 2*pi"
        assert starting_angles[i] >= 0, "Starting angle must be larger than 0"

#----------------------------------------------------------------------------------------

@given(num_nodes = st.integers(4, 10000))
def test_get_nodal_points_inside_unit_circle(num_nodes):
    '''
        Test that the function get_nodal_points only generate points
        that are inside the unit circle. 
    '''
    outward_circles, radii_of_circles, dof_in_circles, starting_angle_for_circles = gm.circle_data(num_nodes)

    # Generating the nodal points.
    nodal_points = gm.get_nodal_points(num_nodes, outward_circles, radii_of_circles, dof_in_circles, starting_angle_for_circles)

    for i in range(len(nodal_points)):
        assert np.round(nodal_points[i, 0]**2 + nodal_points[i, 1]**2, 4) <= 1, "Nodal points are outside unit circle"

#----------------------------------------------------------------------------------------

@given(num_nodes = st.integers(4, 10000))
def test_get_boundary_edges_on_boundary(num_nodes):
    '''
        Test that the function get_boundary_edges only generate edges
        betweem nodes that are on the boundary of the unit circle. 
    '''
    outward_circles, radii_of_circles, dof_in_circles, starting_angle_for_circles = gm.circle_data(num_nodes)

    # Generating all nodes
    nodal_points = gm.get_nodal_points(num_nodes, outward_circles, radii_of_circles, dof_in_circles, starting_angle_for_circles)

    # Generating the boundary nodes
    boundary_edges = gm.get_boundary_edges(num_nodes, dof_in_circles)

    for boundary_edge in boundary_edges:
        first_node = boundary_edge[0]
        second_node = boundary_edge[1]
        print(nodal_points[int(first_node)][0]**2 + nodal_points[int(first_node)][1]**2)
        print(nodal_points[int(second_node)][0]**2 + nodal_points[int(second_node)][1]**2)
        
        # Make sure that first node is on the boundary
        assert np.isclose(nodal_points[int(first_node)][0]**2 + nodal_points[int(first_node)][1]**2, 1), "All boundary nodes needs to be on the boundary"

        # Make sure the second node is on the boundary
        assert np.isclose(nodal_points[int(second_node)][0]**2 + nodal_points[int(second_node)][1]**2, 1), "All boundary nodes needs to be on the boundary"

#----------------------------------------------------------------------------------------

@given (num_nodes = st.integers(4, 1000))
def test_generate_mesh_elements(num_nodes):
    '''
        This is a test function for the function generate_mesh().
        The first output variable is already tested in test_nodal_points_inside_unit_circle.
        The last output variable is already tested in test_get_boundary_edges_on_boundary.
        This function tests that all elements have 3 unique nodes, and that
        all of the nodes are used to create elements.
    '''

    nodal_points, elements, boundary_edges = gm.generate_mesh(num_nodes)

    for element in elements:
        assert len(element) == 3, "All elements must have 3 nodes"
        assert len(np.unique(element) == 3), "All nodes in element must be unique"

#----------------------------------------------------------------------------------------

# Tests from assemble_stiffness_matrix
#----------------------------------------------------------------------------------------

def test_elemental_stiffness_matrix():
    '''
        This is a test function for the function elemental_stiffness_matrix().
        To test this, I check the basic case where
        nodal_points = ([0, 0], [1, 0], [0, 1]). Following the calculations in the 
        .pdf theory file, we get:
        [c_1, c_x,1, c_y, 1] = [1, -1, 0]
        [c_2, c_x,2, c_y, 2] = [0, 1, 0]
        [c_3, c_x,3, c_y, 3] = [0, 0, 1]
        Area = 1/2
        And then from the formula 
        elemental_matrix_{alpha, beta} = area*(c_x,alpha * c_x,beta + c_y, alpha * c_y, beta), 
        the elemental matrix for this simple example is:
        A_k = [[1, -0.5, -0.5], 
               [-0.5, 0.5, 0], 
               [-0.5, 0, 0.5]]
    '''
    nodal_points = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [0.5, 0.5]])
    element = [0, 1, 2]
    A_k = stiffness.elemental_stiffness_matrix(nodal_points, element)

    expected_output = np.array([[1, -0.5, -0.5], 
                                [-0.5, 0.5, 0], 
                                [-0.5, 0, 0.5]])
    
    assert np.allclose(A_k, expected_output), "Wrong elemental matrix in simple case"

#----------------------------------------------------------------------------------------

@given(num_nodes = st.integers(4, 100)) # Only up to 100 due to time condition in pytest
def test_stiffness_matrix(num_nodes):
    '''
        This is a test function for the function stiffness_matrix().
        This function asserts two main properties of the stiffness matrix, 
        that it is square and that it is singular.

    '''
    nodal_points, elements, boundary_edges = gm.generate_mesh(num_nodes)

    # Assemble stiffness matrix
    A = stiffness.stiffness_matrix(num_nodes, nodal_points, elements)

    assert A.shape[0] == A.shape[1], "Stiffness matrix must be square"

    # Check that matrix is singular (condition number is effectively infinite)
    assert np.linalg.cond(A) > 1e16, "Stifness matrix must be singular"

#----------------------------------------------------------------------------------------

# Tests from assemble_load_vector
#----------------------------------------------------------------------------------------

def test_elemental_load_vector():
    '''
        This is a test function for the function elemental_load_vector().
        To test this, I check the basic case where
        nodal_points = ([0, 0], [1, 0], [0, 1]). 
        For a right hand side function I use f(x, y) = x+y
        Following the calculations in the 
        .pdf theory file, we get:
        [c_1, c_x,1, c_y,1] = [1, -1, 0]
        [c_2, c_x,2, c_y,2] = [0, 1, 0]
        [c_3, c_x,3, c_y,3] = [0, 0, 1]
        And then from the formula, where 
        H_alpha = c_alpha + c_x,alpha * x + c_y,alpha * y
        elemental_load_{alpha} = int_{Triangle} f*H dA, 
        the elemental load vector for this simple example is:
        F_k = [1/12, 1/8, 1/8]
    '''
    def f_test(x, y):
        return x+y
    
    nodal_points = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    element = [0, 1, 2]
    F_k = load.elemental_load_vector(nodal_points, element, f_test)

    expected_output = np.array([1/12, 1/8, 1/8])
    
    assert np.allclose(F_k, expected_output), "Wrong elemental load vector in simple case"
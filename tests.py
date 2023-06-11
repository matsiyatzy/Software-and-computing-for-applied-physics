import pytest
import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st


import numerical_integration as numint
import generate_mesh as gm


# Tests from numerical_integration.py
#----------------------------------------------------------------------------------------

def test_gaussian_quadrature_2d_simple():
    '''
        Test that the gaussian_quadrature_2d function can evaluate a simple integral
        on a simple domain. In this case the function g(x, y) = x+y on the triangle
        given by the points (0, 0), (1, 0) and (0, 1).
        Which is \int_0^1\int_0^1 x+y dxdy = 1/3
    '''

    def g(x, y):
        return x+y

    p1 = np.array([0, 0])
    p2 = np.array([0, 1])
    p3 = np.array([1, 0])

    exact = 1/3

    numerical_value = numint.gaussian_quadrature_2D(p1, p2, p3, 4, g)
    assert np.abs(numerical_value-exact) < 0.01

#--------------------------------------------

def test_gaussian_quadrature_2d_advanced():
    '''
        Test that the gaussian_quadrature_2d function can evaluate a tougher integral
        on a non-trivial domain. In this case the function g(x, y) = log(x+y) on the triangle
        given by the points (1, 0), (3, 1) and (3, 2).
        Which is \int_0^1\int_0^1 log(x+y) dxdy \approx 1.16541
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

@given(num_points = st.integers(4, 1000))
def test_circle_data_outwards_circle(num_points):
    '''
        Test that the outward_circle argument from the function circle_data
        is at it should. It should be an integer larger than 0.
    '''
    outwards_circles, _, _, _ = gm.circle_data(num_points)

    assert isinstance(outwards_circles, int), "Number of outward circles should be an integer"
    assert outwards_circles > 0, "There should be a positive number of outwards circles" 

#--------------------------------------------

@given(num_points = st.integers(4, 1000))
def test_circle_data_radii_of_circles(num_points):
    '''
        Test that the radii_of_circles argument from the function circle_data()
        is at it should. The variable should be a np.ndarray. The first element
        is the radius of the origin (that sounds weird but well well) should be 0,
        and the radius of the last circle should be 1 (as the unit circle has radius 1)
    '''
    _, radii_of_circles, _, _ = gm.circle_data(num_points)

    assert isinstance(radii_of_circles, np.ndarray), "The radii of the circles should be a np.array"
    assert radii_of_circles[0] == 0, "Radius of the origin must be 0"
    assert radii_of_circles[-1] == 1, "Radius of the last circle must be 1"

#--------------------------------------------

@given(num_points = st.integers(4, 1000))
def test_circle_data_dof_in_circles(num_points):
    '''
        Test that the dof_in_circles argument from the function circle_data()
        is at it should. The variable should be a np.ndarray and the total
        sum of all elements should be equal to num_points.
    '''
    _, _, dof_in_circles, _ = gm.circle_data(num_points)

    assert isinstance(dof_in_circles, np.ndarray), "The dof in each circle should be a np.array"
    assert np.sum(dof_in_circles) == num_points, "The total degrees of freedom should equal num of nodes"
    
#--------------------------------------------

@given(num_points = st.integers(4, 1000))
def test_circle_data_starting_angle_for_circles(num_points):
    '''
        Test that the starting_angles_for_circles argument from the function circle_data()
        is at it should. The variable should be a np.ndarray and all elements
        should have a value between 0 and 2 pi. 
    '''
    _, _, _, starting_angles = gm.circle_data(num_points)

    assert isinstance(starting_angles, np.ndarray), "The atarting angles list should be a np.array"
    for i in range(len(starting_angles)):
        assert starting_angles[i] < 2*np.pi, "Starting angle must be smaller than 2*pi"
        assert starting_angles[i] >= 0, "Starting angle must be larger than 0"

#----------------------------------------------------------------------------------------

import pytest
import numpy as np
import numerical_integration as numint

# Testing gaussian_quadrature_2d

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


def test_gaussian_quadrature_2d_advanced():
    '''
        Test that the gaussian_quadrature_2d function can evaluate a tougher integral
        on a non-trivial domain. In this case the function g(x, y) = log(x+y) on the triangle
        given by the points (1, 0), (3, 1) and (3, 2).
        Which is \int_0^1\int_0^1 log(x+y) dxdy \approx 1.16541
    '''

    def g(x, y):
        return x+y

    p1 = np.array([1, 0])
    p2 = np.array([3, 1])
    p3 = np.array([3, 2])

    exact = 1.16541

    numerical_value = numint.gaussian_quadrature_2D(p1, p2, p3, 4, g)

    assert np.abs(numerical_value - exact) < 0.01
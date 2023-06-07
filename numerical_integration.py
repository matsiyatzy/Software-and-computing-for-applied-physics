import numpy as np
from tabulate import tabulate


def gaussian_quadrature_2D(p1, p2, p3, N_q : int, g):
    '''
        Integrates the function g over the span of the triangle formed by the three corner points 
        (p1, p2, p3) with a Gaussian quadrature method with N_q integration points
        ----------------
        Inputs: 
            p1: first corner point of a triangle, 
                list of numpy array of size 2
            p2: second corner point of a triangle, 
                list of numpy array of size 2
            p3: third corner point of a triangle, 
                list of numpy array of size 2
            N_q: number of integration points in gaussian quadrature, 
                 type: int
                 options: 1, 2, 3, 4
            g: function to be integrated on the triangle given by (p1, p2, p3)
        
        Outputs:
            integral_value: 
        ----------------
        Raises:
            ValueError:
                If any of p1, p2 or p3 has the wrong length.
                N_q is not an integer in [1, 3, 4].
                g is not a function
        ----------------
        Long description: 
            Numerically solves the 2D-integral of the function g given by
            \iint_\Omega g(z)dz \approx \sum_{q=1}^Nq \rho_q * g(z_q)
            where \Omega is a reference domain (in this case triangles)
            and \rho and z are 
    '''
    # Handle wrong input:
    if (len(p1) != 2):
        raise ValueError (f"The corner point p1 should have length 2 but has length {len(p1)}.")
    if (len(p2) != 2):
        raise ValueError (f"The corner point p1 should have length 2 but has length {len(p1)}.")
    if (len(p3) != 2):
        raise ValueError (f"The corner point p1 should have length 2 but has length {len(p1)}.")
    if (N_q != 1 and N_q != 3 and N_q != 4):
        raise ValueError (f"N_q needs to be either 1, 3, or 4, but is {N_q}")
    if (not callable(g)):
        raise ValueError (f"g needs to be a function, but is now of type {type(g)}")
    
    #Setting integration points and weights
    if(N_q == 1):
        z = np.array([np.array([1/3, 1/3, 1/3])])
        rho = np.array([1])
    
    elif(N_q == 3):
        z = np.array([np.array([1/2, 1/2, 0]), np.array([1/2, 0, 1/2]), np.array([0, 1/2, 1/2])])
        rho = np.array([1/3, 1/3, 1/3])
    
    elif(N_q == 4):
        z = np.array([np.array([1/3, 1/3, 1/3]), np.array([3/5, 1/5, 1/5]),
                    np.array([1/5, 3/5, 1/5]), np.array([1/5, 1/5, 3/5])])
        rho = np.array([-9/16, 25/48, 25/48, 25/48])
    
    # Calculate the area of a triangle given by (p1, p2, p3)
    area = 1/2 * np.abs(p1[0]*(p2[1] - p3[1]) + p2[0]*(p3[1]-p1[1]) + p3[0]*(p1[1]-p2[1]))

    # Performing the numerical integration
    x = np.zeros(N_q)
    y = np.zeros(N_q)
    
    for i in range(N_q):
        x[i] = z[i][0]*p1[0] + z[i][1]*p2[0] + z[i][2]*p3[0]
        y[i] = z[i][0]*p1[1] + z[i][1]*p2[1] + z[i][2]*p3[1]
    
    I = np.sum(rho * g(x, y))

    value_of_integral = I*area

    return value_of_integral

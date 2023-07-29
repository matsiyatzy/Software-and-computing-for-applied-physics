## Table of content 

- [Quick summary](#2D-Poisson-equation)
- [Installation](#Installation)
- [How to use](#How-to-use)

<!----><a name="2D-Poisson-equation"></a>
## 2D Poisson equation
This repository holds an implementation of a solver that solves the 2D-Poisson problem on the unit disc with homogeneous dirichlet boundary conditions. The problem is given by

$$\begin{cases}\nabla^2 u(x, y) = -f(x, y), (x, y)\in\Omega \\\ u(x, y) = 0, (x, y) \in \partial \Omega\end{cases}$$

where the domain is the unit disc, $\Omega = \{(x, y) : x^2 + y^2 \leq 1\}$ with $\partial \Omega = \{ (x, y) : x^2 + y^2 = 1\}$. For a summary of the theory behind the implementation, check out the file *2dPoissonProblem.pdf*.

<!----><a name="Installation"></a>
## How to install
To install the problem, first make sure that you meet the minimum requirements listed in the file *requirements.txt*. 
You should then clone this repository to a designated place on your computer like this. To clone the repository, run these lines in your terminal:

```shell
cd navigate/to/your/designated/place
git clone https://github.com/matsiyatzy/Software-and-computing-for-applied-physics.git
```

<!----><a name="How-to-use"></a>
## How to use
To use this code, follow these steps:

1. Navigate to the place where you installed the program
   ```shell
   cd navigate/to/your/designated/place/Software-and-computing-for-applied-physics
   ```
2. Run the solver with this command
   ```shell
   python main.py <num_nodes> <right_hand_side_function> <verbose>
   ```
   Where you need to edit <num_nodes>, <right_hand_side_function> and <verbose> to be like your desired input.
   
   These values are:
       - num_nodes: number of nodes (and degrees of freedom) in the finite element mesh of the unit circle, it is given as an integer.
       - right_hand_side_function: The right hand side of the poisson eqution. Given as an input without spaces.
       - verbose: Boolean variable with a default value of True. Defines whether or not you want printed outputs during the running of the program:

    Here is an example run:
    
    ```shell
    python main.py 1000 np.sin(x**2+y**2) True
    ```
    
    And here is another (verbose not provided -> verbose takes the default value True):
    
    ```
    python main.py 10000 -8*np.pi*np.cos(2*np.pi*(x**2+y**2))+16*np.pi**2*(x**2+y**2)*np.sin(2*np.pi*(x**2+y**2))
    ```

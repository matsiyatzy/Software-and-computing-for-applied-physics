## Table of content 

- [Background theory of 2D Poisson equation](#2D-Poisson-equation)
- [Structure of repository](#Structure-of-repository)
- [How to use](#How-to-use)
- [Possible extensions](#Possible-extensions)

<!----><a name="2D-Poisson-equation"></a>
## 2D Poisson equation
This repository holds an implementation of a solver that solves the 2D-Poisson problem on the unit disc with homogeneous dirichlet boundary conditions. In this readme, there is a quick summary of the theory behind the problem. For a more detailed explanation, check out the file *2dPoissonProblem.pdf*. The problem is given by

$$\begin{cases}\nabla^2 u(x, y) = -f(x, y), (x, y)\in\Omega \\\ u(x, y) = 0, (x, y) \in \partial \Omega\end{cases}$$

where the domain is the unit disc, $\Omega = \{(x, y) : x^2 + y^2 \leq 1\}$ with $\partial \Omega = \{ (x, y) : x^2 + y^2 = 1\}$. 

Multiplying with an arbitrary test function and doing integration by parts on both side of the equation yields 

$$\iint_\Omega \nabla u \nabla v d\Omega = \iint_\Omega fv d\Omega + \int_{\partial \Omega} \frac{\partial u}{\partial n}v ds$$

and as $u = 0$ on $\partial \Omega$, the problem is rewritten to 

$$\iint_\Omega \nabla u \nabla v d\Omega = \iint_\Omega fv d\Omega \iff a(u, v) = l(v).$$

The weak formulation of the problem is then

$$\begin{align*} \text{find } u &\in H_0^1(\Omega):\\
a(u, v) &= l(v) \forall v\in H_0^1(\Omega)\\
a(u, v) &= \iint_\Omega \nabla u \nabla v d\Omega \\
l(v) &= \iint_\Omega fv d\Omega. \end{align*}$$

Instead of finding a solution in the whole space $H_0^1(\Omega)$, we find a solution in a smaller space $X_h \subset H_0^1$. Let our domain $\Omega$ be discretized into $M$ triangles, such that $\Omega = \cup_{k=1}^M K_k$. Each triangle $K_k$ is then defined by its three corner nodes $(x_i, y_i)$, and there is a basis function corresponding to each node. The space $X_h$ is defined by

$$X_h = \left\lbrace v\in X = H_0^1: v\rvert_{K_k} \in \mathbb{P}_1(K_k), 1\leq k\leq M \right\rbrace.$$
    
and the basis functions $\lbrace\varphi_i\rbrace_{i=1}^n$ satisfy

$$X_h = \text{span}\lbrace\phi_i\rbrace_{i=1}^n, \text{           } \varphi_j(\mathbf{x_i}) = \delta_{ij}.$$

We search to find $u_h\in X_h,$ $\forall v\in X_h$. We write $u_h$ and $v_h$ as weighted sums of the basis functions

$$\begin{align*}
        u_h &= \sum_{i=1}^n u_h^i \varphi_i(x, y)\\
        v_h &= \sum_{j=1}^n v_h^j \varphi_j(x, y)
\end{align*}$$ 

From the weak formulation we then get

$$\begin{align*}
a(u_h, v_h) &= l(v_h)\\
        \iint_{\Omega}\nabla u_h\nabla v_h\mathrm{d}\Omega &= \iint_{\Omega}fv_h \mathrm{d}\Omega\\
        \iint_{\Omega}\sum_{i=1}^n u_h^i \nabla \varphi_i \sum_{j=1}^n v_h^j \nabla \varphi_j \mathrm{d}\Omega &= \iint_{\Omega}f \sum_{j=1}^n v_h^j \varphi_j \mathrm{d}\Omega\\
        \sum_{i=1}^n \sum_{j=1}^n u_h^i v_h^j \iint_{\Omega} \nabla \varphi_i \nabla \varphi_j \mathrm{d}\Omega &= \sum_{j=1}^n v_h^j \iint_{\Omega} f\varphi_j\\
        \sum_{i=1}^n \sum_{j=1}^n u_h^i v_h^j a(\varphi_i, \varphi_j) &= \sum_{j=1}^n v_h^j l(\varphi_j)\\
        \mathbf{v}^TA\mathbf{u} &= \mathbf{v}^T\mathbf{f}\text{  }\forall v\in X_h \\
        A\mathbf{u} &= \mathbf{f},
\end{align*}$$

with use of bilinearity of $a(\cdot, \cdot)$ and linearity of $f(\cdot)$. This gives the galerkin formulation find $u_h \in X_h$ such that $a(u_h, v) = l(v) \forall v \in X_h$, which is then equivalent to solving the linear system

$$A\mathbf{u} = \mathbf{f},$$

with 

$$\begin{align*}
    A &= \[A_{ij}\] = [a(\varphi_i, \varphi_j)]\\
    \mathbf{u} &= [u_h^i]\\
    \mathbf{f} &= [f_j] = [l(\varphi_j)].
\end{align*}$$


<!----><a name="Structure-of-repository"></a>
## Structure of the repository
- The file 2dPoissonProblem.pdf holds a more detailed explanation of the theory behind the code in this repository than the summary given in the paragraph above.
- assemble_load_vector.py holds the implementation of the assembly of the load vector $\mathbf{f}$.
- assemble_stiffness_matrix.py holds the implementation of the assembly of the stiffness matrix $A$.
- generate_mesh.py holds the code that implements the finite element mesh of the unit circle.
- main.py holds the code that runs the whole program, see below for more in-depth use.
- numerical_integration.py holds the code for the numerical integration used in assemble_load_vector.
- plotting.py holds code to plot solutions of the problem and the mesh of the unit circle.
- requirements.txt holds all the requirements to run the code in this repository. Created via pipreqs.
- solver.py holds the code that combines many of the files to solve the problem.
- tests.py holds all the test functions for all the different functions in the repository.


<!----><a name="How-to-use"></a>
## How to use
To use this code, follow these steps:

1. Ensure that your software meets the requirements in requirements.txt.
2. Clone the repository.
3. Navigate to the file "main.py".
4. Edit the function "right_hand_side_f(x, y)" to be the right hand side you want to solve for.
5. If you have the exact solution, implement a function for that as well.
6. Run the code by running the function run_program(). You might want to edit the default inputs.


<!----><a name="Possible-extensions"></a>
## Possible extensions
Some obvious possible extensions to this repository is to allow neumann and mixed boundary conditions. Even further extensions is to implement the possibility to solve other partial differential equations than just the 2D poisson equation.

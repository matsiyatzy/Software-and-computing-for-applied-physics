# 2D Poisson equation
This repository holds an implementation of a solver that solves the 2D-Poisson problem on the unit disc with homogeneous dirichlet boundary conditions. The problem is given by
$$\begin{cases}\nabla^2 u(x, y) = -f(x, y), \,\, (x, y) \in \Omega\\
u(x, y) = 0, (x, y) \in \partial \Omega$$
where the domain is the unit disc, $\Omega = \{(x, y) : x^2 + y^2 \leq 1\}$ with $\partial \Omega = \{ (x, y) : x^2 + y^2 = 1\}$. 

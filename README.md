# 2D Poisson equation
This repository holds an implementation of a solver that solves the 2D-Poisson problem on the unit disc with homogeneous dirichlet boundary conditions. The problem is given by
![eq1](https://latex.codecogs.com/svg.image?&space;\begin{cases}\nabla^2&space;u(x,&space;y)&space;=&space;-f(x,&space;y),\,\,(x,&space;y)\in\Omega&space;\\u(x,&space;y)&space;=&space;0,&space;(x,&space;y)&space;\in&space;\partial&space;\Omega\end{cases})
where the domain is the unit disc, $\Omega = \{(x, y) : x^2 + y^2 \leq 1\}$ with $\partial \Omega = \{ (x, y) : x^2 + y^2 = 1\}$. 

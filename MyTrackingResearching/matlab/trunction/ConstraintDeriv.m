function [E1, E2, d] = ConstraintDeriv(x, E0, E)
E1 = [2*x(1), 0, 2*x(3), 0];
E2 = [2, 0;
      0, 2];
d = E0 - E(x) + E1*x;
return; 

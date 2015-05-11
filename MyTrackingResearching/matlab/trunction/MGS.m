function [W, T] = MGS(A)

% Compute the modified Gram-Schmidt transformation T A = [ W ; 0 ] where A is a given
% m x n matrix, and T is an orthogonal m x m matrix, and W is an n x n matrix.

[m,n] = size(A);
if m < n 
    disp('Error - input matrix cannot have more cols than rows');
    return
end

W = zeros(n);
for k = 1 : n
    sigma = sqrt(A(:, k)' * A(:, k));
    if abs(sigma) < 100 * eps
        disp('The input matrix is not full rank');
        return;
    end
    W(k, k) = sigma;
    for j = k+1 : n
        W(k, j) = A(:, k)' * A(:, j) / sigma;
    end
    T(k, :) = A(:, k)' / sigma;
    for j = k+1 : n
        A(:, j) = A(:, j) - W(k, j) * A(:, k) / sigma;
    end
end

% At this point T is an n x m orthogonal matrix.
% Complete the rows of T so that T is an m x m orthogonal matrix.
% This uses Gram-Schmidt orthonormalization.
%T(n+1:n+m, n+1:n+m) = eye(m);
T(n+1:n+m, 1:m) = eye(m);
index = n + 1;
for k = n+1 : n+m
    temp = T(k, :);
    for i = 1 : k-1
        temp = temp - T(k, :) * T(i, :)' * T(i,:);
    end
    if norm(temp) > 100 * eps
        T(index, :) = temp / norm(temp);
        index = index + 1;
    end
end
T = T(1:m, 1:m);
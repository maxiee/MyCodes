function pc = ckf_packed_pc(x,fmmparam)
% CKF_PACKED_PC - Pack P and C for the Cubature Kalman filter transform
%
% Syntax:
%   pc = CKF_PACKED_PC(x,fmmparam)
%
% In:
%   x - Evaluation point
%   fmmparam - Array of handles and parameters to form the functions.
%
% Out:
%   pc - Output values
%
% Description:
%   Packs the integrals that need to be evaluated in nice function form to
%   ease the evaluation. Evaluates P = (f-fm)(f-fm)' and C = (x-m)(f-fm)'.

% Copyright (c) 2010 Hartikainen, S盲rkk盲, Solin
%
% This software is distributed under the GNU General Public
% Licence (version 2 or later); please refer to the file
% Licence.txt, included with the software, for details.
%%

  f  = fmmparam{1};     % 动态方程
  m  = fmmparam{2};     % 上一时刻后验
  fm = fmmparam{3};     % 用S-R准则求得的下一时刻的先验估计
  if length(fmmparam) >= 4
      param = fmmparam{4};
  end

  % 这里面的x就是容积点，与f的S-R是一样的
  % 这里也是在容积点使用动态方程f来取值
  if ischar(f) || strcmp(class(f),'function_handle')
      if ~exist('param','var')
         F = feval(f,x);
      else
         F = feval(f,x,param);
      end
  elseif isnumeric(f)
         F = f*x;
  else
      if ~exist('param','var')
         F = f(x);
      else
         F = f(x,param);
      end
  end
  d = size(x,1);   % 容积点数
  s = size(F,1);    % 取值数，这俩不该一致吗？
  % 经过实测，d是4，s是2,原来个数是用列来计数的。

  % Compute P = (f-fm)(f-fm)' and C = (x-m)(f-fm)'
  % and form array of [vec(P):vec(C)]
  pc = zeros(s^2+d*s,size(F,2));
  P = zeros(s,s);
  C = zeros(d,s);
  % 对于在每个在容积点处的取值
  for k=1:size(F,2)
    for j=1:s
      for i=1:s
          % 来计算误差协方差
          % 根据上面P和C的公式，第二项后面是不是应该加一个'呢？
          % 默认是没有加的
          % 我给两个都加上了，不知道有没有效果，等回来验证吧
          % 又验证了一次，发现确实是个BUG，我加上转置后，矩阵都是对称阵了。
          P(i,j) = (F(i,k)-fm(i)) * (F(j,k) - fm(j))';
%           P(i,j) = (F(i,k)-fm(i)) * (F(j,k) - fm(j));
      end
      for i=1:d     
          C(i,j) = (x(i,k)-m(i)) * (F(j,k) - fm(j))';
%           C(i,j) = (x(i,k)-m(i)) * (F(j,k) - fm(j));
      end
    end
    % 这最终生成了这么一个矩阵，就是既包含自协方差，也包含混合协方差
    pc(:,k) = [reshape(P,s*s,1);reshape(C,s*d,1)];
  end
  
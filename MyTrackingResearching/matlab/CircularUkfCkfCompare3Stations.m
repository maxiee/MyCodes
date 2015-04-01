f = @(x,param) [1 param(1) 0 0;0  1 0 0;0  0 1 param(1);0  0 0 1]*x;
h = @(x, params) ...
    [atan2(x(1,:),x(3,:));
    (x(3,:).*x(2,:)-x(1,:).*x(4,:))./(x(1,:).^2+x(3,:).^2);
    (-10/3)*(x(3,:).*x(2,:)-x(1,:).*x(4,:)).^2./(x(1,:).^2+x(3,:).^2).^1.5];

dt = 1;
radius = 100;
delta = 2*pi/360*5.73;
count = 70;

txs = zeros(2, count);
uxs = zeros(4, count);
cxs = zeros(4, count);

x0 = [100 0 0 10]';
P0 = diag([100 10 100 10]);

M_ukf = x0;
P_ukf = P0;
M_ckf = x0;
P_ckf = P0;

Qv = [(dt^3)/3    (dt^2)/2          0           0; 
      (dt^2)/2          dt          0           0;
             0           0   (dt^3)/3    (dt^2)/2;
             0           0   (dt^2)/2          dt]; 
Qw = diag([5 5 5]);

for i=1:count
    fprintf('==================第%d轮======================\n',i);
    
    target_pos_x = cos(i*delta)*radius + randn(1)*0.0001;
    target_pos_y = sin(i*delta)*radius + randn(1)*0.0001;
    txs(:,i) = [target_pos_x; target_pos_y];
    
    target_vol_x = sin(i*delta)*10;
    target_vol_y = cos(i*delta)*10;
    
    z1 = atan2(target_pos_x, target_pos_y);
    z2 = (target_pos_y*target_vol_x-target_pos_x*target_vol_y)/(target_pos_x^2+target_pos_y^2);
    z3 = (-10/3)*(target_pos_y*target_vol_x-target_pos_x*target_vol_y)^2/(target_pos_x^2+target_pos_y^2)^1.5;
    
    [M_ukf, P_ukf,D,upSX,upSY] = ukf_predict1(M_ukf, P_ukf, f, Qv, dt);
    [M_ukf, P_ukf,uK,uMU,uS,uLH,uuSx,uuSY] = ukf_update1(M_ukf, P_ukf, [z1; z2; z3], h, Qw);
    
    [M_ckf, P_ckf,cpSX,cpSY] = ckf_predict(M_ckf, P_ckf, f, Qv, dt);
    [M_ckf, P_ckf,cK,cMU,cS,cLH,cuSx,cuSY] = ckf_update(M_ckf, P_ckf, [z1; z2; z3], h, Qw);
    
%     fprintf('predict 变换前 Sigma/Cubature 点比较：\n');
%     upSX
%     uuSx
%     fprintf('predict 变换后 Sigma/Cubature 点比较：\n');
%     upSY
%     cpSY
    fprintf('update 变换前 Sigma/Cubature 点比较：\n');
    uuSx
    cuSx
    fprintf('update 变换后 Sigma/Cubature 点比较：\n');
    uuSY
    cuSY
    
    fprintf('UKF CKF 结果输出：\n');
    M_ukf
    M_ckf
    
    uxs(:,i) = M_ukf;
    cxs(:,i) = M_ckf;
    fprintf('==============================================\n');
end

plot(txs(1,:), txs(2,:), uxs(1,:), uxs(3,:), cxs(1,:), cxs(3,:));
legend('True','UKF','CKF');

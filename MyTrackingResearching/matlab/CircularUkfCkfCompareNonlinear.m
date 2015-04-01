f = @(x,param) ...
    [1 sin(x(5)*param(1))/x(5)      0 -((1-cos(x(5)*param(1)))/x(5)) 0;
     0 cos(x(5)*param(1))           0 -sin(x(5)*param(1))            0;
     0 (1-cos(x(5)*param(1)))/x(5)  1 sin(x(5)*param(1))/x(5)        0;
     0 sin(x(5)*param(1))           0 cos(x(5)*param(1))             0;
     0 0                            0 0                              1]*x;
h = @(x, params) [x(1,:);x(3,:)];

dt = 1;
radius = 100;
delta = 2*pi/360*5.73;
count = 62;

txs = zeros(2, count);
uxs = zeros(5, count);
cxs = zeros(5, count);

x0 = [100 0 0 10 0.1]';
P0 = diag([100 10 100 10 10]);

M_ukf = x0;
P_ukf = P0;
M_ckf = x0;
P_ckf = P0;

Qv = [0.1/3     0.1/2   0         0         0;
      0.1/2     0.1     0         0         0;
      0         0       0.1/3     0.1/2     0;
      0         0       0.1/2     0.1       0;
      0         0       0         0         1.75];

Qw = diag([25 25]);

for i=1:count
    fprintf('==================第%d轮======================\n',i);
    
    target_pos_x = cos(i*delta)*radius + randn(1)*0.0001;
    target_pos_y = sin(i*delta)*radius + randn(1)*0.0001;
    txs(:,i) = [target_pos_x; target_pos_y];
    
    zx = target_pos_x + randn(1)*5;
    zy = target_pos_y + randn(1)*5;
    
    [M_ukf, P_ukf,D,upSX,upSY] = ukf_predict1(M_ukf, P_ukf, f, Qv, dt,1,1,-2);
    [M_ukf, P_ukf,uK,uMU,uS,uLH,uuSx,uuSY] = ukf_update1(M_ukf, P_ukf, [zx; zy], h, Qw);
    
    [M_ckf, P_ckf,cpSX,cpSY] = ckf_predict(M_ckf, P_ckf, f, Qv, dt);
    [M_ckf, P_ckf,cK,cMU,cS,cLH,cuSx,cuSY] = ckf_update(M_ckf, P_ckf, [zx; zy], h, Qw);
    
%     fprintf('predict 变换前 Sigma/Cubature 点比较：\n');
%     upSX
%     cpSX
%     fprintf('predict 变换后 Sigma/Cubature 点比较：\n');
%     upSY
%     cpSY
%     fprintf('update 变换前 Sigma/Cubature 点比较：\n');
%     uuSx
%     cuSx
%     fprintf('update 变换后 Sigma/Cubature 点比较：\n');
%     uuSY
%     cuSY

    fprintf('CKF卡尔曼增益：');
    cK
    
    fprintf('目标真实位置:(%f,%f)\n',zx,zy);
    fprintf('UKF CKF 结果输出：\n');
    M_ukf
    M_ckf
    
    uxs(:,i) = M_ukf;
    cxs(:,i) = M_ckf;
    fprintf('==============================================\n');
end

plot(txs(1,:), txs(2,:), uxs(1,:), uxs(3,:), cxs(1,:), cxs(3,:));
legend('True','UKF','CKF');

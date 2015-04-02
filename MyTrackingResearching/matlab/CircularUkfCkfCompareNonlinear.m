f = @(x,param) ...
    [1 sin(x(5)*param(1))/x(5)      0 -((1-cos(x(5)*param(1)))/x(5)) 0;
     0 cos(x(5)*param(1))           0 -sin(x(5)*param(1))            0;
     0 (1-cos(x(5)*param(1)))/x(5)  1 sin(x(5)*param(1))/x(5)        0;
     0 sin(x(5)*param(1))           0 cos(x(5)*param(1))             0;
     0 0                            0 0                              1]*x;
h = @(x, params) [x(1,:);x(3,:)];
E = @(X)sqrt((X(1,:)).^2 + (X(3,:)).^2);

dt = 1;
radius = 100;
delta = 2*pi/360*5.73;
count = 62;

txs = zeros(2, count);
uxs = zeros(5, count);
puxs = zeros(5, count);
cxs = zeros(5, count);
pcxs = zeros(5,count);

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
    
    zx = target_pos_x + randn(1)*10;
    zy = target_pos_y + randn(1)*10;
    
    [M_ukf, P_ukf,D,upSX,upSY] = ukf_predict1(M_ukf, P_ukf, f, Qv, dt,1,1,-2);
    [M_ukf, P_ukf,uK,uMU,uS,uLH,uuSx,uuSY] = ukf_update1(M_ukf, P_ukf, [zx; zy], h, Qw);
    
    % PUKF
    [M_n,P_n,C_n,sigma,sigma_Y,wei_ut] = ut_transform(M_ukf,P_ukf,f,[dt]);
    sigma_cons = E(sigma);
    dhat = sigma_cons * wei_ut{1};
    Pdd_pukf = 0;
    Pxd_pukf = zeros(5,1);
    for j = 1:11  %magic number
        Pdd_pukf = Pdd_pukf + wei_ut{2}(j)*(sigma_cons(j) - dhat)*(sigma_cons(j) - dhat)';
        Pxd_pukf = Pxd_pukf + wei_ut{2}(j)*(sigma(:,j)-M_ukf)*(sigma_cons(j)-dhat)';
    end
    K_pukf = Pxd_pukf / Pdd_pukf;
    puxs(:,i) = M_ukf + K_pukf*(radius-dhat);
    
    [M_ckf, P_ckf,cpSX,cpSY] = ckf_predict(M_ckf, P_ckf, f, Qv, dt);
    [M_ckf, P_ckf,Kalmanc,cMU,cS,cLH,cuSx,cuSY] = ckf_update(M_ckf, P_ckf, [zx; zy], h, Qw);
    
    % PCKF
    [M_ckf_n,P_ckf_n,C_ckf_n,cube,W] = ckf_transform(M_ckf,P_ckf,f,dt);
    cube_cons = E(cube);
    chat = sum(cube_cons)/10; %magic number
    Pdd_pckf = 0;
    Pxd_pckf = zeros(5,1);
    for q = 1:10
        Pdd_pckf = Pdd_pckf + 0.1*(cube_cons(q) - chat)*(cube_cons(q) - chat)';
        Pxd_pckf = Pxd_pckf + 0.1*(cube(:,q)-M_ckf)*(cube_cons(q) - chat)';
    end
    K_pckf = Pxd_pckf / Pdd_pckf;
    pcxs(:,i) = M_ckf + K_pckf*(radius-chat);
    
    uxs(:,i) = M_ukf;
    cxs(:,i) = M_ckf;
    
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
    
    fprintf('PUKF与UKF偏差：(%f)\n', sqrt((puxs(1,i)-txs(1,i))^2+(puxs(3,i)-txs(2,i))^2));
    fprintf('PCKF与CKF偏差：(%f)\n', sqrt((pcxs(1,i)-txs(1,i))^2+(pcxs(3,i)-txs(2,i))^2));

    fprintf('==============================================\n');
end
plot(txs(1,:), txs(2,:), uxs(1,:), uxs(3,:), cxs(1,:), cxs(3,:),puxs(1,:),puxs(3,:),'o',pcxs(1,:),pcxs(3,:),'*');
legend('True','UKF','CKF','PUKF','PCKF');

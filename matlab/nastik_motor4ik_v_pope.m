clc; 
clear; 
clf;

E=1.;
phi_0=1;
dU=1.;
mu_left = 0;
mu_step = 0.01;
mu_right= 1;

phi=0:pi/50:4*pi;
u=1/2*dU*(1-cos(2*phi));
U_phi = zeros(1, length(phi));
x = zeros(1, length(phi));
y = zeros(1, length(phi));

for mu=mu_left:mu_step:mu_right
    sigma_w = E * mu * cos(phi-phi_0);

    for i=1:length(phi)
        U_phi(i) = u(i) + sigma_w(i);
        x(i) = phi(i);
        y(i) = U_phi(i);
    end

    figure(1);
    plot(x,y);
    hold on
    grid on

    figure(2);
    polarplot(phi, U_phi);
    hold on
    grid on
end

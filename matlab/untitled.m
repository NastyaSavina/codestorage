du=1.;
phi = 0:0.1:2*pi;
u = 1/2*du*(1-cos(phi.*2));
polarplot(phi, u);

for i=1:length(phi)
    x(i) = u(i) * cos(phi(i));
    y(i) = u(i) * sin(phi(i));
end

figure(2);
plot(x,y);
t = 0.7;
w = 0.5;
mu = 3.e-21;
k = 2.e-19;
u = 0.6;
koef_trenia=100;
lambda = 0.6;
lambda_0 = 0.9;
T=5500;
 
D = (1.38064852 * power(10, -23) * T) ...
    / koef_trenia;
 
a = D * power(k, 2);
b = D * power(k, 2);
max_y = 0;
min_y = 1;
 
left_tau=1;
right_tau=5;
tau_step =0.1;
 
for lambda = 0:0.4:1
    tau = left_tau:tau_step:right_tau;
    v_mid_val = arrayfun(@(changable_val) v_mid(u, T, D, ...
        lambda, lambda_0, ...
        k, a, b, mu, t, changable_val, w), tau);
    tau_obr = arrayfun(@(changable_val) 1 / changable_val, tau);
    plot(tau_obr, v_mid_val);    
    if (min(v_mid_val) < min_y)
        min_y = min(v_mid_val);
    end
    if (max(v_mid_val) > max_y)
        max_y = max(v_mid_val);
    end
    axis([1/right_tau 1/left_tau min_y max_y]);
    hold all;
end
function sigma_res = sigma(a, b, mu, t, tau, w)

    sigma_sum = 0;

    for j = 1:1000
        sigma_sum = sigma_sum + ...
            (power(w_j(j), 2) * 2 * power(mu * tau, 2) * (1 - cos(w * t))) ...
            / ((power(w_j(j), 2) + power(a, 2)) ...
            * (power(w_j(j), 2) + power(b, 2)) ...
            * power(power(w * tau, 2) - 4 * power(pi, 2), 2));
    end
    
    sigma_res = 2*(a+b) * sigma_sum; 
end
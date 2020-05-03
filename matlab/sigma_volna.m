function res = sigma_volna(D, k, a, b, mu, t, tau, w)
    res = D * power(k, 2) * sigma(a, b, mu, t, tau, w);
end
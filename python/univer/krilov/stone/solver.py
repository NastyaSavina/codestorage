from numpy.core import arange

def NMDer(t, M, N, P, i):
    G = 0.001
    B = 0.9
    A = 0.1
    
    res1 = -G*M[i]+B*N[i]*M[i]
    res2 = P-A*N[i]-B*N[i]*M[i]

    return (res1, res2)


t = 0
P = 5
cc = -5
dt = 0.1
i = 1
startT = 0
endT = 300
t = arange(startT, endT, dt)
size = int((endT-startT)/dt)
M = [0]
N = [0]

for i in range(1, size):
    if i % 100 == 0:
        P = P + cc;
        cc = cc * -1;
        
    print(N)
    print(M)
    
    k1M, k1N = NMDer(t[i], M, N, P, i);
    k2M, k2N = NMDer(t[i] + dt/2, M + dt*k1M/2, N + dt*k1N/2, P, i);
    k3M, k3N = NMDer(t[i] + dt/2, M + dt*k2M/2, N + dt*k2N/2, P, i);
    k4M, k4N = NMDer(t[i] + dt, M + dt*k3M, N + dt*k3N, P, i);
    
    M.append(M[i] + dt*(k1M + 2*k2M + 2*k3M + k4M)/6);
    N.append(N[i] + dt*(k1N + 2*k2N + 2*k3N + k4N)/6);
    


print(N)
print(M)

# ii=2
# figure(1)
# hold all
# plot(t,N)
# StartTime = cputime

# while (ii<=length(t)) 
#     CurrTime = cputime; 
#     if (t(ii)<=CurrTime-StartTime) 
#         plot(t(ii-1:ii), N(ii-1:ii), 'r');
#         plot(t(ii-1:ii), M(ii-1:ii), 'b'); 
#         grid on; 
#         drawnow; 
#         ii=ii+1; 
#     end 
# end
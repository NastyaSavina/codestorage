def volume_with_attraction(point):

    dist_to_center = ((point[0]**2) + (point[1]**2))**0.5
    
    G = 6.67*10
    M = 5.972*10**8
    r = 6.371
    
    attr = G * M / ((r + dist_to_center) ** 2)
    
    vX = point[0]
    vY = point[1]

    return [-vX, -vY]


def F(p_state, delta_):
    p_state['v'] = list(map(lambda each: each + delta_, p_state['v']))
    p_state_new = {}
    p_state['r'][0] = p_state['r'][0] + p_state['v'][0]
    p_state_new['r'] = p_state['r']
    p_state_new['r'][1] = p_state['r'][1] + p_state['v'][1]
    p_state_new['v'] = volume_with_attraction(p_state['r'])
    return p_state_new


t = 0
dt = 0.05
vx = 300
vy = 10
x = 100
y = 50
current_stone_state = {'r': [x, y], 'v': [vx, vy]}
arrayLens = 1000
points_X = [0] * arrayLens
points_Y = [0] * arrayLens
time = [0] * arrayLens
stoneArrayX = [0] * arrayLens
stoneArrayY = [0] * arrayLens


for i in range(1, arrayLens):
    k1 = F(current_stone_state, 0)*dt
    k2 = F(current_stone_state, 0.5 * k1)*dt
    k3 = F(current_stone_state, 0.5 * k2)*dt
    k4 = F(current_stone_state, k3)*dt

    current_stone_state = current_stone_state + 1.0/6.0 * (k1 + 2*k2 + 2*k3 + k4) 
    stoneArrayX[i] = current_stone_state['r'][0]
    stoneArrayY[i] = current_stone_state['r'][1]
    t = t + dt
    
    points_X[i] = current_stone_state(1)
    points_Y[i] = current_stone_state(2)
    time[i] = t
    
    print(current_stone_state)

# figure(1)

# StartTime = cputime
# ii = 2
# speed = 1
# while (ii < length(points_X))
#     CurrTime = cputime
#     if (time(ii)\speed <= CurrTime - StartTime) 
#         plot(points_X(ii-1:ii), points_Y(1, ii-1:ii), '*r')
#         grid on
#         hold on
#         drawnow
#         ii=ii+1
#     end
# end


# fid = fopen('xPoints.txt', 'w+')
# fprintf(fid, '%f \n', stoneArrayX)
# fclose(fid)



# fid = fopen('yPoints.txt', 'w+')
# fprintf(fid, '%f \n', stoneArrayY)
# fclose(fid)
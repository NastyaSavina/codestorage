function res = attraction(point)

    dist = power(power(point(1),2) + power(point(2),2), 0.5);
    
   
    G = 6.67*10;
    M = 5.972*10^8;
    r = 6.371;
    
    attr = G*M/power((r+dist), 2);
    
    gX = attr * (point(1)/attr);
    gY = attr * (point(2)/attr);
    
    res = [gX gY];
    
    text = ['H=' num2str(dist) ' G=' num2str(attr)];
    disp(text);
end
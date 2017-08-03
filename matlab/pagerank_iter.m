function [pfinish, iterations] = pagerank_iter(G, alpha)
%Pagerank Algorithm

%eliminate self-referential links in G
Gprocess = G;
R = length(Gprocess);
for i = 1:R
    if Gprocess(i,i) ~= 0
        Gprocess(i,i) = 0;
    end
end

%Construct P using new G
P = sparse(zeros(R));
deadend = [0]; %store deadend pages
for j = 1:R
    tempcolsum = 0;
    for i = 1:R
        tempcolsum = tempcolsum + Gprocess(i,j);
    end
    if tempcolsum ~= 0;
        P(:,j) = Gprocess(:,j)/tempcolsum;
    else
        deadend = [deadend,j];
    end
end
deadend = deadend(2:length(deadend));

%Construct Pprime
d = zeros(R,1);
for i = 1:length(deadend)
    d(deadend(i)) = 1;
end
Pprime = sparse(P + (1/R)*ones(R,1)*(d'));

%Set tolerance, alpha, iteration count
tolerance = 1e-8;
iteration = 1;

%Construct Markov Matrix M
M = alpha*Pprime + (1-alpha)*(1/R)*ones(R,1)*ones(1,R);

%Page Rank Algorithm
p = (1/R)*ones(R,1);
pnext = M*p;
while (max(abs(pnext - p)) >= tolerance)
    p = pnext;
    pnext = M*p;
    iteration = iteration + 1;
end
pfinish= pnext;
iterations = iteration;




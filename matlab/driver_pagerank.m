% Driver file
load cbc U G;
spy(G);
title('Adjacency Matrix')

% Run Pagerank Algorithm with alpha=0.85
[pfinish, iterations] = pagerank_iter(G, 0.85);
bar(pfinish)
title('Page Rank')

% Generate the top 50 pages in pagerank order
prnk = sortrows([pfinish,([1:size(G, 1)])'], -1);
for i = 1:50
    disp(U{prnk(i,2)});
end
__author__ = 'liu'
from DFS.node import Node;
from DFS.DepthFS import dfs;

node1 = Node("A");
node2 = Node("B");
node3 = Node("C");
node4 = Node("D");
node5 = Node("E");

node1.adjacenciesList.append(node2);
node1.adjacenciesList.append(node3);
node2.adjacenciesList.append(node4);
node4.adjacenciesList.append(node5);

dfs(node1);

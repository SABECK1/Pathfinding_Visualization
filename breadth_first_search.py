import time
from collections import deque
def fast_bfs(start, goal, graph):
    queue = deque([start])
    visited = {start: None}
    while queue:
        # Gets current node from the start of the queue
        cur_node = queue.popleft()
        if cur_node == goal:
            break
        # Gets all adjacent nodes of cur_node
        next_nodes = graph[cur_node]
        # Loops through every adjacent node and checks if it is not yet visited
        # If it is not visited append it to the queue to check its adjacent nodes
        # and append
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    return queue, visited


# Instead of calculating the path in one go - this instead calculates one iteration per eventloop
# This is indicated through the "if" instead of "while"
# This allows for single frame updates to visualize the algorithm
def slow_bfs(start, goal, graph, queue, visited): 
    if queue:
        # Gets current node from the start of the queue
        cur_node = queue.popleft()
        if cur_node == goal:
            time.sleep(1)
            return True, queue, visited
        # Gets all adjacent nodes of cur_node
        next_nodes = graph[cur_node]
        # Loops through every adjacent node and checks if it is not yet visited
        # If it is not visited append it to the queue to check its adjacent nodes
        # and append
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    return False, queue, visited
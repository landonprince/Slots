# build adjacency list for the lines based on shared shapes
def build_graph(lines):
    # initialize an empty adjacency dictionary
    adjacency = {i: [] for i in range(len(lines))}
    
    # for each pair of lines, check if the matching shapes for each line intersect
    for i in range(len(lines)):
        set_i = set(lines[i]["shapes"]) # get matching shapes for line[i]
        for j in range(i + 1, len(lines)):
            set_j = set(lines[j]["shapes"]) # get matching shapes for line[j]
            
            # if line[i] and line[j] share any matching shape, they are connected
            if set_i & set_j:
                adjacency[i].append(j)
                adjacency[j].append(i)
            
    return adjacency

# return a list of connected components (each component is a set of line indices)
def find_connected_components(adjacency):
    visited = set()
    components = []
    
    # depth-first search to find connected components in the graph
    def dfs(start):
        stack = [start]
        component = set()
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                component.add(node)
                # add neighbors to continue building the current component
                for neighbor in adjacency[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
        return component
    
    # call dfs function, every call to dfs is a separate connected component
    for node in adjacency:
        if node not in visited:
            comp = dfs(node)
            components.append(comp)
    
    return components

# return the component (set of line line indices) with the max size
def get_largest_component(components):
    if not components:
        return set()
    return max(components, key=len)

def color_largest_component(lines):
    adjacency = build_graph(lines) # build adjacency list
    components = find_connected_components(adjacency) # find connected components
    largest_component = get_largest_component(components) # identify the largest one
    
    # color the lines accordingly 
    for i, line_info in enumerate(lines):
        if i in largest_component:
            line_info["color"] = "red"
        else:
            line_info["color"] = "black"

    
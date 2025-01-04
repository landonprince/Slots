# build adjacency list for the lines based on shared shapes
def build_graph(lines):
    # initialize an empty adjacency dictionary
    adjacency = {i: [] for i in range(len(lines))}
    
    # for each pair of lines, check if the matching shapes for each line intersect
    for i in range(len(lines)):
        set_i = set(lines[i]["shapes"]) # get matching shapes for line[i]
        for j in range(i + 1, len(lines)):
            set_j = set(lines[j]["shapes"]) # get matching shapes for line[j]
            
            # if line[i] & line[j] share any matching shape, they are connected
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

# return dictionary containing the shapes in each connected component
def get_component_shapes(lines, components):
    component_shape_sets = {}
    
    for i, component in enumerate(components):
        # gather all shapes from all lines in the component
        component_shapes = set()
        for line_index in component:
            component_shapes.update(lines[line_index]["shapes"])
        component_shape_sets[i] = component_shapes
        
    return component_shape_sets

# return the component (set of line line indices) with the max size
def get_largest_component(lines, components):
    # build dictionary of shapes in each component
    component_shape_sets = get_component_shapes(lines, components)
    
    # find component with max number of shapes
    max_component_index = None
    max_num_shapes = -1
    for index, shape_set in component_shape_sets.items():
        if len(shape_set) > max_num_shapes:
            max_num_shapes = len(shape_set)
            max_component_index = index
    
    # return the largest component's set of line indices
    if max_component_index is not None:
        return components[max_component_index]
    else:
        return None # empty if no components

def color_largest_component(lines):
    # get the component with the largest number of shapes
    adjacency = build_graph(lines) 
    components = find_connected_components(adjacency)
    largest_component = get_largest_component(lines, components) 
    
    # color the lines accordingly 
    for i, line_info in enumerate(lines):
        if i in largest_component:
            line_info["color"] = "black"
        else:
            line_info["color"] = "black"


    
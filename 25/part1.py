class LabeledNode:
    def __init__(self, label, id):
        self.label = label
        self.neighbours = []
        self.id = id

    def connect(self, node):
        self.neighbours.append(node)
        node.neighbours.append(self)

nodes = []

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        line_split = line.strip().split(' ')
        main_label = line_split[0][:-1]
        neighbour_labels = line_split[1:]

        if any(True for node in nodes if node.label == main_label):
            node = next(node for node in nodes if node.label == main_label)
        else:
            node = LabeledNode(main_label, len(nodes))
            nodes.append(node)

        for label in neighbour_labels:

            if any(True for node in nodes if node.label == label):
                neighbour = next(node for node in nodes if node.label == label)
            else:
                neighbour = LabeledNode(label, len(nodes))
                nodes.append(neighbour)

            if not neighbour in node.neighbours:
                node.connect(neighbour)

nodes.sort(key=lambda n: n.id)

# Edge Capacity
C = [[(1 if n in node.neighbours else 0) for n in nodes] for node in nodes]

def get_residual_capacity(capacities, flow, i, j):
    return capacities[j][i] - flow[j][i] + flow[i][j]

def find_max_flow(nodes, capacities, start, end):
    # Flow
    F = [[0 for n in nodes] for node in nodes]
    
    increased_flow = True
    flow_value = 0

    while increased_flow:
        increased_flow = False

        Visited = [False for n in nodes]
        Visited[start.id] = True
        queue = [(start, [start])]

        # search for a start-end path to increase flow on
        while len(queue) > 0:
            node, path = queue.pop()

            # did we find a path?
            if node == end:
                bottleneck = min(get_residual_capacity(capacities, F, path[i].id, path[i + 1].id) for i in range(len(path) - 1))

                # increase flow
                for i in range(len(path) - 1):
                    F[path[i + 1].id][path[i].id] += bottleneck

                flow_value += bottleneck
                increased_flow = True
                break

            for neighbour in node.neighbours:
                if Visited[neighbour.id]:
                    continue

                residual_cap = get_residual_capacity(capacities, F, node.id, neighbour.id)

                if residual_cap > 0:
                    extended_path = path + [neighbour]
                    queue.append((neighbour, extended_path))
                    Visited[neighbour.id] = True

    return (F, flow_value)

def find_flow_cut(capacities, flow, start):
    queue = [start]
    cut = [start]

    while len(queue) > 0:
        node = queue.pop()

        for neighbour in node.neighbours:
            if (not neighbour in cut) and get_residual_capacity(capacities, flow, node.id, neighbour.id) > 0:
                cut.append(neighbour)
                queue.append(neighbour)

    edges = []
    for node in cut:
        for neighbour in node.neighbours:
            if not neighbour in cut:
                edges.append([node, neighbour])

    return cut, edges

start = next(node for node in nodes if node.label == 'zvk')
end = next(node for node in nodes if node.label == 'rcj')

F, flow_value = find_max_flow(nodes, C, start, end)

cut, edges = find_flow_cut(C, F, start)

print(len(cut) * (len(nodes) - len(cut)))
print(len(edges))
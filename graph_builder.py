import os
import matplotlib.pyplot as plt
import networkx as nx


class GraphBuilder:
    def __init__(self):
        self.row = None
        self.graph = None
        self.node_positions = None

    def create_graph(self):
        graph = nx.DiGraph()

        position = {}
        for i, element in enumerate(self.row):
            if isinstance(element, list):
                graph.add_node(element[0].id, label=element[0].label)
                position[element[0].id] = (i, 1.03)
                graph.add_node(element[1].id, label=element[1].label)
                position[element[1].id] = (i, 0.97)
            else:
                graph.add_node(element.id, label=element.label)
                position[element.id] = (i, 1)

        for i in range(len(self.row) - 1):
            element = self.row[i]
            next_element = self.row[i + 1]

            if isinstance(element, list) and isinstance(next_element, list):
                graph.add_edge(element[0].id, next_element[0].id,
                               weight=(next_element[0].top_left_x - element[0].bot_right_x))
                graph.add_edge(element[0].id, next_element[1].id,
                               weight=(next_element[1].top_left_x - element[0].bot_right_x))
                graph.add_edge(element[1].id, next_element[0].id,
                               weight=(next_element[0].top_left_x - element[1].bot_right_x))
                graph.add_edge(element[1].id, next_element[1].id,
                               weight=(next_element[1].top_left_x - element[1].bot_right_x))

            elif not isinstance(element, list) and isinstance(next_element, list):
                graph.add_edge(element.id, next_element[0].id,
                               weight=(next_element[0].top_left_x - element.bot_right_x))
                graph.add_edge(element.id, next_element[1].id,
                               weight=(next_element[1].top_left_x - element.bot_right_x))

            elif isinstance(element, list) and not isinstance(next_element, list):
                graph.add_edge(element[0].id, next_element.id,
                               weight=(next_element.top_left_x - element[0].bot_right_x))
                graph.add_edge(element[1].id, next_element.id,
                               weight=(next_element.top_left_x - element[1].bot_right_x))

            elif not isinstance(element, list) and not isinstance(next_element, list):
                graph.add_edge(element.id, next_element.id,
                               weight=(next_element.top_left_x - element.bot_right_x))

        return graph, position

    def write_nodes(self, output_path):
        full_path = os.path.join(output_path, 'nodes.txt')

        with open(full_path, 'w', encoding='utf-8') as file:
            for node in self.graph.nodes:
                node_label = self.graph.nodes[node]['label']
                file.write(f'{node} {node_label}\n')

    def write_graph(self, output_path):
        full_path = os.path.join(output_path, 'graph.txt')

        with open(full_path, 'w', encoding='utf-8') as file:
            for edge in self.graph.edges():
                source, destination = edge
                weight = self.graph.edges[edge]['weight']
                file.write(f'{source} {destination} {str(weight)}\n')

    def draw_graph(self, output_path):
        plt.figure(figsize=(18, 1))

        # Get labels for each node in the graph
        labels = {node: data['label'] for node, data in self.graph.nodes(data=True)}

        # Draw the graph without labels
        nx.draw(self.graph, self.node_positions, with_labels=False)

        # Draw labels for the nodes
        nx.draw_networkx_labels(self.graph, self.node_positions, labels=labels, font_size=10,
                                font_family='sans-serif')

        # Get the weights of each edge in the graph
        edge_labels = {k: int(v) for k, v in nx.get_edge_attributes(self.graph, 'weight').items()}

        # For each edge, calculate the position for the weight annotation
        for (u, v), label in edge_labels.items():
            x = (self.node_positions[u][0] + self.node_positions[v][0]) / 2
            y = (self.node_positions[u][1] + self.node_positions[v][1]) / 2

            # Define the offset for the annotation based on the value of the weight
            if label < 0:
                offset = (4.15, 2)
            elif label < 10:
                offset = (1, 2)
            else:
                offset = (4, 2)

            # Add the weight annotation to the plot
            plt.annotate(
                label,
                xy=(x, y), xytext=offset,
                textcoords='offset points', ha='right', va='bottom',
                fontsize=8, fontname='calibri'
            )

        full_path = os.path.join(output_path, 'graph.png')
        plt.savefig(full_path)

        plt.close()

    def save_graph(self, output_path):

        self.write_nodes(output_path)
        self.write_graph(output_path)
        self.draw_graph(output_path)

    def build_graph(self, row):

        self.row = row

        self.graph, self.node_positions = self.create_graph()

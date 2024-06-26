import networkx as nx
import random
import n


class BaseStudent:
    def __init__(
        self, edge_list: list[tuple[int, int, int]], begin: int, ends: list[int]
    ) -> None:
        """
        :param edge_list: A list of tuples representing the edge list of the graph. Tuples are of the
        form (u, v, w), where (u, v) specifies that an edge between vertices u and v exist, and w is the
        weight of that edge.
        :param begin: The label of the vertex which students begin on.
        :param ends: A list of labels of vertices that students may end on (i.e. count as a valid exit).
        """
        pass

    def strategy(
        self,
        edge_updates: dict[tuple[int, int], int],
        vertex_count: dict[int, int],
        current_vertex: int,
    ) -> int:
        """
        :param edge_updates: A dictionary where the key is an edge (u, v) and the value is how much that edge's weight increased in the current round.
        Note that this only contains information about edge updates in the current round, and not previous rounds.
        :param vertex_count: A dictionary where the key is a vertex and the value is how many students are currently on that vertex.
        :param current_vertex: The vertex that you are currently on.
        :return: The label of the vertex to move to. The edge (current_vertex, next_vertex) must exist.
        """
        pass


# Starter strategy
class RandomStudent(BaseStudent):

    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends

    def strategy(self, edge_updates, vertex_count, current_vertex):
        # Take a random out-edge
        return random.choice(
            [
                x
                for (_, x, _) in filter(
                    lambda z: z[0] == current_vertex, self.edge_list
                )
            ]
        )
    
class SmartStudent(BaseStudent):
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends

    def declare(self, edges, decision):
        for i in edges:
            print("Edge from " + str(i[0]) + " to " + str(i[1]) + " with w=" + str(i[2]))
        print("DECISION: Edge " + str(decision[0]) + " to " + str(decision[1]) + " with w=" + str(decision[2]))
        print()
        input()
    def strategy(self, edge_updates, vertex_count, current_vertex):
        #update self.edge_list
        fk = {k:v for (k,v) in edge_updates.items() if v != 0}
        for i in range(len(self.edge_list)):
            use = self.edge_list[i]
            if (use[0], use[1]) in fk.keys():
                self.edge_list[i] = (use[0], use[1], use[2] + fk.get((use[0], use[1])))
        
        fd = [(u,v,w) for (u,v,w) in self.edge_list if u == current_vertex]
        least = (0,1,100)
        for i in fd:
            if i[2] < least[2]:
                least = i
        #self.declare(fd, least)
        return least


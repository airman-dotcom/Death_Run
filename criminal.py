import networkx as nx
import random
from operator import itemgetter
import sys
def STA(set):
    a = []
    for x in set:
        a.append(x)
    return a

A = 1

class BaseCriminal:
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
        print(1)
        pass

    def strategy(
        self,
        edge_updates: dict[tuple[int, int], int],
        vertex_count: dict[int, int],
        budget: int,
    ) -> tuple[int, int, int]:
        # Here's the strat: find node which is connected least to final node location
        print(2)
        """
        :param edge_updates: A dictionary where the key is an edge (u, v) and the value is how much that edge's weight increased in the previous round.
        Note that this only contains information about edge updates in the previous round, and not rounds before that.
        :param vertex_count: A dictionary where the key is a vertex and the value is how many students are currently on that vertex.
        :param budget: The remaining budget
        :return: Which edge to attack and by how much. Must be a tuple of the form (u, v, w) where (u, v) represents the edge endpoints
        and w is the increase in edge weight. w must be in the range [0, budget].
        """
        pass


# Starter strategy
class RandomCriminal(BaseCriminal):
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends

    def strategy(self, edge_updates, vertex_count, budget):
        # Find a random populated vertex
        populated_vertices = list(
            filter(lambda z: vertex_count[z], vertex_count.keys())
        )
        vertex = random.choice(populated_vertices)
        # Fill in random out-edge with random weight
        return (
            vertex,
            random.choice(
                [x for (_, x, _) in filter(lambda z: z[0] == vertex, self.edge_list)]
            ),
            random.randint(0, budget),
        )


class BackToFront(BaseCriminal):
    def __init__(self, edge_list, begin, ends):
        #print(edge_list)
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends
        self.added = []
        self.calc = []
        self.turn_num = 1
        self.width = 7
        self.height = 4
        self.students = {}
        #The graded board is 15 * 8

    def delcare(self, updates, decision):
        for (k, v) in updates:
            print("There are %v students at node %k")
        a = decision[2]
        x = decision[0]
        y = decision[1]
        print("DECISION: Add %a to edge (%x, %y)")

    def strategy(self, edge_updates, vertex_count, budget):
        #Update edge_list
        fk = {k:v for (k,v) in edge_updates.items() if v != 0}
        for i in range(len(self.edge_list)):
            use = self.edge_list[i]
            if (use[0], use[1]) in fk.keys():
                self.edge_list[i] = (use[0], use[1], use[2] + fk.get((use[0], use[1])))
        

        self.students = vertex_count
        vertices = {k:v for (k,v) in self.students.items() if v > 0}
        probs = []
        print(vertices)
        for a in vertices.keys():
            b = [items for items in self.edge_list if items[0] == a]
            for i in b:
                print(str(i) + ": " + str(self.calc_all(i[1])))
        for a in vertices.keys():
            use = self.calc_prob(a)
            #[(u,v,w), (u,v,w)]
            use2 = []
            for i in use:
                n = (i[0], i[1], (1/len(use)))
                use2.append(n)
            probs.append(use2)
        delta = 100/(self.width + 2)
        spend = delta
        if budget == 100:
            spend = (3 * delta)
        self.turn_num += 1
        highest = (0,1,0)
        for i in probs:
            use = i[0]
            if highest[2] < use[2]:
                highest = use
        high2 = (highest[0], highest[1], spend)
        return (high2)
        
        
    def calc_all(self, src):
        if src in self.ends:
            return 1
        b = [item for item in self.edge_list if item[0] == src]
        product = len(b)
        for i in range(len(b)):
            product += self.calc_all(b[i][1])
        return product    
    def calc_prob(self, src):
        return sorted([item for item in self.edge_list if item[0] == src], key=lambda x: x[2], reverse=True)
        


class Test(BaseCriminal):
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends
        self.added = []
        self.calc = []
        self.turn_num = 1
        self.width = 7
        self.height = 4
        self.students = {}
        #The graded board is 15 * 8

        

    def strategy(self, edge_updates, vertex_count, budget):
        self.students = vertex_count
        self.calc_all()
        highprob = [item for item in self.calc if item[2] == self.calc[0][2]]
        delta = 100/(self.width + 2)
        spend = delta
        if budget == 100:
            spend = (3 * delta)
        u = (self.calc[0][0], self.calc[0][1], spend)
        self.added.append(u)
        self.turn_num += 1
        return u
    

    def calc_all(self):
        self.calc = []
        dst_layer = list(range((self.turn_num*self.height) - self.height + 1, self.turn_num*self.height + 1))
        #dst_layer = self.ends
        for end in dst_layer:
            c = [item for item in self.edge_list if item[1] == end]
            for i in c:
                self.calc.append((i[0], end, self.calc_prob(i[0], end)))
            #self.calc.append((0, end, self.calc_prob(0, end)))
        self.calc = sorted(self.calc, key=lambda x: x[2], reverse=True)
        return self.calc
    

    def calc_prob(self, src, dst):
        fd = {k:v for (k,v) in self.students.items() if v == 1}
        if src == self.begin or src in fd.keys():
            return 1
        b = [item for item in self.edge_list if item[1] == dst]
        b = [item for item in b if item[0] == src]
        c = [item for item in self.edge_list if item[1] == src]
        new_b = STA(set(c) ^ set(self.added))
        product = (1/len(new_b))
        for i in range(len(c)):
            product *= self.calc_prob(c[i][0], c[i][1])
        return product

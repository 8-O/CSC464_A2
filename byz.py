"""
  CSC464 Assignment 2
  Byzantine Generals in Python

  Thor Reite V00809409
  11/22/2018

  resource: https://marknelson.us/posts/2007/07/23/byzantine.html
"""
from random import randint
from collections import defaultdict

leader_id = 0
processes = dict()
traitor_ids = dict()
children = defaultdict(lambda : defaultdict())
ranked_paths = defaultdict(lambda : defaultdict(lambda : defaultdict()))
init_ids = dict()
n = 7 #num processes
m = 4 #num messages
t = 2 #num traitors

def main():
    for i in range(n):
        traitor_ids[i] = False
        processes[i] = process(i)
    traitors = 0
    while traitors < t:
        i = randint(0,n-1)
        if traitor_ids[i]:
            continue
        else:
            traitor_ids[i] = True
            traitors +=1
    for i in range(m):
        for j in range(n):
            processes[j].send_messages(i, processes)
    for i in range(len(processes)):
        if processes[i].pid is leader_id:
            print("Leader ", end='')
        print("Process %s " % (i), end='')
        if traitor_ids[i]:
            print("(traitor) ", end='')
        print("has decided on value %s" % (processes[i].decide()))
    return

class node():
    def __init__(self, input, output):
        self.input = input
        self.output = output

class process():
    def __init__(self, id):
        self.pid = id
        self.nodes = dict()
        if len(children) is 0:
            self.create_children(m, n, init_ids, leader_id)
        if self.pid is leader_id:
            self.value = randint(0,1)
            self.nodes[''] = node(self.value, '?')

    def confirm_value(self, value, destination):
        if traitor_ids[self.pid]:
            return randint(0,1)
        if self.pid is leader_id:
            return self.value
        return value

    def create_children(self, m, n, pids, source, current_path ='', recursion =0):
        pids[source] = False
        current_path += str(source)
        count = 0
        ranked_paths[recursion][source][count] = current_path
        if recursion < m:
            for i in range(len(pids)):
                if pids[i]:
                    self.create_children(m, n, ids, i, current_path, recursion+1)
                    children[current_path][count] = current_path + str(i)
                    count += 1

    def receive_message(self, path, tar_node):
        self.nodes[str(path)] = tar_node

    def send_messages(self, round, processes):
        for i in range(len(ranked_paths[round][self.pid])):
            source_path = ranked_paths[round][self.pid][i]
            source_path = source_path[0:-1]
            source_node = self.nodes[str(source_path)]
            for j in range(n):
                value = self.confirm_value(source_node.input, j)
                processes[j].receive_message(ranked_paths[round][self.pid][i], 0)

    def decide(self):
        if self.pid is leader_id:
            return self.nodes[''].input
        for i in range(n):
            for j in range(len(ranked_paths[m][i])):
                path = ranked_paths[m][i][j]
                tnode = self.nodes[str(path)]
                tnode.output = tnode.input
        round = m -1
        while round >= 0:
            for i in range(n):
                for j in range(len(ranked_paths[round][i])):
                    path = ranked_paths[round][i][j]
                    tnode = self.nodes[str(path)]
                    tnode.output = self.get_majority(path)
            round -=1
        top_path = ranked_paths[0][leader_id][0]
        top_node = self.nodes[str(top_path)]
        return top_node.output

    def get_majority(self, path):
        tallies = [0,0]
        for child in children[path]:
            node_x = self.nodes[str(child)]
            tallies[node_x.output] +=1
        if tallies[0] < tallies[1]:
            return 1
        else:
            return 0

if __name__ == '__main__':
    main()

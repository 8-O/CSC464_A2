"""
  CSC464 Assignment 2
  Byzantine Generals in Python

  Thor Reite V00809409
  11/22/2018

  resource: https://marknelson.us/posts/2007/07/23/byzantine.html
"""
import copy
from random import randint
from collections import defaultdict

leader_id = 0
processes = dict()
traitor_ids = dict()
children = defaultdict(lambda: dict())
ranked_paths = defaultdict(lambda: defaultdict(list))
init_ids = dict()
n = 7 #num processes
m = 10 #num messages
t = 2 #num traitors

def main():
    for i in range(n):
        traitor_ids[i] = False
        init_ids[i] = True
    create_children(m, n, init_ids, leader_id)
    for i in range(n):
        processes[i] = process(i)
    traitors = 0
    while traitors < t:
        i = randint(0,n-1)
        if traitor_ids[i]:
            continue
        else:
            traitor_ids[i] = True
            traitors +=1
    for i in range(m+1):
        for j in range(n):
            processes[j].send_messages(i, processes)
    for i in range(n):
        if processes[i].pid is leader_id:
            print("Leader Process %s " % (i), end='')
            if traitor_ids[i]:
                print("is a traitor.")
            else:
                print("commanded value %s." % (processes[i].nodes[''].input))
        else:
            print("Process %s has decided on value %s" % (i, processes[i].decide()))
    return

def create_children(m, n, pids, source, current_path ='', recursion =0):
    pids[source] = False
    current_path += str(source)
    count = 0
    ranked_paths[recursion][source].append(current_path)
    if recursion < m:
        for i in range(n):
            if pids[i]:
                create_children(m, n, copy.copy(pids), i, current_path, recursion+1)
                children[current_path][count] = current_path + str(i)
                count += 1

class node():
    def __init__(self, input =0, output =0):
        self.input = input
        self.output = output

class process():
    def __init__(self, id):
        self.pid = id
        self.nodes = dict()
        if self.pid is leader_id:
            value = randint(0,1)
            self.nodes[''] = node(value, '?')

    def confirm_value(self, value):
        if traitor_ids[self.pid]:
            return randint(0,1)
        else:
            return value

    def receive_message(self, path, node):
        self.nodes[str(path)] = node

    def send_messages(self, round, processes):
        for i in range(len(ranked_paths[round][self.pid])):
            source_path = ranked_paths[round][self.pid][i]
            source_path = source_path[:-1]
            source_node = self.nodes[str(source_path)]
            for j in range(n):
                value = self.confirm_value(source_node.input)
                #print('Sending from process ' + str(self.pid) + ' to ' + str(j) + ':', end='')
                #print('{' + str(value) + ', ' + ranked_paths[round][self.pid][i] + ', ' + str('?') + '},',end='')
                #print('getting value from source_node ' + source_path + ' value ' + str(value))
                processes[j].receive_message(ranked_paths[round][self.pid][i], node(value,'?'))

    def decide(self):
        if self.pid is leader_id:
            return self.nodes[''].input
        for i in range(n):
            for j in range(len(ranked_paths[m][i])):
                path = ranked_paths[m][i][j]
                node = self.nodes[str(path)]
                node.output = node.input
        round = m -1
        while round >= 0:
            for i in range(n):
                for j in range(len(ranked_paths[round][i])):
                    path = ranked_paths[round][i][j]
                    node = self.nodes[str(path)]
                    node.output = self.get_majority(path)
            round -=1
        top_path = ranked_paths[0][leader_id][0]
        top_node = self.nodes[str(top_path)]
        return top_node.output

    def get_majority(self, path):
        tallies = [0,0]
        for key, child in children[path].items():
            node = self.nodes[str(child)]
            if node.output is 1:
                tallies[1] +=1
            elif node.output is 0:
                tallies[0] +=1
        if tallies[0] < tallies[1]:
            return 1
        else:
            return 0

if __name__ == '__main__':
    main()

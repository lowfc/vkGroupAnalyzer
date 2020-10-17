import networkx as nx
from lowfchtml import Html
from os.path import exists
from vkparser import VKParser
from time import time
#import matplotlib.pyplot as plt

def pseudo_parser():
    pars = VKParser()
    pars.get_group_users('lowfc_beatz')
    pars.complete_friendship()
    nodes = pars.get_users()
    weights = pars.get_friendship()
    return nodes, weights


class Configurator:
    def __init__(self):
        self.nodes, self.weights = pseudo_parser() #nodes - кортеж id людей, weights - словарь дружеских связей (подразумивается отсутствие дублей)
        if len(self.nodes)<=10:
            self.screen_scale = 2000 # коэффициент масштабирования canvas
        elif len(self.nodes)<=30:
            self.screen_scale = 4000
        elif len(self.nodes)<=60:
            self.screen_scale = 6000
        elif len(self.nodes)<=100:
            self.screen_scale = 9000
        else:
            self.screen_scale = 10000

        self.graph = nx.Graph() # инициализация графа NX
        self.node_html_coords = {} # словарь, хранит данные вида { ребро : (x pos, y pos) }
        self.add_nodes(self.nodes) # добавление вершин в NX
        for i in self.weights: # добавление весов-связей в NX
            self.add_weights(i[0],i[1])
        

    def add_nodes(self, nodes):  # Упрощаем добавление вершин NX
        for i in nodes:
            self.graph.add_node(i.get('id'))
    
    def add_weights(self, f_item, s_item): # Упрощаем добавление весов NX
        self.graph.add_edge(f_item, s_item)
        self.graph.add_edge(s_item, f_item)
    
    
    def refact_coords(self, axis, var): # Перевод из системы координат NX в систему координат HTML (Возвращается положение в процентах,
        if var == 1:                    # Для расположения на экране в PX, домножить на ширину/высоту экрана
            var = 0.9  
        elif var == -1:
            var = -0.9
        if axis == 'x':
            if var<0:
                return .5 * var * -1
            elif var>0:
                return var * .5 + .5
            else:
                return .5
        elif axis == 'y':
            if var<0:
                return ( (var * -1) * .5 ) + .5
            elif var>0:
                return .5 - (var * .5)
            else:
                return .5

    def create_html (self): # Создает HTML документ с помощью класса Html
        nx.draw(self.graph)
        plt.show()
        self.G = Html(self.screen_scale)
        pos = nx.spring_layout(self.graph)
        for i in self.nodes:
            k = i.get('id')
            x = self.refact_coords('x', pos[k][0]) * self.screen_scale
            y = self.refact_coords('y', pos[k][1]) * self.screen_scale + 150
            self.G.add_edge(k, x, y, i.get('first_name')+' '+i.get('last_name'), img = i.get('photo_100'))
            self.node_html_coords.update({k:(x,y)})
        for i in self.weights:
            coords = self.node_html_coords.get(i[0])
            coords2 = self.node_html_coords.get(i[1])
            self.G.add_weight(coords[0], coords[1], coords2[0], coords2[1])
        self.G.pack()
        self.G.open_tab()

if __name__ == '__main__':
    start = time()
    con = Configurator()
    con.create_html()
    print('total time execution:',time() - start)


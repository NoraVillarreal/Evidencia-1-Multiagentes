import mesa
import numpy as np
import time
import random


class CleanAgent(mesa.Agent):
    # An agent with fixed initial wealth.

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.count = 1
        
    def step(self):
        self.move()
        self.clean()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.count = self.count + 1
        print("Cajas apiladas " + str(self.model.cajas_restantes()) + "----" + str(self.count))

    def clean(self):
        if self.model.Box(self.pos):
            self.model.elimBox(self.pos)
        pass
    

class CleanModel(mesa.Model):
    def __init__(self, N, width, height, K):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.dirty_matrix = np.zeros([width,height])
        self.celdas_stnec = float(K/5) + (K -(float(K/5)*5))
        self.celdas_stack = np.empty((0,2), int)
        self.sum = 0
        self.dist_cajas = np.empty([0], int)
        while np.sum(self.dist_cajas) < (K - 5):
            self.dist_cajas = np.append(self.dist_cajas, np.array(random.randint(1, 4)))

        num = K - np.sum(self.dist_cajas)
        self.dist_cajas = np.append(self.dist_cajas, num)

        countw = 0
        counth = 0
        i = 0
        while i < self.celdas_stnec:
            while counth < width and i < self.celdas_stnec:
                countw = 0
                while countw < height and i < self.celdas_stnec:
                    self.celdas_stack = np.append(self.celdas_stack, np.array([[counth,countw]]), axis=0)
                    i = i+1
                    countw = countw+1

                counth = counth+1

        
        countw = 0
        counth = 0
        var = 1
        countcs = self.dist_cajas.size
        for x in self.dirty_matrix:
            if width < countcs:
                while counth < height and var == 1:
                    countw = 0
                    while countw < width and var == 1:
                        if countcs > 0:
                            self.dirty_matrix[countw][counth] = self.dist_cajas[countcs-1]
                            countw = countw + 1
                            countcs = countcs - 1
                        else:
                            var = 0  
                    counth = counth + 1            
            else:
                while countw < width and var == 1:
                    
                    if countcs > 0:
                        self.dirty_matrix[countw][counth] = self.dist_cajas[countcs-1]
                        countw = countw + 1
                        countcs = countcs - 1
                        if countcs <= 0:
                            var = 0
                            pass
                    else:
                        var = 0 
        counth = 0
        countw = 0
        if width < height:
            while countw < width:
                np.random.shuffle(self.dirty_matrix[countw])
                countw = countw + 1
            self.printarray()
        else:
            while counth < height:
                np.random.shuffle(self.dirty_matrix[counth])
                counth = counth + 1
            self.printarray()

        self.width = width
        self.height = height
        
        for i in range(self.num_agents):
            a = CleanAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))

        
    
    def step(self):
        self.schedule.step()


    def Box(self, new_position):
        self.sum = 0
        for j in self.celdas_stack:
            x, y = j
            self.sum = self.sum + self.dirty_matrix[x][y]
        x, y = new_position
        if self.dirty_matrix[x][y] >= 1:
            return True
        else:
            return False

    def elimBox(self, new_position):
        x, y = new_position
        self.dirty_matrix[x][y] = self.dirty_matrix[x][y] - 1
        self.stackll = 0
        for i in self.celdas_stack:
            x, y = i
            if self.dirty_matrix[x][y] < 5:
                self.dirty_matrix[x][y] = self.dirty_matrix[x][y] + 1
                break
            else:
                self.stackll = self.stackll+1
        self.sum = 0
        for j in self.celdas_stack:
            x, y = j
            self.sum = self.sum + self.dirty_matrix[x][y]



    def printarray(self):
        print(self.dirty_matrix)

    def cajas_restantes(self):
        return int(self.sum)

    

    
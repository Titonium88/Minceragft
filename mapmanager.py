# напиши здесь код создания и управления картой
class Mapmanager():
    def __init__(self):
        self.model = 'block'

        self.texture = 'block.png'
        self.colors = [(0.165, 0.169, 0.212, 1),
                       (0.3, 0.3, 0.3, 1),
                       (0.525, 0.525, 0.729, 1),
                       (0.737, 0.737, 0.929, 1),
                       (1, 1, 1, 1)]


        self.startNew()

    
    def startNew(self):
        self.land = render.attachNewNode("Land")

    def addBlock(self, position):
        color = self.getColor(position[2])
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.block.setColor(color)
        self.block.reparentTo(self.land)
        self.block.setTag('at', str(position))

    def getColor(self,z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors)-1]
    
    def clearMap(self):
        self.land.removeNode()
        self.startNew()

    def isEmpty(self, position):
        blocks = self.findBlocks(position)
        if blocks:
            return False
        else:
            return True

    def findBlocks(self,position):
        return self.land.findAllMatches('=at=' + str(position))

    def findHighestEmpty(self, position):
        x, y, z = position
        z = 1
        while not self.isEmpty((x,y,z)):
            z+=1
        return (x, y, z)

    def buildBlock(self, pos):
        self.addBlock(pos)

    def delBlockFrom(self, pos):
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()

    def loadMap(self,filename):
        self.clearMap()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z)+1):
                        self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x,y

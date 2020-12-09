from xml_io import *

fonts = {
    'title':'Ubuntu 36',
    'accent':'Ubuntu 12',
    'accent2':'Ubuntu 8'
}
class ColorScheme(object):
    fills = {'dark':(18,18,18),'light':(215,253,255)}
    fills2 = {'dark':(40,40,40),'light':(200,200,200)}
    accent1 = {'dark':(20,255,236),'light':(148,40,142)}
    accent2 = {'dark':(255,51,204),'light':(255,255,0)}

    types = {
        'type1':settingsXML.getDayColor(1),
        'type2':settingsXML.getDayColor(2),
        'type3':settingsXML.getDayColor(3),
        'type4':settingsXML.getDayColor(4),
        'type5':settingsXML.getDayColor(5),
        'type6':settingsXML.getDayColor(6),
    }
    
    def __init__(self,color):
        self.color = color
        self.fill = ColorScheme.fills[color]
        self.accent1 = ColorScheme.accent1[color]
        self.accent2 = ColorScheme.accent2[color]
        self.fill2 = ColorScheme.fills2[color]
    
    # copied from graphics course notes
    # https://www.cs.cmu.edu/~112/notes/notes-graphics.html
    def rgbString(self, r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def setColor(self,color):
        self.fill = ColorScheme.fills[color]
        self.accent1 = ColorScheme.accent1[color]
        self.color = color
    
    def getColor(self):
        return self.color

    def getFill(self):
        return self.rgbString(self.fill[0],self.fill[1],self.fill[2])
    
    def getFill2(self):
        return self.rgbString(self.fill2[0],self.fill2[1],self.fill2[2])

    def getAccent1(self):
        return self.rgbString(self.accent1[0],self.accent1[1],self.accent1[2])

    def getAccent2(self):
        return self.rgbString(self.accent2[0],self.accent2[1],self.accent2[2])

    def getTypeColor(self,typeNum):
        typeColor = self.types[f'type{typeNum}']
        return self.rgbString(typeColor[0],typeColor[1],typeColor[2])

    def setTypeColor(self,typeNum,r,g,b):
        index = 'type'+str(typeNum)
        self.types[index] = (int(r),int(g),int(b))

scheme = ColorScheme('dark')

import random
class Collage(object):
    def __init__(self,items,width,height):
        self.items = items
        self.allocatedSpace = []
        self.positions = []
        self.margin = 80
        self.width = width-self.margin
        self.height = height-self.margin
        self.rootPosition = (self.margin,self.height)

    def isPositionLegal(self,x,y,size):
        if self.allocatedSpace == []:
            return True
        for zone in self.allocatedSpace:
            if (zone[0] <= x-size <= zone[2] and zone[1] <= y-size <= zone[3]):
                return False
            if (zone[0] <= x+size <= zone[2] and zone[1] <= y+size <= zone[3]):
                return False
            if (zone[0] <= x+size <= zone[2] and zone[1] <= y-size <= zone[3]):
                return False
            if (zone[0] <= x-size <= zone[2] and zone[1] <= y+size <= zone[3]):
                return False
            if (x < self.margin or x > self.width or 
                y < self.margin or y > self.height):
                return False
        return True

    def getImageCollagePosition(self,index):
        print(index)
        numSpots = len(self.items)
        x,y = random.randint(self.margin,self.width),random.randint(self.margin,self.height)
        image = self.items[index][0]
        while not self.isPositionLegal(x,y,image.size[0]//2):
            x,y = random.randint(self.margin,self.width),random.randint(self.margin,self.height)
        self.allocatedSpace.append((x-image.size[0]//2,y-image.size[1]//2,x+image.size[0]//2,y+image.size[1]//2))
        self.positions.append((x,y))
        return (x,y)

    def getImageCollagePositions(self):
        for i in range(len(self.items)):
            self.getImageCollagePosition(i)
        return self.positions
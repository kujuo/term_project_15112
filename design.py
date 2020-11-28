
class ColorScheme(object):
    fills = {'dark':(18,18,18),'light':(215,253,255)}
    accent1 = {'dark':(20,255,236),'light':(148,40,142)}
    
    def __init__(self,color):
        self.color = color
        self.fill = ColorScheme.fills[color]
        self.accent1 = ColorScheme.accent1[color]
    
    def rgbString(self, r, g, b):
        # Don't worry about the :02x part, but for the curious,
        # it says to use hex (base 16) with two digits.
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def setColor(self,color):
        self.fill = ColorScheme.fills[color]
        self.accent1 = ColorScheme.accent1[color]
        self.color = color
    
    def getColor(self):
        return self.color

    def getFill(self):
        return self.rgbString(self.fill[0],self.fill[1],self.fill[2])

    def getAccent1(self):
        return self.rgbString(self.accent1[0],self.accent1[1],self.accent1[2])

scheme = ColorScheme('dark')

class ColorScheme(object):
    colors = {'dark':(18,18,18),'light':(187,234,234)}
    
    def __init__(self,color):
        self.color = ColorScheme.colors[color]
    
    def rgbString(self, r, g, b):
        # Don't worry about the :02x part, but for the curious,
        # it says to use hex (base 16) with two digits.
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def setColor(self,color):
        self.color = ColorScheme.colors[color]

    def getFill(self):
        return self.rgbString(self.color[0],self.color[1],self.color[2])

appColorScheme = ColorScheme('dark')
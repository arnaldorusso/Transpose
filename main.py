from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import *
from reportlab.lib.pagesizes import letter
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

def main():
    c = canvas.Canvas('MyFirstLine.pdf', pagesize=letter)
    width, height = letter

    c.setFont('Helvetica', 12)
    c.drawCentredString(280, 770, 'First Line of Twinkle Twinkle Little Star')

    staff = Staff()
    # TODO: constants, enum different types of clefs & positions
    staff.applyClef(svg2rlg('./Images/GClef.svg'))
    getLinePos = staff.getNotePos
    m1 = Measure(4, getLinePos)
    n = Note(-1)
    m1.addNote(n)
    m1.addNote(Note(-1))
    
    m2 = Measure(4, getLinePos)
    m2.addNote(Note(3))
    m2.addNote(Note(3))
    m2.addNote(Note(4))
    m2.addNote(Note(4))

    m3 = Measure(4, getLinePos)
    m3.addNote(Note(3))
    m3.addNote(Note(3))
    m3.addNote(Note(2))
    m3.addNote(Note(2))
    staff.addMeasure(m1)
    staff.addMeasure(m2)
    staff.addMeasure(m3)
    #staff.addMeasure(Measure(4))
    staff.render(c, 50, 600)
    c.save()


class Staff:
    
    def __init__(self, height=40, width=500):
        self.space = height/5
        self.height = self.space * 5
        self.width = width
        self.drawing = Drawing(self.width, self.height)
        self.measures = []
    
    # render staff from bottom up
    def render(self, canvas, renderX, renderY):
        leftX = 0
        rightX = leftX + self.width
        for i in range(5):
            y = i * self.space
            self.drawing.add(Line(leftX, y, rightX, y))

        measureX = 20 
        for m in self.measures:
            measureX += m.width 
            print str(measureX)
            m.render(self.drawing, measureX, 0)  
        renderPDF.draw(self.drawing, canvas, renderX, renderY)  
        #render children
    
    def getNotePos(self, line):
        dist = self.space/2
        return dist * line
        

    def applyClef(self, clef):
        clef.scale(1.5, 1.5)
        clef.translate(0, -10)
        self.drawing.add(clef)
    
    # return false if too many measures defined
    def addMeasure(self, m):
        if ((self.getTotalMeasureWidth() + m.width) <= self.width):
            self.measures.append(m)
            return True
        return False

    def getTotalMeasureWidth(self):
        width = 0
        for m in self.measures:
            width += m.width
        return width
def enum(**enums):
    return type('Enum', (), enums)

BAR = enum(STD='standard', DOUB='double', END='end') 

class Measure:
    MIN_WIDTH = 150
    HEIGHT = 32 
    # globals defined
    def __init__(self, beats, getLine, barType=BAR.STD, height=HEIGHT, signature=None):
        self.beats = beats
        self.getLine = getLine
        self.barType = barType
        self.timeSignature = signature
        self.width = Measure.MIN_WIDTH 
        self.height = height
        self.drawing = Drawing()
        self.notes = []

    def render(self, drawing, renderX, renderY):
        #self.drawing.add(Line(renderX, renderY, renderX, y))
        self.drawing.add(Line(0, 0, 0, self.height))

        width = self.width/self.beats
        for i in range(len(self.notes)):
            space = (i) * width * - 1 - 10
            index = -1 * (i+1) 
            y = self.getLine(self.notes[index].line)
            self.notes[index].render(self.drawing, space, y)

        self.drawing.translate(renderX, renderY)
        drawing.add(self.drawing);

    def addNote(self, note):
        self.notes.append(note)

class Note:
    def __init__(self, line):
        self.line = line
    
    def render(self, drawing, renderX, renderY):
        drawing.add(Ellipse(renderX - 4, renderY - 4, 8, 4))
    
if __name__ == '__main__':
    main()


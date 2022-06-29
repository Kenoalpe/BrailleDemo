#!/usr/bin/env python
import time
import RPi.GPIO as GPIO

from samplebase import SampleBase
from rgbmatrix import graphics

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pin = [10,9,11,25,8,7]
bitlist = []
BinToB = {
    63 : " ",
    32 : "A",
    48 : "B",
    36 : "C",
    38 : "D",
    34 : "E",
    52 : "F",
    54 : "G",
    50 : "H",
    20 : "I",
    22 : "J",
    40 : "K",
    56 : "L",
    44 : "M",
    46 : "N",
    42 : "O",
    60 : "P",
    62 : "Q",
    58 : "R",
    28 : "S",
    30 : "T",
    41 : "U",
    57 : "V",
    23 : "W",
    45 : "X",
    47 : "Y",
    43 : "Z"
}

def milli(sek):
    time.sleep(sek/1000)

class MoveLED(SampleBase):
    
    def __init__(self, *args, **kwargs):
        super(MoveLED, self).__init__(*args, **kwargs)
    
    def run(self):
        canvas = self.matrix.CreateFrameCanvas()
        font1 = graphics.Font()
        font1.LoadFont("../rpi-rgb-led-matrix/fonts/9x15.bdf")
        font2 = graphics.Font()
        font2.LoadFont("../rpi-rgb-led-matrix/fonts/5x8.bdf")
        textColor = graphics.Color(200,200,200)
        STime = time.time()
        NTime = time.time()
        DTime = 0
        BinOutAlt = 0        
        phase = 0
        StrichX = 5
        text = []
        StartText = 0
        KBuchstabe = 0
        
        while True:
            #Rahmen
            self.DrawBox(canvas,0,0,63,31,78,138,137)
            
            #= Zeichen
            self.FillBox(canvas,28,7,35,8)
            self.FillBox(canvas,28,10,35,11)
            
            #Buttons Testen
            for k in range (0,6):
                if(GPIO.input(pin[k])!=1):
                    #print("Gedrueckt" + str(pin[i]) + " " + str(i+1))
                    #canvas.SetPixel(3,1,160,160,160)s
                    bitlist.append(1)
                    
                else:
                    bitlist.append(0)
            
            #print(bitlist)
            bitX = 16
            bitY = 4
            
            #Braille Punkte schreiben
            if(bitlist[0]):
                self.FillBox(canvas,bitX,bitY,bitX+2,bitY+2)
            if(bitlist[1]):
                self.FillBox(canvas,bitX,bitY+4,bitX+2,bitY+6)
            if(bitlist[2]):
                self.FillBox(canvas,bitX,bitY+8,bitX+2,bitY+10)
            if(bitlist[3]):
                self.FillBox(canvas,bitX+4,bitY,bitX+6,bitY+2)
            if(bitlist[4]):
                self.FillBox(canvas,bitX+4,bitY+4,bitX+6,bitY+6)
            if(bitlist[5]):
                self.FillBox(canvas,bitX+4,bitY+8,bitX+6,bitY+10)
            
            #Array in Zahl Übersetzten
            BinOut = 0
            for bit in bitlist:
                BinOut = (BinOut << 1) | bit
            
            #Schreibe Großen Buchstaben
            try:
                #print(BinToB[BinOut])
                graphics.DrawText(canvas,font1,40,14,textColor,BinToB[BinOut])
                KBuchstabe = 1
            except:
                graphics.DrawLine(canvas,41,14,47,4,graphics.Color(200,0,0))
                KBuchstabe = 0
            
            #Blinkender Strich
            JTime = time.time()-STime
            if(JTime > 0.750):
                STime = time.time()
                if(phase==1):
                    phase = 0
                elif(phase==0):
                    phase = 1
                    
            #Strich
            StrichX = (len(text)*5) + 3
            
            if(phase==1 and len(text) < 11):
                graphics.DrawLine(canvas,StrichX,28,StrichX+3,28,graphics.Color(200,200,200))
            
            #Wurde Buchstabe geschrieben
                
            if(BinOut != BinOutAlt or KBuchstabe == 0):
                NTime = time.time()
                BinOutAlt = BinOut
            else:
                DTime = time.time()-NTime
                #print (DTime)
                
            #print(BinOut)
                
            if(DTime > 2 and time.time()-StartText > 1 and len(text) < 12):
                try:
                    text.append(BinToB[BinOut])
                    StartText = time.time()
                    NTime = time.time()
                except:
                    pass
            
            if(GPIO.input(19)!=1 and GPIO.input(18)!=1):
                text.clear()
            
            #Schreibe Buchstabe
            for BZahl, buchstabe in enumerate(text, start=1):
                graphics.DrawText(canvas,font2,(BZahl*5)-2,28,textColor,buchstabe)
                
            
            #Clear und Reset
            bitlist.clear()
            canvas = self.matrix.SwapOnVSync(canvas)
            milli(250)
            canvas.Clear()
            

if __name__ == "__main__":
    moveled = MoveLED()
    if (not moveled.process()):
        moveled.print_help()

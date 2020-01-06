# Matthew Rutigliano
# ECEGR 3910
# Final Project
# C.R.a.N.K
# Description: Do you yearn for the days of Soulja Boy ringtones on your old Nokia brick? Do you have Razr sharp reaction time?
#              Got Crazy Reflexes and No Kalendar? Get C.R.a.N.Ked!! Text as many of the prompts as you can in the time given!

from RPLCD import CharLCD
import RPi.GPIO as GPIO # Raspberry Pi GPIO library
from keypad import *
from timeit import default_timer as timer
import random
import time

# Setup GPIO
GPIO.setwarnings(False) # Ignore warnings
GPIO.setmode(GPIO.BCM)

lcdCols = 16
lcdRows = 2

pressDelay = .25
newKey = .5

lcd = CharLCD(numbering_mode=GPIO.BCM, cols=lcdCols, rows=lcdRows, pin_rs=2, pin_e=3, pins_data=[4, 17, 27, 22])
lcd.clear()
lcd.cursor_mode = 'hide'

kp = keypad([26,16,20,21],[6,13,19])

words = ('LOL', 'ROFL', 'LMAO', 'BFF', 'B4N', 'DILLIGAS', 'THX', 'TTYL', 'JOE MAMA', '8', 'OFC', 'CRANK', '2MOR', '2PAC CUBA', 'BRB', 'PLS')
            
letters = { 1: (' '),
            2: ('A','B','C','2'),
            3: ('D','E','F','3'),
            4: ('G','H','I','4'),
            5: ('J','K','L','5'),
            6: ('M','N','O','6'),
            7: ('P','R','S','7'),
            8: ('T','U','V','8'),
            9: ('W','X','Y','Z','9'),
            0: (''),
            '#': (''),
            '*': ('')}

try:
    print("Beginning crank.py")
    
    while(1):
        score = 0
        streak = 0
        
        timeLimit = 60 #seconds
        
        digit = None
        
        wordsUsed = []
        for i in words:
            wordsUsed.append(True)
        
        # Attract Mode
        lcd.clear()
        lcd.cursor_pos = (0,3)
        lcd.write_string("C.R.a.N.K.")
        lcd.cursor_pos = (1,0)
        lcd.write_string("1:Space   #:Back")
        while(digit == None):
            digit = kp.getKey()
            
        lcd.clear()
        lcd.cursor_pos = (0,3)
        lcd.write_string("Get ready")
        time.sleep(2)
        lcd.clear()
        
        startTime = time.time()
        while((time.time() - startTime) <= timeLimit):
            # Word Generation
            while(1):
                wordInd = random.randint(0, len(words)-1)
                if (wordsUsed[wordInd]):
                    wordsUsed[wordInd] = False
                    break
                    
            lcd.cursor_pos = (0,0)
            lcd.write_string(words[wordInd])
            
            # Write Score
            if (score < 10):
                lcd.cursor_pos = (lcdRows-1, lcdCols-1)
            else:
                lcd.cursor_pos = (lcdRows-1, lcdCols-2)
            lcd.write_string(str(score))
            
            lcd.cursor_pos = (1,0)
            lcd.write_string("_")
            
            guess = []
            for i in words[wordInd]:
                guess.append(" ")
                
            digit = None
            lastDigit = None
            numPress = 0

            cursCol = -1
            cursRow = 1
            
            while((time.time() - startTime) <= timeLimit):
                perfect = True
                
                # T9 Texting Input Loop
                start = timer()
                while (digit == None or digit == 0 or digit == '*'):
                    # Print Timer
                    lcd.cursor_pos = (0,lcdCols-2)
                    lcd.write_string(str(timeLimit-(time.time() - startTime) + 1)[0:2])
                    # Get Keypress
                    digit = kp.getKey()
                    # Reset lastDigit if newKey seconds pass
                    if (timer() - start >= newKey):
                        lastDigit = None
                        lcd.cursor_pos = (1, cursCol + 1)
                        lcd.write_string("_")
                # Delete
                if (digit == '#'):
                    perfect = False
                    streak = 0
                    if (cursCol >= 0):
                        if (cursCol < len(guess)):
                            guess[cursCol] = " "
                        lcd.cursor_pos = (cursRow, cursCol)
                        lcd.write_string('_ ')
                        cursCol -= 1
                
                else:    
                    if (digit == lastDigit):
                        numPress += 1
                        # Looping through button options
                        if (numPress == len(letters[digit])):
                            numPress = 0
                    else:
                        numPress = 0
                        cursCol += 1
                        
                    lcd.cursor_pos = (cursRow, cursCol)
                    lcd.write_string(letters[digit][numPress])
                    
                    if (cursCol < len(words[wordInd])):
                        guess[cursCol] = letters[digit][numPress]
                    
                    lastDigit = digit
                digit = None
                time.sleep(pressDelay)
                
                # Checking to see if match
                guessString = ""
                for elem in guess:
                    guessString = guessString + elem
                if (guessString == words[wordInd]):
                    score += 1
                    if (perfect):
                        streak += 1
                        if (streak % 3 == 0):
                            timeLimit += streak
                    break
               
            # Reset screen
            lcd.clear()
            
        # Game Over Screen
        lcd.cursor_pos = (0,4)
        lcd.write_string("Time Up!")
        lcd.cursor_pos = (1,1)
        lcd.write_string("Your Score: " + str(score))
        time.sleep(5)
            
        lcd.clear()
        lcd.cursor_pos = (0,3)
        lcd.write_string("Game Over")
        time.sleep(3)
        

except KeyboardInterrupt: 
    # This code runs on a Keyboard Interrupt <CNTRL>+C
    print('\n\n' + 'Program exited on a Keyboard Interrupt' + '\n') 




finally:
    if (lcd.cursor_mode != 'hide'):
        lcd.cursor_mode = 'hide'
    lcd.clear()
    GPIO.cleanup()
    
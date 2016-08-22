'''
----------------------------
    
    Written By Zachary Collins
    August 2015
    
    dumpstertree.com
    dumpstertree@gmail.com
    @dumpstertree
    
----------------------------
'''

import time
import random
import maya.cmds as cmds

_activeShake = False
_activeOpen  = False
_activeClose = False
_activeFlash = False
_activePulse = False
_activeButtonTyping = False
_activeTextTyping = False

def sleep( additionalTime ):
	
	currentTime = time.time()
	endTime = currentTime + additionalTime

	while currentTime < endTime:
		currentTime = time.time()

	return None 
def shakeAnimation( ui, duration, intesity ):
	global _activeShake

	if _activeShake == True:
		return
	else: 
		_activeShake = True

	startTime 	= time.time()
	endTime 	= startTime + duration
	elapsedTime = 0

	startingMenuX = cmds.window(ui, query=True, leftEdge = True)
	startingMenuY = cmds.window(ui, query=True, topEdge = True)
 	
	while (elapsedTime + startTime < endTime):
		
 		if cmds.window( ui, exists=True) == False:
			_activeShake = False
			return

		elapsedTime = time.time() - startTime
		timerFrac 	 = 1.0 - ( elapsedTime / duration )
		
		curIntensity = intesity * timerFrac
		curIntensity = int( clampValue( curIntensity, 1, intesity) )

		plusX = random.randint( -curIntensity, curIntensity)
		plusY = random.randint( -curIntensity, curIntensity)

		cmds.window(ui, edit=True, leftEdge=startingMenuX+plusX, topEdge=startingMenuY+plusY)
		cmds.refresh( force=True )

	cmds.window(ui, edit=True, leftEdge=startingMenuX, topEdge=startingMenuY)
	_activeShake = False
def openAnimation( ui, startHeight, endHeight, duration):
	global _activeOpen

	if _activeOpen == True:
		return
	else: 
		_activeOpen = True

 	startTime 	= time.time()
	endTime 	= startTime + duration
	elapsedTime = 0
 	
 	while (elapsedTime < duration):

 		if cmds.window( ui, exists=True) == False:
			_activeOpen = False
			return

		elapsedTime = time.time() - startTime
		height = tweenEaseInOut( elapsedTime, startHeight, endHeight, duration)
		height = clampValue(height, 1, endHeight)
		
		cmds.window(ui, edit=True, h=height)
		cmds.refresh( force=True )

	_activeOpen = False
def closeAnimation( ui, titleHeight, bodyHeight, duration ):
	global _activeClose

	if _activeClose == True:
		return
	else: 
		_activeClose = True

	stallTime = .1

 	startTime 	= time.time()
	endTime 	= startTime + duration
	elapsedTime = 0
	
	while (elapsedTime < duration):
		
		if cmds.window( ui, exists=True) == False:
			_activeClose = False
			return

		elapsedTime = time.time() - startTime
		height = tweenEaseInOut( elapsedTime, 1, titleHeight+bodyHeight, duration)
		height = titleHeight+bodyHeight - clampValue(height, 0, titleHeight+bodyHeight -1)
		cmds.window(ui, edit=True, h=height)

		cmds.refresh(force=True)

	cmds.deleteUI( ui )
	_activeClose = False
def flashAnimation( ui, numberOfFlashes, flashLength, flashColor ):
	global _activeFlash

	if _activeFlash == True:
		return
	else: 
		_activeFlash = True

	baseColor = cmds.columnLayout( ui, query=True, bgc=True)
	
	for flash in range( numberOfFlashes ):

		if cmds.columnLayout( ui, exists=True) == False:
			_activeFlash = False
			return

		cmds.columnLayout( ui, edit=True, bgc=baseColor)
		cmds.refresh(force=True)
		sleep( flashLength )

		cmds.columnLayout( ui, edit=True, bgc=flashColor)
		cmds.refresh(force=True)
		sleep( flashLength )

	cmds.columnLayout( ui, edit=True, bgc=baseColor)
	cmds.refresh(force=True)
	sleep( flashLength )
	_activeFlash = False
def pulseAnimation( ui, numberOfPulses, pulseLength, pulseColor):
	global _activePulse

	if _activePulse == True:
		return
	else: 
		_activePulse = True

	baseColor = cmds.columnLayout( ui, query=True, bgc=True )

	cmds.columnLayout( ui, edit=True, bgc=pulseColor )
	cmds.refresh( force=True )
	for pulse in range(numberOfPulses):

		startTime 	= time.time()
		endTime 	= startTime + pulseLength
		elapsedTime = 0

		while (startTime + elapsedTime < endTime):
			
			if cmds.columnLayout( ui, exists=True) == False:
				_activePulse = False
				return

			elapsedTime = time.time() - startTime
			timerFrac 	= elapsedTime / pulseLength

			rFrac = abs( pulseColor[0] - baseColor[0] ) * timerFrac + pulseColor[0]
			gFrac = abs( pulseColor[1] - baseColor[1] ) * timerFrac + pulseColor[1]
			bFrac = abs( pulseColor[2] - baseColor[2] ) * timerFrac + pulseColor[2]

			cmds.columnLayout(ui, edit=True, bgc=(rFrac,gFrac,bFrac))
			cmds.refresh(force=True)

		cmds.columnLayout(ui, edit=True, bgc=baseColor)
		cmds.refresh(force=True)
		_activePulse = False
def buttonTypingAnimation( ui, phrase, fullLength):
	global _activeButtonTyping

	if _activeButtonTyping == True:
		return
	else: 
		_activeButtonTyping = True

	timePerLetter = fullLength/len(phrase)
	phraseFrac = ""
	
	cmds.button(ui, edit=True, label = phraseFrac)
	cmds.refresh(force=True)
	
	for letters in phrase :

		if cmds.button( ui, exists=True) == False:
			_activeButtonTyping = False
			return

		sleep(timePerLetter)	
		phraseFrac += letters

		cmds.button(ui, edit=True, label = phraseFrac)
		cmds.refresh(force=True)

	_activeButtonTyping = False
def textTypingAnimation( ui, phrase, fullLength):
	global _activeTextTyping

	if _activeTextTyping == True:
		return
	else: 
		_activeTextTyping = True

	timePerLetter = fullLength/len(phrase)
	phraseFrac = ""
	
	cmds.text(ui, edit=True, label = phraseFrac)
	cmds.refresh(force=True)
	
	for letters in phrase :

		if cmds.text( ui, exists=True) == False:
			_activeTextTyping = False
			return

		sleep(timePerLetter)	
		phraseFrac += letters

		cmds.text(ui, edit=True, label = phraseFrac)
		cmds.refresh(force=True)

	_activeTextTyping = False

def tweenEaseIn( t, b, c, d ):
	t /= d
	return c*t*t + b
def tweenEaseOut( t, b, c, d ):
	t /= d
	return -c * t*(t-2) + b
def tweenEaseInOut( t, b, c, d ):
	t /= d/2

	if (t < 1):
		return c/2*t*t*t*t + b

	t -= 2
	return -c/2 * (t*t*t*t - 2) + b

def clampValue( n, minn, maxn ):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n


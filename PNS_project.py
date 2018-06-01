# -*- coding: utf-8 -*-
"""
Created on Sun May 13 17:38:30 2018

@author: jason
"""

## If the experiment does not run optimally, you might want to consider downgrading pyhton packages.
## The main package versions are listed below

## Psychopy version 1.85.3
from psychopy.visual import Window, TextStim  
from psychopy.event import waitKeys, clearEvents
from psychopy.core import wait
## pandas version 0.22.0
import pandas as pd
import os
## python-pygaze 0.6.0a25
from pygaze.sound import Sound


## calling directory; Change before running!!!!
os.chdir('D:/Muy importante/resmas/ProgrammingTNS')
## participant number
pp = 'test'
## Some initial settings
DISPSIZE = [1536,864]
BGC = (-1,-1,-1)
FGC = (1,1,1)
## creating a background
win = Window(size = DISPSIZE, color = BGC, units = 'pix', fullscr = True)

## welcome text
welcome = TextStim(win,text="Hi There,\nwelcome to this wonderful experiment. In the upcoming trials you will hear a lot of beeps. In every trial you will hear an initial beep, shortly followed by a second beep. It is your task to identify whether the second beep is the same sound as the first. When you think that they are the same you press the z button, if you think they are different, you press /.",  height = 30, color = FGC, wrapWidth = 1000)
## after stimulus text
stim = TextStim(win,text="Did you hear any difference? \nPress slash if you did or z if you didn't.",  height = 30, color = FGC, wrapWidth = 1000)
correct = TextStim(win,text="correct",height=30,color=FGC,wrapWidth=1000)
false = TextStim(win,text="false",height=30,color=FGC,wrapWidth=1000)

## load difficulties/creating data frames for further storage
dat = pd.read_csv('diflist.csv',sep=',')
data = pd.DataFrame()
df = pd.DataFrame()

## updating terms for both difficulty and ability
def dif(difficulty,ability,outcome,K = .5):
    E = 1/(1+10**(ability-difficulty))
    newdif = difficulty + K*(E-outcome)
    return newdif

def ab(difficulty,ability,outcome,K = .5):
    E = 1/(1+10**(ability-difficulty))
    newab = ability + K*(outcome-E)
    return newab

## starting ability
ability = .5
## amount of trials
trials = 20

## initiate welcome text
welcome.draw()
win.flip()
waitKeys()
win.flip()
wait(2)

## open log for participant data storage
log = open(str(pp) + "_data.txt",'w')
log.write("pp\ttrial\tid\toutcome\tdif\tinterim_ability\n")

for j in range(trials):
    ## looking for min dif in ability
    diflist = abs(ability - dat['difficulty'])
    index = min( (diflist[diflist.index[i]],i) for i in range(len(diflist)) )
    ind = index[1]
    ## creating sounds
    snd1 = Sound(osc = 'sine', freq = dat['sound1'][dat.index[ind]], length = 500)
    snd2 = Sound(osc = 'sine', freq = dat['sound2'][dat.index[ind]], length = 500)
    win.flip()
    snd1.play()
    wait(1)
    snd2.play()
    ## indicating answer possibilities
    stim.draw()
    win.flip()
    keys = waitKeys(keyList = ['q','z','slash'])
    press = keys[0]
    ## if the same and z then correct, else false. If not the same and z, correct etc.
    if press == 'q':
        break 
    elif dat['sound1'][dat.index[ind]] == dat['sound2'][dat.index[ind]]:
        if press == 'z':
            outcome = 1
            correct.draw()
            win.flip()
        elif press == 'slash':
            outcome = 0
            false.draw()
            win.flip()
    else:
        if press == 'z':
            outcome = 0
            false.draw()
            win.flip()
        elif press == 'slash':
            outcome = 1
            correct.draw()
            win.flip()
    ## calculating new abilities/difficulties and logging participant data
    ability1 = ab(difficulty = dat['difficulty'][dat.index[ind]],ability = ability,outcome = outcome)
    logid = dat['id'][dat.index[ind]]
    logdif = dat['difficulty'][dat.index[ind]]
    log.write(str(pp) + '\t' + str(j) + '\t' + str(logid) + '\t' + str(outcome) + "\t" + str(logdif) + "\t" + str(ability1) + "\n")
    dat['difficulty'][dat.index[ind]] = dif(difficulty = dat['difficulty'][dat.index[ind]],ability = ability,outcome = outcome)
    ability = ability1
    ## clear buttonpress history
    clearEvents(eventType='keyboard')
    ## storing items in new dataframe and dropping them from old so they are not reused
    data = data.append(dat.loc[dat.index[ind]])
    dat = dat.drop(dat.index[ind])
    wait(.5)

## contatinating dataframes, writing to file, showing ability. The End
df = dat.append(data)
df.to_csv('diflist.csv', sep=',', index=False)
log.close()
abtext = TextStim(win,text = "Your overall ability for this task was:" + str(round(ability,2)) + "\nThank you for playing.",  height = 30, color = FGC, wrapWidth = 1000)
abtext.draw()
win.flip()
waitKeys()
win.close()

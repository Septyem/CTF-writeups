def fail(memes, calcium):
    dank=True
    if calcium<memes:
        if memes%calcium==0:
            dank=False
        else:
            dank=fail(memes,calcium+1)
    return dank
            
def epicfail(memes):
    wow=0
    dank=True
    if memes>1:
        dank=fail(memes,2)
        if dank:
            wew=bill(memes-1)
            wow=wew+1
        else:
            wew=such(memes-1)
            wow=wew
    return wow

def dootdoot(memes,seals):
    doritos=0
    if seals<=memes:
        if seals==0:
            doritos=1
        else:
            if seals==memes:
                doritos=1
            else:
                wew=dootdoot(memes-1,seals-1)
                doritos=wew
                wew=dootdoot(memes-1,seals)
                doritos+=wew
    return doritos

def such(memes):
    wew=dootdoot(memes,5)
    wow=wew
    if wow%7==0:
        wew=bill(memes-1)
        wow=wow+1
    else:
        wew=epicfail(memes-1)
    wow=wow+wew
    return wow

def brotherman(memes):
    hues=0
    if memes!=0:
        if memes<3:
            hues=1
        else:
            wew=brotherman(memes-1)
            hues=wew
            wew=brotherman(memes-2)
            hues+=wew
    hues=hues%987654321
    return hues

def bill(memes):
    wew=brotherman(memes)
    wow=wew
    if wow%3==0:
        wew=such(memes-1)
        wow=wow+1
    else:
        wew=epicfail(memes-1)
    wow=wew+wow
    return wow

#memes=13379447
#wew=epicfail(memes)
#print wew

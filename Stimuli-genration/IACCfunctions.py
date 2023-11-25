import slab

def generateStimuli ():

    monaural = slab.Sound.whitenoise()
    left = slab.Sound.whitenoise()
    right = slab.Sound.whitenoise()
    binaural = slab.Binaural([left,right])

    return monaural,binaural


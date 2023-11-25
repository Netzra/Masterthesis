# ----------------------------------------
# imports
# ----------------------------------------
import slab
import IACCfunctions as func

"""
Notes

- writing a program, that simulates different IACCs 
- Usage of slab.binaural -> allows playing two different sounds at the two ears

"""

if __name__ == "__main__":
# (reads variables from settings file)

# generate stimuli and possibly apply filter on the same time
    monaural, binaural = func.generateStimuli()
    monaural.play()
    binaural.play()

# apply filter
# Mix diotic and dichotic noise


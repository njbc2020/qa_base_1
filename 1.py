from PreParation import PreParation
import numpy as np
import pandas as pd
import pickle

_preparation = PreParation()

def ChangeNumber(txt):
    if txt.isnumeric():
        return "NUM" + str(len(txt))
    else:
        return txt

txtClean1 = _preparation.cleanText('متولد ۶۸ است')
txtClean2 = _preparation.cleanText2(txtClean1)

txt = 'متولد ۶۸'
txt = "1_شوهرم"
txt = "ﻫﻤﺴﺮﺗﻮﻣﻴﺪﻭﻧﻲ"
txt1 = txt.split()
txtClean12 = ' '.join(ChangeNumber(t) for t in txt1)

txtClean21 = _preparation.cleanText('متولد ۶۸')
txtClean22 = _preparation.cleanText2(txtClean21)


aa=55
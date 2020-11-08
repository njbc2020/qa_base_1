from PreParation import PreParation
import numpy as np
import pickle

_preparation = PreParation()

txtClean1 = _preparation.cleanText('متولد ۶۸ است')
txtClean2 = _preparation.cleanText2(txtClean1)

txtClean11 = _preparation.cleanText('متولد ۶۸')
txtClean12 = _preparation.cleanText2(txtClean11)

txtClean21 = _preparation.cleanText('متولد ۶۸')
txtClean22 = _preparation.cleanText2(txtClean21)


aa=55
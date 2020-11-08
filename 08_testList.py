
#%%
# Google Search: csv to dictionary python pandas 
# و از این جا پیچوندم
# آخرین جواب
# https://stackoverflow.com/questions/23057219/how-to-convert-csv-to-dictionary-using-pandas

import pandas as pd

thisdict1 = pd.read_csv("data/vocabDict.csv", index_col=0, header=None, squeeze=True).to_dict()

def clean3(texts):
    _texts=[]
    for _text in texts.split():
        if _text in thisdict1:
            _texts.append(thisdict1[_text])
        else:
            _texts.append(_text)
    return ' '.join(_texts)

text = "اگرمیشد امانمیشود چهکنم"
print(text)
text= clean3(text)

print(text)

# %%

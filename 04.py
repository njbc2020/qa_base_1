# %%% ----
import re
txts = ["salam", "salam123", "123Salam", "سلام123", "123سلام"]
persianmix = re.compile("(([\u0600-\u06FF]+)([0-9]+)|([0-9]+)([\u0600-\u06FF]+)|([a-zA-Z]+)([0-9]+)|([0-9]+)([a-zA-Z]+))")
num = re.compile('\d')

def splitnumber(txt):
    if num.search(txt) != None:
        res = persianmix.match(txt).groups()
        print (" ".join([word for word in res[1:] if word != None]))
    return txt

for txt in txts:
    splitnumber(txt)

# %%

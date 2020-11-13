import hazm.Normalizer as HazmNormal
import hazm.WordTokenizer as HazmTokenizer
import re
import pandas as pd
from parsivar import Tokenizer, FindStems, Normalizer
from gensim.models import Word2Vec
import emoji


class PreParation():
    _tokenizer = Tokenizer()
    sw = None  # Stop Words
    correction = None  # Correction Collection ازتمیخوام -> ازت میخوام
    _normalizer = None  # Normilizer ي --> ی
    _normalizer1 = None  # Normilizer
    _tokenizer1 = None  # Hazm Tokenizer
    _tokenizer2 = None  # Hazm Tokenizer
    _stemmer = None  # Stemmer گفت --> گو

    extraChar1 = ["؛", "؟", ",", ";", "!", "?", ".", ":", "،"]
    extraChar2 = ["'", '"', "+", "{", "}", "-", "(", ")", "$", "#", '/', "\\", "@", "*", "٪", "÷",
                  "¿", "[", "]", "«", "»", "^", "`", "|", "¡", "˘", "¤", "£", "<", ">", "¯", "°", "٭", "٫"]
    _emojiList = None

    # Regular Experssion
    persianmixRE = None
    numRE = None
    removeIrritateRE = None
    emojiRE = None

    # Embedding
    w2vModel = None

    # این کلاس برای مقدار دهی اولیه مورد استفاده قرار میگیرد
    def __init__(self):
        self.sw = pd.read_csv("data/stop_words/stpwrd.csv")
        # از فایل مربوطه ستون واژه های ایست را انتخاب میکنیم و به صورت لیست رشته ای باز میگردانیم
        self.sw = self.sw["StopWord"].astype(str).values.tolist()

        self.correction = pd.read_csv(
            "data/Vocab_dataset_1.csv", index_col=0, header=None, squeeze=True).to_dict()

        self._normalizer = Normalizer(
            statistical_space_correction=True, date_normalizing_needed=True)
        self._normalizer1 = HazmNormal()
        self._tokenizer1 = HazmTokenizer(
            join_verb_parts=False, replace_hashtags=True, replace_numbers=True, separate_emoji=True)
        self._tokenizer2 = HazmTokenizer(
            join_verb_parts=False, replace_hashtags=True, replace_numbers=False, separate_emoji=True)
        self._stemmer = FindStems()

        # region Regular Experssion
        # عبارتی که کلمات و اعداد به هم چسبیده را از هم جدا میکند
        self.persianmixRE = re.compile(
            "(([\u0600-\u06FF]+)([0-9]+)|([0-9]+)([\u0600-\u06FF]+)|([a-zA-Z]+)([0-9]+)|([0-9]+)([a-zA-Z]+))")
        # برای اینکه متوجه شویم در متن عدد وجود دارد از این عبارت استفاده میکنیم
        self.numRE = re.compile('\d')
        self.removeIrritateRE = re.compile(r'(.)\1{2,}', re.IGNORECASE)
        # Emoji
        self.emojiRE = re.compile(pattern="["
                                  u"\U0001F600-\U0001F64F"  # emoticons
                                  u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                  u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                  u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                  "]+", flags=re.UNICODE)
        # endregion
        self._emojiList = list(emoji.UNICODE_EMOJI.keys())
        #self.w2vModel = Word2Vec.load('P:/pkl/newSentence.bin')

        print("\n ** Persian Text PreParation by Naghme Jamali ** \n")

    # Remove Multiple Space - "Salam   khobi?" -> "Salam Khobi?"
    def RemoveMultipleSpace(self, txt):
        return re.sub(' +', ' ', txt)

    # Remove Emoji
    def RemoveEmoji(self, txt):
        for emoji in self._emojiList:
            txt = txt.replace(emoji, ' EMOJI ')
        return txt
        # return self.RemoveMultipleSpace(self.emojiRE.sub(r' ', txt))

    def RemoveExtraChar1(self, txt):
        for i in self.extraChar1:
            txt = txt.replace(i, " ")
        return txt

    def RemoveExtraChar2(self, txt):
        for i in self.extraChar2:
            txt = txt.replace(i, " ")
        return txt

    # تبدیل شماره ها به انگلیسی
    def NumberEN(self, input):
        return input.replace("۰", "0").replace("۱", "1").replace("۲", "2").replace("۳", "3").replace("۴", "4").replace("۵", "5").replace("٥", "5").replace("۶", "6").replace("v", "7").replace("۷", "7").replace("۸", "8").replace("۹", "9")

    # حذف ایست واژه در زبان فارسی
    def stop_word(self, data):
        text = self.RemoveMultipleSpace(data)
        text = self.RemoveMultipleSpace(
            ' '.join([word for word in data.split() if word not in self.sw]))
        return text.strip()
        # if text != " " and text != "":
        #     return ' '.join([word for word in text.split() if word not in self.sw]).strip()
        # else:
        #     return ''

    # جداسازی اعداد و متن از یکدیگر
    def splitnumber(self, txt):
        if self.numRE.search(txt) != None:
            res = self.persianmixRE.match(txt).groups()
            return (" ".join([word for word in res[1:] if word != None]))
        return txt

    # ریشه کلمات را باز میگرداند
    # در صورتی که چند ریشه داشته باشد ما اولی را برمیداریم
    # در صورتی که در این ابزار ریشه برای کلمه پیدا نشد
    # همان کلمه را باز میگرداند
    def Stem(self, txt):
        _txt = self._stemmer.convert_to_stem(txt).split('&')
        return _txt[0]

    # حروف تکراری موجود در متن را حذف مینماید
    # برای مثال خوووووبی میشود خوبی
    def removeIrritate(self, txt):
        return self.removeIrritateRE.sub(r'\1', txt)

    def CorrectionText(self, texts):
        _texts = []
        for _text in self.wordToken(texts):
            if _text in self.correction:
                _texts.append(self.correction[_text])
            else:
                _texts.append(_text)
        return ' '.join(_texts)

    # تمیز کردن متون:
    # نرمال سازی داده ها
    # حذف حروف و نشانه های اضافه
    # در ورود یک فلگ میزاریم برای مواقعی که میخواهیم از حذف ایست واژه ها استفاده کنیم
    def cleanText(self, txt, stopword=False, isSplitNumber=True):
        #txt = txt.replace("\u200c", " ")
        txt = txt.replace("آ", "ا")
        if stopword:  # آیا ایست واژه حذف شوند؟
            txt = self.stop_word(txt)

        txt = self.removeIrritate(txt)  # حذف کاراکترهای تکراری
        txt = self.RemoveEmoji(txt)
        txt = self._normalizer1.normalize(txt)

        txt = self.RemoveExtraChar2(txt)
        txt = self.RemoveMultipleSpace(txt)
        txt = self.NumberEN(txt)

        txt1 = []
        for t in self.wordToken(txt):
            if isSplitNumber:
                try:
                    t = self.splitnumber(t)  # جداسازی اعداد از متن در یک کلمه
                except:
                    pass
            for _t in t.split():
                w1 = self.Stem(_t)
                txt1.append(w1)
        if stopword:
            return self.stop_word(' '.join(txt1)).strip()
        return (' '.join(txt1)).strip()

    # مرحله دوم از حذف علائم و نشانه ها
    # و چرا این همه جایگزینی کلمات و نشانه ها، بدلیل اینکه
    # کتابخانه های موجود عکس العملی به این علامت و نگارش های غلط
    # نشان نمیدهد و برای اینکه بتوان آن ها را تصحیح کرد از روش استفاده میکنیم
    # تا کلمات تصحیح شوند و به شکل درست خود بازگردند
    def cleanText2(self, txt, stopword=False, isTokenize=False):
        _txt = txt
        if stopword:
            _txt = self.stop_word(txt)

        # در این خط، نیم فاصله ای که ابزارهای پارسی وار و هضم ایجاد کرده اند را به فاصله تبدیل میکنیم
        #_txt = _txt.replace("\u200c", " ")
        _txt = ' '.join(self.wordToken(_txt, replaceNumber=True))
        _txt = self.CorrectionText(_txt)

        _txt = self._normalizer1.normalize(_txt)
        _txt = self.NumberEN(_txt)
        if stopword:
            _txt = self.stop_word(_txt).strip()
        return _txt

    # توکنایز در سطح جمله
    def token(self, txt):
        _sents = self._tokenizer.tokenize_sentences(txt)
        sents = []
        for _txt in _sents:
            _txt = self.RemoveExtraChar1(_txt)
            _txt = self.RemoveMultipleSpace(_txt).strip()
            sents.append(_txt)
        return sents

    # جایگزینی اعداد      Exmaple: 5 عدد  --> NUM1 عدد
    # هضم نمیتواند بعضی از اعداد را تشحیص دهد
    # برای همین این تابع را نوشتیم تا آن را پوشش دهد
    def ReplaceNumber(self, input1):
        if input1.isnumeric():
            return "NUM" + str(len(input1))
        else:
            return input1

    def wordToken(self, txt, replaceNumber=False, removeExtra=False, stopword=False):
        if removeExtra:
            txt = self.RemoveExtraChar1(txt)
        txt = self.RemoveMultipleSpace(txt).strip()

        _words = []
        if replaceNumber:
            _words.extend(self.ReplaceNumber(x)
                          for x in self._tokenizer1.tokenize(txt))
        else:
            _words.extend(self._tokenizer2.tokenize(txt))

        if stopword:
            return [word for word in _words if word not in self.sw]
        else:
            return _words

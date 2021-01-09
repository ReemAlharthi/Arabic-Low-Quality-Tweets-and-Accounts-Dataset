import pandas as pd
import re
# coding=utf-8
import re
import string
import pandas as pd
import csv
arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
english_punctuations = string.punctuation

punctuations_list = arabic_punctuations + english_punctuations

arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
EN = r'[A-Za-z0-9_]+'
AN = r'[A-Za-z0-9٠-٩_]+'
Non_Ar_char='[ĦèđóÕŐчεуфĸĹǪɪíжçбšђрҭкĎŃоĄйτпˇפмвдєσİéαнĔξմыиѵĤƒьЖΩСêğşωсаÑĨǹìνòıðבеםCmuno]'
pat1 = r'@[A-Za-z0-9_]+'
pat2 = r'https?://[^ ]+'
S_part=r'[RT-_-💕-🤓-🤔-🤣-۩-•-🤷‍-⤵️-🦋_]+'
#combined_pat = r'|'.join((pat1, pat2))
www_pat = r'www.[^ ]+'
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"(\U00002600-\U000027BF)"
        u"(\U0001f300-\U0001f64F)"
        u"(\U0001f680-\U0001f6FF)"
        u"(\U00002702-\U000027B0)"
        u"(\U000024C2-\U0001F251)"
                           "]+", flags=re.UNICODE)

def normalize_arabic(text):
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ة", "ه", text)
    text = re.sub('\n',' ', text)
    text=re.sub(EN,'', text)
    text = re.sub(AN,'', text)
    return text


def remove_diacritics(text):
    text = re.sub(arabic_diacritics,'', text)
    text=re.sub(emoji_pattern,'',text)
    return text


def remove_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)


def remove_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)

def tweet_cleaner(text):
    stripped = re.sub(pat1, '',text)
    stripped = re.sub(pat2, 'رابط', stripped)
    stripped = re.sub(www_pat, 'رابط', stripped)
    stripped = re.sub(S_part, ' ', stripped)
    stripped = re.sub(Non_Ar_char, ' ', stripped)
    return (stripped)

if __name__ == '__main__':
    File = 'file.txt'
    with open(File, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        csvFile = open('Clean_tweets.csv', 'w', newline='', encoding='utf-8')
        f2 = csv.writer(csvFile, delimiter='\n')
        for row in csv_reader:
            row = row[0]
            # print("the text before ")
            # print (row)
            text = tweet_cleaner(row)
            text = remove_punctuations(text)
            text = remove_diacritics(text)
            text = normalize_arabic(text)
            text = re.sub(r'\W', ' ', text, flags=re.UNICODE)
            # print("the text after ")
            # print(text)
            # print("_____________________________________________")
            f2.writerow([text])


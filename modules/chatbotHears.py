from nltk import word_tokenize,pos_tag
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer,PorterStemmer

sia = SentimentIntensityAnalyzer()
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
def lemmatization(word,ui):
    if len(word.split("_"))==1:
        theLementation=lemmatizer.lemmatize(word)
        if theLementation!= []:
            ui.rememberOneTime("Lemmatize the \""+word+"\" to \""+theLementation+"\"\n")
            return theLementation.title() 
    else:
        splitted=word.split("_")
        txt=""
        for tmp in splitted:
            theLementation=lemmatizer.lemmatize(tmp)
            if theLementation!= []:
                if txt=="":
                    txt=theLementation.title()
                else:
                    txt=txt+"_"+theLementation.title()
                ui.rememberOneTime("Lemmatize the \""+tmp+"\" to \""+theLementation+"\"\n")
            else:
                if txt=="":
                    txt=tmp.title()
                else:
                    txt=txt+"_"+tmp.title()    
        return txt
    return word.title()

def WhatOntologyToAnswer(answer,ui):
    # tokenize and take tags of the words
    tokens=word_tokenize(answer.lower())
    tagged=pos_tag(tokens)
    # define
    nouns={}
    relationships={}
    flagPOS=False
    previous=None
    theWord=""
    relation=""
    for word in tagged:

        # be sure that the VBN is correct tag due to some errors
        if 'VBN' == word[1]:
            word = pos_tag([word[0]])[0]

        # if the word is adj just add it to the word 
        if 'JJ' == word[1] or 'JJR' == word[1] or 'JJS' == word[1]:
            if theWord!="":
                theWord = theWord+word[0].title()
            else:
                theWord = word[0]
        
        # if the the word is noun
        elif 'NN' == word[1] or 'NNS' == word[1] or 'NNP' == word[1] or 'NNPS' == word[1]:

            # Singularize or lemmatize the word to be singular
            x=lemmatization(word[0],ui)
            word=(x,word[1])

            # add it to the word
            if theWord!="":
                theWord = theWord+word[0].title()
            else:
                theWord = word[0]

            # add the word with possessive argument if need be
            if flagPOS==False:
                nouns[theWord]=None
            else:
                nouns[theWord]=previous

            # if a relation needs this word add it
            if relation!="":
                if previous!=None:
                    theRelation=relation
                    relationships[theRelation]=[previous,theWord]

            # re-initialize
            previous=theWord
            theWord=""
            relation=""

        # create a relation
        elif 'IN' == word[1] or 'TO'==word[1]:
            # check if there is a verb for TO
            if relation!="":
                relation = relation+word[0].title()
            else:
                relation = word[0]

        elif 'VB' == word[1] or 'VBG' == word[1] or\
             'VBP' == word[1] or 'VBD' == word[1] or\
             'VBZ' == word[1] or 'VBN' == word[1] :
            if relation!="":
                relation = relation+word[0].title()
            else:
                relation = word[0]
            
        if 'POS' in word[1]:
            flagPOS=True
        else :
            flagPOS=False

    return (nouns,relationships)

def GetTrueOrFalse(answer):
    polarity=sia.polarity_scores(answer.lower())
    if polarity['neg']<polarity['pos']:
        return 1
    elif polarity['neg']>polarity['pos']:
        return -1
    else:
        return 0

def GetDefinition(answer):
    return answer

def thePath(answer):
    # check if the answer is found
    tokens=answer.split()
    for token in tokens:
        # we want either to begin with file:// or http://
        if "file://" == token[0:7]:
            return token
        elif "http://" == token[0:7]:
            return token
    return None

def GetNouns(answer,ui):
    # tokenize and take tags of the words
    tokens=word_tokenize(answer.lower())
    tagged=pos_tag(tokens)

    # define
    nouns=[]
    theWord=""
    flagLem=False
    
    for word in tagged:

        # if the word is adj just add it to the word 
        if 'JJ' == word[1] or 'JJR' == word[1] or 'JJS' == word[1]:
            if theWord!="":
                theWord = theWord+word[0].title()
            else:
                theWord = word[0]
        
        # if the the word is noun
        elif 'NNS' == word[1] or 'NN' == word[1] or 'NNS' == word[1] or 'NNP' == word[1] or 'NNPS' == word[1]:
            
            # Singularize or lemmatize the word to be singular
            x,flagLem=lemmatization(word[0],ui)
            word=(x,word[1])
                
            # add it to the word
            if theWord!="":
                theWord = theWord+word[0].title()
            else:
                theWord = word[0]

            nouns.append(theWord)
            theWord=""

    if flagLem==True:
        ui.rememberOneTime("\n")

    return nouns

def FindNounsInDataBase(answer,ui):
    insideDataBase=[]
    notInside=[]

    tokens = word_tokenize(answer.lower())
    tagged=pos_tag(tokens)
    
    keys=ui.data[0].keys()

    keep=""
    for i in range(len(tagged)):
        word=tagged[i]
        if word[0]=="None":
            continue
        for key in keys:
            if keep.lower()+word[0].lower() == key.lower():
                if ui!=None:
                    ui.rememberOneTime("In the ontology I found the \""+key+"\"\n")
                if keep!="":
                    insideDataBase.append(keep+word[0].title())
                else:
                    returnValue=lemmatization(key,ui)
                    insideDataBase.append(returnValue)
                keep=""
                break
        else:
            # To Do Fix
            # if i+1<=len(tagged) and tagged[i+1]==(":",":"):
            #     keep=word[0]+":"
            if 'NN' == word[1] or 'NNS' == word[1] or 'NNP' == word[1] or 'NNPS' == word[1]:
                returnValue=lemmatization(word[0],ui)
                notInside.append(returnValue)
    return (insideDataBase,notInside)
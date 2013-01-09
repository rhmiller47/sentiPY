from preprocess import *
from evaluate import *
from check import *
import time

def loadSENTI(path):
    fo = open(path)
    global sentiDICT
    for line in fo:
        line =line.strip()
        if line:
            li= line.split()
            if len(li)==2:
                try:
                    sentiDICT[li[0]]= float(li[1])
                except:
                    print "type error, not number",line
    print "Length of sentiment lexion in %s is %s " %(fo.name,len(sentiDICT))
    
oov= set()
def calPHRASEstrength(phrase,advDICT):
    if not phrase:
        return 0
    li = phrase.split()
    if len(li) ==1:
        strength= sentiDICT.get(li[0])
        if strength is None:
            oov.add(li[0]);strength = 0
    elif len(li)==2:
        strength = sentiDICT.get(li[1])
        if strength is None:
            oov.add(li[1])
            strength = 0
        if advDICT.get(li[0]):
            strength*= advDICT.get(li[0])
        elif li[0]=="不太" and strength:
            strength = strength - 5 if strength>0 else strength + 5 

    elif len(li)==3:  
        strength= sentiDICT.get(li[2])
        if strength is None:
            oov.add(li[2])
            strength = 0
        if advDICT.get(li[1]):
            strength*=advDICT.get(li[1])
        ## DO SHIFT(4)
        if li[0] in ['shift','没','没有']:
            if strength>0:
                strength-=4
            elif strength<0:
                strength+=4
        else:
            if advDICT.get(li[0]):
                strength*= advDICT.get(li[0])
    
    else:
        length = len(li)
        strength= sentiDICT.get(li[length-1])
        if strength is None:
            oov.add(li[length-1])
            strength = 0
        for i in range(length-2,-1,-1):
            if advDICT.get(li[i]):
                strength*=advDICT.get(li[i])
##    if strength < 0:
##        strength = strength*1.5
## if mine,comment two lines above
    return strength


def readFILEasDICT(path):
    dict={}
    fo = open(path)
    for line in fo:
        line=line.strip()
        if line:
            li=line.split()
            if len(li)==2:
                try:
                    dict[li[0]]=float(li[1])
                except:
                    print "type error, not number"
    print "the length of dictionary builded from file is %s" %(len(dict))
    return dict


def calALL(advDICTfilePATH,inputPATH,outputPATH):
    fo = open(inputPATH)
    fw = open(outputPATH,'w')
    advDICT = readFILEasDICT(advDICTfilePATH)
    list=[]
    for line in fo:
        line=line.strip()
        if line!='----------':
            if line =='SUM':
                list.append('s')
            else:
                list.append(str(calPHRASEstrength(line,advDICT)))
        else: 
            fw.write("|".join(list)+"\n")
            list=[]  
    fw.close()


def statistics(phraseNUMBERseqs):
    errorLIST = []
    dict ={1:0,0:0,-1:0}
    with open(phraseNUMBERseqs) as myFILE:
        for num, line in enumerate(myFILE, 1):
            line=line.strip()
            strength = findSENTIdroppoint(line)
            #strength = commonSENTI(line)
            if strength > 0:
                errorLIST.append(num)
            dict[calORIENTATION(strength)]+=1
    print dict
    print "the correct percentage is %s" %(dict[-1]/2000.0)
    return errorLIST

if __name__ == '__main__':
    print "starts",time.asctime()
    print '''
**notice : the preprocess 163 line , if segmenter is changed!
'''
    taggedFILE='./neg_tagged.txt'
    phraseFILE='./neg_phrase.txt'
    finalPHRASE='./phrase2.txt'
    phraseNUMBERseqs='./phraseINline2.txt'

##    taggedFILE='./pos_tagged.txt'
##    phraseFILE='./pos_phrase.txt'
##    finalPHRASE='./phrase.txt'
##    phraseNUMBERseqs='./phraseINline.txt'

##    preprocess("preprocess-neg.txt")
##    segANDpos("preprocess-neg.txt")

    sentiDICT = {}
    loadSENTI('./sentiment.txt')
    findPHRASE('neg_tagged.txt','neg_parsed_format.txt','neg_phrase.txt')
    filterPHRASE(phraseFILE,finalPHRASE)
    calALL('advxxx.txt',finalPHRASE,phraseNUMBERseqs)
    errorLIST  = statistics(phraseNUMBERseqs)
    showERROR('preprocess-neg.txt',errorLIST)
    recordOOV(oov)
    print 'finished',time.asctime()
    
            




                
                

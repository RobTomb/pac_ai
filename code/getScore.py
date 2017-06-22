'''
'''
import jieba.posseg as pseg
import time 
import os
import simplejson as json



def getScore(sentenceToWordsList,degreeDict):
	sentimentFile='{0}/dict/{1}'.format(os.path.dirname(os.getcwd()),'sentimentDict.txt')
	notFile='{0}/dict/{1}'.format(os.path.dirname(os.getcwd()),'not.txt')
	conjFile='{0}/dict/{1}'.format(os.path.dirname(os.getcwd()),'conjunction.txt')
	with open(sentimentFile,'r') as sentiment:
		sentimentDict=json.loads(sentiment.read())
	with open(notFile,'r') as notStr:
		notDict=notStr.read().split(' ')
	with open(conjFile,'r') as conj:
		conjDict=json.loads(conj.read())
	stopWords=[]
	conjWight=[]
	sentenceToWordsList.pop()
	wightList=[]
	for wordsList in sentenceToWordsList:
		sentimentWight=[]
		notSite=[]
		degreeWight=[]
		if(wordsList[0][0] in conjDict):
			conjWight.append([wordsList[0][0],conjDict[wordsList[0][0]]])
		for word in wordsList:
			if(word[0] in sentimentDict):
				sentimentWight.append([wordsList.index(word),word[0],sentimentDict[word[0]]])
				wordsList[wordsList.index(word)] = ''
			elif(word[0] in notDict):
				notSite.append([wordsList.index(word),word[0],-1])
				wordsList[wordsList.index(word)] = ''
			elif(word[0] in degreeDict):
				degreeWight.append([wordsList.index(word),word[0],degreeDict[word[0]]])
				wordsList[wordsList.index(word)] = ''
			else: 
				stopWords.append(word[0])
		wight=0
		for sentimentWord in sentimentWight:
			if(len(notSite) == 0):
				for degreeWord in degreeWight:
					if(sentimentWord[0]-degreeWord[0]):
						wight+=sentimentWord[2]*degreeWord[2]
			else:
				for notWords in notSite:
					if(sentimentWord[0]>notWords[0] ):
						flag=1
						for degreeWord in degreeWight:
							if(degreeWord[0]-notWords[0]<3 and degreeWord[0]-notWords[0]>0):
								wight+=degreeWord[2]*sentimentWord[2]
								flag=0
							elif(notWords[0]-degreeWord[0]<3 and notWords[0]-degreeWord[0]>0):
								flag=0
								wight+=(-1)*degreeWord[2]*sentimentWord[2]
							elif(sentimentWord[0]-degreeWord[0]<3 and sentimentWord[0]-degreeWord[0]>0):
								flag=0
								wight+=sentimentWord[2]*degreeWord[2]
								del degreeWight[degreeWight.index(degreeWord)]
						
						if(sentimentWord[0]-notWords[0]<3 and flag):
							wight+=(-1)*sentimentWord[2]

		wightList.append(wight)

	if(len(conjWight)!=0 and len(wightList)!=1):
		for x in range(len(conjWight)):
			if(conjWight[x][0] in conjDict):
				if(conjDict[conjWight[x][0]] == 0):
					wightList[x+1]+=wightList[x]+wightList[x+1]
				if(conjDict[conjWight[x][0]] == -1):
					wightList[x+1]+=wightList[x]-wightList[x+1]
			else:
				wightList[x]+=wightList[x]+wightList[x+1]
	return wightList[len(wightList)-1]
def getDataFrame(dataFile):
	with open(dataFile,'r') as data:
		paragraph=data.read()
	return paragraph

def cutParagraphToWords(paragraph):
	sentenceLists=paragraph.split('。')

	sentenceToWordsList=[]
	for sentence in sentenceLists:
		cutSentneceToWords=pseg.cut(sentence)	
		wordsCutList=[]
		for word,flag in cutSentneceToWords:
			if(word != ' ' and word != ''):
				if(flag != 'x' and flag != 'm'):
					wordsCutList.append([word,flag])
		sentenceToWordsList.append(wordsCutList)
	return sentenceToWordsList#sentenceToWordsList[[],[],[],[]````]



def getDegreeDictList(degreePath,degreeScorePath):
	with open(degreePath,'r') as degreeFile:
		degreeStr=degreeFile.read().split(' ')

	degreeDict=[[],[]]#degreeDict=[[word],[score]]
	for word in degreeStr:
		degreeDict[0].append(word.split('\n'))
	degreeDict[0]=degreeDict[0][1:]

	with open(degreeScorePath,'r') as degreeScoreFile:
		degreeScore=degreeScoreFile.read().split(' ')

	for x in range(6):
		degreeDict[1].append(float(degreeScore[x]))

	dict={}
	for wordsList in degreeDict[0]:
		for words in wordsList:
			dict[words]=degreeDict[1][degreeDict[0].index(wordsList)]

	return dict	




def main():
	degreeDictName='degreeDict.txt'
	degreeScoreName='degreeScore.txt'
	dataName='data.txt'
	degreeDict=getDegreeDictList('{0}/dict/{1}'.format(os.path.dirname(os.getcwd()),degreeDictName),
		'{0}/dict/{1}'.format(os.path.dirname(os.getcwd()),degreeScoreName))
	sentenceToWordsList=cutParagraphToWords(getDataFrame('{0}/dict/{1}'.format(os.path.dirname(os.getcwd()),dataName)))
	score=getScore(sentenceToWordsList,degreeDict)
	print(score)
if __name__ == '__main__':
	main()


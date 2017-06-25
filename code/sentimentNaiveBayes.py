import os
from jieba import posseg as pseg
import pandas as pd



def getP(word,NBDict,flag):

	if(word in NBDict):
		return NBDict[word][flag]+1
	else:	
		return 1

def classify(wordsTest,NBDict):
	p0=p1=p2=1
	for words in wordsTest:
		print(words[0])
		print(p0,p1,p2)
		p0*=getP(words[0],NBDict,0)/(NBDict['evalation'][0]+len(wordsTest))
		p1*=getP(words[0],NBDict,1)/(NBDict['evalation'][1]+len(wordsTest))
		p2*=getP(words[0],NBDict,2)/(NBDict['evalation'][2]+len(wordsTest))
	p0*=NBDict['evalation'][0]/sum(NBDict['evalation'])
	p1*=NBDict['evalation'][1]/sum(NBDict['evalation'])
	p2*=NBDict['evalation'][2]/sum(NBDict['evalation'])
	p=[p0,p1,p2]
	return p.index(max(p))




def countNum(wordsList,trainSet):
	#print(wordsList,trainSet)
	NBDict={'evalation':[0,0,0]}
	for ix in trainSet.index:
		flag = trainSet.ix[ix,'pos_se_tag']
		NBDict['evalation'][flag]+=1
		for words in wordsList[ix]:
			if(words[0] in NBDict):
				NBDict[words[0]][flag]+=1
			else:
				NBDict[words[0]] = [0,0,0]
				NBDict[words[0]][flag]=1

	#print(NBDict)
	return NBDict



def tagTrainSet(trainSet):
	trainSet['pos_se_tag'] = 0
	for ix in trainSet.index:
		if(trainSet.ix[ix,'pos_se'] == '好'):
			trainSet.ix[ix,'pos_se_tag'] = 0

		elif(trainSet.ix[ix,'pos_se'] == '中'):
			trainSet.ix[ix,'pos_se_tag'] = 1

		elif(trainSet.ix[ix,'pos_se'] == '差'):
			trainSet.ix[ix,'pos_se_tag'] = 2



def cutParagraphToWords(trainSet):
	#print('step 1 cut paragraph to words')
	stopWords=['ug','uv','i','s','k','nrt','vn','ad','o','y','e','nz','u','p','ng','x','m','c','r','ul','v','zg','t','n','uj','nr','f','d','j','l','ns','eng','q','uz','b','mq']
	exitWords=['推荐','半价','值','好评','划算','免费']
	dataSet=trainSet['content']
	wordsList=[]
	for paragraph in dataSet.values:
		paragraphToWords=pseg.cut(paragraph.split('>').pop())
		wordsCutList=[]
		for word,flag in paragraphToWords:
			if(word != ' ' and word != ''):
				if(word in exitWords or flag not in stopWords ):
					wordsCutList.append([word,flag])
		wordsList.append(wordsCutList)

	return wordsList





def main():
	dataFileName='data11.xlsx'
	dataFilePath='{0}/NaiveBayesData/{1}'.format(os.path.dirname(os.getcwd()),dataFileName)
	trainSet=pd.read_excel(dataFilePath)
	#print(trainSet)
	wordsList=cutParagraphToWords(trainSet)	
	tagTrainSet(trainSet)
	NBDict=countNum(wordsList,trainSet)
	p=classify([['差', 'a'], ['连单', 'a']],NBDict)
	print('ae: %d' % p)


if __name__ == '__main__':
	main()
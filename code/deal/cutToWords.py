import jieba.posseg as pseg

class cutToWords(object):

	def cutParagraphToWords(dataFilePath):
		print('step 1 cut paragraph to words')
		trainSet=pd.read_excel(dataFilePath)
		stopWords=['ug','uv','i','s','k','nrt','vn','ad','o','y','e','nz','u','p','ng','x','m','c','r','ul','v','zg','t','n','uj','nr','f','d','j','l','ns','eng','q','uz','b','mq']
		exitWords=['推荐','半价','值','好评','划算','免费']
		dataSet=trainSet['content']
		
		for paragraph in dataSet.values:
			paragraphToWords=pseg.cut(paragraph.split('>').pop())
			wordsCutList=[]
			for word,flag in paragraphToWords:
				if(word != ' ' and word != ''):
					if(word in exitWords or flag not in stopWords ):
						wordsCutList.append([word,flag])

	"""docstring for cutToWords"""
	def __init__(self):
		self.data=''
				
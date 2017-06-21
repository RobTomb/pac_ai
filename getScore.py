import jieba.posseg as pseg
import time 
start=time.time()
paragraph="宁馨的点评 国庆活动，用62开头的信用卡可以6.2元买一个印有银联卡标记的冰淇淋，有香草，巧克力和抹茶三种口味可选，我选的是香草口味，味道很浓郁。另外任意消费都可以10元买两个马卡龙，个头虽不是很大，但很好吃，不是很甜的那种，不会觉得腻。"
sentenceLists=paragraph.split('。')

sentenceCutList=[]

stopWords=open('stopwords.txt','r').read()
print(type(stopWords))
print(stopWords[2])
'''
for sentence in sentenceLists:
	print(sentenceCutList)
	sentenceCut=pseg.cut(sentence)	
	wordsCutList=[]
	for word,flag in sentenceCut:
		wordsCutList.append([word,flag])
	sentenceCutList.append(wordsCutList)


'''

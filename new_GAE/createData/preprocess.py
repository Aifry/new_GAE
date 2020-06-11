#删除 1.停用词  2.括号里的内容   3.标点符号

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

with open("D:/Program Files/Python/pubmed/终/abstract_del-stop.txt",'w',encoding="utf-8") as f_new:
    f = open("D:/Program Files/Python/pubmed/终/abstract.txt",'r',encoding="utf-8")
    lines = f.readlines()
    f.close()
    for i in range(len(lines)):
        print(i)
        lines[i]=re.sub("\n","",lines[i])
        lines[i]=re.sub("\\u002E"," ",lines[i]) #去除.
        lines[i]=re.sub(","," ",lines[i])
        lines[i]=re.sub(u"\\(.*?\\)","",lines[i])#去除括号及其内容

        #  停用词集合
        stop_words=set(stopwords.words('english'))

        #  分词
        word_tokens = word_tokenize(lines[i])

        filtered_sentence =[]

        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        #变成空的话
        if len(filtered_sentence)==0:
            if i>365714:
                filtered_sentence.append("abstract")
            else:
                filtered_sentence.append("keyword")

        for w in range(len(filtered_sentence)):
            f_new.write(filtered_sentence[w])
            if w!=len(filtered_sentence)-1:
                f_new.write(" ")
        f_new.write("\n")



#处理长度
#f = open("D:/数据预处理/abstract_new.txt",'r',encoding="utf-8")
# lines = f.readlines()
# f.close()
# maxlen=0;
# id=[]
# for i in range(len(lines)):
#     print(i)
#     lines[i] = lines[i].strip('\n').split(' ')
#     lenth = len(lines[i])
#     if lenth>maxlen:
#         maxlen=lenth
#     if lenth>500:
#         id.append(i)
# print(maxlen)
# print(id)
#
# # 长度处理
# f = open("D:/数据预处理/abstract_del-stop.txt",'r',encoding="utf-8")
# lines = f.readlines()
# f.close()
# maxlen=0;
# with open("D:/数据预处理/abstract_del-stop_500.txt",'w',encoding="utf-8") as f_new:
#     for i in range(len(lines)):
#         print(i)
#         lines[i] = lines[i].strip('\n').split(' ')
#         if(len(lines[i])>500):
#             lines[i] = lines[i][0:501]
#         for w in range(len(lines[i])):
#             f_new.write(lines[i][w])
#             if w!=len(lines[i])-1:
#                 f_new.write(" ")
#         f_new.write("\n")



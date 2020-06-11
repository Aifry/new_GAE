# 这个文件用于生成字典文件，摘要文件
import os
import re
import random
from bs4 import BeautifulSoup

rootpath = "D:\Downloads\pubmed10"
files = os.listdir(rootpath)       # 得到文件夹pubmed里的所有文件夹名（期刊）
dict1 = {}   # 用来存期刊字典（index1）
dict2 = {}   # 用来存论文字典（index2）
dict3 = {}   # 用来存kwd字典（index3）
index1 = 0    # index1即存入期刊的编号
index2 = 0    # index2即存入论文的编号
index3 = 0    # index3即存入kwd的编号
edge1={}    #存期刊-论文的边
edge2={}    #存论文-关键字的边
all_abstract=[]   #存摘要列表
for file in files:
    path = rootpath+'\\'+file       # 得到每个期刊的绝对路径
    files1 = os.listdir(path)       # 得到每个期刊文件夹里的文件名（论文）
    dict1[index1] = file             # 把期刊名对应index存入dict1
    index1 += 1
    edge1[index1-1]=[]
    print(file)
    for file1 in files1:
        position = path+'\\'+file1  # position就是每一篇论文的绝对路径
        f1 = open(position, "r")  # 读取一篇论文
        html = f1.read()
        f1.close()
        bs = BeautifulSoup(html, "html.parser")  # 解析成html树
        try:
            # journal_title = bs.find('journal-title').string  # 提取期刊名journal-title；
            article_title = bs.find('article-title').text  # 论文名article-title
            all_keywords = bs.find_all("kwd")  # 所有关键词kwd,列表
            abstract_content = bs.find("abstract").contents
            s=""
            for w in range(len(all_keywords)):
                all_keywords[w] = str(all_keywords[w]).lower()
                all_keywords[w] = re.sub(r'<.+?>', "", all_keywords[w])
                all_keywords[w] = re.sub("\n", " ", all_keywords[w])
                all_keywords[w] = re.sub(",", " ", all_keywords[w])
            for w in range(len(abstract_content)):
                abstract_content[w] = str(abstract_content[w]).lower()
                abstract_content[w] = re.sub(r'<.+?>', "", abstract_content[w])
                # abstract_content[w] = re.sub(r'(.+?)', "", abstract_content[w])
                abstract_content[w] = re.sub("\n", " ", abstract_content[w])
                abstract_content[w] = re.sub(",", " ", abstract_content[w])
                s += abstract_content[w]
            s=s.split(" ")
            all_abstract.append(s)
        except AttributeError:
            pass
        article_title = article_title.replace('\n', ' ') # 把论文标题里的空格变为下划线_
        dict2[index2] = article_title  # 把论文名对应index存入dict1
        edge1[index1-1].append(index2)
        index2 += 1
        edge2[index2-1]=[]
        for item in all_keywords:   # 遍历关键字，存入字典dict3（判断重复）
            flag = 0
            if len(dict3)==0:
                flag=0
            else:
                if dict3.__contains__(item):  # 判断dict3里是否已经有该关键词
                    flag = 1

            if flag == 0:
                dict3[item] = index3  # 把关键词对应index存入dict1 {word:id}
                index3 += 1

            edge2[index2-1].append(dict3[item])
print("load dada done")


f2 = open("dictionary.txt", "w", encoding="utf-8")  # 遍历字典dict1，把key（编号）、value（期刊、论文、关键词名称）输出到dictionary.txt
for key, value in dict3.items():#先写kwd
    s =  str(value)+ ' ' + str(key).strip('\n')
    f2.write(s+'\n')
for key, value in dict2.items():#写论文名
    s = str(key+index3) + ' ' + str(value).strip('\n')
    f2.write(s+'\n')
for key, value in dict1.items():#写期刊名
    s = str(key+index3+index2) + ' ' + str(value).strip('\n')
    f2.write(s+'\n')
f2.close()
print(index1)##500      50          25           10
print(index2)#263859    38793       14185        4819
print(index3)#366484    89907       35256        13766
print("write dic done")


f3 = open("graph.txt", "w", encoding="utf-8")
for key, value in edge2.items():#先写论文，关键字的边
    for i in range(len(value)):
        s = str(key + index3)
        s +=' '
        s +=str(value[i])
        f3.write(s+'\n')
for key, value in edge1.items():#写期刊，论文的边
    for i in range(len(value)):
        s = str(key + index3 + index2)
        s +=' '
        s +=str(value[i]+index3)
        f3.write(s+'\n')
f3.close()
print("write graph done")


f4 = open("abstract.txt","w",encoding="utf-8")
for key, value in dict3.items():#先写kwd
    s =  str(key)
    f4.write(s+'\n')
for i in range(len(all_abstract)):
    for j in range(len(all_abstract[i])):
        f4.write(str(all_abstract[i][j]))
        f4.write(" ")
    f4.write("\n")
f4.close()
print("write abstract done")

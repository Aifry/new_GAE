#从abstract_del-stop文件生成feature,最后补上期刊的，随机生成
import numpy as np
import gensim
# 使用谷歌训练好的300维的词嵌入矩阵（300是由经验总结的在200-500之间效果较好的）
w2v_model = gensim.models.KeyedVectors.load_word2vec_format('D:/Program Files/Python/pubmed/终/Google_word2vec_zhwiki1709_300d.bin',binary=True)# 预训练的词向量中没有出现的词用0向量表示
embedding_matrix = np.zeros((49466, 300))#630073是所有的节点数量(包括期刊），300是词向量的长度。
f=open("D:/Program Files/Python/pubmed/终/abstract_del-stop.txt",'r',encoding="utf-8")
lines=f.readlines()
for i in range(len(lines)):
    print(i)
    j=0
    lines[i] = lines[i].strip('\n').split(' ')
    for word in lines[i]:
        j=j+1
        try:
            embedding_vector = w2v_model[str(word)]
            embedding_matrix[i] += embedding_vector
        except KeyError:
            continue
    embedding_matrix[i] = embedding_matrix[i]/j
embedding_matrix[49441:]=np.random.rand(25,300)#把后面500个期刊节点的设置成随机数
print(embedding_matrix.shape)
np.savetxt("feature_div_length.txt",embedding_matrix)




























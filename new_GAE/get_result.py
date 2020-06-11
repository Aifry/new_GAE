import numpy as np
from sklearn.metrics import confusion_matrix

def get_confusion_matrix():
    # edges_neg=np.genfromtxt("result3/edges_neg.txt",dtype=np.dtype(int))##采样为负例的边
    edges_pos = np.genfromtxt("result4/edges_pos.txt", dtype=np.dtype(int))  ##采样为正例的边
    length = edges_pos.shape[0]
    # edges_pos_sort=np.sort(edges_pos)
    # edges_pos_sort_reverse=np.sort(edges_pos_sort,axis=0)
    pre_raw = np.genfromtxt("result4/predict_result.txt", dtype=np.dtype(float))[:3005]  # 预测的lable
    lable_raw = np.genfromtxt("result4/lable_true.txt", dtype=np.dtype(int))[:3005]  # 真实标签


    # 生成混淆矩阵
    index = {}
    index[0] = 0
    predict = []
    lables = []
    for i in range(length):
        if not index.__contains__(edges_pos[i][1]):
            index[edges_pos[i][1]] = i + 1
        if pre_raw[i] >= 0.5:
            predict.append(index[edges_pos[i][1]])
        else:
            predict.append(index[0])
        if lable_raw[i] == 1:
            lables.append(index[edges_pos[i][1]])
        else:
            lables.append(index[0])

    result = confusion_matrix(lables, predict)
    np.savetxt("result4/confusion_matrix.txt", result)


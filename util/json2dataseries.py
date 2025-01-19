import pandas as pd

pairs = ['shoulder', 'elbow', 'wrist', 'hip', 'knee', 'heel']
bodyparts = ['neutral_nose'] + ['left_left_' + l for l in pairs] + ['right_right_' + r for r in pairs]
columns = []
for item in bodyparts:
    columns.append(item + '_x')
    columns.append(item + '_y')
def j2ds(dictt):
    data = [0.0 for i in range(len(columns))]
    for lrn in dictt:
        for bp in dictt[lrn]:
            if lrn+'_'+bp in bodyparts:
                index = bodyparts.index(lrn+'_'+bp)
                data[2*index] = dictt[lrn][bp]['x']
                data[2*index+1] = dictt[lrn][bp]['y']
    ds = pd.Series(data, index=columns)
    return ds

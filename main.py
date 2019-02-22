# coding: utf-8
import label_image
import showImages
import pandas as pd
import glob
import os
from tkinter import filedialog

Cor_val = [1,0.5,0.3,0.1]

model_file = "retrained_graph.pb"
label_file = "retrained_labels.txt"
input_layer = "Placeholder"
output_layer = "final_result"

# ファイル名以外の列情報を削除する
def drop_df(df):
    tmp = df.drop("label", axis = 1)
    tmp = tmp.drop("accuracy" , axis = 1)
    return tmp

# 精度を置き換える
def replace_acc(df,rank):
    if rank < 4:
        df.accuracy[df.label =="aogami"] = df.accuracy[df.label =="aogami"] + Cor_val[rank]
    return df

# 青髪が何番目か
def check_aogami_rank(df):
    tmp = df.sort_values('accuracy',ascending=False)
    return tmp.reset_index().query('label == "aogami"').index[0]

# DataFrameからlistに変換する
def TransList(df):
    l = df.values.tolist()
    x = []
    for s in l:
        x.extend(s)
    return x

# listからDataFrameに変換する
def transDF(filename,labels,results):
    df = pd.DataFrame(columns=['filename','label','accuracy'])

    for i in range(len(labels)):
        tmp = pd.DataFrame([[filename,labels[i],results[i]]], columns=['filename','label','accuracy'])
        df = df.append(tmp , ignore_index=True)
    
    return df

def main():
    
    bluehair_df = pd.DataFrame(columns=['filename','label','accuracy'])
    # フォルダ選択ダイアログを出す
    fld = filedialog.askdirectory(initialdir = os.path.dirname(os.path.abspath(__file__)))

    # 何かしらのフォルダが選ばれていれば進む
    if fld is not None:
        files = glob.glob(fld + "/*.jpg")
        files.extend(glob.glob(fld + "/*.jpeg"))
        files.extend(glob.glob(fld + "/*.png"))
        if len(files) > 0:
            for i ,filename in enumerate(files):
                labels, results, top_k = label_image.get_acc(filename,model_file,label_file,input_layer,output_layer)
                df = transDF(filename,labels,results)
                rank = check_aogami_rank(df)
        
                df = replace_acc(df,rank)
                bluehair_df = bluehair_df.append(df.query('label == "aogami"'))

            bluehair_df = bluehair_df.sort_values('accuracy',ascending=False)
            bluehair_df = drop_df(bluehair_df)
            aogami_list = TransList(bluehair_df)

            showImages.showImage(aogami_list)

if __name__ == "__main__":
    main()
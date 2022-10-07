import pandas as pd 
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler
import joblib,os
from sklearn import model_selection
from lightgbm import LGBMClassifier

def train_lgbm(args):
    
    filelist = os.listdir(args.data_path)
    
    df_a1a2 = pd.DataFrame()
    df_a3 = pd.DataFrame()
    df_a4 = pd.DataFrame()
    df_a5 = pd.DataFrame()
    df_a6 = pd.DataFrame()
    label = []
    
    for f in tqdm(filelist):
        f_a1a2 = os.path.join(args.features_path+"\\features_quant",f)
        f_a3 = os.path.join(args.features_path+"\\features_impwords",f)
        f_a4 = os.path.join(args.features_path+"\\features_wordemb",f)
        f_a5 = os.path.join(args.features_path+"\\features_pos",f)
        f_a6 = os.path.join(args.features_path+"\\features_openword",f)
        f_sent = os.path.join(args.features_path+"\\sent-pos",f)
    
    
        df_a1a2 = df_a1a2.append(pd.read_table(f_a1a2,delimiter=' ',header=None)) 
        df_a3 = df_a3.append(pd.read_table(f_a3,delimiter=' ',header=None))
        df_a4 = df_a4.append(pd.read_table(f_a4,delimiter=' ',header=None))
        df_a5 = df_a5.append(pd.read_table(f_a5,delimiter=' ',header=None))
        df_a6 = df_a6.append(pd.read_table(f_a6,delimiter=' ',header=None))
        
      
        fr2 = open(f_sent,"r")
        for sentence in fr2.readlines():
            sentence = sentence.rstrip("\n")
            ls = sentence.split("$$$")
            lab = ls[1].rstrip("\n").lstrip(" ").rstrip(" ")
            label.append(int(lab))
        fr2.close()
    
    label = pd.Series(label)
    
    df_features = pd.concat([df_a1a2,df_a3,df_a4,df_a5,df_a6],axis=1)
    sc = StandardScaler()
    df_features = sc.fit_transform(df_features)

    
    print("TRAINING STARTS")
    


    lgbm = LGBMClassifier(
    objective='binary',
    boosting='gbdt',
    learning_rate = args.lr, #0.001,
    #max_depth = 8,
    num_leaves = args.numleaves,#1043,
    n_estimators = args.n_est,#400,
    bagging_fraction = 0.8,
    feature_fraction = 0.9)
    #reg_alpha = 0.2,
    #reg_lambda = 0.4))

    mod = lgbm.fit(df_features, label)
    joblib.dump(mod,args.model_path+'summary_model.pkl')
    



    #train_data=lgb.Dataset(df_features,label=label)
    
    #param = {'num_leaves':1043, 'objective':'binary','learning_rate':0.001, 'boost_from_average':False}
    #param['metric'] = ['auc', 'binary_logloss']
    
    #training our model using light gbm
    #num_round=50
    
    #lgbm=lgb.train(param,train_data,num_round)
    #joblib.dump(lgbm,args.model_path+'summary_model.pkl')

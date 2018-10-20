 #!/Users/abhinav/Anaconda2/python
 # -*- coding: utf-8 -*-
 
"""
Created on Wed May 24 13:33:12 2017

@author: abhinav
"""
import numpy
import mysql.connector 
import json
import pandas as pd
import sys 
import matplotlib.pyplot as plt



"""
try:
    data=sys.argv[1]
except:
    print "ERROR"

print data
d=json.loads(data)
print d
print d['1']
#raw_input()

with open('Python_input.json') as json_data:
    d = json.load(json_data)
    print d
d = map(int, d)
"""
data = 2
data1 = 3
d1 = int(data)
d2 = int(data1)
#print data1
mathop = d1
Ques_Threshold = 9999999
Count_Threshold = 3
selectlvl = [d2]
n_lvl_val = 0
#Total_No_Wrongs = 50
List_Wrongs = pd.DataFrame([0])
#print selectlvl

def operator_miss(df1,df2,length):
    df1_new = pd.DataFrame([0])
    #print df1
    for lvl_basd_perf in xrange(0,len(df1.index)):
        if (df1.ix[lvl_basd_perf,"selectedLevel"] == selectlvl[0]):
            df1_new = df1_new.append(df1.ix[[lvl_basd_perf]])
    df1_new = df1_new.drop(0,0)
    df1_new = df1_new.drop(0,1).reset_index(drop=1)   
    #print "Iam printhing the new dataframe"     
    #print df1_new        
    for i in xrange(0,len(df1_new.index)):
        if(~(df1_new.ix[i,'userAnswer'] != df1_new.ix[i,'Addition_Ans']) and df1_new.ix[i,'mathOperator'] != 1):
            df2.ix[i,'Match_Case'] = 1
            df2.ix[i,'questionPair_left'] = df1_new.ix[i,'questionPair_left']
            df2.ix[i,'questionPair_right'] = df1_new.ix[i,'questionPair_right']
        elif(~(df1_new.ix[i,'userAnswer'] != df1_new.ix[i,'Substraction_Ans']) and df1_new.ix[i,'mathOperator'] != 2):
            df2.ix[i,'Match_Case'] = 2
            df2.ix[i,'questionPair_left'] = df1_new.ix[i,'questionPair_left']
            df2.ix[i,'questionPair_right'] = df1_new.ix[i,'questionPair_right']
        elif(~(df1_new.ix[i,'userAnswer'] != df1_new.ix[i,'Multiplication_Ans']) and df1_new.ix[i,'mathOperator'] != 3):
            df2.ix[i,'Match_Case'] = 3 
            df2.ix[i,'questionPair_left'] = df1_new.ix[i,'questionPair_left']
            df2.ix[i,'questionPair_right'] = df1_new.ix[i,'questionPair_right']
        elif(~(df1_new.ix[i,'userAnswer'] != df1_new.ix[i,'Division_Ans']) and df1_new.ix[i,'mathOperator'] != 4): 
            df2.ix[i,'Match_Case'] = 4 
            df2.ix[i,'questionPair_left'] = df1_new.ix[i,'questionPair_left']
            df2.ix[i,'questionPair_right'] = df1_new.ix[i,'questionPair_right']
        else:
            df2.ix[i,'Match_Case'] = 0
    
    df2 = df2.drop(0, 1)
    #print df2
    return  df2  

def missentry(df_train,unintentional_df):
    #unintentional_df = pd.DataFrame(['Match_Case'])
    
    for j in xrange(0,len(df_train.index)):

        if ((df_train.ix[j,'userAnswer'] == 99779977 or df_train.ix[j,'userAnswer'] == 99889988) or df_train.ix[j,'questionDurationinS'] <= 1.000):
            unintentional_df.ix[j,'Match_Case'] = 1
            unintentional_df.ix[j,'questionPair_left'] = df_train.ix[j,'questionPair_left']
            unintentional_df.ix[j,'questionPair_right'] = df_train.ix[j,'questionPair_right']
            unintentional_df.ix[j,'mathOperator'] = df_train.ix[j,'mathOperator']
            unintentional_df.ix[j,'questionDurationinS'] = df_train.ix[j,'questionDurationinS']
            unintentional_df.ix[j,'userAnswer'] = df_train.ix[j,'userAnswer']
        else:
            unintentional_df.ix[j,'Match_Case'] = 0
    
    unintentional_df = unintentional_df.drop(0,1)        
    return unintentional_df

def weights(Total_Wrongs,Total_Wrong_Count,weight_result_df):
    
    #print Total_Wrong_Count
    #print Total_Wrongs
    for wrg_val in xrange(0,len(Total_Wrongs.index)):
        for x in xrange(0,len(Total_Wrong_Count.index)):
            if(Total_Wrongs.ix[wrg_val,"level"] == Total_Wrong_Count.ix[x,"selectedLevel"]):
                weight_result_df.ix[x,'Questions'] = Total_Wrong_Count.ix[x,'Questions']
                weight_result_df.ix[x,'weights(%)']  = (Total_Wrong_Count.ix[x,'Total_Frequency']/Total_Wrongs.ix[wrg_val,"Wrongs"])*100
                weight_result_df.ix[x,'Total_Frequency'] = Total_Wrong_Count.ix[x,"Total_Frequency"]
                weight_result_df.ix[x,'Total_No_Wrongs'] = Total_Wrongs.ix[wrg_val,"Wrongs"]
                weight_result_df.ix[x,'SelectedLevel'] = Total_Wrongs.ix[wrg_val,"level"]
                
    weight_result_df = weight_result_df.drop(0,1)  
    #print weight_result_df
    return weight_result_df

def count_questions_fun(my_list_2,extended_my_list,selectlvl,List_Wrongs):
    #print my_list_2
    for row in xrange(0,len(my_list_2)):
        if ((my_list_2.ix[row,'mathOperator']) == mathop):
            extended_my_list = (extended_my_list.append(my_list_2.ix[[row]],ignore_index=True))
    #print extended_my_list
    extended_my_list =extended_my_list.drop(0,1)
    extended_my_list =extended_my_list.drop(0,0).reset_index(drop=1)
    extended_my_list['questionPair_left'], extended_my_list['questionPair_right'] = zip(*extended_my_list['questionPair'].map(lambda x: x.split(',')))
    extended_my_list =extended_my_list.drop('questionPair',axis=1)
    extended_my_list[['questionPair_left', 'questionPair_right']] = extended_my_list[['questionPair_left', 'questionPair_right']].astype(int)
    extended_my_list = extended_my_list.apply(pd.to_numeric)
    temp1 = 0
    #print temp1
    for lvl_val in range(len(selectlvl)):
        final_extended_my_list = pd.DataFrame([0])
        for new_row in xrange(0,len(extended_my_list)):  
            if ((extended_my_list.ix[new_row,'selectedLevel']) == selectlvl[lvl_val]):
                final_extended_my_list = (final_extended_my_list.append(extended_my_list.ix[[new_row]],ignore_index=True))
        #print final_extended_my_list
        final_extended_my_list =final_extended_my_list.drop(0,0).reset_index(drop=1)
        #print final_extended_my_list
        Total_Wrongs = len(final_extended_my_list)
        List_Wrongs.ix[temp1,'level'] = selectlvl[lvl_val]
        List_Wrongs.ix[temp1,'Wrongs'] = Total_Wrongs
        temp1= temp1 + 1
        final_extended_my_list =final_extended_my_list.drop(final_extended_my_list.index,inplace=True)
    
    #final_extended_my_list = final_extended_my_list.drop(0,1)
    #print final_extended_my_list
    #List_Wrongs =List_Wrongs.drop(0,0).reset_index(drop=1)
    List_Wrongs = List_Wrongs.drop(0,1)
    #print List_Wrongs
    return List_Wrongs

def add_sub_analysis_lvl_4(lvl_data_df):
    
    #print  lvl_data_df
    new_final_extended_my_list = pd.DataFrame([0])
    new_df_1 = pd.DataFrame()
    new_df_2 = pd.DataFrame([0])
    new_count_1 = pd.DataFrame()
    new_count_2 = pd.DataFrame()
    new_count_1_df2 = pd.DataFrame()
    new_count_1_df2 = pd.DataFrame()
    #print lvl_data_df
    #print temp_updated_df_train
    for row in xrange(0,len(lvl_data_df)):
        if((lvl_data_df.ix[row,"questionPair_right"]) <=9  and (lvl_data_df.ix[row,"selectedLevel"]) == 4 and selectlvl[0] == 4):    
           new_final_extended_my_list = (new_final_extended_my_list.append(lvl_data_df.ix[[row]],ignore_index=True))
        elif((lvl_data_df.ix[row,"selectedLevel"])==4 and selectlvl[0] == 4):
           new_df_2 = new_df_2.append(lvl_data_df.ix[[row]],ignore_index=True) 
        else:
            break
    new_final_extended_my_list =new_final_extended_my_list.drop(0,1)
    new_final_extended_my_list =new_final_extended_my_list.drop(0,0).reset_index(drop=1) 
    new_df_2 =new_df_2.drop(0,1)
    new_df_2 =new_df_2.drop(0,0).reset_index(drop=1) 
    
    """    
    The questions of type where left_question>9 and right_question>9 are analysed and
    the frequecies are calculated in the below code.
    """
    
    if (len(new_final_extended_my_list.index) != 0):

        new_df_1 = new_final_extended_my_list.copy()
        #print new_df_1
        new_df_1 = new_df_1[[4,5,6,7]]
        #print "This is df1"
        #print new_df_1
        new_temp_count = new_df_1.groupby(['selectedLevel','mathOperator','questionPair_left','questionPair_right']).size().to_frame('size').reset_index()  
        new_count_1 = new_df_1.groupby(['selectedLevel','mathOperator','questionPair_left']).size().to_frame('size').reset_index()
        new_count_2 = new_df_1.groupby(['selectedLevel','mathOperator','questionPair_right']).size().to_frame('size').reset_index()
        #summ_new_count = pd.concat([new_count_1,new_count_2], axis=1).reset_index().apply(pd.to_numeric)
        new_count_1 = new_count_1[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        new_count_2 = new_count_2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        new_count_1 = new_count_1.rename(columns={'questionPair_left': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})
        new_count_2 = new_count_2.rename(columns={'questionPair_right': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})    
        #print new_count_1
        #print new_count_2
        #print new_temp_count
        #new_final_extended_my_list = new_final_extended_my_list.groupby(['selectedLevel','questionPair_left','questionPair_right','mathOperator']).size().reset_index()
        #new_val_22 = ((count_val/len(lvl_data_df.index))*100)
        #new_df_2 =new_df_2.drop(0,1)
        #new_df_2 =new_df_2.drop(0,0).reset_index(drop=1)
        
    """
    Analysing the second dataframe questions saved in new_df_2
    """
    
    if (len(new_df_2.index) != 0):
        
        new_df_2 = new_df_2[[4,5,6,7]]
        #print "This is df3"
        #print new_df_3
        new_temp_count_df2 = new_df_2.groupby(['selectedLevel','mathOperator','questionPair_left','questionPair_right']).size().to_frame('size').reset_index()
        new_count_1_df2 = new_df_2.groupby(['selectedLevel','mathOperator','questionPair_left']).size().to_frame('size').reset_index()
        new_count_2_df2 = new_df_2.groupby(['selectedLevel','mathOperator','questionPair_right']).size().to_frame('size').reset_index()
        #summ_new_count = pd.concat([new_count_1,new_count_2], axis=1).reset_index().apply(pd.to_numeric)
        new_count_1_df2 = new_count_1_df2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        new_count_2_df2 = new_count_2_df2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        new_count_1_df2 = new_count_1_df2.rename(columns={'questionPair_left': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})
        new_count_2_df2 = new_count_2_df2.rename(columns={'questionPair_right': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})    
        #print new_count_1_df3
        #print new_count_2_df3
        #print new_temp_count_df3
        count_val = len(new_final_extended_my_list)
        count_val = float(count_val)
        #print count_val
        #print new_val_22
        #print new_final_extended_my_list
        #print new_df_1
        #new_count_1 = new_count_1[[0,1,2,3]].sort_values(by=['Count_As_Left_Question','Operator','Questions'], ascending=[False,False,False])
    #if(len(new_df_1.index) != 0 and len(new_df_2) !=0 ):    
    #print new_count_2_df2
    return new_count_1,new_count_2,new_df_1,new_count_1_df2,new_count_2_df2,new_df_2
    """
    elif(len(new_df_1.index) == 0 and len(new_df_2) !=0 ):
        
        return new_count_1_df2,new_count_2_df2,new_df_2
    
    elif(len(new_df_1.index) != 0 and len(new_df_2) ==0 ):
        
        return new_count_1,new_count_2,new_df_1
    else:
        return 0
    """
    """
    for row_2 in xrange(0,len(new_df_2)):
        if ((new_df_2.ix[row_2,"questionPair_left"<=9] and new_df_2.ix[row_2,"questionPair_left"<=9]))
            print new_df_2.ix[row_2,"questionPair_left"<=9] 
    #print new_final_extended_my_list
    #print lvl_data_df
   """
   
   
def add_sub_analysis_lvl_3(lvl_data_df):
    
    #print  lvl_data_df
    new_final_extended_my_list = pd.DataFrame([0])
    new_df_1 = pd.DataFrame()
    new_df_2 = pd.DataFrame([0])
    new_count_1 = pd.DataFrame()
    new_count_2 = pd.DataFrame()
    new_count_1_df2 = pd.DataFrame()
    new_count_2_df2 = pd.DataFrame()
    
    #print lvl_data_df
    #print temp_updated_df_train
    for row in xrange(0,len(lvl_data_df)):
        if((lvl_data_df.ix[row,"questionPair_right"]) <= 9 and (lvl_data_df.ix[row,"selectedLevel"]) == 3 and selectlvl[0] == 3):    
           new_final_extended_my_list = (new_final_extended_my_list.append(lvl_data_df.ix[[row]],ignore_index=True))
        elif((lvl_data_df.ix[row,"selectedLevel"])==3 and selectlvl[0] == 3):
           new_df_2 = new_df_2.append(lvl_data_df.ix[[row]],ignore_index=True) 
        else:
            break
    new_final_extended_my_list =new_final_extended_my_list.drop(0,1)
    new_final_extended_my_list =new_final_extended_my_list.drop(0,0).reset_index(drop=1) 
    new_df_2 =new_df_2.drop(0,1)
    new_df_2 =new_df_2.drop(0,0).reset_index(drop=1) 
    
    """    
    The questions of type where left_question>9 and right_question>9 are analysed and
    the frequecies are calculated in the below code.
    """
    
    if (len(new_final_extended_my_list.index) != 0):

        new_df_1 = new_final_extended_my_list.copy()
        #print new_df_1
        new_df_1 = new_df_1[[4,5,6,7]]
        #print "This is df1"
        #print new_df_1
        new_temp_count = new_df_1.groupby(['selectedLevel','mathOperator','questionPair_left','questionPair_right']).size().to_frame('size').reset_index()  
        new_count_1 = new_df_1.groupby(['selectedLevel','mathOperator','questionPair_left']).size().to_frame('size').reset_index()
        new_count_2 = new_df_1.groupby(['selectedLevel','mathOperator','questionPair_right']).size().to_frame('size').reset_index()
        #summ_new_count = pd.concat([new_count_1,new_count_2], axis=1).reset_index().apply(pd.to_numeric)
        new_count_1 = new_count_1[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        new_count_2 = new_count_2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        new_count_1 = new_count_1.rename(columns={'questionPair_left': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})
        new_count_2 = new_count_2.rename(columns={'questionPair_right': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})    
        #print new_count_1
        #print new_count_2
        #print new_temp_count
        #new_final_extended_my_list = new_final_extended_my_list.groupby(['selectedLevel','questionPair_left','questionPair_right','mathOperator']).size().reset_index()
        #new_val_22 = ((count_val/len(lvl_data_df.index))*100)
        #new_df_2 =new_df_2.drop(0,1)
        #new_df_2 =new_df_2.drop(0,0).reset_index(drop=1)
        
    """
    Analysing the second dataframe questions saved in new_df_2
    """
    
    if (len(new_df_2.index) != 0):
        
        new_df_2 = new_df_2[[4,5,6,7]]
        #print "This is df3"
        #print new_df_3
        new_temp_count_df2 = new_df_2.groupby(['selectedLevel','mathOperator','questionPair_left','questionPair_right']).size().to_frame('size').reset_index()
        new_count_1_df2 = new_df_2.groupby(['selectedLevel','mathOperator','questionPair_left']).size().to_frame('size').reset_index()
        new_count_2_df2 = new_df_2.groupby(['selectedLevel','mathOperator','questionPair_right']).size().to_frame('size').reset_index()
        #summ_new_count = pd.concat([new_count_1,new_count_2], axis=1).reset_index().apply(pd.to_numeric)
        new_count_1_df2 = new_count_1_df2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        new_count_2_df2 = new_count_2_df2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        new_count_1_df2 = new_count_1_df2.rename(columns={'questionPair_left': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})
        new_count_2_df2 = new_count_2_df2.rename(columns={'questionPair_right': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})    
        #print new_count_1_df3
        #print new_count_2_df3
        #print new_temp_count_df3
        count_val = len(new_final_extended_my_list)
        count_val = float(count_val)
        #print count_val
        #print new_val_22
        #print new_final_extended_my_list
        #print new_df_1
        #new_count_1 = new_count_1[[0,1,2,3]].sort_values(by=['Count_As_Left_Question','Operator','Questions'], ascending=[False,False,False])
    #if(len(new_df_1.index) != 0 and len(new_df_2) !=0 ):    
    
    return new_count_1,new_count_2,new_df_1,new_count_1_df2,new_count_2_df2,new_df_2
    """
    elif(len(new_df_1.index) == 0 and len(new_df_2) !=0 ):
        
        return new_count_1_df2,new_count_2_df2,new_df_2
    
    elif(len(new_df_1.index) != 0 and len(new_df_2) ==0 ):
        
        return new_count_1,new_count_2,new_df_1
    else:
        return 0
    """
    """
    for row_2 in xrange(0,len(new_df_2)):
        if ((new_df_2.ix[row_2,"questionPair_left"<=9] and new_df_2.ix[row_2,"questionPair_left"<=9]))
            print new_df_2.ix[row_2,"questionPair_left"<=9] 
    #print new_final_extended_my_list
    #print lvl_data_df
   """
   
def add_sub_analysis_lvl_2(lvl_data_df):
     
    new_final_extended_my_list_lvl_2 = pd.DataFrame([0])
    new_df_1_lvl_2 = pd.DataFrame([0])
    new_df_2_lvl_2 = pd.DataFrame([0])
    new_count_1_lvl_2 = pd.DataFrame()
    new_count_2_lvl_2 = pd.DataFrame()
    new_count_1_lvl_2_1 = pd.DataFrame()
    new_count_2_lvl_2_2 = pd.DataFrame()
    
    #print lvl_data_df
    #print temp_updated_df_train
    for row in xrange(0,len(lvl_data_df)):
        if((lvl_data_df.ix[row,"questionPair_right"]) <= 9 and (lvl_data_df.ix[row,"selectedLevel"]) ==2 and selectlvl[0] == 2):    
           new_final_extended_my_list_lvl_2 = (new_final_extended_my_list_lvl_2.append(lvl_data_df.ix[[row]],ignore_index=True))
        elif(lvl_data_df.ix[row,"selectedLevel"]==2 and selectlvl[0] == 2):
           new_df_2_lvl_2 = new_df_2_lvl_2.append(lvl_data_df.ix[[row]],ignore_index=True) 
        else:
           break   
       
    new_final_extended_my_list_lvl_2 =new_final_extended_my_list_lvl_2.drop(0,1)
    new_final_extended_my_list_lvl_2 =new_final_extended_my_list_lvl_2.drop(0,0).reset_index(drop=1)    
    new_df_2_lvl_2 =new_df_2_lvl_2.drop(0,1)
    new_df_2_lvl_2 =new_df_2_lvl_2.drop(0,0).reset_index(drop=1)
    #print "chking the dataframe values !!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    #print   new_final_extended_my_list_lvl_2
    #print   new_df_2_lvl_2
    
    if (len(new_final_extended_my_list_lvl_2.index) != 0):
        
        
        new_df_1_lvl_2 = new_final_extended_my_list_lvl_2.copy()
        #print new_df_2_lvl_2
        new_df_1_lvl_2 = new_df_1_lvl_2[[4,5,6,7]]
        #print "This is df1"
        #print new_df_1
        new_temp_count_lvl_2 = new_df_1_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_left','questionPair_right']).size().to_frame('size').reset_index()
        new_count_1_lvl_2 = new_df_1_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_left']).size().to_frame('size').reset_index()
        new_count_2_lvl_2 = new_df_1_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_right']).size().to_frame('size').reset_index()
        #summ_new_count = pd.concat([new_count_1,new_count_2], axis=1).reset_index().apply(pd.to_numeric)
        new_count_1_lvl_2 = new_count_1_lvl_2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        new_count_2_lvl_2 = new_count_2_lvl_2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        new_count_1_lvl_2 = new_count_1_lvl_2.rename(columns={'questionPair_left': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})
        new_count_2_lvl_2 = new_count_2_lvl_2.rename(columns={'questionPair_right': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})    
        #print new_val_22
        #print new_final_extended_my_list
        #print new_df_1

    if (len(new_df_2_lvl_2.index) != 0):
        
        new_df_2_lvl_2 = new_df_2_lvl_2[[4,5,6,7]]
        #print "This is df1"
        #print new_df_1
        new_temp_count_lvl_2 = new_df_2_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_left','questionPair_right']).size().to_frame('size').reset_index()
        new_count_1_lvl_2_1 = new_df_2_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_left']).size().to_frame('size').reset_index()
        new_count_2_lvl_2_2 = new_df_2_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_right']).size().to_frame('size').reset_index()
        #summ_new_count = pd.concat([new_count_1,new_count_2], axis=1).reset_index().apply(pd.to_numeric)
        new_count_1_lvl_2_1 = new_count_1_lvl_2_1[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        new_count_2_lvl_2_2 = new_count_2_lvl_2_2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        new_count_1_lvl_2_1 = new_count_1_lvl_2_1.rename(columns={'questionPair_left': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})
        new_count_2_lvl_2_2 = new_count_2_lvl_2_2.rename(columns={'questionPair_right': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})    
        #print new_count_2_lvl_2_2
        #print new_count_1_lvl_2_1
        #print new_df_2_lvl_2
        
    #if(len(new_df_1_lvl_2.index) != 0 and len(new_df_2_lvl_2) !=0 ):    
    
    return new_count_1_lvl_2,new_count_2_lvl_2,new_df_1_lvl_2,new_count_1_lvl_2_1,new_count_2_lvl_2_2,new_df_2_lvl_2
    """
    elif(len(new_df_1_lvl_2.index) == 0 and len(new_df_2_lvl_2) !=0 ):
        
        return new_count_1_lvl_2_1,new_count_2_lvl_2_2,new_df_2_lvl_2
    
    elif(len(new_df_1_lvl_2.index) != 0 and len(new_df_2_lvl_2) ==0 ):
        
        return new_count_1_lvl_2,new_count_2_lvl_2,new_df_1_lvl_2
    else:
        return 0       
    """    
def add_analysis_lvl_2(lvl_data_df):
    new_final_extended_my_list_lvl_2 = pd.DataFrame([0])
    new_df_1_lvl_2 = pd.DataFrame([0])
    new_df_2_lvl_2 = pd.DataFrame([0])
    new_df_3_lvl_2 = pd.DataFrame([0])
    new_df_4_lvl_2 = pd.DataFrame([0])
    new_count_1_lvl_2 = pd.DataFrame()
    new_count_2_lvl_2 = pd.DataFrame()
    new_count_1_lvl_2_1 = pd.DataFrame()
    new_count_2_lvl_2_2 = pd.DataFrame()
    counts_ty3_lvl2_1 = pd.DataFrame()
    counts_ty3_lvl2_2 = pd.DataFrame()
    counts_ty4_lvl2_1 = pd.DataFrame()
    counts_ty4_lvl2_2 = pd.DataFrame()
    
    #print lvl_data_df
    #print temp_updated_df_train
    for row in xrange(0,len(lvl_data_df)):
        if((lvl_data_df.ix[row,"questionPair_left"]) > 9 and (lvl_data_df.ix[row,"questionPair_right"]) <= 9 and (lvl_data_df.ix[row,"selectedLevel"]) ==2 and selectlvl[0] == 2):    
           new_final_extended_my_list_lvl_2 = (new_final_extended_my_list_lvl_2.append(lvl_data_df.ix[[row]],ignore_index=True))
        elif((lvl_data_df.ix[row,"questionPair_left"]) <= 9 and (lvl_data_df.ix[row,"questionPair_right"]) > 9 and (lvl_data_df.ix[row,"selectedLevel"]) ==2 and selectlvl[0] == 2):
           new_df_2_lvl_2 = new_df_2_lvl_2.append(lvl_data_df.ix[[row]],ignore_index=True) 
        elif((lvl_data_df.ix[row,"questionPair_left"]) <= 9 and (lvl_data_df.ix[row,"questionPair_right"]) <= 9 and (lvl_data_df.ix[row,"selectedLevel"]) ==2 and selectlvl[0] == 2):
           new_df_3_lvl_2 = new_df_3_lvl_2.append(lvl_data_df.ix[[row]],ignore_index=True) 
        elif((lvl_data_df.ix[row,"questionPair_left"]) > 9  and (lvl_data_df.ix[row,"questionPair_right"]) > 9 and (lvl_data_df.ix[row,"selectedLevel"]) ==2 and selectlvl[0] == 2):
           new_df_4_lvl_2 = new_df_4_lvl_2.append(lvl_data_df.ix[[row]],ignore_index=True) 
        else:   
            break   
        
    new_final_extended_my_list_lvl_2 =new_final_extended_my_list_lvl_2.drop(0,1)
    new_final_extended_my_list_lvl_2 =new_final_extended_my_list_lvl_2.drop(0,0).reset_index(drop=1) 
    new_df_4_lvl_2 =new_df_4_lvl_2.drop(0,1)
    new_df_4_lvl_2 =new_df_4_lvl_2.drop(0,0).reset_index(drop=1)      
    new_df_2_lvl_2 =new_df_2_lvl_2.drop(0,1)
    new_df_2_lvl_2 =new_df_2_lvl_2.drop(0,0).reset_index(drop=1)
    new_df_3_lvl_2 =new_df_3_lvl_2.drop(0,1)
    new_df_3_lvl_2 =new_df_3_lvl_2.drop(0,0).reset_index(drop=1)
    
    if (len(new_final_extended_my_list_lvl_2.index) != 0):
        #print "!!!!!!!!!!!!!!!!!!!!!This is Typ-0 DataFrame!!!!!!!!!!!!!!!!!!!!!!"
        #print new_final_extended_my_list_lvl_2
        new_df_1_lvl_2 = new_final_extended_my_list_lvl_2.copy()
        #print new_df_2_lvl_2
        new_df_1_lvl_2 = new_df_1_lvl_2[[4,5,6,7]]
        #print "This is df1"
        #print new_df_1
        if (len(new_df_1_lvl_2) != 0):
            new_temp_count_lvl_2 = new_df_1_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_left','questionPair_right']).size().to_frame('size').reset_index()
            new_count_1_lvl_2 = new_df_1_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_left']).size().to_frame('size').reset_index()
            new_count_2_lvl_2 = new_df_1_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_right']).size().to_frame('size').reset_index()
            #summ_new_count = pd.concat([new_count_1,new_count_2], axis=1).reset_index().apply(pd.to_numeric)
            new_count_1_lvl_2 = new_count_1_lvl_2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
            new_count_2_lvl_2 = new_count_2_lvl_2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
            new_count_1_lvl_2 = new_count_1_lvl_2.rename(columns={'questionPair_left': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})
            new_count_2_lvl_2 = new_count_2_lvl_2.rename(columns={'questionPair_right': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})    
        #print new_val_22
        #print new_final_extended_my_list
        #print new_df_1

    if (len(new_df_2_lvl_2.index) != 0):
        #print "!!!!!!!!!!!!!!!!!!!!!This is Typ-1 DataFrame!!!!!!!!!!!!!!!!!!!!!!"
        #print new_df_2_lvl_2
        new_df_2_lvl_2 = new_df_2_lvl_2[[4,5,6,7]]
        #print "This is df1"
        #print new_df_1
        new_temp_count_lvl_2 = new_df_2_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_left','questionPair_right']).size().to_frame('size').reset_index()
        new_count_1_lvl_2_1 = new_df_2_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_left']).size().to_frame('size').reset_index()
        new_count_2_lvl_2_2 = new_df_2_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_right']).size().to_frame('size').reset_index()
        #summ_new_count = pd.concat([new_count_1,new_count_2], axis=1).reset_index().apply(pd.to_numeric)
        new_count_1_lvl_2_1 = new_count_1_lvl_2_1[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        new_count_2_lvl_2_2 = new_count_2_lvl_2_2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        new_count_1_lvl_2_1 = new_count_1_lvl_2_1.rename(columns={'questionPair_left': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})
        new_count_2_lvl_2_2 = new_count_2_lvl_2_2.rename(columns={'questionPair_right': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})    
        #print new_count_2_lvl_2_2
        #print new_count_1_lvl_2_1
        #print new_df_2_lvl_2
        
    if (len(new_df_3_lvl_2.index) != 0):
        #print "!!!!!!!!!!!!!!!!!!!!!This is Typ-2 DataFrame!!!!!!!!!!!!!!!!!!!!!!"
        #print new_df_3_lvl_2
        new_df_3_lvl_2 = new_df_3_lvl_2[[4,5,6,7]]
        
        #print "This is df1"
        #print new_df_1
        new_tot_typ3_count = new_df_3_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_left','questionPair_right']).size().to_frame('size').reset_index()
        counts_ty3_lvl2_1 = new_df_3_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_left']).size().to_frame('size').reset_index()
        counts_ty3_lvl2_2 = new_df_3_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_right']).size().to_frame('size').reset_index()
        #summ_new_count = pd.concat([new_count_1,new_count_2], axis=1).reset_index().apply(pd.to_numeric)
        counts_ty3_lvl2_1 = counts_ty3_lvl2_1[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        counts_ty3_lvl2_2 = counts_ty3_lvl2_2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        counts_ty3_lvl2_1 = counts_ty3_lvl2_1.rename(columns={'questionPair_left': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})
        counts_ty3_lvl2_2 = counts_ty3_lvl2_2.rename(columns={'questionPair_right': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})    
       
        #print new_count_2_lvl_2_2
        #print new_count_1_lvl_2_1
        #print new_df_2_lvl_2
        
    if (len(new_df_4_lvl_2.index) != 0):
        #print "!!!!!!!!!!!!!!!!!!!!!This is Typ-3 DataFrame!!!!!!!!!!!!!!!!!!!!!!"
        #print new_df_4_lvl_2
        new_df_4_lvl_2 = new_df_4_lvl_2[[4,5,6,7]]
        
        #print "This is df1"
        #print new_df_1
        new_tot_typ4_count = new_df_4_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_left','questionPair_right']).size().to_frame('size').reset_index()
        counts_ty4_lvl2_1 = new_df_4_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_left']).size().to_frame('size').reset_index()
        counts_ty4_lvl2_2 = new_df_4_lvl_2.groupby(['selectedLevel','mathOperator','questionPair_right']).size().to_frame('size').reset_index()
        #summ_new_count = pd.concat([new_count_1,new_count_2], axis=1).reset_index().apply(pd.to_numeric)
        counts_ty4_lvl2_1 = counts_ty4_lvl2_1[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        counts_ty4_lvl2_2 = counts_ty4_lvl2_2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
        counts_ty4_lvl2_1 = counts_ty4_lvl2_1.rename(columns={'questionPair_left': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})
        counts_ty4_lvl2_2 = counts_ty4_lvl2_2.rename(columns={'questionPair_right': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})    
    
        #print new_count_2_lvl_2_2
        #print new_count_1_lvl_2_1
        #print new_df_2_lvl_2
    #if(len(new_df_1_lvl_2.index) != 0 and len(new_df_2_lvl_2) !=0 ):    
    
    return new_count_1_lvl_2,new_count_2_lvl_2,new_df_1_lvl_2,new_count_1_lvl_2_1,new_count_2_lvl_2_2,new_df_2_lvl_2,counts_ty3_lvl2_1,counts_ty3_lvl2_2,new_df_3_lvl_2,counts_ty4_lvl2_1,counts_ty4_lvl2_2,new_df_4_lvl_2
    """
    elif(len(new_df_1_lvl_2.index) == 0 and len(new_df_2_lvl_2) !=0 ):
        
        return new_count_1_lvl_2_1,new_count_2_lvl_2_2,new_df_2_lvl_2
    
    elif(len(new_df_1_lvl_2.index) != 0 and len(new_df_2_lvl_2) ==0 ):
        
        return new_count_1_lvl_2,new_count_2_lvl_2,new_df_1_lvl_2
    else:
        return 0       
    """    
       
def add_sub_analysis_lvl_1(lvl_data_df):
     
    #new_final_extended_my_list = pd.DataFrame([0])
    new_df_1_lvl_1= pd.DataFrame([0])
    #print lvl_data_df
    #print temp_updated_df_train
    for row in xrange(0,len(lvl_data_df)):
        if((lvl_data_df.ix[row,"questionPair_right"]) <= 9 and (lvl_data_df.ix[row,"selectedLevel"])==1 and selectlvl[0] == 1):    
           new_df_1_lvl_1 = (new_df_1_lvl_1.append(lvl_data_df.ix[[row]],ignore_index=True))
        else:
            break
    
    new_df_1_lvl_1 =new_df_1_lvl_1.drop(0,1)
    new_df_1_lvl_1 =new_df_1_lvl_1.drop(0,0).reset_index(drop=1) 
    new_df_1_lvl_1 = new_df_1_lvl_1[[4,5,6,7]]
    #print "This is df1"
    #print new_df_1
    new_temp_count = new_df_1_lvl_1.groupby(['selectedLevel','mathOperator','questionPair_left','questionPair_right']).size().to_frame('size').reset_index()
    new_count_1_lvl_1 = new_df_1_lvl_1.groupby(['selectedLevel','mathOperator','questionPair_left']).size().to_frame('size').reset_index()
    new_count_2_lvl_1 = new_df_1_lvl_1.groupby(['selectedLevel','mathOperator','questionPair_right']).size().to_frame('size').reset_index()
    #summ_new_count = pd.concat([new_count_1,new_count_2], axis=1).reset_index().apply(pd.to_numeric)
    new_count_1_lvl_1 = new_count_1_lvl_1[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
    new_count_2_lvl_1 = new_count_2_lvl_1[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
    new_count_1_lvl_1 = new_count_1_lvl_1.rename(columns={'questionPair_left': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})
    new_count_2_lvl_1 = new_count_2_lvl_1.rename(columns={'questionPair_right': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})    
    #print new_val_22
    #print new_final_extended_my_list
    #print new_df_1
    return new_count_1_lvl_1,new_count_2_lvl_1,new_df_1_lvl_1
       
def mul_analy_fun(mul_df):
    
    mul_df = mul_df[[4,5,6,7]]
    #print mul_df
    mul_new_temp = mul_df.groupby(['selectedLevel','mathOperator','questionPair_left','questionPair_right']).size().to_frame('size').reset_index()
    mul_new_count_1 = mul_df.groupby(['selectedLevel','mathOperator','questionPair_left']).size().to_frame('size').reset_index()
    mul_new_count_2 = mul_df.groupby(['selectedLevel','mathOperator','questionPair_right']).size().to_frame('size').reset_index()
    #summ_new_count = pd.concat([new_count_1,new_count_2], axis=1).reset_index().apply(pd.to_numeric)
    mul_new_count_1 = mul_new_count_1[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
    mul_new_count_2 = mul_new_count_2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
    mul_new_count_1 = mul_new_count_1.rename(columns={'questionPair_left': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})
    mul_new_count_2 = mul_new_count_2.rename(columns={'questionPair_right': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})    
    #print mul_new_count_1
    #print mul_new_count_2
    #print new_df_1
    return mul_new_count_1,mul_new_count_2,mul_df

def div_analy_fun(div_df):
    
    div_df = div_df[[4,5,6,7]]
    #print mul_df
    div_new_temp = div_df.groupby(['selectedLevel','mathOperator','questionPair_left','questionPair_right']).size().to_frame('size').reset_index()
    div_new_count_1 = div_df.groupby(['selectedLevel','mathOperator','questionPair_left']).size().to_frame('size').reset_index()
    div_new_count_2 = div_df.groupby(['selectedLevel','mathOperator','questionPair_right']).size().to_frame('size').reset_index()
    #summ_new_count = pd.concat([new_count_1,new_count_2], axis=1).reset_index().apply(pd.to_numeric)
    div_new_count_1 = div_new_count_1[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
    div_new_count_2 = div_new_count_2[[0,1,2,3]].sort_values(by=['size'], ascending=[False]).reset_index(drop=1)
    div_new_count_1 = div_new_count_1.rename(columns={'questionPair_left': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})
    div_new_count_2 = div_new_count_2.rename(columns={'questionPair_right': 'Questions', 'size': 'Total_Frequency', 'mathOperator': 'Operator'})    
    #print mul_new_count_1
    #print mul_new_count_2
    #print new_df_1
    return div_new_count_1,div_new_count_2,div_df

    
def count_sub_lvl_3(my_sub_dataframe,selectlvl,List_Wrongs):
     #print my_sub_dataframe
     temp1 = 0
     #print my_list_2
     #print my_sub_dataframe
     for lvl_val in range(len(selectlvl)):
        final_extended_my_list_1 = pd.DataFrame([0])
        for new_row in xrange(0,len(my_sub_dataframe)):  
            if ((my_sub_dataframe.ix[new_row,'selectedLevel']) == selectlvl[lvl_val]):
                final_extended_my_list_1 = (final_extended_my_list_1.append(my_sub_dataframe.ix[[new_row]],ignore_index=True))
        #print final_extended_my_list
        final_extended_my_list_1 =final_extended_my_list_1.drop(0,0).reset_index(drop=1)
        #print final_extended_my_list
        Total_Wrongs = len(final_extended_my_list_1)
        List_Wrongs.ix[temp1,'level'] = selectlvl[lvl_val]
        List_Wrongs.ix[temp1,'Wrongs'] = Total_Wrongs
        temp1= temp1 + 1
        final_extended_my_list_1 =final_extended_my_list_1.drop(final_extended_my_list_1.index,inplace=True)
    
     #final_extended_my_list = final_extended_my_list.drop(0,1)
     #print final_extended_my_list
     #List_Wrongs =List_Wrongs.drop(0,0).reset_index(drop=1)
     List_Wrongs = List_Wrongs.drop(0,1)
     #print List_Wrongs
     return List_Wrongs
    
def php_data(new_data,weight_result_df_1_right,selectlvl):
    #print "Function successfully called"
    sub_return_list_1 = []
    sub_return_list_2 = []
    sub_return_list_3 = []
    sub_return_list_4 = []
    sub_return_list_5 = []
    sub_return_list_6 = []
    return_list = []
    #print "!!!!!!!!!!!This is new_data !!!!!!!!!!!!!!!!11"
    #print new_data
    #print weight_result_df_1_right
    x_list_sugg_questions = []
    y_list_sugg_questions = []
    new_data = new_data[[0,5,4,6]]
    weight_result_df_1_right = weight_result_df_1_right[[0,5,4,6]]
    new_data = new_data.reset_index(drop =1)
    for abhi in xrange(0,len(new_data.index)):
        abhi_temp_data =  map( int, new_data.ix[abhi,"Suggested_Numbers"].split(','))
        for jj in abhi_temp_data:
          x_list_sugg_questions.append(new_data.ix[abhi,"Questions"])
          y_list_sugg_questions.append(jj)    
    plot_x_1 = x_list_sugg_questions
    plot_y_1 = y_list_sugg_questions
    #print plot_x
    #print plot_y
    plt.plot(plot_x_1, plot_y_1, 'bo')
    #plt.show()
    weight_result_df_1_right = weight_result_df_1_right.reset_index(drop = 1)
    for w_1 in xrange(0,len(new_data.index)):
        iam_temp = new_data.ix[w_1,"Questions"]
        sub_return_list_1.append(iam_temp)
        sub_return_list_2.append(new_data.ix[w_1,"Right_Question_Choice"])
        sub_return_list_5.append(new_data.ix[w_1,"Suggested_Numbers"])
        #sub_return_list_3.append(new_data.ix[w_1,"Suggested_Numbers"])
    #print sub_return_list_1 
    #print return_list
    #print sub_return_list_2
    #print weight_result_df_1_right
    for w_2 in xrange(0,len(weight_result_df_1_right.index)):
        iam_temp_1 = weight_result_df_1_right.ix[w_2,"Questions"]
        #print iam_temp_1
        sub_return_list_3.append(iam_temp_1)
        sub_return_list_4.append(weight_result_df_1_right.ix[w_2,"Left_Question_Choice"])
        sub_return_list_6.append(weight_result_df_1_right.ix[w_2,"Suggested_Numbers"])
    return_list = [sub_return_list_1,sub_return_list_2,sub_return_list_5,sub_return_list_3,sub_return_list_4,sub_return_list_6]   
    #print return_list
  
    return return_list

#return new_final_extended_my_list             
"""
This part of the code is used to connect to the student database and extract the data.
"""
con = mysql.connector.connect(host='localhost',user='root',password='',db='mysql',port=3306)
cur1 = con.cursor(buffered=True)    
cur2 = con.cursor(buffered=True)  
cur3 = con.cursor(buffered=True)  
cur4 = con.cursor(buffered=True)  
cur1.execute('SELECT a.selectedLevel,a.additionProblemCount,a.additionProblemsMissed,a.subtractionProblemCount,a.subtractionProblemsMissed,a.multiplicationProblemCount,a.multiplicationProblemsMissed,a.divisionProblemCount,a.divisionProblemsMissed,a.numberofWrongs,a.numberofCorrects,a.totalNumberOfProblems,a.studentScore,a.cummulativePoints,b.questionPair,b.userAnswer,b.correctAnswer,a.problemType,a.selectedLevel,b.mathOperator,b.questionTime,b.questionDurationinS FROM a1234 as a, a1234_details as b where a.dateOfUse=b.dateOfUse and a.selectedLevel=b.selectedLevel and a.problemType=b.problemType')
cur2.execute('SELECT a.selectedLevel,a.additionProblemCount,a.additionProblemsMissed,a.subtractionProblemCount,a.subtractionProblemsMissed,a.multiplicationProblemCount,a.multiplicationProblemsMissed,a.divisionProblemCount,a.divisionProblemsMissed,a.numberofWrongs,a.numberofCorrects,a.totalNumberOfProblems,a.studentScore,a.cummulativePoints,b.questionPair,b.userAnswer,b.correctAnswer,a.problemType,a.selectedLevel,b.mathOperator,b.questionTime,b.questionDurationinS FROM m1234 as a, m1234_details as b where a.dateOfUse=b.dateOfUse and a.selectedLevel=b.selectedLevel and a.problemType=b.problemType')
cur3.execute('SELECT a.selectedLevel,a.additionProblemCount,a.additionProblemsMissed,a.subtractionProblemCount,a.subtractionProblemsMissed,a.multiplicationProblemCount,a.multiplicationProblemsMissed,a.divisionProblemCount,a.divisionProblemsMissed,a.numberofWrongs,a.numberofCorrects,a.totalNumberOfProblems,a.studentScore,a.cummulativePoints,b.questionPair,b.userAnswer,b.correctAnswer,a.problemType,a.selectedLevel,b.mathOperator,b.questionTime,b.questionDurationinS FROM ur1234 as a, ur1234_details as b where a.dateOfUse=b.dateOfUse and a.selectedLevel=b.selectedLevel and a.problemType=b.problemType')
cur4.execute('SELECT a.dateOfUse,a.studentID,a.selectedLevel,a.problemType,a.modeOfUse,a.questionTime,a.questionDurationinS,a.questionPair,a.mathOperator,a.userAnswer,a.correctAnswer FROM detail_performance as a')
try:
   data1=cur1.fetchall()
   data2=cur2.fetchall()
   data3=cur3.fetchall()
   data4=cur4.fetchall()
except mysql.connector.errors.InterfaceError as ie:
   if ie.msg == 'No result set to fetch from.':
       pass
   else:
       raise
#print data1
#print data2
#new_array_a1234 = numpy.array(data1)
#new_array_a1234_details = numpy.array(data2)
#x = new_array_a1234[:,][0:1:,],cur1.description
#print x
df_a = pd.DataFrame(data1)
df_m = pd.DataFrame(data2)
df_rn=pd.DataFrame(data3)
df_new_data = pd.DataFrame(data4)
"""
The part is oriented to change the column names of the dataframes and later 
all the individual table data re being combined ofr analysis.
"""
old_names = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
new_names = ['selectedLevel','additionProblemCount','additionProblemsMissed','subtractionProblemCount','subtractionProblemsMissed','multiplicationProblemCount','multiplicationProblemsMissed','divisionProblemCount','divisionProblemsMissed','numberofWrongs','numberofCorrects','totalNumberOfProblems','studentScore','cummulativePoints','questionPair','userAnswer','correctAnswer','problemType','selectedLevel','mathOperator','questionTime','questionDurationinS']
df_a.rename(columns=dict(zip(old_names, new_names)), inplace=True)
df_m.rename(columns=dict(zip(old_names, new_names)), inplace=True)
df_rn.rename(columns=dict(zip(old_names, new_names)), inplace=True)
df_new_data_old_names = [0,1,2,3,4,5,6,7,8,9,10]
df_new_data_new_names = ['dateOfUse','studentID','selectedLevel','problemType','modeOfUse','questionTime','questionDurationinS','questionPair','mathOperator','userAnswer','correctAnswer']
df_new_data.rename(columns=dict(zip(df_new_data_old_names, df_new_data_new_names)), inplace=True)
df_new = pd.concat([df_a, df_m,df_rn],ignore_index=True)
df_train = df_new[[18,16,19,14,15,20,21,17]]
df_train_2 = df_new_data[[2,10,8,7,9,5,6,3]]
df_train = pd.concat([df_train, df_train_2],ignore_index=True)
df_train['problemType'] = df_train['problemType'].map({'Subtraction': 2, 'Random': 5,'Addition':1,'Multiplication':3,'Division':4})
df_train['mathOperator'] = df_train['mathOperator'].map({'-': 2, '+': 1,'x': 3,'/': 4,'&di':4})
#print df_train
updated_df_train = pd.DataFrame()
for val in xrange(0,len(df_train)):
    if (df_train.ix[val,"mathOperator"]==mathop):
        updated_df_train = updated_df_train.append(df_train.ix[[val]],ignore_index=True)   
#print updated_df_train
updated_df_train[["selectedLevel"]] = updated_df_train[["selectedLevel"]].apply(pd.to_numeric)
new_temp_updt_df_train = pd.DataFrame()

for dfg in xrange(0,len(updated_df_train.index)):
    if (updated_df_train.ix[dfg,"selectedLevel"] == selectlvl[n_lvl_val]):
        new_temp_updt_df_train = new_temp_updt_df_train.append(updated_df_train.ix[[dfg]],ignore_index=True)

#print new_temp_updt_df_train
"""
Here the Total_Wrongs is the variable which is used to capture the no of wrongs
by taking the count of the total no of questions asked on that particular operator
count_questions_fun is the function used to calculate the counts.
"""
my_list = pd.DataFrame(['questionPair','mathOperator'])
extended_my_list = pd.DataFrame([0])
#print df_train
my_list = df_train[[0,2,3]]
my_list_2 = df_train[[0,2,3,4]] 
#print my_list_2
Total_Wrongs =  count_questions_fun(my_list_2,extended_my_list,selectlvl,List_Wrongs)
#print Total_Wrongs
#final_list_dataframe = pd.DataFrame([0])
"""
for values in xrange(0,len(list_dataframe)):
    if ((list_dataframe.ix[values,'userAnswer'] == 99889988) or (list_dataframe.ix[values,'userAnswer'] == 99779977) or (list_dataframe.ix[values,'userAnswer'] == 123456)):
        list_dataframe = list_dataframe.drop(values,0)
list_dataframe = list_dataframe.reset_index(drop=1)
"""
#print list_dataframe
#Total_Wrongs = count_questions_fun(my_list,extended_my_list)
#print  Total_Wrongs
my_list = my_list.groupby(['selectedLevel','questionPair','mathOperator']).size().reset_index()
my_list = my_list.rename(columns={0: 'Counts'})
#print my_list
my_new_list = pd.DataFrame()
for o in xrange(0,len(my_list.index)):
    if ((my_list.ix[o,'mathOperator'] == mathop)):
         my_new_list = (my_new_list.append(my_list.ix[[o]],ignore_index=True)).fillna(0)
my_new_list = my_new_list.sort_values(by=['Counts'],ascending=[False]).reset_index(drop=1)
#print my_new_list
updated_df_train['questionPair_left'], updated_df_train['questionPair_right'] = zip(*updated_df_train['questionPair'].map(lambda x: x.split(',')))
updated_df_train[['questionPair_left', 'questionPair_right']] = updated_df_train[['questionPair_left', 'questionPair_right']].astype(int)
#print df_train

"""
The Left question are taken and all the possible operations like (+,-,*,/) are applied 
and saved into the dataframe for kid-operator confusion problem.
"""

updated_df_train['Addition_Ans'] =  updated_df_train[['questionPair_left', 'questionPair_right']].sum(axis=1).astype(int)
updated_df_train['Substraction_Ans'] =  (updated_df_train['questionPair_left'] - updated_df_train['questionPair_right']).astype(int)
updated_df_train['Multiplication_Ans'] =  (updated_df_train['questionPair_left'] * updated_df_train['questionPair_right']).astype(int)
for m in xrange(0,len(updated_df_train.index)):
    if ((updated_df_train.ix[m,'questionPair_right'] == 0 and updated_df_train.ix[m,'questionPair_left'] != 0) or (updated_df_train.ix[m,'questionPair_left'] == 0 and updated_df_train.ix[m,'questionPair_right'] == 0)):
        updated_df_train.ix[m,'Division_Ans'] = 453453
    else:
        updated_df_train.ix[m,'Division_Ans'] =  (updated_df_train.ix[m,'questionPair_left'] / updated_df_train.ix[m,'questionPair_right']).astype(int)

temp_updated_df_train = updated_df_train
nw_tmp_updt_df = updated_df_train
#print temp_updated_df_train
for values in xrange(0,len(temp_updated_df_train)):
    if ((temp_updated_df_train.ix[values,'userAnswer'] == 99889988) or (temp_updated_df_train.ix[values,'userAnswer'] == 99779977) or (temp_updated_df_train.ix[values,'userAnswer'] == 123456)):
        temp_updated_df_train = temp_updated_df_train.drop(values,0)
    elif ((temp_updated_df_train.ix[values,"userAnswer"] == temp_updated_df_train.ix[values,"Addition_Ans"]) or  (temp_updated_df_train.ix[values,"userAnswer"] == temp_updated_df_train.ix[values,"Multiplication_Ans"]) or (temp_updated_df_train.ix[values,"userAnswer"] == temp_updated_df_train.ix[values,"Substraction_Ans"]) or (temp_updated_df_train.ix[values,"userAnswer"] == temp_updated_df_train.ix[values,"Division_Ans"])):   
        temp_updated_df_train = temp_updated_df_train.drop(values,0)

temp_updated_df_train = temp_updated_df_train.reset_index(drop=1)
#temp_updated_df_train = temp_updated_df_train[[0,3,8,9,4,10,11,12,13]].apply(pd.to_numeric)
temp_updated_df_train = temp_updated_df_train[[0,2,8,9,4,10,11,12,13]].apply(pd.to_numeric)
nw_tmp_updt_df = nw_tmp_updt_df[[0,2,8,9,4,10,11,12,13]].apply(pd.to_numeric)
#temp_updated_df_train = temp_updated_df_train[[0,2,8,9,4,10,11,12,13]]
#print temp_updated_df_train

"""
Here we are checking for the kind of operation and if the requested operation is 
substraction then this loop is executed.
"""

if (mathop==2):

    lvl_data_df = pd.DataFrame([0]) 
    for lvl_v in range(len(selectlvl)): 
        for it_1 in xrange(0,len(nw_tmp_updt_df)):
            if (nw_tmp_updt_df.ix[it_1,"selectedLevel"]  == selectlvl[lvl_v] and selectlvl[lvl_v] <= 4 and mathop==2):
                lvl_data_df = lvl_data_df.append(nw_tmp_updt_df.ix[[it_1]],ignore_index=True)
    lvl_data_df = lvl_data_df.drop(0,0)
    lvl_data_df = lvl_data_df.drop(0,1).reset_index(drop=1)            
    #print lvl_data_df    
    plot_x = lvl_data_df[['questionPair_left']]
    plot_y = lvl_data_df[['questionPair_right']]
    #print plot_x
    #print plot_y
    plt.plot(plot_x, plot_y, 'ro')
    plt.show()
    sub_weight_result_df_1_left = pd.DataFrame(['weights(%)'])
    sub_weight_result_df_1_right = pd.DataFrame(['weights(%)'])
    sub_weight_result_df_2_left = pd.DataFrame(['weights(%)'])
    sub_weight_result_df_2_right = pd.DataFrame(['weights(%)'])
    sub_weight_result_df_3_left = pd.DataFrame(['weights(%)'])
    sub_weight_result_df_3_right = pd.DataFrame(['weights(%)'])
    #print my_list_2
    my_list_2['questionPair_left'], my_list_2['questionPair_right'] = zip(*my_list_2['questionPair'].map(lambda x: x.split(',')))
    my_list_2[['questionPair_left', 'questionPair_right']] = my_list_2[['questionPair_left', 'questionPair_right']].astype(int)
    my_list_2["selectedLevel"]=my_list_2["selectedLevel"].apply(pd.to_numeric)
    for new_v_1 in xrange(0,len(my_list_2.index)):
        if (my_list_2.ix[new_v_1,'selectedLevel'] != selectlvl[0] or  my_list_2.ix[new_v_1,'mathOperator'] != mathop):
            my_list_2 = my_list_2.drop(new_v_1,0)
    my_list_2 = my_list_2.reset_index(drop=1)
    #print my_list_2
    my_list_2 = my_list_2.groupby(['questionPair_left','questionPair_right']).size().reset_index()
    my_list_2 = my_list_2.rename(columns={0: 'Counts'})
    #print my_list_2
    my_list_2 = my_list_2.sort_values(by=['Counts'],ascending=[False]).reset_index(drop=1)
    for count_thresh in xrange(0,len(my_list_2.index)):
        if (my_list_2.ix[count_thresh,"Counts"] < 9 ):
            my_list_2 = my_list_2.drop(count_thresh,0)
    my_list_2 = my_list_2.reset_index(drop = 1)
    print my_list_2    
    zzzz = my_list_2[[0,1,2]].astype(str)
    ddnn = pd.crosstab([zzzz.questionPair_left,zzzz.questionPair_right],zzzz.Counts,margins=True)
    ddnn_right = pd.crosstab([zzzz.questionPair_right,zzzz.questionPair_left],zzzz.Counts,margins=True)
    #p1 = numpy.polyfit(new_temp_my_list.questionPair_left,new_temp_my_list.questionPair_right,1)
    #print ddnn
    #print p1
    ddnn = ddnn.reset_index()
    ddnn_right = ddnn_right.reset_index()
    #print ddnn
    ddnn = ddnn.drop(ddnn.index[len(ddnn)-1])
    ddnn_right = ddnn_right.drop(ddnn_right.index[len(ddnn_right)-1])
    #print ddnn    
    #print ddnn_right
    #ddnn = ddnn.drop(ddnn.index[len(ddnn)-1])

    ddnn = ddnn.apply(pd.to_numeric)
    ddnn_right = ddnn_right.apply(pd.to_numeric)
    #ddnn = ddnn.drop(0,2)
    #ddnn = ddnn
    #print ddnn    
    """
    Based on the level requested for we go into that particular loop and analyse the problems and 
    later calicluate the weights for left and right question with the total no of wrongs 
    commited at that particular level
    """
    if (selectlvl[0] == 4):
         analysis_count_4_1_1,analysis_count_4_1_2,dataframe_4_1,analysis_count_4_2_1,analysis_count_4_2_2,dataframe_4_2 = add_sub_analysis_lvl_4(lvl_data_df)
         #print analysis_count_4_1_1
         #print analysis_count_4_1_2
         #print analysis_count_4_2_1
         #print analysis_count_4_2_2
         #print dataframe_4_1
         #print dataframe_4_2
         sending_data_1 = pd.DataFrame()
         sending_data_3 = pd.DataFrame()
         if (len(analysis_count_4_1_1) != 0 and len(analysis_count_4_1_2) != 0):

             sub_weight_result_df_1_left = weights(Total_Wrongs,analysis_count_4_1_1,sub_weight_result_df_1_left)
             sub_weight_result_df_1_right = weights(Total_Wrongs,analysis_count_4_1_2,sub_weight_result_df_1_right)
             #print sub_weight_result_df_1_left
             #print sub_weight_result_df_1_right
             for q in xrange(0,len(sub_weight_result_df_1_left)):
                 sub_weight_result_df_1_left.ix[q,"Right_Question_Choice"] = 1
             for q in xrange(0,len(sub_weight_result_df_1_right)):
                 sub_weight_result_df_1_right.ix[q,"Left_Question_Choice"] = 2
             sugg_val_list_left_lvl3 = [] 
             sugg_val_list_right_lvl3 = []
             #backup_sugg_val = [[]]
             #List_index_val = 0
             #print sub_weight_result_df_1_left
             #print sub_weight_result_df_1_right
             for weig_tab_lvl3 in xrange(0,len(sub_weight_result_df_1_left.index)):
                for crs_tab_lvl3 in xrange(0,len(ddnn)):
                     if (sub_weight_result_df_1_left.ix[weig_tab_lvl3,"Questions"] == ddnn.ix[crs_tab_lvl3,"questionPair_left"] and ddnn.ix[crs_tab_lvl3,"questionPair_right"] <= 9):
                         sugg_val_list_left_lvl3.append(ddnn.ix[crs_tab_lvl3,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_lvl3 = ",".join(map(str,sugg_val_list_left_lvl3))
                sub_weight_result_df_1_left.ix[weig_tab_lvl3,"Suggested_Numbers"] = result_lvl3
                del sugg_val_list_left_lvl3[:]
                #List_index_val        
             #print result
             #print sub_weight_result_df_1_left

             for weig_tab_1_lvl3 in xrange(0,len(sub_weight_result_df_1_right.index)):
                for crs_tab_1_lvl3 in xrange(0,len(ddnn_right)):
                     if (sub_weight_result_df_1_right.ix[weig_tab_1_lvl3,"Questions"] == ddnn_right.ix[crs_tab_1_lvl3,"questionPair_right"] and ddnn_right.ix[crs_tab_1_lvl3,"questionPair_left"] > 9):
                         sugg_val_list_right_lvl3.append(ddnn_right.ix[crs_tab_1_lvl3,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_lvl3 = ",".join(map(str,sugg_val_list_right_lvl3))
                sub_weight_result_df_1_right.ix[weig_tab_1_lvl3,"Suggested_Numbers"] = result_1_lvl3
                del sugg_val_list_right_lvl3[:]
                #List_index_val        
             #print sub_weight_result_df_1_right
             #print sub_weight_result_df_1_left
             sub_weight_result_df_1_left['#Suggested_Numbers'] = sub_weight_result_df_1_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             sub_weight_result_df_1_right['#Suggested_Numbers'] = sub_weight_result_df_1_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)

             for sw_1 in xrange(0,len(sub_weight_result_df_1_left.index)):
                  if ((sub_weight_result_df_1_left.ix[sw_1,'Suggested_Numbers'] == "" and sub_weight_result_df_1_left.ix[sw_1,'weights(%)'] < 10) or (sub_weight_result_df_1_left.ix[sw_1,'#Suggested_Numbers'] > 1 and sub_weight_result_df_1_left.ix[sw_1,'weights(%)'] < 10)):
                      sub_weight_result_df_1_left = sub_weight_result_df_1_left.drop(sw_1,0)
             #print sub_weight_result_df_1_left

             for sw in xrange(0,len(sub_weight_result_df_1_right.index)):
                  if ((sub_weight_result_df_1_right.ix[sw,'Suggested_Numbers'] == "" and sub_weight_result_df_1_right.ix[sw,'weights(%)'] < 10) or (sub_weight_result_df_1_right.ix[sw,'#Suggested_Numbers'] > 1 and sub_weight_result_df_1_right.ix[sw,'weights(%)'] < 10)):
                      sub_weight_result_df_1_right = sub_weight_result_df_1_right.drop(sw,0)
             #print sub_weight_result_df_1_right
             
             #for amg in xrange(0,len(sub_weight_result_df_1_right.index)):
             """
             for i in xrange(0,len(sub_weight_result_df_1_right["Suggested_Numbers"].index)):
                    sub_weight_result_df_1_right.loc[i, '#Suggested_Numbers'] = len(i.split(","))
             sub_weight_result_df_1_right = sub_weight_result_df_1_right.reset_index(drop=1)       
             print sub_weight_result_df_1_right       
             """
             sending_data_1= php_data(sub_weight_result_df_1_left,sub_weight_result_df_1_right,selectlvl)
             #print sending_data_1

         if (len(analysis_count_4_2_1) != 0 and len(analysis_count_4_2_2) != 0):
             #print "Helloo iam in the second loop of level 2"
             sub_weight_result_df_2_left = weights(Total_Wrongs,analysis_count_4_2_1,sub_weight_result_df_2_left)
             sub_weight_result_df_2_right = weights(Total_Wrongs,analysis_count_4_2_2,sub_weight_result_df_2_right)
            
             for q in xrange(0,len(sub_weight_result_df_2_left)):
                 sub_weight_result_df_2_left.ix[q,"Right_Question_Choice"] = 2
             for q in xrange(0,len(sub_weight_result_df_2_right)):
                 sub_weight_result_df_2_right.ix[q,"Left_Question_Choice"] = 2
             sugg_val_list_left_cas2_lvl3 = [] 
             sugg_val_list_right_cas2_lvl3 = []
             #print sub_weight_result_df_1_left
             #print sub_weight_result_df_1_right
             for weig_tab_22_lvl3 in xrange(0,len(sub_weight_result_df_2_left.index)):
                  for crs_tab_22_lvl3 in xrange(0,len(ddnn)):
                     if (sub_weight_result_df_2_left.ix[weig_tab_22_lvl3,"Questions"] == ddnn.ix[crs_tab_22_lvl3,"questionPair_left"] and ddnn.ix[crs_tab_22_lvl3,"questionPair_right"] > 9):
                         sugg_val_list_left_cas2_lvl3.append(ddnn.ix[crs_tab_22_lvl3,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                  result_cas2_lvl3= ",".join(map(str,sugg_val_list_left_cas2_lvl3))
                  sub_weight_result_df_2_left.ix[weig_tab_22_lvl3,"Suggested_Numbers"] = result_cas2_lvl3
                  #print sugg_val_list_left_cas2_lvl3
                  del sugg_val_list_left_cas2_lvl3[:]
                #List_index_val        
             
             #print sub_weight_result_df_2_left
             for weig_tab_1_22_lvl3 in xrange(0,len(sub_weight_result_df_2_right.index)):
                for crs_tab_1_22_lvl3 in xrange(0,len(ddnn_right)):
                     if (sub_weight_result_df_2_right.ix[weig_tab_1_22_lvl3,"Questions"] == ddnn_right.ix[crs_tab_1_22_lvl3,"questionPair_right"] and ddnn_right.ix[crs_tab_1_22_lvl3,"questionPair_left"] > 9):
                         sugg_val_list_right_cas2_lvl3.append(ddnn_right.ix[crs_tab_1_22_lvl3,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_cas2_lvl3= ",".join(map(str,sugg_val_list_right_cas2_lvl3))
                sub_weight_result_df_2_right.ix[weig_tab_1_22_lvl3,"Suggested_Numbers"] = result_1_cas2_lvl3
                del sugg_val_list_right_cas2_lvl3[:]
             
             #print sub_weight_result_df_2_left
             #print sub_weight_result_df_2_right
             sub_weight_result_df_2_left['#Suggested_Numbers'] = sub_weight_result_df_2_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             sub_weight_result_df_2_right['#Suggested_Numbers'] = sub_weight_result_df_2_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)

             for ab_1_lvl4 in xrange(0,len(sub_weight_result_df_2_left.index)):
                  if ((sub_weight_result_df_2_left.ix[ab_1_lvl4,'Suggested_Numbers'] == "" and sub_weight_result_df_2_left.ix[ab_1_lvl4,'weights(%)'] < 10) or (sub_weight_result_df_2_left.ix[ab_1_lvl4,'#Suggested_Numbers'] > 1  and sub_weight_result_df_2_left.ix[ab_1_lvl4,'weights(%)'] < 10)):
                      sub_weight_result_df_2_left = sub_weight_result_df_2_left.drop(ab_1_lvl4,0)
             #print sub_weight_result_df_2_left
             
             for ab_lvl4 in xrange(0,len(sub_weight_result_df_2_right.index)):
                  if ((sub_weight_result_df_2_right.ix[ab_lvl4,'Suggested_Numbers'] == "" and sub_weight_result_df_2_right.ix[ab_lvl4,'weights(%)'] < 10) or (sub_weight_result_df_2_right.ix[ab_lvl4,'#Suggested_Numbers'] > 1 and sub_weight_result_df_2_right.ix[ab_lvl4,'weights(%)'] < 10)):
                      sub_weight_result_df_2_right = sub_weight_result_df_2_right.drop(ab_lvl4,0)
             #print sub_weight_result_df_2_right
             
             sending_data_3 = php_data(sub_weight_result_df_2_left,sub_weight_result_df_2_right,selectlvl)
             #sending_data_4 = php_data(sub_weight_result_df_2_right,selectlvl)
             print sending_data_3  
         
         if (len(sending_data_1) !=0 and len(sending_data_3) !=0):
             
             d = {'a':sending_data_1, 'b':sending_data_3}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php
             
         elif (len(sending_data_1) == 0 and len(sending_data_3) !=0):
             
             d = {'a':sending_data_3}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php
                
         elif (len(sending_data_1) != 0 and len(sending_data_3) == 0):
             
             d = {'a':sending_data_1}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php
                     
      
    if (selectlvl[0] == 3):
    
         #print selectlvl
         analysis_count_3_1_1,analysis_count_3_1_2,dataframe_3_1,analysis_count_3_2_1,analysis_count_3_2_2,dataframe_3_2 = add_sub_analysis_lvl_3(lvl_data_df)
         #print analysis_count_3_1_1
         #print analysis_count_3_1_2
         #print analysis_count_3_2_1
         #print analysis_count_3_2_2
         #print dataframe_3_1
         #print dataframe_3_2
         sending_data_1 = pd.DataFrame()
         sending_data_3 = pd.DataFrame()
         """
         sub_lvl3_wrongs_1 = count_sub_lvl_3(dataframe_3_1,selectlvl,List_Wrongs)
         sub_lvl3_wrongs_2 = count_sub_lvl_3(dataframe_3_2,selectlvl,List_Wrongs)
         print sub_lvl3_wrongs_1
         print sub_lvl3_wrongs_2
         """
         """
         The weights function if called inorder to calculate the importance of each question by 
         diving the frequency of that partcular number with the number question which a student
         commited wrong at that particular level.
         """
         """
         Used to call the php_data function when after the calculatio of weights the dataframe
         is passed to the php_data function to squeeze the data into a dictonary
         """
         if (len(analysis_count_3_1_1) != 0 and len(analysis_count_3_1_2) != 0):

             sub_weight_result_df_1_left = weights(Total_Wrongs,analysis_count_3_1_1,sub_weight_result_df_1_left)
             sub_weight_result_df_1_right = weights(Total_Wrongs,analysis_count_3_1_2,sub_weight_result_df_1_right)
             for q in xrange(0,len(sub_weight_result_df_1_left)):
                 sub_weight_result_df_1_left.ix[q,"Right_Question_Choice"] = 1
             for q in xrange(0,len(sub_weight_result_df_1_right)):
                 sub_weight_result_df_1_right.ix[q,"Left_Question_Choice"] = 2
             sugg_val_list_left_lvl3 = [] 
             sugg_val_list_right_lvl3 = []
             #backup_sugg_val = [[]]
             #List_index_val = 0
             #print sub_weight_result_df_1_left
             #print sub_weight_result_df_1_right
             for weig_tab_lvl3 in xrange(0,len(sub_weight_result_df_1_left.index)):
                for crs_tab_lvl3 in xrange(0,len(ddnn)):
                     if (sub_weight_result_df_1_left.ix[weig_tab_lvl3,"Questions"] == ddnn.ix[crs_tab_lvl3,"questionPair_left"] and ddnn.ix[crs_tab_lvl3,"questionPair_right"] <= 9):
                         sugg_val_list_left_lvl3.append(ddnn.ix[crs_tab_lvl3,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_lvl3 = ",".join(map(str,sugg_val_list_left_lvl3))
                sub_weight_result_df_1_left.ix[weig_tab_lvl3,"Suggested_Numbers"] = result_lvl3
                del sugg_val_list_left_lvl3[:]
                #List_index_val        
             #print result
             #print sub_weight_result_df_1_left
             for weig_tab_1_lvl3 in xrange(0,len(sub_weight_result_df_1_right.index)):
                for crs_tab_1_lvl3 in xrange(0,len(ddnn_right)):
                     if (sub_weight_result_df_1_right.ix[weig_tab_1_lvl3,"Questions"] == ddnn_right.ix[crs_tab_1_lvl3,"questionPair_right"] and ddnn_right.ix[crs_tab_1_lvl3,"questionPair_left"] > 9):
                         sugg_val_list_right_lvl3.append(ddnn_right.ix[crs_tab_1_lvl3,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_lvl3 = ",".join(map(str,sugg_val_list_right_lvl3))
                sub_weight_result_df_1_right.ix[weig_tab_1_lvl3,"Suggested_Numbers"] = result_1_lvl3
                del sugg_val_list_right_lvl3[:]
                #List_index_val        
             #print result_1
             sub_weight_result_df_1_left['#Suggested_Numbers'] = sub_weight_result_df_1_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             sub_weight_result_df_1_right['#Suggested_Numbers'] = sub_weight_result_df_1_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)

             for sw_1 in xrange(0,len(sub_weight_result_df_1_left.index)):
                  if ((sub_weight_result_df_1_left.ix[sw_1,'Suggested_Numbers'] == "" and sub_weight_result_df_1_left.ix[sw_1,'weights(%)'] < 10) or (sub_weight_result_df_1_left.ix[sw_1,'#Suggested_Numbers'] > 1 and sub_weight_result_df_1_left.ix[sw_1,'weights(%)'] < 10)):
                      sub_weight_result_df_1_left = sub_weight_result_df_1_left.drop(sw_1,0)
             #print sub_weight_result_df_1_left
             for sw in xrange(0,len(sub_weight_result_df_1_right.index)):
                  if ((sub_weight_result_df_1_right.ix[sw,'Suggested_Numbers'] == "" and sub_weight_result_df_1_right.ix[sw,'weights(%)'] < 10) or (sub_weight_result_df_1_right.ix[sw,'#Suggested_Numbers'] > 1 and sub_weight_result_df_1_right.ix[sw,'weights(%)'] < 10)):
                      sub_weight_result_df_1_right = sub_weight_result_df_1_right.drop(sw,0)
             #print sub_weight_result_df_1_right
             
             #print sub_weight_result_df_1_left
             #print sub_weight_result_df_1_right
             sending_data_1= php_data(sub_weight_result_df_1_left,sub_weight_result_df_1_right,selectlvl)
             #sending_data_2 = php_data(sub_weight_result_df_1_right,selectlvl)
             print sending_data_1
             #print sending_data_2

         if (len(analysis_count_3_2_1) != 0 and len(analysis_count_3_2_2) != 0):
             
             sub_weight_result_df_2_left = weights(Total_Wrongs,analysis_count_3_2_1,sub_weight_result_df_2_left)
             sub_weight_result_df_2_right = weights(Total_Wrongs,analysis_count_3_2_2,sub_weight_result_df_2_right)
            
             for q in xrange(0,len(sub_weight_result_df_2_left)):
                 sub_weight_result_df_2_left.ix[q,"Right_Question_Choice"] = 2
             for q in xrange(0,len(sub_weight_result_df_2_right)):
                 sub_weight_result_df_2_right.ix[q,"Left_Question_Choice"] = 2
             sugg_val_list_left_cas2_lvl3 = [] 
             sugg_val_list_right_cas2_lvl3 = []
             #print sub_weight_result_df_1_left
             #print sub_weight_result_df_1_right
             for weig_tab_22_lvl3 in xrange(0,len(sub_weight_result_df_2_left.index)):
                  for crs_tab_22_lvl3 in xrange(0,len(ddnn)):
                     if (sub_weight_result_df_2_left.ix[weig_tab_22_lvl3,"Questions"] == ddnn.ix[crs_tab_22_lvl3,"questionPair_left"] and ddnn.ix[crs_tab_22_lvl3,"questionPair_right"] > 9):
                         sugg_val_list_left_cas2_lvl3.append(ddnn.ix[crs_tab_22_lvl3,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                  result_cas2_lvl3= ",".join(map(str,sugg_val_list_left_cas2_lvl3))
                  sub_weight_result_df_2_left.ix[weig_tab_22_lvl3,"Suggested_Numbers"] = result_cas2_lvl3
                  #print sugg_val_list_left_cas2_lvl3
                  del sugg_val_list_left_cas2_lvl3[:]
                #List_index_val        
             
             #print sub_weight_result_df_2_left
             for weig_tab_1_22_lvl3 in xrange(0,len(sub_weight_result_df_2_right.index)):
                for crs_tab_1_22_lvl3 in xrange(0,len(ddnn_right)):
                     if (sub_weight_result_df_2_right.ix[weig_tab_1_22_lvl3,"Questions"] == ddnn_right.ix[crs_tab_1_22_lvl3,"questionPair_right"] and ddnn_right.ix[crs_tab_1_22_lvl3,"questionPair_left"] > 9):
                         sugg_val_list_right_cas2_lvl3.append(ddnn_right.ix[crs_tab_1_22_lvl3,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_cas2_lvl3= ",".join(map(str,sugg_val_list_right_cas2_lvl3))
                sub_weight_result_df_2_right.ix[weig_tab_1_22_lvl3,"Suggested_Numbers"] = result_1_cas2_lvl3
                del sugg_val_list_right_cas2_lvl3[:]
             
             #print sub_weight_result_df_2_left
             #print sub_weight_result_df_2_right
             sub_weight_result_df_2_left['#Suggested_Numbers'] = sub_weight_result_df_2_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             sub_weight_result_df_2_right['#Suggested_Numbers'] = sub_weight_result_df_2_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)

             for ab_1_lvl3 in xrange(0,len(sub_weight_result_df_2_left.index)):
                  if ((sub_weight_result_df_2_left.ix[ab_1_lvl3,'Suggested_Numbers'] == "" and sub_weight_result_df_2_left.ix[ab_1_lvl3,'weights(%)'] < 10) or (sub_weight_result_df_2_left.ix[ab_1_lvl3,'#Suggested_Numbers'] > 1 and sub_weight_result_df_2_left.ix[ab_1_lvl3,'weights(%)'] < 10)):
                      sub_weight_result_df_2_left = sub_weight_result_df_2_left.drop(ab_1_lvl3,0)
             #print sub_weight_result_df_2_left
             for ab_lvl3 in xrange(0,len(sub_weight_result_df_2_right.index)):
                  if ((sub_weight_result_df_2_right.ix[ab_lvl3,'Suggested_Numbers'] == "" and sub_weight_result_df_2_right.ix[ab_lvl3,'weights(%)'] < 10 ) or (sub_weight_result_df_2_right.ix[ab_lvl3,'#Suggested_Numbers'] > 1 and sub_weight_result_df_2_right.ix[ab_lvl3,'weights(%)'] < 10)):
                      sub_weight_result_df_2_right = sub_weight_result_df_2_right.drop(ab_lvl3,0)
             #print sub_weight_result_df_2_left
             #print sub_weight_result_df_2_right
             
             sending_data_3 = php_data(sub_weight_result_df_2_left,sub_weight_result_df_2_right,selectlvl)
             #sending_data_4 = php_data(sub_weight_result_df_2_right,selectlvl)
             #print sending_data_3
      
         if (len(sending_data_1) !=0 and len(sending_data_3) !=0):
             
             d = {'a':sending_data_1, 'b':sending_data_3}
             #print d
             final_result_php = json.dumps(d)
             #print final_result_php
             
         elif (len(sending_data_1) == 0 and len(sending_data_3) !=0):
             
             d = {'a':sending_data_3}
             #print d
             final_result_php = json.dumps(d)
             #print final_result_php
             
         elif (len(sending_data_1) != 0 and len(sending_data_3) == 0):
             
             d = {'a':sending_data_1}
             #print d
             final_result_php = json.dumps(d)
             #print final_result_php    
    
    elif (selectlvl[0] == 2):
         #print lvl_data_df
         analysis_count_2_1_1,analysis_count_2_1_2,dataframe_2_1,analysis_count_2_2_1,analysis_count_2_2_2,dataframe_2_2 = add_sub_analysis_lvl_2(lvl_data_df)
         #print analysis_count_2_1_1
         #print analysis_count_2_1_2
         #print dataframe_2_1
         #print analysis_count_2_2_1
         #print analysis_count_2_2_2
         #print dataframe_2_2
         sending_data_1 = pd.DataFrame()
         sending_data_3 = pd.DataFrame()
         """
         sub_lvl2_wrongs_1 = count_sub_lvl_3(dataframe_2_1,selectlvl,List_Wrongs)
         sub_lvl2_wrongs_2 = count_sub_lvl_3(dataframe_2_2,selectlvl,List_Wrongs)
         print sub_lvl2_wrongs_1
         print sub_lvl2_wrongs_2
         """
         if (len(analysis_count_2_1_1) != 0 and len(analysis_count_2_1_2) != 0):

             sub_weight_result_df_1_left = weights(Total_Wrongs,analysis_count_2_1_1,sub_weight_result_df_1_left)
             sub_weight_result_df_1_right = weights(Total_Wrongs,analysis_count_2_1_2,sub_weight_result_df_1_right)
             
             for q in xrange(0,len(sub_weight_result_df_1_left)):
                 sub_weight_result_df_1_left.ix[q,"Right_Question_Choice"] = 1
             for q in xrange(0,len(sub_weight_result_df_1_right)):
                 sub_weight_result_df_1_right.ix[q,"Left_Question_Choice"] = 2
             sugg_val_list_left = [] 
             sugg_val_list_right = []
             backup_sugg_val = [[]]
             List_index_val = 0
             #print sub_weight_result_df_1_left
             #print sub_weight_result_df_1_right
             for weig_tab in xrange(0,len(sub_weight_result_df_1_left.index)):
                for crs_tab in xrange(0,len(ddnn)):
                     if (sub_weight_result_df_1_left.ix[weig_tab,"Questions"] == ddnn.ix[crs_tab,"questionPair_left"] and ddnn.ix[crs_tab,"questionPair_right"] < 10):
                         sugg_val_list_left.append(ddnn.ix[crs_tab,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result= ",".join(map(str,sugg_val_list_left))
                sub_weight_result_df_1_left.ix[weig_tab,"Suggested_Numbers"] = result
                del sugg_val_list_left[:]
                #List_index_val        
             #print result
             #print sub_weight_result_df_1_left
             for weig_tab_1 in xrange(0,len(sub_weight_result_df_1_right.index)):
                for crs_tab_1 in xrange(0,len(ddnn_right)):
                     if (sub_weight_result_df_1_right.ix[weig_tab_1,"Questions"] == ddnn_right.ix[crs_tab_1,"questionPair_right"] and ddnn_right.ix[crs_tab_1,"questionPair_left"] > 9):
                         sugg_val_list_right.append(ddnn_right.ix[crs_tab_1,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1= ",".join(map(str,sugg_val_list_right))
                sub_weight_result_df_1_right.ix[weig_tab_1,"Suggested_Numbers"] = result_1
                del sugg_val_list_right[:]
                #List_index_val        
             #print result_1
             #print sub_weight_result_df_1_right
             sub_weight_result_df_1_left['#Suggested_Numbers'] = sub_weight_result_df_1_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             sub_weight_result_df_1_right['#Suggested_Numbers'] = sub_weight_result_df_1_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)

             for sw_1 in xrange(0,len(sub_weight_result_df_1_left.index)):
                  if ((sub_weight_result_df_1_left.ix[sw_1,'Suggested_Numbers'] == "" and sub_weight_result_df_1_left.ix[sw_1,'weights(%)'] < 10) or (sub_weight_result_df_1_left.ix[sw_1,'#Suggested_Numbers'] > 1 and sub_weight_result_df_1_left.ix[sw_1,'weights(%)'] < 10)):
                      sub_weight_result_df_1_left = sub_weight_result_df_1_left.drop(sw_1,0)
             #print sub_weight_result_df_1_left
             for sw in xrange(0,len(sub_weight_result_df_1_right.index)):
                  if ((sub_weight_result_df_1_right.ix[sw,'Suggested_Numbers'] == "" and sub_weight_result_df_1_right.ix[sw,'weights(%)'] < 10) or (sub_weight_result_df_1_right.ix[sw,'#Suggested_Numbers'] > 1 and sub_weight_result_df_1_right.ix[sw,'weights(%)'] < 10)):
                      sub_weight_result_df_1_right = sub_weight_result_df_1_right.drop(sw,0)
             #print sub_weight_result_df_1_right
             #print "About to call th function"
             sending_data_1 = php_data(sub_weight_result_df_1_left,sub_weight_result_df_1_right,selectlvl)
             #sending_data_2 = php_data(sub_weight_result_df_1_right,selectlvl)
             #print sending_data_1
             #print sending_data_2

         if (len(analysis_count_2_2_2) != 0 and len(analysis_count_2_2_2) != 0):
              
              sub_weight_result_df_2_left = weights(Total_Wrongs,analysis_count_2_2_1,sub_weight_result_df_2_left)
              sub_weight_result_df_2_right = weights(Total_Wrongs,analysis_count_2_2_2,sub_weight_result_df_2_right)
              
              for q in xrange(0,len(sub_weight_result_df_2_left)):
                  sub_weight_result_df_2_left.ix[q,"Right_Question_Choice"] = 1
              for q in xrange(0,len(sub_weight_result_df_2_right)):
                  sub_weight_result_df_2_right.ix[q,"Left_Question_Choice"] = 1
              sugg_val_list_left_cas2 = [] 
              sugg_val_list_right_cas2 = []
              backup_sugg_val = [[]]
              List_index_val = 0
              #print sub_weight_result_df_1_left
              #print sub_weight_result_df_1_right
              for weig_tab_22 in xrange(0,len(sub_weight_result_df_2_left.index)):
                  for crs_tab_22 in xrange(0,len(ddnn)):
                     if (sub_weight_result_df_2_left.ix[weig_tab_22,"Questions"] == ddnn.ix[crs_tab_22,"questionPair_left"] and ddnn.ix[crs_tab_22,"questionPair_right"] < 10):
                         sugg_val_list_left_cas2.append(ddnn.ix[crs_tab_22,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                  result_cas2= ",".join(map(str,sugg_val_list_left_cas2))
                  sub_weight_result_df_2_left.ix[weig_tab_22,"Suggested_Numbers"] = result_cas2
                  del sugg_val_list_left_cas2[:]
                #List_index_val        
              #print result
              #print sub_weight_result_df_1_left
              for weig_tab_1_22 in xrange(0,len(sub_weight_result_df_2_right.index)):
                for crs_tab_1_22 in xrange(0,len(ddnn_right)):
                     if (sub_weight_result_df_2_right.ix[weig_tab_1_22,"Questions"] == ddnn_right.ix[crs_tab_1_22,"questionPair_right"] and ddnn_right.ix[crs_tab_1_22,"questionPair_left"] < 10):
                         sugg_val_list_right_cas2.append(ddnn_right.ix[crs_tab_1_22,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_cas2= ",".join(map(str,sugg_val_list_right_cas2))
                sub_weight_result_df_2_right.ix[weig_tab_1_22,"Suggested_Numbers"] = result_1_cas2
                del sugg_val_list_right_cas2[:]
             
              #print sub_weight_result_df_2_left
              #print sub_weight_result_df_2_right
              
              sub_weight_result_df_2_left['#Suggested_Numbers'] = sub_weight_result_df_2_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
              sub_weight_result_df_2_right['#Suggested_Numbers'] = sub_weight_result_df_2_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)

              for ab_1 in xrange(0,len(sub_weight_result_df_2_left.index)):
                  if ((sub_weight_result_df_2_left.ix[ab_1,'Suggested_Numbers'] == "" and sub_weight_result_df_2_left.ix[ab_1,'weights(%)'] < 10)  or (sub_weight_result_df_2_left.ix[ab_1,'#Suggested_Numbers'] > 1 and sub_weight_result_df_2_left.ix[ab_1,'weights(%)'] < 10)):
                      sub_weight_result_df_2_left = sub_weight_result_df_2_left.drop(ab_1,0)
              #print sub_weight_result_df_2_left
              for ab in xrange(0,len(sub_weight_result_df_2_right.index)):
                  if ((sub_weight_result_df_2_right.ix[ab,'Suggested_Numbers'] == "" and sub_weight_result_df_2_right.ix[ab,'weights(%)'] < 10)  or (sub_weight_result_df_2_right.ix[ab,'#Suggested_Numbers'] > 1 and sub_weight_result_df_2_right.ix[ab,'weights(%)'] < 10)):
                      sub_weight_result_df_2_right = sub_weight_result_df_2_right.drop(ab,0)
              #print sub_weight_result_df_2_right
              sending_data_3 = php_data(sub_weight_result_df_2_left,sub_weight_result_df_2_right,selectlvl)
              #print sending_data_3

              
         if (len(sending_data_1) !=0 and len(sending_data_3) !=0):
             
             d = {'a':sending_data_1, 'b':sending_data_3}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php
                 
         elif (len(sending_data_1) == 0 and len(sending_data_3) !=0):
             
             d = {'a':sending_data_3}
             # print d
             final_result_php = json.dumps(d)
             print final_result_php
                 
         elif (len(sending_data_1) != 0 and len(sending_data_3) == 0):
             
             d = {'a':sending_data_1}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php   
                 
             
    elif (selectlvl[0] == 1):    
        analysis_count_1_1,analysis_count_1_2,dataframe_1 = add_sub_analysis_lvl_1(lvl_data_df)
        #sub_lvl1_wrongs_1 = count_sub_lvl_3(dataframe_2_1,selectlvl,List_Wrongs)
        #print sub_lvl1_wrongs_1
        sub_weight_result_df_1_left = weights(Total_Wrongs,analysis_count_1_1,sub_weight_result_df_1_left)
        sub_weight_result_df_1_right = weights(Total_Wrongs,analysis_count_1_2,sub_weight_result_df_1_right)
        for q in xrange(0,len(sub_weight_result_df_1_left.index)):
            sub_weight_result_df_1_left.ix[q,"Right_Question_Choice"] = 1
        for q in xrange(0,len(sub_weight_result_df_1_right.index)):
            sub_weight_result_df_1_right.ix[q,"Left_Question_Choice"] = 1
        sugg_val_list_left_cas1_lvl1 = [] 
        sugg_val_list_right_cas1_lvl1 = []
        #print sub_weight_result_df_2_left
        #print sub_weight_result_df_1_right
        for weig_tab_22_lvl3 in xrange(0,len(sub_weight_result_df_1_left.index)):
                  for crs_tab_22_lvl3 in xrange(0,len(ddnn)):
                     if (sub_weight_result_df_1_left.ix[weig_tab_22_lvl3,"Questions"] == ddnn.ix[crs_tab_22_lvl3,"questionPair_left"] and ddnn.ix[crs_tab_22_lvl3,"questionPair_right"] < 10):
                         sugg_val_list_left_cas1_lvl1.append(ddnn.ix[crs_tab_22_lvl3,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                  result_cas2_lvl1= ",".join(map(str,sugg_val_list_left_cas1_lvl1))
                  sub_weight_result_df_1_left.ix[weig_tab_22_lvl3,"Suggested_Numbers"] = result_cas2_lvl1
                  #print sugg_val_list_left_cas1_lvl1
                  del sugg_val_list_left_cas1_lvl1[:]
                #List_index_val        
             
       #print sub_weight_result_df_1_left
        for weig_tab_1_22_lvl3 in xrange(0,len(sub_weight_result_df_1_right.index)):
                for crs_tab_1_22_lvl3 in xrange(0,len(ddnn_right)):
                     if (sub_weight_result_df_1_right.ix[weig_tab_1_22_lvl3,"Questions"] == ddnn_right.ix[crs_tab_1_22_lvl3,"questionPair_right"] and ddnn_right.ix[crs_tab_1_22_lvl3,"questionPair_left"] < 10):
                         sugg_val_list_right_cas1_lvl1.append(ddnn_right.ix[crs_tab_1_22_lvl3,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_cas2_lvl1= ",".join(map(str,sugg_val_list_right_cas1_lvl1))
                sub_weight_result_df_1_right.ix[weig_tab_1_22_lvl3,"Suggested_Numbers"] = result_1_cas2_lvl1
                del sugg_val_list_right_cas1_lvl1[:]
             
        #print sub_weight_result_df_1_right
        #print sub_weight_result_df_1_left
        
        sub_weight_result_df_1_left['#Suggested_Numbers'] = sub_weight_result_df_1_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
        sub_weight_result_df_1_right['#Suggested_Numbers'] = sub_weight_result_df_1_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)

        for ab_1_lvl1 in xrange(0,len(sub_weight_result_df_1_left.index)):
                  if ((sub_weight_result_df_1_left.ix[ab_1_lvl1,'Suggested_Numbers'] == "" and sub_weight_result_df_1_left.ix[ab_1_lvl1,'weights(%)'] < 10) or (sub_weight_result_df_1_left.ix[ab_1_lvl1,'#Suggested_Numbers'] > 1 and sub_weight_result_df_1_left.ix[ab_1_lvl1,'weights(%)'] < 10)):
                      sub_weight_result_df_1_left = sub_weight_result_df_1_left.drop(ab_1_lvl1,0)
                      
  
        
        for ab_lvl1 in xrange(0,len(sub_weight_result_df_1_right.index)):
                  if ((sub_weight_result_df_1_right.ix[ab_lvl1,'Suggested_Numbers'] == "" and sub_weight_result_df_1_right.ix[ab_lvl1,'weights(%)'] < 10) or (sub_weight_result_df_1_right.ix[ab_lvl1,'#Suggested_Numbers'] > 1 and sub_weight_result_df_1_right.ix[ab_lvl1,'weights(%)'] < 10)):
                      sub_weight_result_df_1_right = sub_weight_result_df_1_right.drop(ab_lvl1,0)
             
        #print sub_weight_result_df_1_left
        #print sub_weight_result_df_1_right
        sending_data_1 = php_data(sub_weight_result_df_1_left,sub_weight_result_df_1_right,selectlvl)
        #sending_data_2 = php_data(sub_weight_result_df_1_right,selectlvl)
        #print sending_data_1
        if (len(sending_data_1) !=0):
             
             d = {'a':sending_data_1}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php
                  

"""
When the operation requested for is multiplication then the below loop if loop is executed 
"""

if (mathop==3):
    
    #print nw_tmp_updt_df
    mul_df = pd.DataFrame([0]) 
    for lvl_v in range(len(selectlvl)): 
        for it_1 in xrange(0,len(nw_tmp_updt_df)):
            if (nw_tmp_updt_df.ix[it_1,"selectedLevel"]  == selectlvl[lvl_v] and nw_tmp_updt_df.ix[it_1,"mathOperator"] == mathop):
                mul_df = mul_df.append(nw_tmp_updt_df.ix[[it_1]],ignore_index=True)
    mul_df = mul_df.drop(0,0)
    mul_df = mul_df.drop(0,1).reset_index(drop=1)            
    #print mul_df    
    mul_weight_res_left = pd.DataFrame(['weights(%)'])
    mul_weight_res_right = pd.DataFrame(['weights(%)'])
    my_list_2['questionPair_left'], my_list_2['questionPair_right'] = zip(*my_list_2['questionPair'].map(lambda x: x.split(',')))
    my_list_2[['questionPair_left', 'questionPair_right']] = my_list_2[['questionPair_left', 'questionPair_right']].astype(int)
    my_list_2["selectedLevel"]=my_list_2["selectedLevel"].apply(pd.to_numeric)
    for new_v_1 in xrange(0,len(my_list_2.index)):
        if (my_list_2.ix[new_v_1,'selectedLevel'] != selectlvl[0] or  my_list_2.ix[new_v_1,'mathOperator'] != mathop):
            my_list_2 = my_list_2.drop(new_v_1,0)
    my_list_2 = my_list_2.reset_index(drop=1)
    my_list_2 = my_list_2.groupby(['questionPair_left','questionPair_right']).size().reset_index()
    my_list_2 = my_list_2.rename(columns={0: 'Counts'})
    my_list_2 = my_list_2.sort_values(by=['Counts'],ascending=[False]).reset_index(drop=1)
    #print my_list_2
    for count_thresh in xrange(0,len(my_list_2.index)):
        if (my_list_2.ix[count_thresh,"Counts"] < 10 ):
            my_list_2 = my_list_2.drop(count_thresh,0)
    my_list_2 = my_list_2.reset_index(drop = 1)
    #print my_list_2    
    zzzz = my_list_2[[0,1,2]].astype(str)
    ddnn = pd.crosstab([zzzz.questionPair_left,zzzz.questionPair_right],zzzz.Counts,margins=True)
    ddnn_right = pd.crosstab([zzzz.questionPair_right,zzzz.questionPair_left],zzzz.Counts,margins=True)
    #p1 = numpy.polyfit(new_temp_my_list.questionPair_left,new_temp_my_list.questionPair_right,1)
    #print ddnn
    #print p1
    ddnn = ddnn.reset_index()
    ddnn_right = ddnn_right.reset_index()
    #print ddnn
    ddnn = ddnn.drop(ddnn.index[len(ddnn)-1])
    ddnn_right = ddnn_right.drop(ddnn_right.index[len(ddnn_right)-1])
    #print ddnn    
    #print ddnn_right
    #ddnn = ddnn.drop(ddnn.index[len(ddnn)-1])

    ddnn = ddnn.apply(pd.to_numeric)
    ddnn_right = ddnn_right.apply(pd.to_numeric)
    
    mul_anly_df_1,mul_anly_df_2,muldf = mul_analy_fun(mul_df)
    #print mul_anly_df_1
    #print mul_anly_df_2
    #print muldf
    mul_weight_res_right = weights(Total_Wrongs,mul_anly_df_2,mul_weight_res_right)
    #print mul_weight_res_left
    #print mul_weight_res_right
    for q in xrange(0,len(mul_weight_res_right)):
        if (selectlvl[0] <= 9):
           mul_weight_res_right.ix[q,"Left_Question_Choice"] = 1
        else:
           mul_weight_res_right.ix[q,"Left_Question_Choice"] = 2
    
    sugg_val_list_mul = [] 
    sugg_val_list_mul_1 = []
    backup_sugg_val = [[]]
    List_index_val = 0
    #print sub_weight_result_df_1_left
    #print sub_weight_result_df_1_right       
    #print mul_weight_res_right
    sub_return_list_1 = []

    for w_1_3 in xrange(0,len(mul_weight_res_right.index)):
        if (mul_weight_res_right.ix[w_1_3,"weights(%)"] > 9):
            iam_temp = mul_weight_res_right.ix[w_1_3,"Questions"]
            sub_return_list_1.append(iam_temp)
        
    if (len(mul_weight_res_right) !=0):
             
             d = {'a':sub_return_list_1}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php
                 
"""
When the operation requested for is Division then the below loop if loop is executed 
"""

if(mathop==4):
    div_df = pd.DataFrame([0]) 
    #print nw_tmp_updt_df
    for lvl_v in range(len(selectlvl)): 
        for it_1 in xrange(0,len(nw_tmp_updt_df)):
            if (nw_tmp_updt_df.ix[it_1,"selectedLevel"]  == selectlvl[lvl_v] and nw_tmp_updt_df.ix[it_1,"mathOperator"] == mathop):
                div_df = div_df.append(nw_tmp_updt_df.ix[[it_1]],ignore_index=True)
    div_df = div_df.drop(0,0)
    div_df = div_df.drop(0,1).reset_index(drop=1)            
    #print div_df    
    div_weight_res_left = pd.DataFrame(['weights(%)'])
    div_weight_res_right = pd.DataFrame(['weights(%)'])
    my_list_2 = my_list_2.reset_index(drop=1)
    my_list_2 = my_list_2.groupby(['questionPair_left','questionPair_right']).size().reset_index()
    my_list_2 = my_list_2.rename(columns={0: 'Counts'})
    my_list_2 = my_list_2.sort_values(by=['Counts'],ascending=[False]).reset_index(drop=1)
    #print my_list_2
    for count_thresh in xrange(0,len(my_list_2.index)):
        if (my_list_2.ix[count_thresh,"Counts"] < 10 ):
            my_list_2 = my_list_2.drop(count_thresh,0)
    my_list_2 = my_list_2.reset_index(drop = 1)
    #print my_list_2    
    zzzz = my_list_2[[0,1,2]].astype(str)
    ddnn = pd.crosstab([zzzz.questionPair_left,zzzz.questionPair_right],zzzz.Counts,margins=True)
    ddnn_right = pd.crosstab([zzzz.questionPair_right,zzzz.questionPair_left],zzzz.Counts,margins=True)
    #p1 = numpy.polyfit(new_temp_my_list.questionPair_left,new_temp_my_list.questionPair_right,1)
    #print ddnn
    #print p1
    ddnn = ddnn.reset_index()
    ddnn_right = ddnn_right.reset_index()
    #print ddnn
    ddnn = ddnn.drop(ddnn.index[len(ddnn)-1])
    ddnn_right = ddnn_right.drop(ddnn_right.index[len(ddnn_right)-1])
    #print ddnn    
    #print ddnn_right
    #ddnn = ddnn.drop(ddnn.index[len(ddnn)-1])

    ddnn = ddnn.apply(pd.to_numeric)
    ddnn_right = ddnn_right.apply(pd.to_numeric)
    
    div_anly_df_1,div_anly_df_2,divdf = div_analy_fun(div_df)
    #print mul_weight_res_right  
    #print mul_weight_res_left
    div_weight_res_left = weights(Total_Wrongs,div_anly_df_1,div_weight_res_left)
    div_weight_res_right = weights(Total_Wrongs,div_anly_df_2,div_weight_res_right)
    for q in xrange(0,len(div_weight_res_left)):
         if (selectlvl[0] <= 9):
           div_weight_res_right.ix[q,"Left_Question_Choice"] = 1
         else:
           div_weight_res_right.ix[q,"Left_Question_Choice"] = 2

    div_sending_data_1 = php_data(div_weight_res_left,div_weight_res_right,selectlvl)
    #print div_anly_df_1
    #print div_anly_df_2
    #print divdf
    #div_weight_res_left = weights(Total_Wrongs,div_anly_df_1,div_weight_res_right)
    #print div_weight_res_left   
    #div_sending_data_lvl_3_2_1= php_data(div_weight_res_left,div_weight_result_df_2_right,selectlvl)
    #print sub_weight_result_df_1_left
    #print sub_weight_result_df_1_right       
    #print mul_weight_res_right
    return_list_1_div = []

    for w_div in xrange(0,len(div_weight_res_left.index)):
        if (div_weight_res_left.ix[w_div,"weights(%)"] > 9):
            iam_temp = div_weight_res_left.ix[w_div,"Questions"]
            return_list_1_div.append(iam_temp)
        
    if (len(div_weight_res_left) !=0):
             
             d = {'a':return_list_1_div}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php


"""
When the operation requested for is Addition then the below loop if loop is executed 
"""  

if(mathop==1):
    
    add_df = pd.DataFrame([0]) 
    for lvl_v in range(len(selectlvl)): 
        for it_1 in xrange(0,len(nw_tmp_updt_df)):
            if (nw_tmp_updt_df.ix[it_1,"selectedLevel"]  == selectlvl[lvl_v] and nw_tmp_updt_df.ix[it_1,"mathOperator"] == mathop):
                add_df = add_df.append(nw_tmp_updt_df.ix[[it_1]],ignore_index=True)
    add_df = add_df.drop(0,0)
    add_df = add_df.drop(0,1).reset_index(drop=1)            
    #print add_df    
    add_weight_result_df_1_left = pd.DataFrame(['weights(%)'])
    add_weight_result_df_1_right = pd.DataFrame(['weights(%)'])
    add_weight_result_df_2_left = pd.DataFrame(['weights(%)'])
    add_weight_result_df_2_right = pd.DataFrame(['weights(%)'])
    add_weight_result_df_3_left = pd.DataFrame(['weights(%)'])
    add_weight_result_df_3_right = pd.DataFrame(['weights(%)'])
    add_weight_result_df_4_left = pd.DataFrame(['weights(%)'])
    add_weight_result_df_4_right = pd.DataFrame(['weights(%)'])
    my_list_2['questionPair_left'], my_list_2['questionPair_right'] = zip(*my_list_2['questionPair'].map(lambda x: x.split(',')))
    my_list_2[['questionPair_left', 'questionPair_right']] = my_list_2[['questionPair_left', 'questionPair_right']].astype(int)
    my_list_2["selectedLevel"]=my_list_2["selectedLevel"].apply(pd.to_numeric)
    for new_v_1 in xrange(0,len(my_list_2.index)):
        if (my_list_2.ix[new_v_1,'selectedLevel'] != selectlvl[0] or  my_list_2.ix[new_v_1,'mathOperator'] != mathop):
            my_list_2 = my_list_2.drop(new_v_1,0)
    my_list_2 = my_list_2.reset_index(drop=1)
    my_list_2 = my_list_2.groupby(['questionPair_left','questionPair_right']).size().reset_index()
    my_list_2 = my_list_2.rename(columns={0: 'Counts'})
    my_list_2 = my_list_2.sort_values(by=['Counts'],ascending=[False]).reset_index(drop=1)
    #print my_list_2
    for count_thresh in xrange(0,len(my_list_2.index)):
        if (my_list_2.ix[count_thresh,"Counts"] < 10 ):
            my_list_2 = my_list_2.drop(count_thresh,0)
    my_list_2 = my_list_2.reset_index(drop = 1)
    #print my_list_2    
    zzzz = my_list_2[[0,1,2]].astype(str)
    ddnn = pd.crosstab([zzzz.questionPair_left,zzzz.questionPair_right],zzzz.Counts,margins=True)
    ddnn_right = pd.crosstab([zzzz.questionPair_right,zzzz.questionPair_left],zzzz.Counts,margins=True)
    #p1 = numpy.polyfit(new_temp_my_list.questionPair_left,new_temp_my_list.questionPair_right,1)
    #print ddnn
    #print p1
    ddnn = ddnn.reset_index()
    ddnn_right = ddnn_right.reset_index()
    #print ddnn
    ddnn = ddnn.drop(ddnn.index[len(ddnn)-1])
    ddnn_right = ddnn_right.drop(ddnn_right.index[len(ddnn_right)-1])
    #print ddnn    
    #print ddnn_right
    #ddnn = ddnn.drop(ddnn.index[len(ddnn)-1])

    ddnn = ddnn.apply(pd.to_numeric)
    ddnn_right = ddnn_right.apply(pd.to_numeric)
    """
    Based on the level requested for we go into that particular loop and analyse the problems and 
    later calicluate the weights for left and right question with the total no of wrongs 
    commited at that particular level
    """
    """
    When requested level is 3 then the following loop present below is executed
    """
    if (selectlvl[0] == 4):
         add_analysis_count_4_1_1,add_analysis_count_4_1_2,add_dataframe_4_1,add_analysis_count_4_2_1,add_analysis_count_4_2_2,add_dataframe_4_2 = add_sub_analysis_lvl_4(add_df)
         #print add_analysis_count_4_1_1
         #print add_analysis_count_4_1_2
         #print add_analysis_count_4_2_1
         #print add_analysis_count_4_2_2
         #print add_dataframe_4_1
         #print add_dataframe_4_2
         sending_data_1 = pd.DataFrame()
         sending_data_3 = pd.DataFrame()
         if (len(add_analysis_count_4_1_1) != 0 and len(add_analysis_count_4_1_2) != 0):

             add_weight_result_df_1_left = weights(Total_Wrongs,add_analysis_count_4_1_1,add_weight_result_df_1_left)
             add_weight_result_df_1_right = weights(Total_Wrongs,add_analysis_count_4_1_2,add_weight_result_df_1_right)
             for q in xrange(0,len(add_weight_result_df_1_left)):
                 add_weight_result_df_1_left.ix[q,"Right_Question_Choice"] = 1
             for q in xrange(0,len(add_weight_result_df_1_right)):
                 add_weight_result_df_1_right.ix[q,"Left_Question_Choice"] = 2
             sugg_val_list_left_lvl3 = [] 
             sugg_val_list_right_lvl3 = []
             #backup_sugg_val = [[]]
             #List_index_val = 0
             #print add_weight_result_df_1_left
             #print add_weight_result_df_1_right
             for weig_tab_lvl3 in xrange(0,len(add_weight_result_df_1_left.index)):
                for crs_tab_lvl3 in xrange(0,len(ddnn)):
                     if (add_weight_result_df_1_left.ix[weig_tab_lvl3,"Questions"] == ddnn.ix[crs_tab_lvl3,"questionPair_left"] and ddnn.ix[crs_tab_lvl3,"questionPair_right"] <= 9 ):
                         sugg_val_list_left_lvl3.append(ddnn.ix[crs_tab_lvl3,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_lvl3 = ",".join(map(str,sugg_val_list_left_lvl3))
                add_weight_result_df_1_left.ix[weig_tab_lvl3,"Suggested_Numbers"] = result_lvl3
                del sugg_val_list_left_lvl3[:]
                #List_index_val        
             #print result
             #print sub_weight_result_df_1_left

             for weig_tab_1_lvl3 in xrange(0,len(add_weight_result_df_1_right.index)):
                for crs_tab_1_lvl3 in xrange(0,len(ddnn_right)):
                     if (add_weight_result_df_1_right.ix[weig_tab_1_lvl3,"Questions"] == ddnn_right.ix[crs_tab_1_lvl3,"questionPair_right"] and ddnn_right.ix[crs_tab_1_lvl3,"questionPair_left"] > 9):
                         sugg_val_list_right_lvl3.append(ddnn_right.ix[crs_tab_1_lvl3,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_lvl3 = ",".join(map(str,sugg_val_list_right_lvl3))
                add_weight_result_df_1_right.ix[weig_tab_1_lvl3,"Suggested_Numbers"] = result_1_lvl3
                del sugg_val_list_right_lvl3[:]
                #List_index_val        
             #print sub_weight_result_df_1_right
             add_weight_result_df_1_left['#Suggested_Numbers'] = add_weight_result_df_1_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             add_weight_result_df_1_right['#Suggested_Numbers'] = add_weight_result_df_1_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)

             for sw_1 in xrange(0,len(add_weight_result_df_1_left.index)):
                  if ((add_weight_result_df_1_left.ix[sw_1,'Suggested_Numbers'] == "" and add_weight_result_df_1_left.ix[sw_1,'weights(%)'] < 10) or (add_weight_result_df_1_left.ix[sw_1,'#Suggested_Numbers'] > 1 and add_weight_result_df_1_left.ix[sw_1,'weights(%)'] < 10)):
                      add_weight_result_df_1_left = add_weight_result_df_1_left.drop(sw_1,0)
             #print sub_weight_result_df_1_left

             for sw in xrange(0,len(add_weight_result_df_1_right.index)):
                  if ((add_weight_result_df_1_right.ix[sw,'Suggested_Numbers'] == "" and add_weight_result_df_1_right.ix[sw,'weights(%)'] < 10) or (add_weight_result_df_1_right.ix[sw,'#Suggested_Numbers'] > 1 and add_weight_result_df_1_right.ix[sw,'weights(%)'] < 10)):
                      add_weight_result_df_1_right = add_weight_result_df_1_right.drop(sw,0)
             #print sub_weight_result_df_1_right
             
             #for amg in xrange(0,len(sub_weight_result_df_1_right.index)):
             """
             for i in xrange(0,len(sub_weight_result_df_1_right["Suggested_Numbers"].index)):
                    sub_weight_result_df_1_right.loc[i, '#Suggested_Numbers'] = len(i.split(","))
             sub_weight_result_df_1_right = sub_weight_result_df_1_right.reset_index(drop=1)       
             print sub_weight_result_df_1_right       
             """
             sending_data_1= php_data(add_weight_result_df_1_left,add_weight_result_df_1_right,selectlvl)
             #print sending_data_1

         if (len(add_analysis_count_4_2_1) != 0 and len(add_analysis_count_4_2_2) != 0):
             #print "Helloo iam in the second loop of level 2"
             add_weight_result_df_2_left = weights(Total_Wrongs,add_analysis_count_4_2_1,add_weight_result_df_2_left)
             add_weight_result_df_2_right = weights(Total_Wrongs,add_analysis_count_4_2_2,add_weight_result_df_2_right)
            
             for q in xrange(0,len(add_weight_result_df_2_left)):
                 add_weight_result_df_2_left.ix[q,"Right_Question_Choice"] = 2
             for q in xrange(0,len(add_weight_result_df_2_right)):
                 add_weight_result_df_2_right.ix[q,"Left_Question_Choice"] = 2
             sugg_val_list_left_cas2_lvl3 = [] 
             sugg_val_list_right_cas2_lvl3 = []
             #print add_weight_result_df_2_left
             #print add_weight_result_df_2_right
             for weig_tab_22_lvl3 in xrange(0,len(add_weight_result_df_2_left.index)):
                  for crs_tab_22_lvl3 in xrange(0,len(ddnn)):
                     if (add_weight_result_df_2_left.ix[weig_tab_22_lvl3,"Questions"] == ddnn.ix[crs_tab_22_lvl3,"questionPair_left"] and ddnn.ix[crs_tab_22_lvl3,"questionPair_right"] > 9):
                         sugg_val_list_left_cas2_lvl3.append(ddnn.ix[crs_tab_22_lvl3,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                  result_cas2_lvl3= ",".join(map(str,sugg_val_list_left_cas2_lvl3))
                  add_weight_result_df_2_left.ix[weig_tab_22_lvl3,"Suggested_Numbers"] = result_cas2_lvl3
                  #print sugg_val_list_left_cas2_lvl3
                  del sugg_val_list_left_cas2_lvl3[:]
                #List_index_val        
             
             #print add_weight_result_df_2_left
             for weig_tab_1_22_lvl3 in xrange(0,len(add_weight_result_df_2_right.index)):
                for crs_tab_1_22_lvl3 in xrange(0,len(ddnn_right)):
                     if (add_weight_result_df_2_right.ix[weig_tab_1_22_lvl3,"Questions"] == ddnn_right.ix[crs_tab_1_22_lvl3,"questionPair_right"] and ddnn_right.ix[crs_tab_1_22_lvl3,"questionPair_left"] > 9):
                         sugg_val_list_right_cas2_lvl3.append(ddnn_right.ix[crs_tab_1_22_lvl3,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_cas2_lvl3= ",".join(map(str,sugg_val_list_right_cas2_lvl3))
                add_weight_result_df_2_right.ix[weig_tab_1_22_lvl3,"Suggested_Numbers"] = result_1_cas2_lvl3
                del sugg_val_list_right_cas2_lvl3[:]
             
             #print add_weight_result_df_2_left
             #print add_weight_result_df_2_right
             add_weight_result_df_2_left['#Suggested_Numbers'] = add_weight_result_df_2_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             add_weight_result_df_2_right['#Suggested_Numbers'] = add_weight_result_df_2_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)

             for ab_1_lvl4 in xrange(0,len(add_weight_result_df_2_left.index)):
                  if ((add_weight_result_df_2_left.ix[ab_1_lvl4,'Suggested_Numbers'] == "" and add_weight_result_df_2_left.ix[ab_1_lvl4,'weights(%)'] < 10) or (add_weight_result_df_2_left.ix[ab_1_lvl4,'#Suggested_Numbers'] > 1  and add_weight_result_df_2_left.ix[ab_1_lvl4,'weights(%)'] < 10)):
                      add_weight_result_df_2_left = add_weight_result_df_2_left.drop(ab_1_lvl4,0)
             #print sub_weight_result_df_2_left
             
             for ab_lvl4 in xrange(0,len(add_weight_result_df_2_right.index)):
                  if ((add_weight_result_df_2_right.ix[ab_lvl4,'Suggested_Numbers'] == "" and add_weight_result_df_2_right.ix[ab_lvl4,'weights(%)'] < 10) or (add_weight_result_df_2_right.ix[ab_lvl4,'#Suggested_Numbers'] > 1 and add_weight_result_df_2_right.ix[ab_lvl4,'weights(%)'] < 10)):
                      add_weight_result_df_2_right = add_weight_result_df_2_right.drop(ab_lvl4,0)
             #print sub_weight_result_df_2_right
             
             sending_data_3 = php_data(add_weight_result_df_2_left,add_weight_result_df_2_right,selectlvl)
             #sending_data_4 = php_data(sub_weight_result_df_2_right,selectlvl)
             #print sending_data_3  
         
         if (len(sending_data_1) !=0 and len(sending_data_3) !=0):
             
             d = {'a':sending_data_1, 'b':sending_data_3}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php
             
         elif (len(sending_data_1) == 0 and len(sending_data_3) !=0):
             
             d = {'a':sending_data_3}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php
                
         elif (len(sending_data_1) != 0 and len(sending_data_3) == 0):
             
             d = {'a':sending_data_1}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php
                     
      
    if (selectlvl[0] == 3):
        
         #print selectlvl
         add_analysis_count_3_1_1,add_analysis_count_3_1_2,add_dataframe_3_1,add_analysis_count_3_2_1,add_analysis_count_3_2_2,add_dataframe_3_2 = add_sub_analysis_lvl_3(add_df)
         #add_anly_df_1_1,add_anly_df_1_2,add_df_1,add_anly_df_2_1,add_anly_df_2_2,add_df_2 = add_sub_analysis_lvl_3(add_df)
         #print add_analysis_count_3_1_1
         #print add_analysis_count_3_1_2
         #print add_analysis_count_3_2_1
         #print add_analysis_count_3_2_2
         #print add_dataframe_3_1
         #print add_dataframe_3_2
         add_sending_data_lvl_3_1 = pd.DataFrame()
         add_sending_data_lvl_3_2_1 = pd.DataFrame()
         """
         The weights function if called inorder to calculate the importance of each question by 
         diving the frequency of that partcular number with the number question which a student
         commited wrong at that particular level.
         """
         """
         Used to call the php_data function when after the calculatio of weights the dataframe
         is passed to the php_data function to squeeze the data into a dictonary
         """
         
         if (len(add_analysis_count_3_1_1) != 0 and len(add_analysis_count_3_1_2) != 0):
             add_weight_result_df_1_left = weights(Total_Wrongs,add_analysis_count_3_1_1,add_weight_result_df_1_left)
             add_weight_result_df_1_right = weights(Total_Wrongs,add_analysis_count_3_1_2,add_weight_result_df_1_right)
             for q in xrange(0,len(add_weight_result_df_1_left)):
                 add_weight_result_df_1_left.ix[q,"Right_Question_Choice"] = 1
             for q in xrange(0,len(add_weight_result_df_1_right)):
                 add_weight_result_df_1_right.ix[q,"Left_Question_Choice"] = 2
             sugg_val_list_left_cas1_lvl3 = [] 
             sugg_val_list_right_cas1_lvl3 = []
             #print sub_weight_result_df_1_left
             #print sub_weight_result_df_1_right
             for weig_tab_22 in xrange(0,len(add_weight_result_df_1_left.index)):
                  for crs_tab_22 in xrange(0,len(ddnn)):
                     if (add_weight_result_df_1_left.ix[weig_tab_22,"Questions"] == ddnn.ix[crs_tab_22,"questionPair_left"] and ddnn.ix[crs_tab_22,"questionPair_right"] <= 9):
                         sugg_val_list_left_cas1_lvl3.append(ddnn.ix[crs_tab_22,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                  result_cas2= ",".join(map(str,sugg_val_list_left_cas1_lvl3))
                  add_weight_result_df_1_left.ix[weig_tab_22,"Suggested_Numbers"] = result_cas2
                  del sugg_val_list_left_cas1_lvl3[:]
                #List_index_val        
             #print result
             #print add_weight_result_df_1_left
             for weig_tab_1_22 in xrange(0,len(add_weight_result_df_1_right.index)):
                for crs_tab_1_22 in xrange(0,len(ddnn_right)):
                     if (add_weight_result_df_1_right.ix[weig_tab_1_22,"Questions"] == ddnn_right.ix[crs_tab_1_22,"questionPair_right"] and ddnn_right.ix[crs_tab_1_22,"questionPair_left"] > 9):
                         sugg_val_list_right_cas1_lvl3.append(ddnn_right.ix[crs_tab_1_22,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_cas2_lvl3= ",".join(map(str,sugg_val_list_right_cas1_lvl3))
                add_weight_result_df_1_right.ix[weig_tab_1_22,"Suggested_Numbers"] = result_1_cas2_lvl3
                del sugg_val_list_right_cas1_lvl3[:]
             #print add_weight_result_df_1_right   
             
             add_weight_result_df_1_left['#Suggested_Numbers'] = add_weight_result_df_1_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             add_weight_result_df_1_right['#Suggested_Numbers'] = add_weight_result_df_1_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)

             for ab_1 in xrange(0,len(add_weight_result_df_1_left.index)):
                  if ((add_weight_result_df_1_left.ix[ab_1,'Suggested_Numbers'] == "" and add_weight_result_df_1_left.ix[ab_1,'weights(%)'] < 10) or (add_weight_result_df_1_left.ix[ab_1,'#Suggested_Numbers'] > 1  and add_weight_result_df_1_left.ix[ab_1,'weights(%)'] < 10)):
                      add_weight_result_df_1_left = add_weight_result_df_1_left.drop(ab_1,0)
             #print add_weight_result_df_1_left
             for ab in xrange(0,len(add_weight_result_df_1_right.index)):
                  if ((add_weight_result_df_1_right.ix[ab,'Suggested_Numbers'] == "" and add_weight_result_df_1_right.ix[ab,'weights(%)'] < 10) or (add_weight_result_df_1_right.ix[ab,'#Suggested_Numbers'] > 1  and add_weight_result_df_1_right.ix[ab,'weights(%)'] < 10)):
                      add_weight_result_df_1_right = add_weight_result_df_1_right.drop(ab,0)
             #print add_weight_result_df_1_right
              
             
             add_sending_data_lvl_3_1= php_data(add_weight_result_df_1_left,add_weight_result_df_1_right,selectlvl)
             #add_sending_data_lvl_3_2 = php_data(add_weight_result_df_1_right,selectlvl)
             #print add_sending_data_lvl_3_1
         
         if(len(add_analysis_count_3_2_1) !=0 and len(add_analysis_count_3_2_2) != 0): 
             
             add_weight_result_df_2_left = weights(Total_Wrongs,add_analysis_count_3_2_1,add_weight_result_df_2_left)
             add_weight_result_df_2_right = weights(Total_Wrongs,add_analysis_count_3_2_2,add_weight_result_df_2_right)

             for q in xrange(0,len(add_weight_result_df_2_left)):
                 add_weight_result_df_2_left.ix[q,"Right_Question_Choice"] = 2
             for q in xrange(0,len(add_weight_result_df_2_right)):
                 add_weight_result_df_2_right.ix[q,"Left_Question_Choice"] = 2
             sugg_val_list_left_cas2_lvl3 = [] 
             sugg_val_list_right_cas2_lvl3 = []
             #print sub_weight_result_df_1_left
             #print sub_weight_result_df_1_right
             for weig_tab_22_2 in xrange(0,len(add_weight_result_df_2_left.index)):
                  for crs_tab_22_2 in xrange(0,len(ddnn)):
                     if (add_weight_result_df_2_left.ix[weig_tab_22_2,"Questions"] == ddnn.ix[crs_tab_22_2,"questionPair_left"] and ddnn.ix[crs_tab_22_2,"questionPair_right"] > 9):
                         sugg_val_list_left_cas2_lvl3.append(ddnn.ix[crs_tab_22_2,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                  result_cas2= ",".join(map(str,sugg_val_list_left_cas2_lvl3))
                  add_weight_result_df_2_left.ix[weig_tab_22_2,"Suggested_Numbers"] = result_cas2
                  del sugg_val_list_left_cas2_lvl3[:]
                #List_index_val        
             #print result
             #print add_weight_result_df_2_left
             add_weight_result_df_2_left = add_weight_result_df_2_left.reset_index(drop = 1)
             for weig_tab_1_22 in xrange(0,len(add_weight_result_df_2_right.index)):
                for crs_tab_1_22 in xrange(0,len(ddnn_right)):
                     if (add_weight_result_df_2_right.ix[weig_tab_1_22,"Questions"] == ddnn_right.ix[crs_tab_1_22,"questionPair_right"] and ddnn_right.ix[crs_tab_1_22,"questionPair_left"] > 9):
                         sugg_val_list_right_cas2_lvl3.append(ddnn_right.ix[crs_tab_1_22,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_cas2_lvl3= ",".join(map(str,sugg_val_list_right_cas2_lvl3))
                add_weight_result_df_2_right.ix[weig_tab_1_22,"Suggested_Numbers"] = result_1_cas2_lvl3
                del sugg_val_list_right_cas2_lvl3[:]
             #print add_weight_result_df_2_right 
             add_weight_result_df_2_right = add_weight_result_df_2_right.reset_index(drop = 1)
             
             add_weight_result_df_2_left['#Suggested_Numbers'] = add_weight_result_df_2_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             add_weight_result_df_2_right['#Suggested_Numbers'] = add_weight_result_df_2_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             
             for he in xrange(0,len(add_weight_result_df_2_left.index)):
                  if ((add_weight_result_df_2_left.ix[he,'Suggested_Numbers'] == "" and add_weight_result_df_2_left.ix[he,'weights(%)'] < 10) or (add_weight_result_df_2_left.ix[he,'#Suggested_Numbers'] > 1 and add_weight_result_df_2_left.ix[he,'weights(%)'] < 10)):
                      add_weight_result_df_2_left = add_weight_result_df_2_left.drop(he,0)
             #print add_weight_result_df_2_left
             for he_1 in xrange(0,len(add_weight_result_df_2_right.index)):
                  if ((add_weight_result_df_2_right.ix[he_1,'Suggested_Numbers'] == "" and add_weight_result_df_2_right.ix[he_1,'weights(%)'] < 10) or (add_weight_result_df_2_right.ix[he_1,'#Suggested_Numbers'] > 1 and add_weight_result_df_2_right.ix[he_1,'weights(%)'] < 10)):
                      add_weight_result_df_2_right = add_weight_result_df_2_right.drop(he_1,0)
             #print add_weight_result_df_2_right
             #print add_weight_result_df_2_left
             #print add_weight_result_df_2_right
             add_sending_data_lvl_3_2_1= php_data(add_weight_result_df_2_left,add_weight_result_df_2_right,selectlvl)
             #add_sending_data_lvl_3_2_2 = php_data(add_weight_result_df_2_right,selectlvl)
            
             #print add_sending_data_lvl_3_2_1
             
         if (len(add_sending_data_lvl_3_1) !=0 and len(add_sending_data_lvl_3_2_1) !=0):
             
             d = {'a':add_sending_data_lvl_3_1, 'b':add_sending_data_lvl_3_2_1}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php
                 
         elif (len(add_sending_data_lvl_3_1) == 0 and len(add_sending_data_lvl_3_2_1) !=0):
             
             d = {'a':add_sending_data_lvl_3_2_1}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php
                 
         elif (len(add_sending_data_lvl_3_1) != 0 and len(add_sending_data_lvl_3_2_1) == 0):
             
             d = {'a':add_sending_data_lvl_3_1}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php     

    elif (selectlvl[0] == 2):
        
         #print selectlvl
         add_analysis_count_2_1_1,add_analysis_count_2_1_2,add_dataframe_2_1,add_analysis_count_2_2_1,add_analysis_count_2_2_2,add_dataframe_2_2,add_analysis_count_2_3_1,add_analysis_count_2_3_2,add_dataframe_2_3,add_analysis_count_2_4_1,add_analysis_count_2_4_2,add_dataframe_2_4 = add_analysis_lvl_2(add_df)
         #print add_analysis_count_2_1_1
         #print add_analysis_count_2_1_2
         #print add_dataframe_2_1
         #print "!!!!!!!!!!!!Printing the second set of DataFrames!!!!!!!!!!!!!!!!!!!!!"
         #print add_analysis_count_2_2_1
         #print add_analysis_count_2_2_2
         #print add_dataframe_2_2
         add_sending_data_lvl_2_1 = []
         add_sending_data_lvl_2_2 = []
         add_sending_data_lvl_2_3 = []
         add_sending_data_lvl_2_4 = []
         d = {'a': [], 'b': [], 'c': [], 'd': []}
         
         """
         sub_lvl2_wrongs_1 = count_sub_lvl_3(dataframe_2_1,selectlvl,List_Wrongs)
         sub_lvl2_wrongs_2 = count_sub_lvl_3(dataframe_2_2,selectlvl,List_Wrongs)
         print sub_lvl2_wrongs_1
         print sub_lvl2_wrongs_2
         """
         
         if (len(add_analysis_count_2_1_1) != 0 and len(add_analysis_count_2_1_2) != 0):

             add_weight_result_df_1_left = weights(Total_Wrongs,add_analysis_count_2_1_1,add_weight_result_df_1_left)
             add_weight_result_df_1_right = weights(Total_Wrongs,add_analysis_count_2_1_2,add_weight_result_df_1_right)
             #print add_weight_result_df_1_right
             #print add_weight_result_df_1_left
             for q in xrange(0,len(add_weight_result_df_1_left)):
                 add_weight_result_df_1_left.ix[q,"Right_Question_Choice"] = 1
             for q in xrange(0,len(add_weight_result_df_1_right)):
                 add_weight_result_df_1_right.ix[q,"Left_Question_Choice"] = 2
             sugg_val_list_left_cas2_lvl2 = [] 
             sugg_val_list_right_cas2_lvl2 = []
             #print sub_weight_result_df_1_left
             #print sub_weight_result_df_1_right
             for weig_tab_22_2 in xrange(0,len(add_weight_result_df_1_left.index)):
                  for crs_tab_22_2 in xrange(0,len(ddnn)):
                     if (add_weight_result_df_1_left.ix[weig_tab_22_2,"Questions"] == ddnn.ix[crs_tab_22_2,"questionPair_left"] and ddnn.ix[crs_tab_22_2,"questionPair_right"] <= 9):
                         sugg_val_list_left_cas2_lvl2.append(ddnn.ix[crs_tab_22_2,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                  result_cas2= ",".join(map(str,sugg_val_list_left_cas2_lvl2))
                  add_weight_result_df_1_left.ix[weig_tab_22_2,"Suggested_Numbers"] = result_cas2
                  del sugg_val_list_left_cas2_lvl2[:]
                #List_index_val        
             #print result
             #print add_weight_result_df_1_left
             
             add_weight_result_df_1_left = add_weight_result_df_1_left.reset_index(drop = 1)
             for weig_tab_2_22 in xrange(0,len(add_weight_result_df_1_right.index)):
                for crs_tab_2_22 in xrange(0,len(ddnn_right)):
                     if (add_weight_result_df_1_right.ix[weig_tab_2_22,"Questions"] == ddnn_right.ix[crs_tab_2_22,"questionPair_right"] and ddnn_right.ix[crs_tab_2_22,"questionPair_left"] > 9):
                         sugg_val_list_right_cas2_lvl2.append(ddnn_right.ix[crs_tab_2_22,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_cas2_lvl2= ",".join(map(str,sugg_val_list_right_cas2_lvl2))
                add_weight_result_df_1_right.ix[weig_tab_2_22,"Suggested_Numbers"] = result_1_cas2_lvl2
                del sugg_val_list_right_cas2_lvl2[:]
                
             #print add_weight_result_df_1_right 
             add_weight_result_df_1_right['#Suggested_Numbers'] = add_weight_result_df_1_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             add_weight_result_df_1_right['#Suggested_Numbers'] = add_weight_result_df_1_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             
             add_weight_result_df_1_right = add_weight_result_df_1_right.reset_index(drop = 1)
             for lx in xrange(0,len(add_weight_result_df_1_left.index)):
                  if ((add_weight_result_df_1_left.ix[lx,'Suggested_Numbers'] == "" and add_weight_result_df_1_left.ix[lx,'weights(%)'] < 10) or (add_weight_result_df_1_left.ix[lx,'#Suggested_Numbers'] > 1 and add_weight_result_df_1_left.ix[lx,'weights(%)'] < 10)):
                      add_weight_result_df_1_left = add_weight_result_df_1_left.drop(lx,0)
             #print add_weight_result_df_1_left
             for lx_1 in xrange(0,len(add_weight_result_df_1_right.index)):
                  if ((add_weight_result_df_1_right.ix[lx_1,'Suggested_Numbers'] == "" and  add_weight_result_df_1_right.ix[lx_1,'weights(%)'] < 10) or (add_weight_result_df_1_right.ix[lx_1,'#Suggested_Numbers'] > 1 and add_weight_result_df_1_right.ix[lx_1,'weights(%)'] < 10)):
                      add_weight_result_df_1_right = add_weight_result_df_1_right.drop(lx_1,0)
             #print add_weight_result_df_1_right
             #print add_weight_result_df_1_left
             #print add_weight_result_df_1_right
             
             add_sending_data_lvl_2_1 = php_data(add_weight_result_df_1_left,add_weight_result_df_1_right,selectlvl)
             d['a'].append(add_sending_data_lvl_2_1)
             #add_sending_data_lvl_2_2 = php_data(add_weight_result_df_1_right,selectlvl)
             #print add_sending_data_lvl_2_1
             #print add_sending_data_lvl_2_2

         if (len(add_analysis_count_2_2_1) != 0 and len(add_analysis_count_2_2_2) != 0):
             
             add_weight_result_df_2_left = weights(Total_Wrongs,add_analysis_count_2_2_1,add_weight_result_df_2_left)
             add_weight_result_df_2_right = weights(Total_Wrongs,add_analysis_count_2_2_2,add_weight_result_df_2_right)
             #print add_weight_result_df_2_left
             #print add_weight_result_df_2_right
             
             for q in xrange(0,len(add_weight_result_df_2_left)):
                 add_weight_result_df_2_left.ix[q,"Right_Question_Choice"] = 2
             for q in xrange(0,len(add_weight_result_df_2_right)):
                 add_weight_result_df_2_right.ix[q,"Left_Question_Choice"] = 1
             
             sugg_val_list_left_cas12_lvl2 = [] 
             sugg_val_list_right_cas12_lvl2 = []
             #print add_weight_result_df_2_left
             #print add_weight_result_df_2_right
             
             for weig_tab_22_22 in xrange(0,len(add_weight_result_df_2_left.index)):
                  for crs_tab_22_22 in xrange(0,len(ddnn)):
                     if (add_weight_result_df_2_left.ix[weig_tab_22_22,"Questions"] == ddnn.ix[crs_tab_22_22,"questionPair_left"] and ddnn.ix[crs_tab_22_22,"questionPair_right"] > 9):
                         sugg_val_list_left_cas12_lvl2.append(ddnn.ix[crs_tab_22_22,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                  result_cas2= ",".join(map(str,sugg_val_list_left_cas12_lvl2))
                  add_weight_result_df_2_left.ix[weig_tab_22_22,"Suggested_Numbers"] = result_cas2
                  del sugg_val_list_left_cas12_lvl2[:]
                #List_index_val        
             #print result
             #print add_weight_result_df_2_left
             
             
             add_weight_result_df_2_left = add_weight_result_df_2_left.reset_index(drop = 1)
             for weig_tab_12_22 in xrange(0,len(add_weight_result_df_2_right.index)):
                for crs_tab_12_22 in xrange(0,len(ddnn_right)):
                     if (add_weight_result_df_2_right.ix[weig_tab_12_22,"Questions"] == ddnn_right.ix[crs_tab_12_22,"questionPair_right"] and ddnn_right.ix[crs_tab_12_22,"questionPair_left"] <= 9):
                         sugg_val_list_right_cas12_lvl2.append(ddnn_right.ix[crs_tab_12_22,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_cas2_lvl2= ",".join(map(str,sugg_val_list_right_cas12_lvl2))
                add_weight_result_df_2_right.ix[weig_tab_12_22,"Suggested_Numbers"] = result_1_cas2_lvl2
                del sugg_val_list_right_cas12_lvl2[:]
                
             #print add_weight_result_df_2_right 
             add_weight_result_df_2_right = add_weight_result_df_2_right.reset_index(drop = 1)

             add_weight_result_df_2_left['#Suggested_Numbers'] = add_weight_result_df_2_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             add_weight_result_df_2_right['#Suggested_Numbers'] = add_weight_result_df_2_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             
             for ad in xrange(0,len(add_weight_result_df_2_left.index)):
                  if ((add_weight_result_df_2_left.ix[ad,'Suggested_Numbers'] == "" and add_weight_result_df_2_left.ix[ad,'weights(%)'] < 10) or (add_weight_result_df_2_left.ix[ad,'#Suggested_Numbers'] > 1 and add_weight_result_df_2_left.ix[ad,'weights(%)'] < 10)):
                      add_weight_result_df_2_left = add_weight_result_df_2_left.drop(ad,0)
             #print add_weight_result_df_2_left
             
             for ad_1 in xrange(0,len(add_weight_result_df_2_right.index)):
                  if ((add_weight_result_df_2_right.ix[ad_1,'Suggested_Numbers'] == "" and add_weight_result_df_2_right.ix[ad_1,'weights(%)'] < 10) or (add_weight_result_df_2_right.ix[ad_1,'#Suggested_Numbers'] > 1 and add_weight_result_df_2_right.ix[ad_1,'weights(%)'] < 10)):
                      add_weight_result_df_2_right = add_weight_result_df_2_right.drop(ad_1,0)
                
                
                
             add_sending_data_lvl_2_2 = php_data(add_weight_result_df_2_left,add_weight_result_df_2_right,selectlvl)
             #add_sending_data_lvl_2_4 = php_data(add_weight_result_df_2_right,selectlvl)
             #print add_sending_data_lvl_2_2
             d['b'].append(add_sending_data_lvl_2_2)

             
         if (len(add_analysis_count_2_3_1) != 0 and len(add_analysis_count_2_3_2) != 0):
             
             add_weight_result_df_3_left = weights(Total_Wrongs,add_analysis_count_2_3_1,add_weight_result_df_3_left)
             add_weight_result_df_3_right = weights(Total_Wrongs,add_analysis_count_2_3_2,add_weight_result_df_3_right)
             #print add_weight_result_df_3_left
             #print add_weight_result_df_3_right
             
             for q_123 in xrange(0,len(add_weight_result_df_3_left)):
                 add_weight_result_df_3_left.ix[q_123,"Right_Question_Choice"] = 1
             for q_456 in xrange(0,len(add_weight_result_df_3_right)):
                 add_weight_result_df_3_right.ix[q_456,"Left_Question_Choice"] = 1
             
             sugg_val_list_left_typ3 = [] 
             sugg_val_list_right_typ3 = []
             #print sub_weight_result_df_1_left
             #print sub_weight_result_df_1_right
             for wgt_chk in xrange(0,len(add_weight_result_df_3_left.index)):
                  for crs_chk in xrange(0,len(ddnn)):
                     if (add_weight_result_df_3_left.ix[wgt_chk,"Questions"] == ddnn.ix[crs_chk,"questionPair_left"] and ddnn.ix[crs_chk,"questionPair_right"] <= 9):
                         sugg_val_list_left_typ3.append(ddnn.ix[crs_chk,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                  result_cas2= ",".join(map(str,sugg_val_list_left_typ3))
                  add_weight_result_df_3_left.ix[wgt_chk,"Suggested_Numbers"] = result_cas2
                  del sugg_val_list_left_typ3[:]
                #List_index_val        
             #print result
             #print add_weight_result_df_3_left
             add_weight_result_df_3_left = add_weight_result_df_3_left.reset_index(drop = 1)
             
             
             for wgt_chk_1 in xrange(0,len(add_weight_result_df_3_right.index)):
                for crs_chk_1 in xrange(0,len(ddnn_right)):
                     if (add_weight_result_df_3_right.ix[wgt_chk_1,"Questions"] == ddnn_right.ix[crs_chk_1,"questionPair_right"] and ddnn_right.ix[crs_chk_1,"questionPair_left"] <= 9):
                         sugg_val_list_right_typ3.append(ddnn_right.ix[crs_chk_1,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_cas2_lvl2= ",".join(map(str,sugg_val_list_right_typ3))
                add_weight_result_df_3_right.ix[wgt_chk_1,"Suggested_Numbers"] = result_1_cas2_lvl2
                del sugg_val_list_right_typ3[:]
             #print "Iam printing this value ------   add_weight_result_df_3_right" 
             #print add_weight_result_df_3_right 
             add_weight_result_df_3_right = add_weight_result_df_3_right.reset_index(drop = 1)
             
             add_weight_result_df_3_left['#Suggested_Numbers'] = add_weight_result_df_3_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             add_weight_result_df_3_right['#Suggested_Numbers'] = add_weight_result_df_3_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             
             for df_chk_val in xrange(0,len(add_weight_result_df_3_left.index)):
                  if ((add_weight_result_df_3_left.ix[df_chk_val,'Suggested_Numbers'] == "" and add_weight_result_df_3_left.ix[df_chk_val,'weights(%)'] < 10) or (add_weight_result_df_3_left.ix[df_chk_val,'#Suggested_Numbers'] > 1 and add_weight_result_df_3_left.ix[df_chk_val,'weights(%)'] < 10)):
                      add_weight_result_df_3_left = add_weight_result_df_3_left.drop(df_chk_val,0)
             #print add_weight_result_df_3_left
             
             for df_chk_val_1 in xrange(0,len(add_weight_result_df_3_right.index)):
                  if ((add_weight_result_df_3_right.ix[df_chk_val_1,'Suggested_Numbers'] == "" and add_weight_result_df_3_right.ix[df_chk_val_1,'weights(%)'] < 10) or (add_weight_result_df_3_right.ix[df_chk_val_1,'#Suggested_Numbers'] > 1 and add_weight_result_df_3_right.ix[df_chk_val_1,'weights(%)'] < 10)):
                      add_weight_result_df_3_right = add_weight_result_df_3_right.drop(df_chk_val_1,0)
                
                
                
             add_sending_data_lvl_2_3 = php_data(add_weight_result_df_3_left,add_weight_result_df_3_right,selectlvl)
             #add_sending_data_lvl_2_4 = php_data(add_weight_result_df_2_right,selectlvl)
             #print add_sending_data_lvl_2_3    
             d['c'].append(add_sending_data_lvl_2_3)

         if (len(add_analysis_count_2_4_1) != 0 and len(add_analysis_count_2_4_2) != 0):
             
             add_weight_result_df_4_left = weights(Total_Wrongs,add_analysis_count_2_4_1,add_weight_result_df_4_left)
             add_weight_result_df_4_right = weights(Total_Wrongs,add_analysis_count_2_4_2,add_weight_result_df_4_right)
             #print add_weight_result_df_4_left
             #print add_weight_result_df_4_right
             
             for chk_4 in xrange(0,len(add_weight_result_df_4_left)):
                 add_weight_result_df_4_left.ix[chk_4,"Right_Question_Choice"] = 2
             for chk_4_1 in xrange(0,len(add_weight_result_df_4_right)):
                 add_weight_result_df_4_right.ix[chk_4_1,"Left_Question_Choice"] = 2
             
             sugg_val_list_left_typ4 = [] 
             sugg_val_list_right_typ4 = []
             #print add_weight_result_df_4_left
             #print add_weight_result_df_4_right
             for wght_chk_typ4 in xrange(0,len(add_weight_result_df_4_left.index)):
                  for crs_chk_typ4 in xrange(0,len(ddnn)):
                     if (add_weight_result_df_4_left.ix[wght_chk_typ4,"Questions"] == ddnn.ix[crs_chk_typ4,"questionPair_left"] and ddnn.ix[crs_chk_typ4,"questionPair_right"] > 9):
                         sugg_val_list_left_typ4.append(ddnn.ix[crs_chk_typ4,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                  result_cas2= ",".join(map(str,sugg_val_list_left_typ4))
                  add_weight_result_df_4_left.ix[wght_chk_typ4,"Suggested_Numbers"] = result_cas2
                  del sugg_val_list_left_typ4[:]
                #List_index_val        
             #print result
             #print add_weight_result_df_4_left
             add_weight_result_df_4_left = add_weight_result_df_4_left.reset_index(drop = 1)
             
             for wght_chk_typ4_1 in xrange(0,len(add_weight_result_df_4_right.index)):
                for crs_chk_typ4_1 in xrange(0,len(ddnn_right)):
                     if (add_weight_result_df_4_right.ix[wght_chk_typ4_1,"Questions"] == ddnn_right.ix[crs_chk_typ4_1,"questionPair_right"] and ddnn_right.ix[crs_chk_typ4_1,"questionPair_left"] > 9):
                         sugg_val_list_right_typ4.append(ddnn_right.ix[crs_chk_typ4_1,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_cas2_lvl2= ",".join(map(str,sugg_val_list_right_typ4))
                add_weight_result_df_4_right.ix[wght_chk_typ4_1,"Suggested_Numbers"] = result_1_cas2_lvl2
                del sugg_val_list_right_typ4[:]
                
             #print add_weight_result_df_4_right 
             add_weight_result_df_4_right = add_weight_result_df_4_right.reset_index(drop = 1)

             add_weight_result_df_4_left['#Suggested_Numbers'] = add_weight_result_df_4_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             add_weight_result_df_4_right['#Suggested_Numbers'] = add_weight_result_df_4_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
             
             for har in xrange(0,len(add_weight_result_df_4_left.index)):
                  if ((add_weight_result_df_4_left.ix[har,'Suggested_Numbers'] == "" and add_weight_result_df_4_left.ix[har,'weights(%)'] < 10) or (add_weight_result_df_4_left.ix[har,'#Suggested_Numbers'] > 1 and add_weight_result_df_4_left.ix[har,'weights(%)'] < 10)):
                      add_weight_result_df_4_left = add_weight_result_df_4_left.drop(har,0)
             #print add_weight_result_df_4_left
             
             for har_1 in xrange(0,len(add_weight_result_df_4_right.index)):
                  if ((add_weight_result_df_4_right.ix[har_1,'Suggested_Numbers'] == "" and add_weight_result_df_4_right.ix[har_1,'weights(%)'] < 10) or (add_weight_result_df_4_right.ix[har_1,'#Suggested_Numbers'] > 1 and add_weight_result_df_4_right.ix[har_1,'weights(%)'] < 10)):
                      add_weight_result_df_4_right = add_weight_result_df_4_right.drop(har_1,0)
                
                
                
             add_sending_data_lvl_2_4 = php_data(add_weight_result_df_4_left,add_weight_result_df_2_right,selectlvl)
             #add_sending_data_lvl_2_4 = php_data(add_weight_result_df_2_right,selectlvl)
             #print add_sending_data_lvl_2_4
             d['d'].append(add_sending_data_lvl_2_4)

         #print  d
         final_result_php = json.dumps(d)
         print final_result_php
         
         
    elif (selectlvl[0] == 1):   
        
        add_analysis_count_1_1,add_analysis_count_1_2,add_dataframe_1 = add_sub_analysis_lvl_1(add_df)
        #sub_lvl1_wrongs_1 = count_sub_lvl_3(dataframe_2_1,selectlvl,List_Wrongs)
        #print sub_lvl1_wrongs_1
        add_weight_result_df_1_left = weights(Total_Wrongs,analysis_count_1_1,add_weight_result_df_1_left)
        add_weight_result_df_1_right = weights(Total_Wrongs,analysis_count_1_2,add_weight_result_df_1_right)
        for q in xrange(0,len(add_weight_result_df_1_left)):
            add_weight_result_df_1_left.ix[q,"Right_Question_Choice"] = 1
        for q in xrange(0,len(add_weight_result_df_1_right)):
            add_weight_result_df_1_right.ix[q,"Left_Question_Choice"] = 1
        
        add_sugg_val_list_left_lvl1 = [] 
        add_sugg_val_list_right_lvl1 = []
        #print sub_weight_result_df_2_left
        #print sub_weight_result_df_1_right
        for weig_tab_22_lvl1 in xrange(0,len(add_weight_result_df_1_left.index)):
                  for crs_tab_22_lvl1 in xrange(0,len(ddnn)):
                     if (add_weight_result_df_1_left.ix[weig_tab_22_lvl1,"Questions"] == ddnn.ix[crs_tab_22_lvl1,"questionPair_left"] and ddnn.ix[crs_tab_22_lvl1,"questionPair_right"] < 10):
                         add_sugg_val_list_left_lvl1.append(ddnn.ix[crs_tab_22_lvl3,"questionPair_right"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                  result_cas2_lvl1= ",".join(map(str,add_sugg_val_list_left_lvl1))
                  add_weight_result_df_1_left.ix[weig_tab_22_lvl1,"Suggested_Numbers"] = result_cas2_lvl1
                  #print add_sugg_val_list_left_lvl1
                  del add_sugg_val_list_left_lvl1[:]
                #List_index_val        
             
        #print add_weight_result_df_1_left
        for weig_tab_1_22_lvl1 in xrange(0,len(add_weight_result_df_1_right.index)):
                for crs_tab_1_22_lvl1 in xrange(0,len(ddnn_right)):
                     if (add_weight_result_df_1_right.ix[weig_tab_1_22_lvl1,"Questions"] == ddnn_right.ix[crs_tab_1_22_lvl1,"questionPair_right"] and ddnn_right.ix[crs_tab_1_22_lvl1,"questionPair_left"] < 10):
                         add_sugg_val_list_right_lvl1.append(ddnn_right.ix[crs_tab_1_22_lvl3,"questionPair_left"])
                         #backup_sugg_val[List_index_val] = sugg_val_list
                result_1_cas2_lvl1= ",".join(map(str,add_sugg_val_list_right_lvl1))
                add_weight_result_df_1_right.ix[weig_tab_1_22_lvl1,"Suggested_Numbers"] = result_1_cas2_lvl1
                del add_sugg_val_list_right_lvl1[:]
             
        #print add_weight_result_df_1_right
        add_weight_result_df_1_left['#Suggested_Numbers'] = add_weight_result_df_1_left.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
        add_weight_result_df_1_right['#Suggested_Numbers'] = add_weight_result_df_1_right.Suggested_Numbers.map(lambda x: [i.strip() for i in x.split(",")]).apply(len)
            
        for ab_1_lvl1 in xrange(0,len(add_weight_result_df_1_left.index)):
                  if ((add_weight_result_df_1_left.ix[ab_1_lvl1,'Suggested_Numbers'] == "" or add_weight_result_df_1_left.ix[ab_1_lvl1,'weights(%)'] < 10)or (add_weight_result_df_1_left.ix[ab_1_lvl1,'#Suggested_Numbers'] > 1 and add_weight_result_df_1_left.ix[ab_1_lvl1,'weights(%)'] < 10)):
                      add_weight_result_df_1_left = add_weight_result_df_1_left.drop(ab_1_lvl1,0)
                      
        #print sub_weight_result_df_2_left
        
        for ab_lvl1 in xrange(0,len(add_weight_result_df_1_right.index)):
                  if ((add_weight_result_df_1_right.ix[ab_lvl1,'Suggested_Numbers'] == "" or add_weight_result_df_1_right.ix[ab_lvl1,'weights(%)'] < 10)or (add_weight_result_df_1_right.ix[ab_lvl1,'#Suggested_Numbers'] > 1 and add_weight_result_df_1_right.ix[ab_lvl1,'weights(%)'] < 10)):
                      add_weight_result_df_1_right = sub_weight_result_df_1_right.drop(ab_lvl1,0)
             
        #print add_weight_result_df_1_left
        #print add_weight_result_df_1_right
        #print add_weight_result_df_1_left
        #print add_weight_result_df_1_right
        add_sending_data_lvl_1_1 = php_data(add_weight_result_df_1_left,add_weight_result_df_1_right,selectlvl)
        #add_sending_data_lvl_1_2 = php_data(add_weight_result_df_1_right,selectlvl)
        #print add_sending_data_lvl_1_1
        
        if (len(add_sending_data_lvl_1_1) != 0 ):
             
             d = {'a':add_sending_data_lvl_1_1}
             #print d
             final_result_php = json.dumps(d)
             print final_result_php       
#counts = df_train['questionPair_right'].value_counts()
#print counts
#count = df_train['questionPair_left'].value_counts()
#print count
#print df_train
#new_counts = df_train.groupby(['mathOperator', 'questionPair_left']).agg({'C':['mean', 'median'], 'D':'max'})
"""
Here The counts for the number appearing as left question and for number appearing
as the right part of question are taken.
"""
counts = updated_df_train.groupby(['selectedLevel','mathOperator','questionPair_left']).size()
count = updated_df_train.groupby(['selectedLevel','mathOperator','questionPair_right']).size()
#print count
#print counts
new_count = pd.concat([counts,count], axis=1).reset_index().apply(pd.to_numeric)
#print new_count
old_names_123 = ['level_0','level_1','level_2',0,1]
new_names_123 = ['selectedLevel','Operator','Questions','Count_As_Left_Question','Count_As_Right_Question']
new_count.rename(columns=dict(zip(old_names_123, new_names_123)), inplace=True)
temp_data_frame = pd.DataFrame(columns={'selectedLevel','Operator', 'Questions', 'Count_As_Left_Question' , 'Count_As_Right_Question'})
#pd.DataFrame(columns= {'Operator','Questions','Count_As_Left_Question','Count_As_Right_Question'})
#print new_count
    
#weights_df = pd.DataFrame()
"""
choose the operator and no of digits in question for which your are calculating
the counts--- include the select level in the if condition
"""
for lvl_value in range(len(selectlvl)):
    for r in xrange(0,len(new_count.index)):
        if (mathop == 3):
            if ((new_count.ix[r,'Questions'] < Ques_Threshold and new_count.ix[r,'Operator']==mathop and new_count.ix[r,'selectedLevel']==selectlvl[lvl_value])):
                temp_data_frame = (temp_data_frame.append(new_count.ix[[r]],ignore_index=True)).fillna(0)
        elif (mathop == 1):
            if ((new_count.ix[r,'Questions'] < Ques_Threshold and new_count.ix[r,'Operator']==mathop and new_count.ix[r,'selectedLevel']==selectlvl[lvl_value])):
                temp_data_frame = (temp_data_frame.append(new_count.ix[[r]],ignore_index=True)).fillna(0)
        elif(mathop == 2):
            if ((new_count.ix[r,'Questions'] < Ques_Threshold and new_count.ix[r,'Operator']==mathop and new_count.ix[r,'selectedLevel']==selectlvl[lvl_value])):
                temp_data_frame = (temp_data_frame.append(new_count.ix[[r]],ignore_index=True)).fillna(0)
        elif(mathop == 4):
            if ((new_count.ix[r,'Questions'] < Ques_Threshold and new_count.ix[r,'Operator']==mathop and new_count.ix[r,'selectedLevel']==selectlvl[lvl_value])):
                temp_data_frame = (temp_data_frame.append(new_count.ix[[r]],ignore_index=True)).fillna(0)
        else:
            break

#print temp_data_frame        
temp_data_frame['Total_Frequency'] = temp_data_frame['Count_As_Left_Question']+ temp_data_frame['Count_As_Right_Question']
#print temp_data_frame        
temp_data_frame = temp_data_frame[[0,1,2,3,4,5]].sort_values(by=['Total_Frequency'], ascending=[False])
#print temp_data_frame
""" The df_Total_Wrong_Count constitutes of the count for the numbers for which
Students have given wrong answers  """
df_Total_Wrong_Count = pd.DataFrame()
df_Total_Wrong_Count = temp_data_frame[[3,4,2,5]].reset_index(drop=1)
#print df_Total_Wrong_Count
df_Total_Wrong_Count =df_Total_Wrong_Count.loc[df_Total_Wrong_Count['Total_Frequency'] > Count_Threshold]
df_Total_Wrong_Count.loc["Total", "Total_Frequency"] = df_Total_Wrong_Count.Total_Frequency.sum()
df_Total_No_Wrongs = df_Total_Wrong_Count.loc["Total", "Total_Frequency"]
df_Total_Wrong_Count = df_Total_Wrong_Count.drop("Total")
#print df_Total_Wrong_Count
#print Total_Wrongs
weight_result_df = pd.DataFrame(['weights(%)'])
#weight_result_df = weights(Total_Wrongs,df_Total_Wrong_Count,weight_result_df)
#print weight_result_df
#Trans_data_final = php_data(weight_result_df,selectlvl)
#print Trans_data_final
"""The Lef_part_frame consists of the counts for the questions which appeared at left and
were wongly solved by the children """
Left_part_frame = temp_data_frame[[0,2,3]].sort_values(by=['Count_As_Left_Question','Operator','Questions'], ascending=[False,False,False])
#print Left_part_frame
"""The Right_part_frame consists of the counts for the questions which appeared on right and
were wongly solved by the children """
Right_part_frame = temp_data_frame[[1,2,3]].sort_values(by=['Count_As_Right_Question','Operator','Questions'], ascending=[False,False,False])
#print Right_part_frame
"""Consists of the combined Left_part_frame and Right_part_frame's data"""
full_partframe = pd.concat([Left_part_frame,Right_part_frame],ignore_index=True)
#print full_partframe.describe()
#print full_partframe
#temp_data_frame = temp_data_frame.sort(['Count_As_Left_Question','Count_As_Right_Question','Operator','Questions'],ascending=[False,False,False,False])
#print temp_data_frame.describe()
#print temp_data_frame.stat.crosstab("Count_As_Left_Question", "Count_As_Right_Question")
#freq = temp_data_frame.stat.freqItems(["Count_As_Left_Question", "Count_As_Right_Question"], 0.4)
#print freq
#counts = pd.merge(left = counts, right = count,how='inner')
#print counts
"""
This code is used to caliculate the question counts for those confused among the operators 
and have been answered with on one second. 
"""
new_df = pd.DataFrame(['Match_Case'])
missentry_df = pd.DataFrame(['Match_case'])
#print df_train
new_df = operator_miss(updated_df_train,new_df,len(updated_df_train.index))
new_df = new_df.loc[new_df['Match_Case'] != 0]
#print new_df   
missentry_df = missentry(updated_df_train,missentry_df)
missentry_df = missentry_df.loc[missentry_df['Match_Case'] != 0]
#print missentry_df
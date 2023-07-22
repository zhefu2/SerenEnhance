# -*- coding: utf-8 -*-
# load necessary packages
import os
import pandas as pd
import numpy as np
import json
import random
import math

data_df = pd.read_csv("../data/SerenLens_Books.csv")  # load SerenLens data

fp = open("../data/reviews_Books_5.json", "r") # load raw data for Amazon book review
print ("ile name: ", fp.name)
item_id = []
for line in fp:
    item_id.append(json.loads(line)['asin'].lower())
fp.close()

fp = open("../data/meta_Books.json", "r")  # load meta data of Amazon book review
print ("file name: ", fp.name)
meta_item_id = []  # item id
co_id = []  # also buy
co2_id = []  # also view
for line in fp:
    meta_item_id.append(json.loads(line)['asin'].lower())
    co_id.append(json.loads(line)['also_buy'])
    co2_id.append(json.loads(line)['also_view'])
fp.close()
dic_table = pd.DataFrame(meta_item_id)
dic_table['also_buy'] = co_id
dic_table['also_view'] = co2_id
dic_table = dic_table.set_index(0)

# extract unique user id and corresponding item sequence
item_seq = []
user_list = np.unique(data_df['user_id'].values)
for i in range(len(user_list)):
  temp_item_list = data_df[data_df['user_id']==user_list[i]]['item_id'].tolist()
  item_seq.append(temp_item_list)
user_table = pd.DataFrame(user_list,columns=['user'])
user_table['item seq']= item_seq

# match co-occurred items for each user
user_co_item = []
for i in range(len(user_table)):
  temp_co = []
  for j in range(len(item_seq)):
    item_current_seq = item_seq[j]
    # merge also buy and also view
    if item_current_seq in dic_table.index.values:
      if type(dic_table.loc[item_current_seq]['also_buy'])!=list:
          temp_co = temp_co + dic_table.loc[item_current_seq]['also_buy'][0] + dic_table.loc[item_current_seq]['also_view'][0]
      else:
          temp_co = temp_co + dic_table.loc[item_current_seq]['also_buy'] + dic_table.loc[item_current_seq]['also_view']
  user_co_item.append(temp_co)
user_table['co-occurrence item'] = user_co_item
# save the data
user_table.to_csv('../data/co_occurrence condition.csv')

# calculate p(i) - item popularity
item_list = np.unique(item_id)  # item list
item_pop = np.zeros((len(item_list)))  # item count matrix
item_ix = np.arange(0,len(item_list))  # item index in the matrix
item_df = pd.DataFrame(item_list, columns=['item_id'])
item_df['item index'] = item_ix
item_df = item_df.set_index('item_id')

for i in range(len(item_id)):  # count occurrence of each item
    ix = item_df.loc[item_id[i]]['item index']
    item_pop[ix] = item_pop[ix] + 1
item_df['count'] = item_pop
item_pob = []
for i in range(len(item_pop)): # calculate the probability
    item_pob.append(item_pop[i]/len(item_list))
item_df['probability'] = item_pob
item_df.to_csv('item_popularity.csv')

# calculate p(i|u) - probability of an item being co-occurred with the item in user sequence
item_dic = np.unique(dic_table.index)
item_serelens_list = np.unique(data_df['item_id'].values) # items in SerenLens

for i in range(len(item_serelens_list)):
    ix = item_serelens_list[i]
    item_co_count = np.zeros((len(item_list)))
    item_df_co = pd.DataFrame(item_list,columns=['item_id'])
    if ix in item_dic:  # extract co-occurred items of the target item ix
        if type(dic_table.loc[ix]['also_buy'])!=list:
            also_b = dic_table.loc[ix]['also_buy'][0]
            also_v = dic_table.loc[ix]['also_view'][0]
        else:
            also_b = dic_table.loc[ix]['also_buy']  
            also_v = dic_table.loc[ix]['also_view']

        # calculate n(i, ix) for the target item ix  (item_co_count)
        for j in range(len(also_b)):  
            if also_b[j] in item_list:
                p = item_df.loc[also_b[j]]['item index']
                p = int(p)
                item_co_count[p] = item_co_count[p] + 1
        for k in range(len(also_v)):
            if also_v[k] in item_list:
                p = item_df.loc[also_v[k]]['item index']
                p = int(p)
                item_co_count[p] = item_co_count[p] + 1
    item_df_co['count'] = item_co_count
    item_df_co['popularity'] = item_df['probability'].values
    file_name = '../data/co_occurrence/' + ix + '.csv'
    item_df_co.to_csv(file_name)
    
# smoothed p(i|u)
item_co_list = os.listdir('../data/co_occurrence/')
file_dir = '../data/co_occurrence/'
miu = 1  # smooth factor
for i in range(len(item_co_list)):
    file_path = file_dir + item_co_list[i]
    item_co_temp = pd.read_csv(file_path)
    n_total = 0
    new_count_list = []
    for j in range(len(item_co_temp)):
        pi = item_co_temp.loc[j]['popularity']
        pc = item_co_temp.loc[j]['count']
        new_count = pc + miu * pi  # n(i, ix) + miu* popularity
        n_total = n_total + pc # sum(n(i, ix))
        new_count_list.append(new_count)
    new_prob = np.array(new_count_list)/(n_total+ miu)  # smoothed p(i|u)
    item_co_temp['smooth_probability'] = new_prob

    file_name = '../data/co_occurrence_smooth/' + item_co_list[i]
    item_df_co.to_csv(file_name)


# generate positive samples and negative samples for each user (unexpectedness)
item_embedding = pd.read_csv('../data/item_encoding.csv') # load item embeddings
for i in range(len(user_list)):
    user_unexpect_pos = []  
    user_unexpect_neg = []

    user_item_seq_temp = data_df[data_df['user_id']==user_list[i]]['item_id'].tolist() # current item sequence for a user
    prob_list_temp = np.zeros((len(item_list))) # initalize the item appearance probability in a user sequence

    for j in range(len(user_item_seq_temp)):
        fp = str(user_item_seq_temp[j])
        item_file_path = '../data/co_occurrence_smooth/' + fp + '.csv'
        ps = pd.read_csv(item_file_path)['smooth_probability'].values # smoothed p(i|u)
        prob_list_temp = prob_list_temp + ps / len(user_item_seq_temp)  # calculate unexpectedness score
    
      user_unexp_df = pd.DataFrame(item_list, columns=['item_id'])
      user_unexp_df['user_unexpectedness_score'] = -1 * math.log(prob_list_temp)
      user_unexp_df = item_df_co.sort_values(by="user_unexpectedness_score" , ascending=True)

    idx = int(len(user_unexp_df)*0.3) # first or last 30% of the data
    exp = iuser_unexp_df.iloc[:idx]['item_id'] # negative samples for unexpectedness
    unexp = user_unexp_df.iloc[len(user_unexp_df)-idx:]['item_id'] # positive samples for unexpectedness

    # generate 50 pairs of positive and negative items for each user
    for k in range(50):
        rsp_unp = random.randint(0,idx-1)
        rsp_exp = random.randint(0,idx-1)

        i_exp = exp.iloc[rsp_exp]
        i_unp = unexp.iloc[rsp_unp]

        ix_exp = item_list.loc[i_exp]['index']
        ix_unp = item_list.loc[i_unp]['index']

        e_exp = item_embedding.loc[ix_exp].values
        e_unp = item_embedding.loc[ix_unp].values

        user_unexpect_pos.append(e_unp)
        user_unexpect_neg.append(e_exp)
    user_sample = user_unexpect_pos + user_unexpect_neg
    file_name = '../data/user_unexpectedness_samples/' + user_list[i]
    pd.DataFrame(user_sample).to_csv(file_name)

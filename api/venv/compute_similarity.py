import json
import pandas as pd
from pathlib import Path
import os
import heapq
from collections import Counter
from ast import literal_eval
from file_operations import process_token

from scipy.sparse import csr_matrix

root = str(Path.cwd().parent.parent) + "/data/tfidf/"


def weighted_search(people, location, organization, date, k=100):
    people_list,location_list,org_list,date_list = [],[],[],[]

    if people != "":
        people_list = search_query(people, "people", k)

    if location != "":
        location_list = search_query(location, "location", k)

    if organization != "":
        org_list = search_query(organization, "organization", k)

    if date != "":
        date_list = search_query(date, "date", k)

    top_10 = calculate_weight(people_list,location_list,org_list,date_list)

    return top_10




def search_query(query, entity, k):
    global vocabulary_file

    with open(root+entity+'/vocabulary.json', 'r') as file:
        vocabulary_file = json.load(file)
    with open(root+entity+'/idf.json', 'r') as file:
        idf_file = json.load(file)

    tfidf = read_tfidf(entity)
    
    q_vector = vectorize_query(query, vocabulary_file, idf_file)
    similarity =  compute_similarity(q_vector, tfidf, k)
    return extract_filename(similarity)



def calculate_weight(people_list,location_list,org_list,date_list):
    people_weight,location_weight,org_weight,date_weight=0,0,0,0
    length_list=[len(people_list),len(location_list),len(org_list),len(date_list)]
    f1_list=[0.6870607074633088,0.5287373720763592,0.42593168321979474,0.38440931970917164]
    sum_=0
    for i in range(len(length_list)):
        if length_list[i] !=0:
            sum_+=f1_list[i]
    if len(people_list)!=0:
        people_weight=f1_list[0]/sum_
    if len(location_list)!=0:
        location_weight=f1_list[1]/sum_
    if len(org_list)!=0:
        org_weight=f1_list[2]/sum_
    if len(date_list)!=0:
        date_weight=f1_list[3]/sum_
    keys_set=set(people_list + location_list + org_list + date_list)
    filename_value={}
    for name in keys_set:
        filename_value[name]=0
        if name in people_list:
            filename_value[name]+=people_weight
        if name in location_list:
            filename_value[name]+=location_weight
        if name in org_list:
            filename_value[name]+=org_weight
        if name in date_list:
            filename_value[name]+=date_weight
    # sorted_dict = dict(sorted(filename_value.items(), key=lambda item: item[1], reverse=True))
    # top_10_items = dict(islice(sorted_dict.items(), 10))
    # return top_10_items
    sorted_dict = sorted(filename_value.items(), key=lambda item: item[1], reverse=True)[:10]
    return sorted_dict


def extract_filename(similarity_result):
    result = []
    for s, fn in similarity_result:
        if not fn.endswith("story"):
            result.append(fn+".story")
        else:
            result.append(fn)

    return result



def vectorize_query(query, vocabulary_file, idf_file):
    term_counts=Counter(query)
    tokens = process_token(query)
    TF_list=Counter(tokens)
    non_zero_values = []
    nonzero_position = []
    i=0
    for word in vocabulary_file:
        if word in TF_list:
            non_zero_values.append(idf_file[word] * TF_list[word])
            nonzero_position.append(i)
        i+=1
            
    return csr_matrix((non_zero_values, nonzero_position, [0, len(non_zero_values)]), shape=(1, len(vocabulary_file)))
    

def convert_to_array(row):
    nonzero_values = literal_eval(row["values"])
    nonzero_position = literal_eval(row["positions"])
    
    vector = csr_matrix((nonzero_values, nonzero_position, [0, len(nonzero_values)]), shape=(1, len(vocabulary_file)))
    
    # return vector.toarray()[0]
    return vector

def top_k(heap, element, k=10):
    # element format: (value, id)
    if len(heap) < k:
        heapq.heappush(heap, element)
    else:
        heapq.heappushpop(heap, element)
        
    return heap

def compute_similarity(q_vector, tfidf, k=20):
    top_files = []
    
    for i in range(len(tfidf)):
        r_vector = convert_to_array(tfidf.loc[i])
        similarity = r_vector.multiply(q_vector).sum()
        top_files = top_k(top_files, [similarity, tfidf.loc[i,"id"]], k)
        
    return sorted(top_files, reverse=True)


def read_tfidf(entity):
    if entity in ["people","organization","full_text"]:
        df1 = pd.read_csv(root+entity+"/tfidf_result1.csv", header = None, names=["id", "values", "positions"])
        df2 = pd.read_csv(root+entity+"/tfidf_result2.csv", header = None, names=["id", "values", "positions"])
        tfidf = pd.concat([df1,df2], axis=0, ignore_index=True)
    else:
        tfidf = pd.read_csv(root+entity+"/tfidf_result.csv", header = None, names=["id", "values", "positions"])

    return tfidf


if __name__ == '__main__':
    # print(os.listdir(root))
    pass
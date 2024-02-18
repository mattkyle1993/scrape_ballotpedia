import requests
import psutil    
import os
import glob
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from datetime import datetime
import time
import math
import codecs
import pathlib
import sys
import re
import random
import requests
from bs4 import BeautifulSoup
import joblib
from sklearn.datasets import make_hastie_10_2
from sklearn.ensemble import GradientBoostingClassifier

class BallotpediaPersonURLGuesserModel():
    def __init__(self,new_joblib=False):
        self.new_joblib = new_joblib
        pass
    def article_guesser_model_builder(self,max_depth=10,ran_state=14,test_size=0.10,learning_rate=0.05,new_joblib=False,n_estimators=250,save_csv=True,model_name="GradientBoosting"):
        data = pd.read_csv("people_urls_model/people_url_guesser_data.csv")

        X = data.drop(['URL','is_person','Unnamed: 0'], axis=1)
        y = data['is_person']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=ran_state,) # random_state = 42
        if model_name == "GradientBoosting":
            model = GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth, random_state=ran_state).fit(X_train, y_train)
        if model_name == "DecisionTree":
            model = DecisionTreeClassifier(max_depth=max_depth).fit(X_train, y_train)
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy:.2f}')

        # Compare y_pred to y_test
        comparison_df = pd.DataFrame({
            'Actual': y_test.values,
            'Predicted': y_pred
        })

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        comparison_df_filename = f'people_urls_model/model_output_y_test_y_pred/y_true_y_pred_{timestamp}.csv'
        if save_csv == True:
            comparison_df.to_csv(comparison_df_filename, index=True)

        true_pos = 0
        true_neg = 0
        false_pos = 0
        false_neg = 0
        for true, pred in zip(y_test.values,y_pred):
            if true == 1:
                if true == pred:
                    true_pos+=1
                if true > pred:
                    false_neg+=1
            if true == 0:
                if true == pred:
                    true_neg+=1
                if true < pred:
                    false_pos+=1
        
        print("true pos:",true_pos)
        print("true neg:",true_neg)
        print("false pos:",false_pos)
        print("false neg:", false_neg)

        feature_importances = model.feature_importances_
        feature_names = X.columns
        important_features = sorted(zip(feature_names, feature_importances), key=lambda x: x[1], reverse=True)
        print('\nMost important features:')
        for feature, importance in important_features:
            print(f'{feature}: {importance:.4f}')

        output_filename = f'people_urls_model/model_output_important_features/important_features_{timestamp}.csv'
        important_features_df = pd.DataFrame(important_features, columns=['Feature', 'Importance'])
        if save_csv == True:
            important_features_df.to_csv(output_filename, index=False)
        print(f'\nImportant features saved to {output_filename}')
        if new_joblib == True:

            # Train and save the model
            model = DecisionTreeClassifier(max_depth=max_depth)
            model.fit(X_train, y_train)
            joblib.dump(model, 'people_urls_model/joblibs/ALPHA_trained_{model_name}_ballotpedia_people_url_guesser_model.joblib'.format(model_name=model_name))
        
    def prepare_url_data_for_model(self,urls_list=[],save_csv=False,return_data=False,model_guess=False):
        """
        prepares ballotpedia people url training data for modeling
        """
        # states = [
        #     'alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware',
        #     'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky',
        #     'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri',
        #     'montana', 'nebraska', 'nevada', 'new_hampshire', 'new_jersey', 'new_mexico', 'new_york',
        #     'north_carolina', 'north_dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhode_island',
        #     'south_carolina', 'south_dakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington',
        #     'west_virginia', 'wisconsin', 'wyoming'
        # ]
        # states = [' '.join([part.capitalize() for part in state.split('_')]) for state in states]
        # under_states = [state.replace(" ","_") for state in states if state.count(" ") == 1]
        # no_under_states = [state for state in states if state.count(" ") == 0]
        # states = under_states + no_under_states

        def vowelOrConsonant(x,v_score,c_score): 
            if (x == 'a' or x == 'e' or
                x == 'i' or x == 'o' or x == 'u'): 
                return v_score
            else: 
                return c_score 

        # Initialize data lists
        uppercase_count = []
        paren_count = []
        underscore_counts = []
        url_len = []
        is_person = []
        vowel_count = []
        consonant_count = []
        first_char_lower_ct = []
        lowercase_count = []
        feature_1_underscore_div_lowercase = []

        if len(urls_list) == 0:
            urls_list = []
            with open("people_urls_model/urls_data.text","r",encoding="utf-8") as file:
                for line in file:
                    if line not in urls_list:
                        urls_list.append(line)
        else:
            urls_list = urls_list
        for i in range(0,len(urls_list)):
            url = urls_list[i]
            url = url.strip() # remove trailing white space
            if url.endswith(",1"):
                is_person.append(0)
                url = url[:-2] # remove ",1" from url string
            else:
                is_person.append(1)
            
            # get url len
            try:
                url_len.append(len(url))
            except:
                url_len.append(0)

            # get upper case count
            try:
                uppercase_count.append(sum(1 for c in url if c.isupper()))
            except:
                uppercase_count.append(0)

            # get lower case count
            try:
                lowercase_count.append(sum(1 for c in url if c.islower()))
            except:
                lowercase_count.append(0)

            # get paren count
            try:
                paren_count.append(sum(1 for c in url if c in [')','(']))
            except:
                paren_count.append(0)

            # get underscore count
            try:
                underscore_counts.append(sum(1 for c in url if c is '_'))
            except:
                underscore_counts.append(0)
            
            # get vowel count
            try:
                vowel_count.append(sum(vowelOrConsonant(c,v_score=1,c_score=0) for c in url))
            except:
                vowel_count.append(0)
            
            # get consonant count
            try:
                consonant_count.append(sum(vowelOrConsonant(c,v_score=0,c_score=1) for c in url))
            except:
                consonant_count.append(0)

            # build feature: underscore_ct/lowercase_ct
            try:
                try:
                    feature_1_underscore_div_lowercase.append((underscore_counts[0]/lowercase_count[0]))
                except:
                    feature_1_underscore_div_lowercase.append(0)
            except:
                feature_1_underscore_div_lowercase.append(0)

            
            # get lowercase first letter count
            try:
                the_ct = 0
                url_short = url.split('/')[-1]
                url_short = url_short.replace("_", " ")
                url_shorts = url_short.split()
                for shrt in url_shorts:
                    if shrt[0].islower():
                        the_ct +=1
                first_char_lower_ct.append(the_ct)
            except:
                first_char_lower_ct.append(0)

        print("urls",len(urls_list))
        print("upper:",len(uppercase_count))
        print("paren:",len(paren_count))
        print("underscore:",len(underscore_counts))
        print("url_len:",len(url_len))
        print("is_person:",len(is_person))
        print("vowel:",len(vowel_count))
        print("consonant:",len(consonant_count))
        print("first char lower:",len(first_char_lower_ct))
        print("lowercase:",len(lowercase_count))

        if model_guess == True:
            df = pd.DataFrame({
                "url_len":url_len,
                'uppercase_count': uppercase_count,
                'paren_count': paren_count,
                'underscore_counts': underscore_counts,
                'is_person': is_person,
                'vowel_count': vowel_count,
                'consonant_count': consonant_count,
                'first_char_lower_ct': first_char_lower_ct,
                "lowercase_count":lowercase_count,
                # "feature_1_underscore_div_lowercase":feature_1_underscore_div_lowercase,
            })
        if model_guess == False:
            df = pd.DataFrame({
                "URL": urls_list,
                "is_person":is_person,
                "url_len":url_len,
                'uppercase_count': uppercase_count,
                'paren_count': paren_count,
                'underscore_counts': underscore_counts,
                'is_person': is_person,
                'vowel_count': vowel_count,
                'consonant_count': consonant_count,
                'first_char_lower_ct': first_char_lower_ct,
                "lowercase_count":lowercase_count,
                # "feature_1_underscore_div_lowercase":feature_1_underscore_div_lowercase,
            })
        if save_csv == True:
            df.to_csv("people_urls_model/people_url_guesser_data.csv")

        if return_data == True:
            return df

    def run_ballotpedia_person_url_guesser_model(self,url,print_results=False,print_both_results=False,print_only_neg_results=False,model_name="GradientBoosting"): # save_article_guesses=False,
        """
        takes a given URL and predicts if it's an ballotpedia_person_url or not, then returns the answer: 1 or 0.
        """
        model = joblib.load('people_urls_model/joblibs/ALPHA_trained_{model_name}_ballotpedia_person_url_guesser_model.joblib'.format(model_name=model_name))
        new_features = self.prepare_url_data_for_model(urls_list=[url],return_data=True,model_guess=True)
        try:
            prediction = model.predict(new_features)
        except Exception as error:
            print("error:",str(error))
        # if save_article_guesses == True:
        #     with open('article_urls_model/model_guesses_output/model_guesses.txt', 'a') as file:
        #         if prediction == 1:
        #             text_to_append = f"{url},1\n"
        #         if prediction == 0:
        #             text_to_append = f"{url}\n"
        #         file.write(text_to_append)
        if print_results==True:
            if prediction[0] == 1:
                pred = "Guess: is a person url"
            if prediction[0] == 0:
                pred = "Guess: is not a person url"
            if True:
                if print_only_neg_results == True:
                    print_both_results = True
                    skip = True
                if print_both_results == True:
                    if skip == False:
                        print("ballotpedia-person-url-guesser-model prediction:",(url,pred))
                    if print_only_neg_results == True:
                        if prediction == 0:
                            print("ballotpedia-person-url-guesser-model:",(url,pred))
                else:
                    if prediction == 1:
                        print("ballotpedia-person-url-guesser-model:",(url,pred))
        return prediction
    
GUESS = BallotpediaPersonURLGuesserModel()
GUESS.prepare_url_data_for_model(save_csv=True)
GUESS.article_guesser_model_builder(new_joblib=True)
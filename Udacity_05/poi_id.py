#!/usr/bin/python

import sys
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
#from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedShuffleSplit


sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','total_stock_value', 'exercised_stock_options','bonus','salary','total_payments',
'long_term_incentive','shared_receipt_with_poi','other','expenses','from_poi_to_this_person',
'from_this_person_to_poi','restricted_stock','to_messages','deferred_income','ratio_restricted_total_stock','ratio_exercised_stock_total_stock'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers

data_dict.pop('TOTAL', 0)

### Task 3: Create new feature(s)

df = pd.DataFrame.from_records(list(data_dict.values()))
employees = pd.Series(list(data_dict.keys()))
df.set_index(employees, inplace=True)
#Since 'NaN' is string, replace to np.nan first
df.replace('NaN', np.nan, inplace=True)
#Then use fillna
df.fillna(0.0, inplace=True)

#create new feature
df['ratio_restricted_total_stock'] = df['restricted_stock']/df['total_stock_value']
df['ratio_exercised_stock_total_stock'] = df['exercised_stock_options']/df['total_stock_value']
df['salary_times_bonus'] = (df['salary'])*(df['bonus'])

#Replace 'NaN' and 'np.inf' to np.nan first
df.replace('NaN', np.nan, inplace=True)
df.replace([np.inf, -np.inf], np.nan, inplace=True)
#Then use fillna
df.fillna(0.0, inplace=True)
# Convert the data frame back to dict
cleaned_data = df.to_dict('index')

### Store to my_dataset for easy export below.
my_dataset = cleaned_data

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html



### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
#from sklearn.cross_validation import train_test_split
#features_train, features_test, labels_train, labels_test = \
    #train_test_split(features, labels, test_size=0.3, random_state=42)


#set minmax, pca, svc classifier
minmax = MinMaxScaler()
skb = SelectKBest()
#pca = PCA()
#tree = DecisionTreeClassifier()
nb = GaussianNB()

#set pipeline
pipe = Pipeline(steps = [('SKB',skb),('MinMax',minmax),('NaiveBayes', nb)])

#set parameters
parameters = {
'SKB__k':list(range(1,(len(features_list)-1))),
#'PCA__n_components':range(1,2),
#'PCA__whiten':[True],
#'DecisionTree__criterion':['gini','entropy'],
#'DecisionTree__splitter':['best','random'],
#'DecisionTree__min_samples_split':[2, 10, 20],
#'DecisionTree__max_depth':[10,15,20,25,30],
#'DecisionTree__max_leaf_nodes':[5,10,30,40]
}

cv = StratifiedShuffleSplit(labels, n_iter=100, random_state = 42)
#set gridsearchCV for try out different combinations
gs = GridSearchCV(pipe, parameters, cv=cv, scoring = "f1")

#fit the best combination
gs.fit(features, labels)
#predict test data based on the traning data

clf = gs.best_estimator_
#selected_feature = [feature_list[i+1] for i in gs.get_support(indices=True)]

print(clf)
#print(selected_feature)
print('done')

#NaiveBayes
#Pipeline(steps=[('SKB', SelectKBest(k=5, score_func=<function f_classif at 0x10f2678c0>)),
#('MinMax', MinMaxScaler(copy=True, feature_range=(0, 1))), ('NB', GaussianNB(priors=None))])
#'total_stock_value', 'exercised_stock_options','bonus','salary','total_payments'
#Accuracy: 0.84833	Precision: 0.41964	Recall: 0.35900	F1: 0.38696	F2: 0.36968

#PCA brings down the recall score from 0.35900 to 0.21450. Precision increases from 0.41964 to 0.51501

#Adding new feature imroved the accuracy from 0.84833 to 0.85200, precision from 0.41964 to 0.43134
# but the recall score decreased from 0.35900 to 0.34550

#Accuracy: 0.85200 Precision: 0.43134	Recall: 0.34550	F1: 0.38368	F2: 0.35982


#Decision Tree

#Best parameter
#Pipeline(steps=[('SKB', SelectKBest(k=3, score_func=<function f_classif at 0x1179998c0>)), ('MinMax', MinMaxScaler(copy=True, feature_range=(0, 1))),
#('DecisionTree', DecisionTreeClassifier(class_weight=None, criterion='entropy', max_depth=30,
#max_features=None, max_leaf_nodes=30, min_impurity_split=1e-07, min_samples_leaf=1, min_samples_split=2,
#min_weight_fraction_leaf=0.0, presort=False, random_state=None,splitter='random'))]
#Accuracy: 0.82380	Precision: 0.32780	Recall: 0.30600	F1: 0.31652	F2: 0.31012

#'DecisionTree__criterion':['gini','entropy'],
#'DecisionTree__splitter':['best','random'],
#'DecisionTree__min_samples_split':[2, 10,20],
#'DecisionTree__max_depth':[10,15,20,25,30],
#'DecisionTree__max_leaf_nodes':[5,10,30]

#--------------------------------------------------------------------------
#Feature selection best scores

#16
#total_stock_value', 'exercised_stock_options','bonus','salary','total_payments',
#'long_term_incentive','shared_receipt_with_poi','other','expenses','from_poi_to_this_person',
#'from_this_person_to_poi','restricted_stock','to_messages','deferred_income','from_messages'
#'deferral_payments'
#Accuracy: 0.85200	Precision: 0.43134	Recall: 0.34550	F1: 0.38368	F2: 0.35982

#15
#total_stock_value', 'exercised_stock_options','bonus','salary','total_payments',
#'long_term_incentive','shared_receipt_with_poi','other','expenses','from_poi_to_this_person',
#'from_this_person_to_poi','restricted_stock','to_messages','deferred_income','from_messages'
#Accuracy: 0.85200	Precision: 0.43134	Recall: 0.34550	F1: 0.38368	F2: 0.35982

#14
#total_stock_value', 'exercised_stock_options','bonus','salary','total_payments',
#'long_term_incentive','shared_receipt_with_poi','other','expenses','from_poi_to_this_person',
#'from_this_person_to_poi','restricted_stock','to_messages','deferred_income'
#Accuracy: 0.85200	Precision: 0.43134	Recall: 0.34550	F1: 0.38368	F2: 0.35982

#13
#'total_stock_value', 'exercised_stock_options','bonus','salary','total_payments',
#'long_term_incentive','shared_receipt_with_poi','other','expenses','from_poi_to_this_person',
#'from_this_person_to_poi','restricted_stock','to_messages'
#Accuracy: 0.84853	Precision: 0.41677	Recall: 0.34050	F1: 0.37479	F2: 0.35344

#12
#'total_stock_value', 'exercised_stock_options','bonus','salary','total_payments',
#'long_term_incentive','shared_receipt_with_poi','other','expenses','from_poi_to_this_person',
#'from_this_person_to_poi','restricted_stock'
#Accuracy: 0.84967	Precision: 0.41935	Recall: 0.33150	F1: 0.37029	F2: 0.34600

#10
#'total_stock_value', 'exercised_stock_options','bonus','salary','total_payments','long_term_incentive',
#'shared_receipt_with_poi','other','expenses','from_poi_to_this_person'
#Accuracy: 0.84860	Precision: 0.41783	Recall: 0.34450	F1: 0.37764	F2: 0.35703

#7
#'poi','total_stock_value', 'exercised_stock_options','bonus','salary','total_payments','long_term_incentive',
#'shared_receipt_with_poi'
#Accuracy: 0.84887	Precision: 0.41884	Recall: 0.34450	F1: 0.37805	F2: 0.35718

#5
#'poi','total_stock_value', 'exercised_stock_options','bonus','salary','total_payments'
#Accuracy: 0.85473	Precision: 0.43815	Recall: 0.31700	F1: 0.36786	F2: 0.33556

#Decision Tree best parameter scores

#'DecisionTree__criterion':['gini','entropy'],
#'DecisionTree__splitter':['best','random'],
#'DecisionTree__min_samples_split':[2, 10, 20],
#'DecisionTree__max_depth':[10,15,20,25,30],
#'DecisionTree__max_leaf_nodes':[5,10,30,40]

#Accuracy: 0.84300	Precision: 0.33966	Recall: 0.18800	F1: 0.24203	F2: 0.20643


#'DecisionTree__criterion':['gini','entropy'],
#'DecisionTree__splitter':['best','random'],
#'DecisionTree__min_samples_split':[2, 10, 20],
#'DecisionTree__max_depth':[10,15,20,25,30],
#'DecisionTree__max_leaf_nodes':[5,10,30]

#Accuracy: 0.81300	Precision: 0.29285	Recall: 0.28450	F1: 0.28861	F2: 0.28613


#'DecisionTree__criterion':['gini','entropy'],
#'DecisionTree__splitter':['best','random'],
#'DecisionTree__min_samples_split':[2, 10, 20],
#'DecisionTree__max_depth':[10,15,20,25,30],
#'DecisionTree__max_leaf_nodes':[5]

#Accuracy: 0.86220	Precision: 0.44691	Recall: 0.14100	F1: 0.21437	F2: 0.16336


#'DecisionTree__criterion':['gini','entropy'],
#'DecisionTree__splitter':['best','random'],
#'DecisionTree__min_samples_split':[2, 10, 20],
#'DecisionTree__max_depth':[10,15,20,25,30]

#Accuracy: 0.80160	Precision: 0.27281	Recall: 0.29300	F1: 0.28255	F2: 0.28873

#'DecisionTree__criterion':['gini','entropy'],
#'DecisionTree__splitter':['best','random'],
#'DecisionTree__min_samples_split':[2, 10, 20],
#'DecisionTree__max_depth':[10,20,30]

#Accuracy: 0.80887	Precision: 0.29028	Recall: 0.30000	F1: 0.29506	F2: 0.29800


#'DecisionTree__criterion':['gini','entropy'],
#'DecisionTree__splitter':['best','random'],
#'DecisionTree__min_samples_split':[2, 10, 20],
#'DecisionTree__max_depth':[10,20],

#Accuracy: 0.80453	Precision: 0.27466	Recall: 0.28400	F1: 0.27925	F2: 0.28208


#'DecisionTree__criterion':['gini','entropy'],
#'DecisionTree__splitter':['best','random'],
#'DecisionTree__min_samples_split':[2, 10, 20],
#'DecisionTree__max_depth':[10]

#Accuracy: 0.83380	Precision: 0.32228	Recall: 0.22350	F1: 0.26395	F2: 0.23810

#'DecisionTree__criterion':['gini','entropy'],
#'DecisionTree__splitter':['best','random'],
#'DecisionTree__min_samples_split':[2, 10, 20],

#Accuracy: 0.84173	Precision: 0.34391	Recall: 0.20600	F1: 0.25766	F2: 0.22396


#'DecisionTree__criterion':['gini','entropy'],
#'DecisionTree__splitter':['best','random'],
#'DecisionTree__min_samples_split':[2, 10],

#Accuracy: 0.80087	Precision: 0.26240	Recall: 0.27250	F1: 0.26735	F2: 0.27042

#No parameter
#Accuracy: 0.82187	Precision: 0.23872	Recall: 0.15350	F1: 0.18685	F2: 0.16530



### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)

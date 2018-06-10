import sys
import pickle
import matplotlib.pyplot as plt
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectKBest

#load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

#Removing outliers
data_dict.pop('TOTAL', 0)
data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 0)
data_dict.pop('loan_advances', 0)
data_dict.pop('director_fees', 0)

my_dataset = data_dict

feature_list = ['poi', 'salary', 'deferral_payments','total_payments', \
 'bonus', 'restricted_stock_deferred', 'deferred_income','total_stock_value', 'expenses', \
 'exercised_stock_options','other', 'long_term_incentive', 'restricted_stock', \
 'to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', \
  'shared_receipt_with_poi']

print('the number of features', len(feature_list))
### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, feature_list, sort_keys = True)
target, feature = targetFeatureSplit(data)

#Set minmax classifier
scaler = MinMaxScaler()
#Transform the entire feature with minmax scaler
minmax_features = scaler.fit_transform(feature)

#set kbest classfier
k_best = SelectKBest(chi2,k=16)
#select k best features
selectedFeature = k_best.fit(minmax_features, target)
#Round 2 dicimals and get the feature scores
feature_scores = ['%.2f' % elem for elem in selectedFeature.scores_ ]
#Round 3 dicimals and get the feature's p-values
p_values = ['%.3f' % elem for elem in selectedFeature.pvalues_]
#Get tuple of scores, p-values and feature names
feature_tuples = [(feature_list[i+1], feature_scores[i], p_values[i]) for i in k_best.get_support(indices = True)]
#reverse the feature based on the feature_score
feature_tuples = sorted(feature_tuples, key=lambda feature: float(feature[1]), reverse=True)
print(feature_tuples)

'''
k=2
('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019')

k=3
('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019'), ('bonus', '5.12', '0.024')

k=4
('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019'),
('bonus', '5.12', '0.024'), ('salary', '3.05', '0.081')

k=5
('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019'),
('bonus', '5.12', '0.024'), ('salary', '3.05', '0.081'), ('total_payments', '2.78', '0.095')

k=6
('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019'),
('bonus', '5.12', '0.024'), ('salary', '3.05', '0.081'), ('total_payments', '2.78', '0.095'),
('long_term_incentive', '2.54', '0.111')


k=7
('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019'),
('bonus', '5.12', '0.024'), ('salary', '3.05', '0.081'), ('total_payments', '2.78', '0.095'),
('long_term_incentive', '2.54', '0.111'), ('shared_receipt_with_poi', '2.43', '0.119')

k=8
('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019'),
('bonus', '5.12', '0.024'), ('salary', '3.05', '0.081'), ('total_payments', '2.78', '0.095'),
('long_term_incentive', '2.54', '0.111'), ('shared_receipt_with_poi', '2.43', '0.119'),
('other', '1.72', '0.190')

k=9
('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019'),
('bonus', '5.12', '0.024'), ('salary', '3.05', '0.081'), ('total_payments', '2.78', '0.095'),
('long_term_incentive', '2.54', '0.111'), ('shared_receipt_with_poi', '2.43', '0.119'),
('other', '1.72', '0.190'), ('expenses', '1.49', '0.223')

k=10

('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019'),
('bonus', '5.12', '0.024'), ('salary', '3.05', '0.081'), ('total_payments', '2.78', '0.095'),
('long_term_incentive', '2.54', '0.111'), ('shared_receipt_with_poi', '2.43', '0.119'),
 ('other', '1.72', '0.190'), ('expenses', '1.49', '0.223'), ('from_poi_to_this_person', '1.37', '0.242')

k=11

('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019'),
 ('bonus', '5.12', '0.024'), ('salary', '3.05', '0.081'), ('total_payments', '2.78', '0.095'),
  ('long_term_incentive', '2.54', '0.111'), ('shared_receipt_with_poi', '2.43', '0.119'),
  ('other', '1.72', '0.190'), ('expenses', '1.49', '0.223'), ('from_poi_to_this_person', '1.37', '0.242'),
  ('from_this_person_to_poi', '1.00', '0.317')


k=12

('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019'),
('bonus', '5.12', '0.024'), ('salary', '3.05', '0.081'), ('total_payments', '2.78', '0.095'),
 ('long_term_incentive', '2.54', '0.111'), ('shared_receipt_with_poi', '2.43', '0.119'),
 ('other', '1.72', '0.190'), ('expenses', '1.49', '0.223'), ('from_poi_to_this_person', '1.37', '0.242'),
 ('from_this_person_to_poi', '1.00', '0.317'), ('restricted_stock', '0.59', '0.443')

k=13

('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019'),
('bonus', '5.12', '0.024'), ('salary', '3.05', '0.081'), ('total_payments', '2.78', '0.095'),
('long_term_incentive', '2.54', '0.111'), ('shared_receipt_with_poi', '2.43', '0.119'),
('other', '1.72', '0.190'), ('expenses', '1.49', '0.223'), ('from_poi_to_this_person', '1.37', '0.242'),
('from_this_person_to_poi', '1.00', '0.317'), ('restricted_stock', '0.59', '0.443'),
('to_messages', '0.44', '0.509')

k=14

('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019'),
('bonus', '5.12', '0.024'), ('salary', '3.05', '0.081'), ('total_payments', '2.78', '0.095'),
('long_term_incentive', '2.54', '0.111'), ('shared_receipt_with_poi', '2.43', '0.119'),
('other', '1.72', '0.190'), ('expenses', '1.49', '0.223'), ('from_poi_to_this_person', '1.37', '0.242'),
('from_this_person_to_poi', '1.00', '0.317'), ('restricted_stock', '0.59', '0.443'),
('to_messages', '0.44', '0.509'), ('deferred_income', '0.34', '0.560')

k=15

('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019'),
('bonus', '5.12', '0.024'), ('salary', '3.05', '0.081'), ('total_payments', '2.78', '0.095'),
('long_term_incentive', '2.54', '0.111'), ('shared_receipt_with_poi', '2.43', '0.119'),
('other', '1.72', '0.190'), ('expenses', '1.49', '0.223'), ('from_poi_to_this_person', '1.37', '0.242'),
('from_this_person_to_poi', '1.00', '0.317'), ('restricted_stock', '0.59', '0.443'),
('to_messages', '0.44', '0.509'), ('deferred_income', '0.34', '0.560'), ('from_messages', '0.07', '0.793')

k=16

('exercised_stock_options', '6.85', '0.009'), ('total_stock_value', '5.48', '0.019'),
('bonus', '5.12', '0.024'), ('salary', '3.05', '0.081'), ('total_payments', '2.78', '0.095'),
('long_term_incentive', '2.54', '0.111'), ('shared_receipt_with_poi', '2.43', '0.119'),
('other', '1.72', '0.190'), ('expenses', '1.49', '0.223'), ('from_poi_to_this_person', '1.37', '0.242'),
('from_this_person_to_poi', '1.00', '0.317'), ('restricted_stock', '0.59', '0.443'),
('to_messages', '0.44', '0.509'), ('deferred_income', '0.34', '0.560'), ('from_messages', '0.07', '0.793'),
('deferral_payments', '0.06', '0.805')

'''

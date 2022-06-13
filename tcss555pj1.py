import pandas as pd
import os
import sys
from collections import OrderedDict
from xml.etree import cElementTree as ET
#from lxml import etree as ET

# Read data
args = sys.argv[1:]
input_traing_file_path = "/data/training/profile/profile.csv"
print(input_traing_file_path)
df = pd.read_csv(input_traing_file_path)

# classify age ot age range
# “xx-24”, “25-34”, “35-49”, or “50-xx”
df['age group'] = "50-xx"
df.loc[df['age'] < 50, 'age group'] = "35-49"
df.loc[df['age'] < 35, 'age group'] = "25-34"
df.loc[df['age'] < 25, 'age group'] = "xx-24"

# find majority age range
pred_age = df.groupby("age group")['userid'].count().idxmax()

# find majority gender
pred_gender = df.groupby("gender")['userid'].count().idxmax()
# 0 = male and 1 = female.
pred_gender = 'female' if pred_gender else 'male'

# find 5 mean persionality

persionality_li = df.mean()[["ope",'con', 'ext', 'agr', 'neu']]
# convert to string
ope, con, ext, agr, neu = (str(s) for s in persionality_li)

# read test data
test_file_name = os.path.join(args[1], 'profile', 'profile.csv')
print(test_file_name)
test = pd.read_csv(test_file_name)
# for each data sample 
for index, row in test.iterrows():
  # print(index)
  # put value into output data frame
  userid = df.loc[index, 'userid']
  attribute = OrderedDict([('id',userid),('age_group',pred_age),
                            ('gender',pred_gender),('extrovert',ext),
                            ('neurotic', neu), ('agreeable', agr),
                            ('conscientious', con), ('open', ope)
  ])
  root = ET.Element('user', attribute)
  tree = ET.ElementTree(root)
  # write the df to .xml file 
  output_file_name = os.path.join(args[3], "{}.xml".format(userid))
  tree.write(output_file_name)

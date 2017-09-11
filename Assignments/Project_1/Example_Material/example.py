
# coding: utf-8

# In[3]:

import matplotlib.pyplot as plt
import numpy as np
import csv
get_ipython().magic('matplotlib inline')


# In[4]:

the_data = open("/sciclone/home2/geogdan/project_1/geo_results.csv", 'rt')
csv_dta = csv.reader(the_data)
for row in csv_dta:
    print(row)


# In[5]:

import pandas as pd
csv_data_pandas = pd.read_csv("/sciclone/home2/geogdan/project_1/geo_results.csv", delimiter=",")
print(csv_data_pandas[['worldbank_geocodedresearchrelease_level1_v1_4_2.3161dcb.sum','ltdr_avhrr_ndvi_v4_yearly.2014.mean']])

subset_dta = csv_data_pandas[['worldbank_geocodedresearchrelease_level1_v1_4_2.3161dcb.sum','ltdr_avhrr_ndvi_v4_yearly.2014.mean']]


# In[6]:

subset_dta.columns=['EnvironmentAid','Vegetation']

plt.figure()
subset_dta.plot.scatter(x="Vegetation",y="EnvironmentAid")


# In[8]:

subset_dta.plot.hexbin(x="Vegetation",y="EnvironmentAid", gridsize=25)


# In[17]:

remove_outliers_aid = subset_dta[np.abs(subset_dta.EnvironmentAid<=100000)]

remove_outliers_aid.plot.hexbin(x="Vegetation",y="EnvironmentAid", gridsize=10)


# In[29]:

#Smaller values indicate more vegetation - i.e., rank 1 is the most vegetated
subset_dta["Veg_Rank"] = subset_dta["Vegetation"].rank(ascending=0)
subset_dta["Veg_Rank"]

subset_dta["Aid_Rank"] = subset_dta["EnvironmentAid"].rank(ascending=0)
subset_dta.plot.hexbin(x="Vegetation",y="EnvironmentAid", gridsize=10)

remove_outliers_aid = subset_dta[np.abs(subset_dta.EnvironmentAid<=50000)]

remove_outliers_aid.plot.hexbin(x="Vegetation",y="EnvironmentAid", gridsize=10)


# In[36]:

#Simulation and Uncertainty
#What if the monetary estimates are wrong?

import seaborn as sns
uniform_ex = np.random.rand(10000,1)

sns.distplot(uniform_ex)




# In[73]:

import random

beta_ex = np.random.beta(4,5,size=10000)

sns.distplot(beta_ex)

#Other distributions you can explore include chisquare, dirichlet, exponential, f, gamma, 
#geometric, gumbel, hypergeometric, and more.  


# In[83]:

#Assume monetary values are mostly accurate, with small amounts of error.

#Original distribution:
sns.distplot(subset_dta["EnvironmentAid"], bins=10, label="Raw Data")

#Add error to the distribution - note for your assignment, 
#you will need to add error in both directions (positive and negative).
#Here, we only introduce error in the positive direction.
subset_dta["uncertain_Env"] = subset_dta["EnvironmentAid"] + (subset_dta["EnvironmentAid"] * np.random.beta(4,5,subset_dta.shape[0]))

sns.distplot(subset_dta["uncertain_Env"], bins = 10, label="With Uncertainty")

sns.plt.legend()
sns.plt.show()


# In[93]:

#Establish a statement we can test in a simulation environment.
#A simple one might be: How much more funding do areas with high vegetation receive
#for environmental protection than those with low?

least_vegetation = subset_dta[np.abs(subset_dta.Vegetation<=subset_dta["Vegetation"].mean())]
aid_dollars_least = least_vegetation["EnvironmentAid"].sum()

most_vegetation = subset_dta[np.abs(subset_dta.Vegetation>subset_dta["Vegetation"].mean())]
aid_dollars_most = most_vegetation["EnvironmentAid"].sum()

#Positive values indicate areas with low vegetation have more aid than those with high
#Negative values indicate areas with high vegetation have more aid than those with low
diff_least_most = aid_dollars_least - aid_dollars_most

print(diff_least_most)


# In[129]:

#Now, we want to do the same thing, but account for uncertainty in the aid dollars.
#We could do it just once, but that wouldn't tell us much as all we're doing
#is adding random noise!  However, as an example, each time you run the below you will get a different
#answer:
subset_dta["uncertain_Env"] = subset_dta["EnvironmentAid"] + (subset_dta["EnvironmentAid"] * np.random.beta(4,5,subset_dta.shape[0]))

least_vegetation = subset_dta[np.abs(subset_dta.Vegetation<=subset_dta["Vegetation"].mean())]
aid_dollars_least = least_vegetation["uncertain_Env"].sum()

most_vegetation = subset_dta[np.abs(subset_dta.Vegetation>subset_dta["Vegetation"].mean())]
aid_dollars_most = most_vegetation["uncertain_Env"].sum()

#Negative values indicate areas with low vegetation have more aid than those with high
#Positive values indicate areas with high vegetation have more aid than those with low
diff_least_most = aid_dollars_most - aid_dollars_least

print(diff_least_most)


# In[128]:

#Simulation is as simple as doing this hundreds (if not thousands) of times,
#recording the answer each time, and interpreting the resulting distribution.
#While this is a simple system with few parameters, you will eventually be
#simulating uncertainty across multiple parameters and observing how
#uncertainty in different parts of your model can impact - or add - to 
#other uncertainties.

#Try changing the number_of_sims to see how many sims you need to get
#a consistent distribution.  With more complex systems (and more uncertainties)
#you tend to need more sims.

number_of_sims = 100

count = 0
results_df = pd.DataFrame()

while count < number_of_sims:
    subset_dta["uncertain_Env"] = subset_dta["EnvironmentAid"] + (subset_dta["EnvironmentAid"] * np.random.beta(4,5,subset_dta.shape[0]))

    least_vegetation = subset_dta[np.abs(subset_dta.Vegetation<=subset_dta["Vegetation"].mean())]
    aid_dollars_least = least_vegetation["uncertain_Env"].sum()

    most_vegetation = subset_dta[np.abs(subset_dta.Vegetation>subset_dta["Vegetation"].mean())]
    aid_dollars_most = most_vegetation["uncertain_Env"].sum()

    #Negative values indicate areas with low vegetation have more aid than those with high
    #Positive values indicate areas with high vegetation have more aid than those with low
    diff_least_most = aid_dollars_most - aid_dollars_least 
    
    results_df = results_df.append({"Results":diff_least_most}, ignore_index=True)
    
    count = count + 1

print(results_df)


# In[130]:

#Finally, we can look at our distributions to answer our question
#Accounting for uncertainty.

sns.distplot(results_df["Results"], bins = 10, label="With Uncertainty")


# In[ ]:





# coding: utf-8

# In[51]:


import requests
from bs4 import BeautifulSoup

#sample website
r=requests.get("https://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
c=r.content

#reads though the website and looks for the important content we are looking for
soup = BeautifulSoup(c,"html.parser")

all = soup.find_all("div", {"class":"propertyRow"})

all[0].find("h4",{"class":"propPrice"}).text.replace("\n","")

page_nr=soup.find_all("a",{"class":"Page"})[-1].text
print(page_nr)


# In[52]:

#script loops through every page of the sample website
#reads though all of the property data and grabs the useful info we want
#and adds it to an empty dictionary
#address,locality, price, beds, baths and Area
#and adds dictionary info into an empty list item to more easily create a dataframe object
l=[]
base_url="https://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range(0,int(page_nr)*10,10):
    print(base_url+str(page)+".html")
    r=requests.get(base_url+str(page)+".html")
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    print(soup.prettify())
    all = soup.find_all("div", {"class":"propertyRow"})

    for item in all:
            d={}
            d["Address"]=item.find_all("span",{"class", "propAddressCollapse"})[0].text
            try:
                d["Locality"]=item.find_all("span",{"class", "propAddressCollapse"})[1].text
            except:
                d["locality"]=None
            d["Price"]=item.find("h4",{"class","propPrice"}).text.replace("\n","").replace(" ","")
            try:
                d["Beds"]=item.find("span",{"class","infoBed"}).find("b").text
            except:
                d["Beds"]=None

            try:
                d["Area"]=item.find("span",{"class","infoSqFt"}).find("b").text
            except:
                d["Area"]=None
            try:
                d["Full Baths"]=item.find("span",{"class","infoValueFullBath"}).find("b").text
            except:
                d["Full Baths"]=None
            try:
                d["Half Baths"]=item.find("span",{"class","infoValueHalfBath"}).find("b").text
            except:
                d["Half Baths"]=None
            #try:
                #print(item.find("div",{"class","propertyMLS"}).text)
            #except:
                #print(None)
            for column_group in item.find_all("div",{"class":"columnGroup"}):
                for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}), column_group.find_all("span",{"class":"featureName"})):
                    if "Lot Size" in feature_group.text:
                        d["Lot Size"]=feature_name.text
            l.append(d)


# In[31]:


l


# In[53]:

#uses pandas to create a dataframe object
import pandas
df=pandas.DataFrame(l)


# In[46]:


df


# In[54]:

#creates a csv file from the dataframe
df.to_csv("Output.csv")

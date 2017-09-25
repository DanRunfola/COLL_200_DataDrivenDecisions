
# coding: utf-8

# In[1]:

#Libraries used to ping many APIs to retrieve information
import urllib.request, json
import warnings
warnings.filterwarnings('ignore')


# In[2]:

#Google maps provides a fairly simple API.  As a test example:
with urllib.request.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=google") as url:
    data = json.loads(url.read().decode())
    print(json.dumps(data, indent=4, sort_keys=True))


# In[3]:

#We can fairly simply request detailed information from google maps - 
#for example, all Starbucks locations they have information for.
#Keep in mind every time you run this line of code, your API key is pinged.
#You only get 2,500 free requests each day, so be careful!

#First, we want to build our request URL.
#https://developers.google.com/places/web-service/search has more details on what options you can specify.
key = "AIzaSyAuGB1Ancie4CWfjnEblCqczgdo3Yn_e6c"
latitude_center = "37.2707"
longitude_center = "76.7075"
radius = "50000"
rankby = "distance"
keyword = "Starbucks"
types = "establishment"

request_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" + "location=" + latitude_center + "," + longitude_center + "&radius=" + radius + "&types=" + types + "&keywords=" + keyword + "&key=" + key
print(request_url)

with urllib.request.urlopen(request_url) as url:
    starbucks_data = json.loads(url.read().decode())
    
#Let's save the output as a file so we don't have to ping Google every time we want to use it:
with open('/sciclone/home2/geogdan/Project_2/starbucks_locations.json', 'w') as out_json:
    json.dump(starbucks_data, out_json)
    


# In[4]:

#Let's see what we got:
print(request_url)
with open('/sciclone/home2/geogdan/Project_2/starbucks_locations.json', 'r') as dta:
    retrieved_data = json.load(dta)

print(json.dumps(retrieved_data, indent=4, sort_keys=True))
    


# In[5]:

#Let's make a quick map to visualize where these locations are:

#First, make a record of the lat/lon locations:
count = 0
lat_list = []
lon_list = []
for item in retrieved_data['results']:
    lat_list.append(retrieved_data['results'][count]['geometry']['location']['lat'])
    lon_list.append(retrieved_data['results'][count]['geometry']['location']['lng'])
    count = count + 1
    
print(lat_list)
print(lon_list)


# In[6]:

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

#Now, map!
m_sb = Basemap(projection='stere', lon_0=float(longitude_center), lat_0=float(latitude_center),                width=500000, height=500000)

m_sb.bluemarble()

x , y = m_sb(lon_list, lat_list)
m_sb.scatter(x,y,1,marker='o',color="red", zorder=10)
plt.title("200 Starbucks Locations Nearest to lat " + latitude_center + " lon " + longitude_center)
plt.show()


# In[7]:

#Something seems wrong... let's zoom out and see what's going on.

m_sb = Basemap(projection='stere', lon_0=float(longitude_center), lat_0=float(latitude_center),                width=5000000, height=5000000)

m_sb.bluemarble()

x , y = m_sb(lon_list, lat_list)
m_sb.scatter(x,y,1,marker='o',color="red", zorder=10)
plt.title("200 Starbucks Locations Nearest to lat " + latitude_center + " lon " + longitude_center)
plt.show()


# In[8]:

#We're in china!  
#Double check the longitude - if we want Williamsburg for this example,
#it's 76.7075 W - which is represented by a negative.  Let's try again.
key = "AIzaSyAuGB1Ancie4CWfjnEblCqczgdo3Yn_e6c"

#Fix these:
latitude_center_new = "37.2707"
longitude_center_new = "-76.7075"


radius = "50000"
rankby = "distance"
keyword = "Starbucks"
types = "establishment"

request_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" + "location=" + latitude_center_new + "," + longitude_center_new + "&radius=" + radius + "&types=" + types + "&keywords=" + keyword + "&key=" + key
print(request_url)

with urllib.request.urlopen(request_url) as url:
    starbucks_data = json.loads(url.read().decode())
    
#Let's save the output as a file so we don't have to ping Google every time we want to use it:
with open('/sciclone/home2/geogdan/Project_2/starbucks_locations_new.json', 'w') as out_json:
    json.dump(starbucks_data, out_json)


# In[9]:

#Let's see what we got:
print(request_url)
with open('/sciclone/home2/geogdan/Project_2/starbucks_locations_new.json', 'r') as dta:
    retrieved_data = json.load(dta)

print(json.dumps(retrieved_data, indent=4, sort_keys=True))

#And update our long/lat information
count = 0
lat_list_new = []
lon_list_new = []
for item in retrieved_data['results']:
    lat_list_new.append(retrieved_data['results'][count]['geometry']['location']['lat'])
    lon_list_new.append(retrieved_data['results'][count]['geometry']['location']['lng'])
    count = count + 1
    
print(lat_list_new)
print(lon_list_new)


# In[10]:

m_sb = Basemap(projection='stere', lon_0=float(longitude_center_new), lat_0=float(latitude_center_new),                width=5000000, height=5000000)

m_sb.bluemarble(zorder=0)

x , y = m_sb(lon_list_new, lat_list_new)
print(lon_list)
m_sb.scatter(x,y,1,marker='o',color="red", zorder=10)
plt.title("200 Starbucks Locations Nearest to lat " + latitude_center_new + " lon " + longitude_center_new)
plt.show()


# In[11]:

m_sb = Basemap(projection='stere', lon_0=float(longitude_center_new), lat_0=float(latitude_center_new),                width=750000, height=750000)

m_sb.bluemarble(zorder=0)

x , y = m_sb(lon_list_new, lat_list_new)
m_sb.scatter(x,y,10,marker='o',color="red", zorder=10)
plt.title("200 Starbucks Locations Nearest to lat " + latitude_center_new + " lon " + longitude_center_new)
plt.show()


# In[55]:

#We now have all starbucks locations (up to 200) within 50km of Williamsburg.
#However, what if we wanted to map out all locations in VA?
#We could manually run a hundred or so searches to cover the entire state, or we
#can automate the process by adding our latitude and longitude
#starting point to a while loop.
#To do this, we will look at the "bounding box" of Virginia - i.e.,
#the upper-left, upper-right, lower-left, and lower-right latitude and longitude
#coordinates of a box that covers the entire state.

#upper-left: 36.5409, -83.6752
#lower-right: 36.5409, -75.2418
#lower-left: 39.4659, -83.6752
#Upper-right: 39.4659, -75.2418

#First, let's create a grid of latitude / longitude areas we want to request data for.
#This will let us know how many requests we're going to put in
#(as we don't want to exceed the free request limits on google).

all_lat_coords = list()
all_lon_coords = list()

#We'll start in the upper left corner, and work our way to the lower right.
cur_lat = 36.5409
start_lon = -83.6752
cur_lon = start_lon

#As a test case, let's put a point every 50 kilometers (roughly equivalent to 0.5 decimal degrees)
while(cur_lat < 39.4659):
    while(cur_lon < -75.2418):
        all_lat_coords.append(cur_lat)
        all_lon_coords.append(cur_lon)
        cur_lon = cur_lon + 0.5
    cur_lat = cur_lat + 0.5
    cur_lon = start_lon
    
grid_sb = Basemap(projection='stere', lon_0=float(longitude_center_new), lat_0=float(latitude_center_new),                width=1500000, height=1500000)

grid_sb.bluemarble(zorder=0)
grid_sb.drawstates()

x , y = grid_sb(all_lon_coords, all_lat_coords)
grid_sb.scatter(x,y,10,marker='o',color="red", zorder=10)
plt.title("Grid for Data Retrieval")
plt.show()


# In[25]:

#As you can see, there are many points that don't fall inside of Virginia.
#This is because we defined the entire bounding box as our search area.
#We won't worry about this for now; at a later step that data will be removed. 
#However, in cases where you are pinging google for more data, you may want to use
#a more specific location creation routine than a simple bounding box.

#Using our new array, let's loop through our google searches:

total_searches = len(all_lat_coords)

radius = "50000"
rankby = "distance"
keyword = "Starbucks"
types = "establishment"

#We're going to automatically build url's and send our requests, each time
#saving the results into a file for parsing later (just in case!).

loc_count = 0
while loc_count < total_searches:
    request_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" +     "location=" + str(all_lat_coords[loc_count]) + "," + str(all_lon_coords[loc_count]) +     "&radius=" + radius + "&types=" + types + "&keywords=" + keyword + "&key=" + key
    #Print here so we can see the progress of the script as it's running -
    #you can replace this with something more informative if you want.
    print(request_url)


    with urllib.request.urlopen(request_url) as url:
        starbucks_data = json.loads(url.read().decode())
    
    #Let's save the output as a file so we don't have to ping Google every time we want to use it:
    file_name = '/sciclone/home2/geogdan/Project_2/starbucks_locations_'+ str(loc_count) +'.json'
    
    with open(file_name, 'w') as out_json:
        json.dump(starbucks_data, out_json)

    loc_count = loc_count + 1
    
total_loc_count = loc_count





# In[54]:

#Let's parse our downloaded files and see what we got.

total_loc_count
file_count = 0
lat_list_va_sb = []
lon_list_va_sb = []

while file_count < total_loc_count:
    file_name = '/sciclone/home2/geogdan/Project_2/starbucks_locations_'+ str(file_count) +'.json'
    with open(file_name, 'r') as dta:
        retrieved_data = json.load(dta)

    #Update our long/lat information
    count = 0
    for item in retrieved_data['results']:
        lat_list_va_sb.append(retrieved_data['results'][count]['geometry']['location']['lat'])
        lon_list_va_sb.append(retrieved_data['results'][count]['geometry']['location']['lng'])
        count = count + 1

    file_count = file_count + 1
        

        #Check if it made sense:
        
all_va_sb = Basemap(projection='stere', lon_0=float(longitude_center_new), lat_0=float(latitude_center_new),                width=1500000, height=1500000)

all_va_sb.bluemarble(zorder=0)
all_va_sb.drawstates()

x , y = all_va_sb(lon_list_va_sb, lat_list_va_sb)
all_va_sb.scatter(x,y,10,marker='o',color="red", zorder=10)
plt.title("Grid for Data Retrieval")
plt.show()


# In[71]:

#Now, let's save our results to do some of the
#spatial operations we need locally.
#You can also implement these steps (detailed below) programmatically as a stretch goal.
f = open('/sciclone/home2/geogdan/Project_2/starbucks_locations_all.csv', 'w')

#Create our headers, adding a new line at the end:
f.write("lat,lon\n")
count = 0
for j in lat_list_va_sb:
    f.write(str(lat_list_va_sb[count]) +"," +str(lon_list_va_sb[count])+ "\n")
    count = count + 1
    
f.close()


# In[69]:

#Alright!  Now we're going to pull in our census data, which will also be
#used in a spatial data processing tool as described below.
#To get this data, we'll use the University of Minnesota's
#IPUMS NHGIS: https://www.nhgis.org/

#Choose to Get Data, and choose a level of analysis you're interested in.
#Here, I use county as an example, with the 2015 "GIS Boundary File".
#I chose Median Household Income in the past 12 months (2014-2015) as a variable
#to compare my findings to.  Save this file locally when NHGIS finishes processing it, and extract
#both the GIS boundary file and data table.



# In[72]:

#Now, we're going to use QuantumGIS (QGIS) locally to open
#(a) our CSV of all starbucks locations, and (b)
#our map of districts.

#Click on the "," on the left to add a CSV,
#and the "line" on the left to open the NHGIS boundaries.
#Then run the "points in polygon" analysis using the menu at the top.

#You may additionally get an error about the map projection coordinates.
#If you do, you can hop into terminal and convert the file
#to WGS84, or do it in Q - to learn more about why you need to do this, take a look at
#https://en.wikipedia.org/wiki/Map_projection .

#Once you have your "Numpoints" field calculated, which gives the number of starbucks in each county,
#subset your data to only include Virginia (or, your state) counties and then save it as a CSV.

#From here, you will join the NHGIS data into the shapefile CSV based on the GIS join column,
#and use the simulation tools you learned in project 1 to make a case for if your companies
#business model has been predicated upon any type of demographic targeting.


# In[ ]:

#Some code snippets and examples you may find helpful:
NHGIS_shp_base = Basemap(projection='stere', lon_0=float(longitude_center_new), lat_0=float(latitude_center_new),                width=1500000, height=1500000, resolution='i')


NHGIS_shp_base.readshapefile('/sciclone/home2/geogdan/Project_2/NHGIS/US_county_2015_reprojected', 'US_county_2015_reprojected')

#Highlight countries in virginia
for info, shape in zip(NHGIS_shp_base.US_county_2015_reprojected_info, NHGIS_shp_base.US_county_2015_reprojected):
    if info['STATEFP'] == '51':
        x , y = zip(*shape)
        NHGIS_shp_base.plot(x,y, marker=None, color='m')
    else:
        NHGIS_shp_base.

plt.show()

#Other notes:
#Getting an encoding error?  There are multiple solutions to this, both code-based and
#otherwise.  The issue is in the dbf file; change the encoding on that file however you know how if you run
#into this issue!  utf-8 is what you want.



# **Coursework 1 Volcanoes and Meteorite Landings**

[Repository URL](https://github.com/ucl-comp0035/comp0034-cw1-group-14)

[Video Demo on UCL Media Central](https://mediacentral.ucl.ac.uk/Player/6cBjAC9J)

## **HOW TO RUN THE WEB APP** 

Run the [main.py](main.py) file to run the web app on [http://127.0.0.1:8050/](http://127.0.0.1:8050/)

DASH MUST BE AT LEAST VERSION 2.1.0, THE APP WILL NOT WORK WITH 2.0.0.

The dash version can be checked using: 
```
pip show dash
```

You can specify the dash version in pip by running:
```
pip install dash==2.1.0
```
## File Structure 

[main.py](main.py) -Runs the web app <br/>
[Scripts](scripts) -Includes code which was used to edit the data files<br/>
[Data](data) -Contains updated data. Most visualisation in the web app needed an updated version of the data so multiple new data files were made<br/>
[dash_app](dash_app) -Contains the main code for the app<br/>
-[dash_app\assets](dash_app/assets) -Contains most of the styling for the web app<br/>
-[dash_app\tabs](dash_app/tabs) -Includes the contents of each tab in a seperate file<br/>
-[dash_app\tabs\classes\map.py](dash_app/tabs/classes/map.py) -Contains a map class because the map needed to be reused many times<br/>



## **General Features and Design Layout**

This dash app is a multipage design consisting of four tabs, each containing different visualisations to address the needs of the target audience in different ways and present volcano and meteorite data in different ways. Each visualisation contains a method to filter the data such as range sliders or filter search boxes within tables. The dash app has a night mode feature which spans across all pages and allows the user to change the colour scheme of the page to a darker colour palette in order to reduce blue light exposure and help reduce eye strain when viewing for long periods of time, this does not change the functionality of visualisations or tabs.

The general target audience for the dash app comes under three general categories, astrologists who take interest in data regarding meteorites such as their names, locations and masses who require quick and easy to understand information so that they can use it for their research and projects as well as farmers who show interest in volcano information such as location as the land around volcanoes is rich in minerals and thus more fertile, making it a better location for farms. The third category for the target audience covers generic hobbyists who simply take interest in meteorite and volcano information.  

Personas for the two main target audience members, astrologists and farmers, are shown below:  
["Astrologist Persona"](personas/astrologist_persona.png)  
["Farmer Persona"](personas/farmer.png)

# **Map Tab**
## **Dot Map of Volcano and Meteorite Landings and Discoveries**
### **Target Audience**

For this visualisation the target audience focuses on members who are specifically interested in a general overview of all the data such as location of meteorites, masses of individual meteorites, names of meteorites as well as location, volcano explosivity index (VEI), names of volcanoes as well as their start and end dates. Astrologists and farmers who require a general overview of all the information can access it quickly and easily.

### **Which questions does this visualisation answer?**

This visualisation answers the following questions and can be filtered by year:  
- What are the locations of meteorite landing sites?  
- When did each meteorite land/ when was it found? 
- What is the mass distribution of the meteorites that landed?  
- Where do volcanoes occur?  
- How intensive were the eruptions of these volcanoes?
- Are historic volcano data points recorded in more specific areas of the world?  
- How long do volcanoes last for?

### **Explanation**

The data needed to answer these questions includes the date, name, latitude and longitude of the meteorite landings as well as the masses of the respective meteorites, all of which is present in the dataset. For the volcanoes, the locations, date, name of volcano, VEI as well as start and end dates for the volcano are used.

This visualisation is in a dot map format and contains an interactive map which highlights the position of the meteorite discoveries/ landings as well as volcanoes using coloured dots which are proportional to the mass, or VEI of the respective meteorites or volcanoes with larger dots representing greater masses or VEI respectively.
When the user hovers over a given meteorite or volcano, all the information regarding the object is given in the hover menu as well as an indicator to the right of the map to show the mass or VEI of the meteorite or volcano respectively, as well as a link to a browser search where more information regarding a specific meteorite or volcano can be found.

A dot map is useful for this application because it allows the users to visually identify patterns or trends for the landing locations while being easy to grasp and providing a good overview of the data. A disadvantage of dot maps is that they generally are not good at allowing users to retrieve exact values. This is overcome by the ability for the user to hover over specific dots to provide exact information as well as the ability to pan and zoom the map, giving the user the ability to focus on specific locations with ease. 

The dot map also included features such as a checklist to allow the user to show only meteorite discovery or volcano locations as well as range sliders which filter the data by year. This prevents the dot map from becoming cluttered and allows the user to fulfil their need to easy data navigation. There is also an option to view the map in a 3D mode which causes the map to appear as a globe instead of a 2D map, this is simply an aesthetic change which may be preferable to some users. An option to view the dots as a heat map where different colours represent the years that the data was recorded, is also included and allows the user to visualise the data over a time period.

### **Evaluation**

This visualisation answers the questions very well as it provides a great deal of information about both meteorites and volcanos. Firstly, the dot map design allows the user to quickly identify where the meteorites and volcanos are located in an easy to understand manner and the dots provide useful visual cues as to the VEI of the volcanos and the masses as their size represents these qualities. Secondly, all the other information regarding the volcanoes and meteorites, is displayed in a visually appealing way through the hover menu and the additional pop-up menu to the side of the map. The user has access to all the necessary information that they can need and have the ability to filter the data by year, tailoring to each user's individual needs. The interactive nature of the visualisation allows users to refine their search and only view the important information to them.  

A weakness of this visualisation is due to the amount of information it shows. When there are few filters applied, the map can appear rather cluttered and it can be difficult to navigate to specific meteors and/or meteorites. This can sometimes be avoided by panning and zooming into different areas of the map however, this could be improved by adding further filters which allow the user to reduce the amount of information being displayed at any one time and thus decluttering the map.

# **Bar Chart Tab**
## **Bar Chart of Countries with the Most Meteorites**

### **Target Audience**
This visualisation focuses on a target audience of astrologists as well as hobbyists who take particular interest in the locations of meteorites and which countries experience the largest number of landings/ discoveries over the years. 

### **Which questions does this visualisation answer?**

This visualisation answers the following questions and can be filtered by year:  

- Which countries have the largest number of meteorite discoveries/ landings over the years?
- How many meteorites land in each country over the years?
- Does the year have an effect on the country which has the highest number of meteorite landings/ discoveries?

### **Explanation**

The data needed to answer these questions is the location of the meteorite landings, specifically the country which was added to the dataset as part of the data preparation, using the existing latitude and longitude data.  

As the questions revolve around the concept of 'how many', a bar chart format was chosen to effectively display the number of meteorite landings per country in descending order, showing discrete data in an ordered and easy to understand format. This visualisation includes two range slider filters, one for the years shown on the chart and one for the number of meteorites so that the user can on view countries with a specified number of meteorites over a certain time period. There is a colour gradient used for the bars in order to distinguish countries from one another and make the visualisation easier to understand and extract data from. When the user hovers over a particular bar, the exact number of meteorites also given.

### **Evaluation**

The bar chart successfully informs the user of the number of meteorites per country through the use of the bar chart and this information can be filtered depending on the year and number of landings so that a user can efficiently access the data they need.  

The strengths of this chart are that it is easy to read and displays the number of meteorites for each country within the dataset. The ability to filter by year and number of meteorites using the two sliders makes the data very accessible and applicable to the user's specific needs. Sliders are very intuitive and require little thought during use, allowing the filtering to be quick and simple. 

Some weaknesses of this chart are that the user cannot search by country making some data harder to locate and this may become an issue if the user intends to search for a specific country that is not located within the dataset such as those with zero meteorite landings which are not included in the dataset. This could be improved by using a list of all the countries in the world on the data-frame so that those without any landings could be included. Another weakness is that the slider which filters by the number of landings is linearly scaled meaning that in some cases when the user changes the values on the slider, the data shown in the graph will not change by a large extent until the bottom end of the slider is reached as the maximum value. This could be improved by changing the scaling of the slider to a logarithmic scale, for example.

## **Bar chart of Average Mass of Meteorites per Country**
### **Target Audience**

This visualisation focuses on a target audience of astrologists as well as hobbyists who take particular interest in the average masses of meteors in each country throughout the years. They will be able to see which countries had meteors with the largest average mass of meteors.

### **Which questions does this visualisation answer?**

This visualisation answers the following questions and can be filtered by year:  

- What is the average mass of the meteors in each country?
- Which country has the largest average mass of meteors?
- How does the year affect the country with the largest average mass of meteors?

### **Explanations**
The data needed to answer these questions is the location/ country of the meteorite landings as well as the individual masses of each meteorite. The locations are available in the dataset, and the corresponding country was found and added to the csv file. 

Similar to the previous visualisation and chart. the questions revolve around the concept of 'how many', a bar chart format was chosen to effectively display the average masses of the meteors by country and thus displaying discrete data in an ordered and easy to understand format. The visualisation includes the same range slider to filter the years over which the data is shown and another slider to filter the data by the average mass of the meteors. There is also a colour gradient used for the bars in order to distinguish countries from one another, making the visualisation easier to understand and extract data from. Similar to the previous chart, the user can also hover over each bar for more specific and exact information.

### **Evaluation**
This visualisation performs in a similar way to the previous chart and has similar strengths and weaknesses. It successfully answers the intended questions and is easy to use and extract information from. The ability to filter by year and average mass of meteorites. The bar chart successfully informs the user of the number of meteorites per country through the use of the bar chart and this information can be filtered depending on the year and number of landings so that a user can efficiently access the data they need. The main strength is that it is very effective in providing the required information.  

Once again, the user is unable to search by country, therefore if the user wishes to find data for a country which is not present in the dataset, there is no element which informs them that it is missing. To improve this, the data-frame could be modified to include all countries so that it is clear that there is no data for some countries. The slider which filters by the average masses of the meteors also has the same issue as the previous chart due to the fact that the majority of the data lies at one end of the slider. For example, the USA has a very high average mass compared to other countries, so when moving the top end of the slider, the data will not change by a significant extent until the very bottom end of the slider is reached. This could be changed my modifying the scaling of the slider so that the range of masses is better represented along the length of the slider.

# **Line Graph Tab**
## **Lines Graph of Recorded Meteor Landings and volcanoes by year**
### **Target Audience**
The target audience for these two visualisations are meteorologists, farmers and hobbyists who are interested in the trend of the number of meteorites/ volcanoes recorded in each year. 
### **Which questions does this visualisation answer?**

- Is there a trend in the number of meteorites/ volcanoes discovered each year?
- What is the trend in the number of meteorites/ volcanoes discovered each year?

### **Explanation**
The data needed to answer these questions is the year in which the information about the meteorites and volcanos was recorded which is included in the dataset.  

These visualisations are in the line graph format as "line graphs are used to display quantitative values over a continuous interval or time period. A Line Graph is most frequently used to show trends and analyse how the data has changed over time." [3] For these reasons, a line chart is very appropriate to answer questions regarding trends over time.  

Similar to the previous visualisations, these line graphs also include a range slider which allows the user to filter data by years and focus the information on a specific time period, depending on the user's individual needs. The user can then see the line which shows the general trend.

### **Evaluation**

The main strength of these visualisations is that they are effective in displaying the number of volcano and meteorite recordings over a given time period, as line graphs are very well suited and very appropriate for this application. The user can easily see the increases and decreases in the number of recordings in a given period which makes the information easy to graph and extract a hypothesis from. However, these visualisations each only answer a single question regarding the trends in number of recordings and do not display any other information. These graphs can therefore be described as having a low information density. This could be improved by adding additional traces to the graphs, perhaps including the number of recordings from specific countries over time.


# **Data Table Tab**
## **Data Table with all Available Data Regarding Meteorites**
### **Target Audience**
The target audience for this visualisation covers all three of the target audience subgroups, meteorologists, farmers and hobbyists, specifically those who want to visualise all of the data in a tabular form in order to extract specific data regarding aspects. This could be in order to create their own visualisations or graphs as the pure numerical data is shown here.

### **Which questions does this visualisation answer?**

- What are the locations of the meteorites and volcanoes?
- When was the information recorded?
- What are the names of the volcanos and meteorites?
- What are the masses of the meteorites?
- What are the volcano explosivity indices of the volcanoes?
- What are the start and end dates of the volcanoes?
- Are historic volcano data points recorded in more specific areas of the world?

### **Explanation**

The data needed to answer these questions includes: the names of the volcanoes and meteorites, the years in which the data was recorded, the latitude and longitude of the meteorite landings and volcano locations, the masses of the meteorites, the VEI of the volcanos and the start and end dates of the volcanos. All of this data is present in the dataset files.  

This visualisation consists of a data table which lists all the data within the meteorite and volcano datasets, toggled between through the use of a dropdown menu, with the ability to search by column value by typing into the search fields within each column. For example, the user can search for a meteor with a given name by typing it at the top of the 'name' column and all the data regarding matching meteors will be displayed within the table. The search can be refined by sorting the data by year (ascending or descending) using the buttons next to the table headers. Finally, the user also has the ability to click on the desired meteor or volcano and a pop-up will be displayed showing the location on an interactive map. 

### **Evaluation**
This visualisation contains a very large amount of data that the user can utilise, as it contains the entire datasets and the user has the ability to filter through it, however, it has a number of limitations, mainly the fact that it does not visualise the data, but rather displays it all in a table. This results in poor readability as the user must navigate purely numerical and text data in order to find what they are looking for and this does not allow any trends or direct questions to be answered. The user can infer certain answers to the questions using the data, but it is neither quick, nor simple to do so due to the layout of the data. This form of data presentation would function better as complementary information to the other visualisations rather than a stand-alone one.  

However, the user can get an approximate understanding of where historical volcano points were recorded by sorting the data by year. Not only can they find out about the very earliest recorded volcanoes but can also sort them to see the most recent ones.

# **Testing**

Using Selenium to load the web app and switch between tabs, tests were performed using Pytest to confirm that the headings of the pages changed as the different tabs were navigated. A test was also performed to check that when the main page was loaded, the default values of the checkboxes were as expected. Another test was also performed to check that the dropdown menu on the 'Table' tab was correctly set to meteor data when the page was loaded

## **References**
### IEEE Format**



[1](dash_app\tabs\table.py)
Dash, 2020. Rename dash table columns. [online] Plotly Community Forum. 
Available at: <https://community.plotly.com/t/rename-dash-table-columns/39604/6> [Accessed 13 February 2022].

[2](dash_app\tabs\table.py)

Dash, 2020. Rename dash table columns. [online] Plotly Community Forum. 
Available at: <https://community.plotly.com/t/rename-dash-table-columns/39604/6> [Accessed 13 February 2022].

[3](README.md)

Dash, 2020. Rename dash table columns. [online] Plotly Community Forum. 
Available at: <https://community.plotly.com/t/rename-dash-table-columns/39604/6> [Accessed 13 February 2022].

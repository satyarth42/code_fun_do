# codefundo++
<hr>

## Challenge
  Find better ways to save lives and prevent economic losses through mechanisms to predict, prevent, or manage the impact of natural disasters.

## Abstract
  Natural Language Processing will be implemented with the use of Machine Learning techniques on text data mined from Twitter and News sites with the help of APIs to collect the mentions of natural disasters such as flood, earthquake, cyclone, tsunami, forest fires etc. and then identify the geographical location of the calamity in order to create some sort of alert notification to the public in that area and also the different governmental and non-governmental organisations in order to minimise the loss of life and also of the economy in an efficient manner. Facebook's Disaster Maps' data can also be used to identify the population density, movement data and safety checks ratio according to the geospatial mapping in the calamity struck area. Using these data we will be able to predict the population which requires help in order to minimise the loss of life and economy.
  
## Details
  1 We will be using the <a href='https://www.figure-eight.com/data-for-everyone/'><b>Disasters on social media</b></a> to train our Machine Learning model to identify the mentions of natural disasters. This model will then check for the mentions of natural disasters through checking through Tweets in real time to identify the disasters and if possible the location where it has occured to create some kind of geo-spatial analytics and then use those analytics to raise an alarm towards the governmental and non-governmental bodies active in those area.
 
 2 We will also mine the text data from news using <a href='https://newsapi.org/'>NewsAPI</a> to mine for type pf natural calamity and the location and raise public warnings.
 
 3 The Facebok Disaster Maps data will provide us with the population density in each locality in disaster affected area in order to identify the risk involved in each small area and distribution of rescue teams and resources accordingly. The Safety Check functionality can be used to come up with insights to measure the instensity of the calamity in each small sector in order to alert the authorities accordingly. The Movement maps data will allow us to identify the movement insights of the general public in the calamity hit area, this can be used to inform the authorities to come up with an efficient plan of action such as allocation of transport facility accordingly, raising warnings if necessary etc.
 
## Dataset to be used
[Disasters on social media](https://www.figure-eight.com/data-for-everyone/)

# Solution for codefundo++
<hr>

## Workflow for the Solution
  
 1 We are using Natural Processing Language to extract names of relevant cities from data collected from Twitter and various News Api's.
  
 2 We are using Machine Learning algorithm for predicting the severity of the earthquake based on the Earthquake dataset available on
 Kaggle.The dataset contains the magnitude,Latitude and Longitude of the earthquakes in last 65 years.Now we have the complete predicted 
 data in JSON form which we can get using a Location API.
  
 3 Creation of Location API which updates the Admin with recent Twitter data and various News api's data.

 4 Creation of a user-login application which has two types of users(Admin and Public User).
   
 5 We have a registration page for new users whose credentials are being stored in a Mongodb Database.
   
 6 Role of the Admin is to update the Location API in every regular interval.
   
 7 The application uses geolocation feature to fetch the current location of the User.
   
 8 After fetching the current location we are using the Euclidean Distance formula considering the Latitude and Longitude and will alert the user with a proper notification of the nearest calamity with proper details based on the calculated Euclidean Distance.      
  
## Dataset used 
[Disasters on Kaggle](https://www.kaggle.com/usgs/earthquake-database#database.csv)

## Technologies Used

  1. 

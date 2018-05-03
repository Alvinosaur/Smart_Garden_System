Plant Simulator Garden: https://drive.google.com/file/d/1y4aT1SPUd-Vwk_GRunY7M-RDs1hJOZL3/view

Automated, Self-Learning Garden
Alvin Shek
15-112 Term Project
April 2018



Project Summary
The Automated, Self-Learning Garden is an CNC-styled gardening system that can distinguish between crops and weeds using computer vision and machine learning. With sensors to monitor the environment and computer vision for plant growth, the system will learn the most optimal environmental factors and times for growing different plant species and provide this as advice to users. The garden will also incorporate data weekly forecasts and warn the user about days where proactive measures may be necessary to protect certain plants. 

Parts
Hardware:
Arduino
Raspberry Pi
Raspberry Pi Camera Module
Wireless Bluetooth module (2)
Temperature, light, and moisture sensors
CNC-styled setup with stepper motors and bearings

Software:
Languages: Python, Arduino IDE(C/C++)
Pyserial, Matplotlib

Specifications
The core component of this project will involve the development of a program to take in data on different instances of different plant species and not only provide advice to the user for the best plants to grow at the current time, but also output estimated yield. 

The system will use OpenCV to detect plants and classify them as desirable or unwanted. Using machine learning, the system will find the best-fit match of the plant and record the plant’s size, leaf color, soil humidity, and location with the arduino remaining aware of how far its stepper motor ran. Every hour, an Arduino will record the temperature and brightness and send this to the raspberry pi to log. 

Such a huge database will have to be organized object-oriented programming and different levels of dictionaries and sets for high efficiency. Data will then be plotted with matplotlib and user interface. The user will be able to enter the name of a specific plant and choose between different instances of that plant to see its growth over time in conjunction with data on temperature, humidity, and brightness. 

Competitive Analysis
Automated farming is not new. Many DIY enthusiasts, research groups, and startups have created their own automated gardens using many features that I hope to develop: weed detection and extermination and collecting online weather data. A startup created at CMU, Farmbot has already commercialized automated gardening with the use of Arduino’s and sensors, weed-detection with computer vision, and even an app that helps users plan out their garden. Countless tutorials and Youtube videos also demonstrate computer vision with machine learning. 

My program, however, will be unique for its ability to analyze data on plant growth and determine the most optimal environmental parameters for that specific plant. This system will learn from the results of different planting choices by users and determine where, when, and how different species of plants grow best. Over time, the system will apply weather-tracking and time-awareness to advise the user on planting choices. 

Structural Plan
The program will have a major collection of csv files and functions to perform the image processing for weed detection and plant growth monitoring. A body of files will collect images from an online database. Plants themselves will be stored into a dictionary as keys with incremental numbers following their name and contain values for location, size, and soil moisture in that location. 

Algorithmic Plan
The most difficult part of this project will involve the heuristic or machine learning model for taking in large amounts of data and classify species of plants with their most optimal growth environments. The system will weigh factors based on their influence on plant growth and also create an continuous average of values for environmental factors. For sorting all the plants, the program will create a series of classes for plant species with specific instances of each species. Instances will be named by their count(ex: the fourth pepper plant will be named “Pepper4”); each instance will contain its own data set as a dictionary with dates as dictionaries themselves using hourly times as keys and sensor recordings as values. All this data will be stored securely in csv files organized in a similar hierarchy of folders:
Data → Species → Instances → Dates → real data
The system will allow the user to display different graphs: collective growth trends of a certain plant instance or species with temperature, moisture, and light values. This will involve collecting data 
Timeline

Date
Task Completed
Thursday, April 19
Machine Learning Tech Demo
Tuesday, April 24
Learning system, graph plotting
Thursday, May 3
Fully-functional system!

Github
https://github.com/Alvinosaur

Future Goals
Once I complete all my goals for the project, I have many more extensions in mind: 
Predict if the player is smashing or dropping a birdie before action happens, use this is player v.s computer game AI or provide information to opponent
Show interactive screen for allowing user to “start match”
Kinect will be placed under the net
Maybe lock onto birdie to analyze whether birdie will go over net in interactive player game v.s AI
Maybe have doubles game mode to analyze two players.. Lock onto players’ skeletons based on their shirt color
Possibly have it detect snails on the leaves or infections
Isolate the plant image and then run processing again for large blob anomalies of color like brown
Send user warning


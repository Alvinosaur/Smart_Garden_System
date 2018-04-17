# Smart_Garden_System
Uses machine learning to determine optimal growth environment of diff. plant species and advise user.
Automated, Self-Learning Garden
Alvin Shek
15-112 Term Project

Project Summary
The Automated, Self-Learning Garden is an interactive program that will distinguish between desired plants and weeds and incorporate various sensors and computer vision to monitor plant growth and provide the user optimal environmental factors for growth. The garden will also incorporate data weekly forecasts and warn the user about days where proactive measures may be needed to protect plants. 

Parts
Hardware:
Arduino
Raspberry Pi
Raspberry Pi Camera Module
Wireless Bluetooth module (2)

Software:
Languages: Python, Arduino IDE(C/C++)
PostgreSQL, Pyserial, Matplotlib

Specifications

The core component of the project will use OpenCV to detect plants and classify them as desirable or unwanted. Using machine learning, the system will find the best-fit match of the plant and record the plant’s size, leaf color, soil humidity, and location with the arduino remaining aware of how far its stepper motor ran. Every hour, an Arduino will record the temperature and brightness and send this to the raspberry pi to log. 

Such a huge database will have to be organized with MySQL. Data will then be plotted onto a webserver with matplotlib and user interface. The user will be able to enter the name of a specific plant and choose between different instances of that plant to see its growth over time in conjunction with data on temperature, humidity, and brightness. 

Some additional features that I hope to achieve include additional learning models that will allow the program to provide the user with advice for growing different plants based on optimal environmental factors and seasons. The program 

Possibly have it detect snails on the leaves or infections
Isolate the plant image and then run processing again for large blob anomalies of color like brown
Send user warning


Competitive Analysis
Automated farming is not new. Many DIY enthusiasts and startups have created their own automated gardens using many features that I hope to develop: weed detection and extermination, data logging, and reading online weather data. My program, however, will be unique for its ability to analyze data on plant growth and determine the most optimal environmental parameters for that specific plant. The system will then apply weather-tracking and time-awareness to offer advice to the user on where and when to grow a specific plant. 

Structural Plan
The program will have a major collection of csv files and functions to perform the image processing for weed detection and plant growth monitoring. A body of files will collect images from an online database. Plants themselves will be stored into a dictionary as keys with incremental numbers following their name and contain values for location, size, and soil moisture in that location. 


Algorithmic Plan
The most tricky part of the kinect-side of this project will involve guessing the player’s stance from all the joint positions in 3D space. 

Timeline


Github
https://github.com/Alvinosaur

Future Goals
Once I complete all my goals for the project, I have many more extensions in mind: 
Predict if the player is smashing or dropping a birdie before action happens, use this is player v.s computer game AI or provide information to opponent
Show interactive screen for allowing user to “start match”
Kinect will be placed under the net
Maybe lock onto birdie to analyze whether birdie will go over net in interactive player game v.s AI
Maybe have doubles game mode to analyze two players.. Lock onto players’ skeletons based on their shirt color

# Strategy-Based Farming Game:

Alvin Shek  

15-112 Term Project, video: https://youtu.be/0gHhN09BUe0

April 2018

# Project Summary:
The Garden Simulator is a single-player game that reflects real-life problems surrounding modern agriculture. Often, environmental factors such as rain, heat, and brightness fluctuate throughout the year, confining conventional farmers to specific seasons with specific tasks. This game allows the user the to experiment with different months for growing as well as their idea of ideal environmental factors for plants. The game also features a mini-game of killing weeds either with manual clicking or with herbicides. 

# Modules:
Languages: Python
Numpy, sklearn, scipy, pandas

# Specifications:
The first noticeable feature of this game is the extreme weather generation. Users can select a specific month and see the probability of at least one occurrence of a particular weather event: hot weather, rain, and brightness. These weather events not only affect plant growth rate, but also determine the probability of bugs and weeds spawning. The heat normal distribution is centered around June. Rain is centered around January. Brightness is a bimodal distribution with peaks in spring and fall months. 

The next major feature is the plant growth. Users can interact with three sliders to guess the ideal temperature, soil moisture, and brightness levels of the garden. Then, every plant species’ predicted growth rate is calculated by passing through each environmental factor into an sklearn linear regression model with prebuilt data. Of course, different plant species favor different environmental parameters and this uncertainty forces users to experiment and find a balance for all their crops-- a problem farmers everywhere face. 

Another key component is the bug and weed generation. Both these factors have their own probabilities that weigh environmental anomalies. For instance, bugs weigh the occurrence of hot and rain events with 0.4 and weigh brightness with 0.2. This is because brightness should not really affect bug activity. Every so often, every plant will get a chance of getting spawned with a bug. If infected, the bugs will continue to spawn and weak the plant(ie: reduce their size). Every plant’s probability of spawning a bug is not only determined by its own species, but also the distance from neighboring plants. In nature and new farms, crops are often planted with seemingly random plants. This increases biodiversity and reduced the likelihood that bugs can quickly spread. In a similar way, players can surround high-valued plants like strawberries with low-value, but “defense” plants like dill that ward off bugs. Also, already-infected plants can spawn bugs on other plants based on the distance. In nature, plants living next to infected neighbors will most likely get infected themselves. 

Lastly, users can get more points by killing the weeds that randomly spawn. Weeds spawn almost randomly, except they have a higher probability based on their distance from other weeds. This makes sense since weeds spread seeds near themselves. Users can either manually click weeds or use giant “bombs” of herbicides. While herbicides effectively wipe out large groups of weeds, they can have a long-lasting impact on the health of the soil and environment. Thus, wherever players use herbicides, they will not be able to plant plants in that location for all future rounds. This hopefully teaches players that all choices have drawbacks. Manual removal with organic/safe methods is extremely slow, but herbicides and chemicals can hurt the environment. 

# Competitive Analysis:
As far as I know, there are lots of gardening simulator games, but these all focus on the typical style of collecting resources and growing new plants. These do not focus on real-world factors such as herbicide usage on weeds, bugs, and biodiversity. 

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


# Updates:
This entire document is my TP3 update! I chose to restart projects twice actually. I wasn’t able to collect depth values of specific joints with the microsoft kinect. I also wasn’t able to make a functioning neural network for predicting variables-- mine instead only could be used for probability classification. Although my project didn’t meet my initial dreams, I am more than pleased with my persistence in working, even after two grueling failures. To put this situation into perspective, 15112 students are expected to finish “TP2” or a minimum viable product by the week before the project is due. I was just moving on from the neural network at this point and had to create a completely new project within a week with papers and two final exams


# To play, please follow the below instructions:

1. Download "Plant_Data". Make sure these are in the same directory as the file.  
2. Download one file:
      plantGame.py
3. Download homebrew by entering this into terminal:

```/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"```

4. Download pip by entering this into terminal:

```brew install pip```

5. Download packages:
```brew install python numpy scipy
      pip install -U scikit-learn
      pip install pandas```
6. Run the game with your IDE!

If you do not have an IDE(Integrated Development Environment):
Download the Sublime IDE for your operating system: https://www.sublimetext.com/3

# Sources:
15112 Website: http://www.cs.cmu.edu/~112/notes/notes-animations-demos.html
      Tkinter animation and run() function
      
Linear Regression Tutorial with scikit: http://scikit-learn.org/stable/modules/linear_model.html
      linReg(data) function 
 

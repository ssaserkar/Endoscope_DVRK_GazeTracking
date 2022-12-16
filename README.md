# Automating the Endoscope Camera of the DVRK using Tobii Eye Tracker 5 

##### In this repository, as a part of our Human-Robot Interaction Project, we have attempted to automate/operate the endoscope camera based on - Gaze tracking, keyboard and mouse interfaces.

 The main contributors of the Project were :
 Soham Shantanu Aserkar
 Uthiralakshmi Sivaraman
 Olivia Raisbeck

For this project, the following software dependencies are required:
```
Unity 3D 2020+
Anaconda 
Python 3.7
Torch 1.7.1
CUDA 11.0
```

For the purpose of the Project, we have used the Tobii Eye Tracker 5 to track the gaze and move the Camera wihtin the Unity Simulation.
We have setup the Unity Environment based on the real daVinci Research Kit from scratch and integrated the camera output to the main camera. 

Here are the steps to run the Unity Simulation:
```
1) Open the Unity Hub, find the project name titled "DVRK-ROS"
2) Click on the Project Structure.
3) Find the 'Working_Scene' in the Scenes Folder.
4) Connect the Tobii Eye Tracker 5
5) Upon pressing play, 
    hold down the key 'A' to move the camera based on Gaze
    hold down the key 'B' to move the camera based on Keyboard
    hold down the key 'C' to move the camera based on Mouse
```

For running the training of the Semantic Segmentation using the UNet++ architecture:
1) Install Anaconda and create new virtual environment based on the environment.yml.
```
conda create -f environment.yml
```
2) Upon ensuring the dependencies match the architecture from the environment and the dataset is structured as below:
  ```
  |__ src
	|__ data
		|__ datasets
                    |__ synapse
                        |__ train
                            |__ images
                            |__ groundtruth
                        |__ trainval
                            |__ images
                            |__ groundtruth
                        |__ test
                            |__ images
                            |__ groundtruth
                            
                    |__ cholec
                        |__ train
                            |__ images
                            |__ groundtruth
                        |__ trainval
                            |__ images
                            |__ groundtruth
                        |__ test
                            |__ images
                            |__ groundtruth
 ```
 3) Run the trainSegNet.sh file
 4) The resultant image is saved in the folder 'results'.
 
 

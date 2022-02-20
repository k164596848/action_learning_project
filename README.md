# Action_Learning_Project
## Introduction
- This project is for action estimation without any senser, it only use the video to estimate your action performance. The project have two part, one is the [UI system]( action_learning_UI ) , another is the [Core system](action_learning).


## Prerequisites
install python3.8, openpose, Vue3, Flask, and some packages.


## Result 

### Actions estimation 


<p align="center">
 <img src="doc/action_estimation.gif" width="360">    
</p>

### Different capture angle could work 
- if you move your camera capture angle, it still can estimate the action.
<p align="center">
 <img src="doc/multiangle.gif" width="360">    
</p>

### Multiple person action reconigtion and estimation
-you could do different action at one place , then estimate two action performance.

<p align="center">
 <img src="doc/multiperson.gif" width="360">    
</p>


# Limitaions 
- the capture angle is only 0~180 degree, and don't shot video from back.

- multiple person can't change switch their position.

- it's not real time process.

- the background should be pure and clear.



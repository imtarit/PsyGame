# PsyGame
## Pre requisities:
  1. Python 3.6
  2. Pygame 1.9
## Execution
```
python psyGame.py
````
## File list
### [icon.jpg](./icon.jpg)
Icon of the software
### psyGame.py
Main executable file
### pygame_textinput.py
Module for text input through pygame
### variables.txt
Difficulty variables. Can be changed during execution. Variable list:
* amplitude: Amplitude of the sin wave of the particle path
* length: Wave length of the sin wave
* slow: The inverse of the speed of the particle motion
* randDelay: Delay between random changes of particle positions from sin wave path
* randLevelX: Highest random range of value added to X coordinates of particles
* randLevelY: Highest random range of value added to Y coordinates of particles
* PartcleSize: Size of the particles in pixel

### Output files 
#### (SubID)_particle_result_(DateTime) 
Columns:
* subjectID: Subject ID
* block: Current block number
* trial: Current trial number
* randDelay: Delay between random changes of particle positions from sin wave path
* randLevelX: Highest random range of value added to X coordinates of particles
* randLevelY: Highest random range of value added to Y coordinates of particles
* PartcleSize: Size of the particles in pixel
* xPos: Position of the coursour in X axis.
* yPos: Position of the coursour in Y axis.
* Particle_(num)_X: X coordinate of	particle number (num). If the particle is touched then the coordinate is 'nan'.
* Particle_(num)_Y: Y coordinate of	particle number (num). If the particle is touched then the coordinate is 'nan'.

#### (SubID)_particle_result_(DateTime)
Columns: 
* subjectID: Subject ID
* block: block number of current trial
* trial: Trial number of current trial
* trialLen: Length of current trial
* DRTAStart: Start time of DRTA in current trial 
* DRTAEnd: End time of DRTA in current trial
* RTTime: Response
* trialTime: Trial end time 
* trialScore: Number of particle touched in current trial






 

# twip
Simulation for two-wheeled* inverted pendulum

## Environment
Simple sim is only dependent on matplotlib, scipy, yaml, and numpy.   
These packages can be installed or, after installing Anacoonda, the following line can be run to set up a venv automatically:   
`conda env create --file <your twip directory>/config/environment.yml --name twip`

## Settings
The yaml file `settings.yml` is used to set the physical parameters of the pendulum, the dimensions of the animation, and any control parameters the algorithm requires.   
The control algorithm of choice is modified by changing line 36 of sim.py to assign the `control` variable a different class.   

## Running 
Run `sim.py` from the src folder. A plot showing the state space and an animation will appear

*Currently only 2D, so one wheel

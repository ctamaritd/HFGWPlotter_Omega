# HFGWplotter_Omega: Gravitational Waves Plotter for stochastic signals and power-law-integrated sensitivities

### Created by Francesco Muia, Andreas Ringwald and Carlos Tamarit. Code maintained by Carlos Tamarit

### Credit for the data of the plots go the authors of arXiv:2501.11723, whose results and figures are the basis of this plotter

HFGWplotter_Omega is an interactive web application designed for visualizing and analyzing gravitational wave data in the form of stochastic signals plus power-law-integrated sensitivities. It offers a user-friendly interface, allowing researchers and enthusiasts to explore and interpret gravitational wave data effectively.

# Online version

The app is running online at 

https://incandenza-01.zdv.uni-mainz.de/Omegaplot/

# Dependencies

Requires python3 with the following additional dependencies:

numpy
scipy
bokeh
flask
matplotlib

For example, assuming python3 is installed you can create a python virtual environment

$python3 -m venv python-virtual-env

Inside the environment, you can install the dependencies using pip

$pip install numpy scipy bokeh flask matplotlib

To load the environment:

$source python-virtual-env/bin/activate


# How to run

If you are using a virtual environment, make sure it is activated (see "source" command above)

Execute the following command in the main folder

python3 app_local.py 

The plot can be accessed in a browser by entering the following local address:

http://127.0.0.1:5003/Omegaplot




## Project Structure

The application is organized as follows:

```
HFGWplotter_Omega/                  # Project directory
│
├── Curves                          # Repository containing all the curves to be plotted
|   ├── TheoreticalBoundsCurves     # Repository containing all theoretical bounds
│   ├── DetectorCurves              # Repository containing all detector curves
│   └── SignalCurves                # Repository containing all signal curves, divided into "Cosmological sources" and "PBHs"
│       ├── CosmologicalSources
│       └── PBHs
│
├── aux                             # Repository containing auxiliary files
│   ├── aux_functions.py            # File containing auxiliary functions
│   ├── data_files.py               # File containing information about the curves to be plotted
│   ├── imports.py                  # File containing all the imports
|   └── signal_functions.py         # File containing definitions for functions for some signal spectra (e.g. 1st order phase transitions)
|
│   
├── Omegaplot 
│   ├──static/                      # Static files
│   │   ├── css/                    # CSS files
│   │   │   └── styles.css          # Main stylesheet
│   │   └── js/                     # JavaScript files
│   │         └── scripts.js        # JavaScript logic
│   │ 
│   └── templates/                  # HTML templates
│         └── index.html            # Main HTML template
│
├── app_local.py                    # Main Flask application
└── README.md                       # README file
```

## Features

### Current Features

- Interactive plotting of gravitational wave signals and power-law-integrated sensitivity curves
- Change between plotting energy spectrum or characteristic strain
- Toggle visibility of different curves.
- Annotations on the plot that provide additional information.
- Customizable plot ranges and dimensions through interactive sliders.
- Users can upload their own signal curves from a csv file
- For user supplied curves, the total energy fraction in GWs, and the corresponding ΔNeff are estimated and checked against the BBN dark radiation bound



## Contributing

Contributions to HFGWplotter are welcome, whether they be in the form of feature requests, bug reports, or pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License

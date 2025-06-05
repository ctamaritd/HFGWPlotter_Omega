# HFGWplotter_Omega: Gravitational Waves Plotter for stochastic signals and power-law-integrated sensitivities

### Created, updated and maintained by Francesco Muia, Andreas Ringwald and Carlos Tamarit.

HFGWplotter_Omega is an interactive web application designed for visualizing and analyzing gravitational wave data. It offers a user-friendly interface for plotting various gravitational wave signals and detector sensitivity curves, allowing researchers and enthusiasts to explore and interpret gravitational wave data effectively.

# Dependencies

Requires python3 with the following additional dependencies:

numpy
scipy
bokeh
flask
matplotlib


# How to run

Execute the following command in the main folder:

python3 app.py 

The plot can be accessed in a browser by entering the following local address:

http://127.0.0.1:5003/Omegaplot




## Project Structure

The application is organized as follows:

```
GWplots/                            # Project directory
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
│   └── import.py                   # File containing all the imports
│   
├── Omegaplot 
│   ├──static/                         # Static files
│   │   ├── css/                        # CSS files
│   │   │   └── styles.css              # Main stylesheet
│   │   └── js/                         # JavaScript files
│   │         └── scripts.js              # JavaScript logic
│   │ 
│   └── templates/                      # HTML templates
│         └── index.html                  # Main HTML template
│
├── app.py                          # Main Flask application
└── README.md                       # README file
```

## Features

### Current Features

- Interactive plotting of gravitational wave signals.
- Toggle visibility of different gravitational wave detector sensitivity curves.
- Annotations on the plot that provide additional information.
- Customizable plot ranges and dimensions through interactive sliders.


### Planned Features

1. **Custom Curve Addition**: Introduce options for users to add their custom curves, either through mathematical expressions or by uploading data files in txt/csv formats.

2. **Total ΔN<sub>eff</sub> Calculation**: Provide a feature to calculate the total effective number of relativistic species (ΔN<sub>eff</sub>), based on the plotted signals.



## Contributing

Contributions to HFGWplotter are welcome, whether they be in the form of feature requests, bug reports, or pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This is a public project, open to everyone, and aimed at serving the scientific community by providing a standard yet fully customizable gravitational waves plotter.

Users are free to use, modify, and distribute this software. If you utilize this project in your research or in any other capacity, please acknowledge the authors by citing the relevant publications.

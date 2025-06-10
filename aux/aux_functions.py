# aux_functions.py
import numpy as np
import pandas as pd
from bokeh.models import RangeSlider,  CustomJSTickFormatter, Slider, LabelSet, ColumnDataSource, Line, ColorPicker, TextInput
from bokeh.models.widgets import RadioButtonGroup
from scipy.interpolate import RegularGridInterpolator as RGI
from aux.signal_functions import OmegaPT
#from aux.data_files import signal_data


Tstar0 = 1E15
alpha0 = 0.1
betaOverH0 = 1.
vw0 = 0.4
gstar0 = 106.75




class Data:
    def __init__(self, x_coord, y_coord, color, linewidth, linestyle, opacity, depth, label, physics_category=None,  curve_category=None, comment=None, delta_x=0, delta_y=0, label_angle = 0, label_color = 'black', label_size ='9pt'):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.color = color
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.opacity = opacity
        self.depth = depth
        self.label = label
        self.physics_category = physics_category
        self.curve_category = curve_category
        self.comment = comment
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.label_angle = label_angle
        self.label_color = label_color
        self.label_size = label_size

        #if len(x_coord) != len(y_coord):
        #    raise Warning("x_coord and y_coord have different dimensions")

    def load_data(file_path, color, linewidth, linestyle, opacity, depth, label, physics_category,  curve_category, comment, delta_x, delta_y, label_angle, label_color, label_size):  # Update function signature to accept category
        if file_path.lower().endswith(".txt"):
            data = np.loadtxt(file_path, dtype=float)
            if (data.ndim >= 2):
                x_coord, y_coord = data[:, 0], data[:, 1]
            else:
                #Only single value
                x_coord = np.array([data[0]])
                y_coord = np.array([data[1]])
        if file_path.lower().endswith(".csv"):
            data = np.genfromtxt(file_path, delimiter=",", dtype=None, encoding=None)
            # Sort the array based on the first value in each pair
            #data = data[np.argsort(data[:, 0])]
            #data = data[np.argsort(data[:, 0])]
            x_coord, y_coord = data[:, 0], data[:, 1]
            #Implement corrections. MAGO data shows things in terms of omega, not f, so need factors of 2pi
            if (label=='MAGO') or (label == 'MAGO (res)'):
                x_coord = 1/(2*np.pi)*x_coord
                y_coord = 1/np.sqrt(2*np.pi)*y_coord
        #For signals calculated on the fly: phase transitions
        if label == '1st-order p.t.':
            #For PT, compute array for default parameters, T at weak scale 200 GeV, alpha = 0.1, beta = 10, v = 0.4, gstar = 106.75
            x_coord = 10**np.linspace(-18,21,200)
            x_coord = np.array(x_coord)
            y_coord = OmegaPT(Tstar0, alpha0, betaOverH0, vw0, gstar0, x_coord)
            y_coord = np.array(y_coord)
            #For 1st-order p.t. we compute label position and angle near peak
            derivative = np.gradient(np.log10(y_coord), np.log10(x_coord))
            nan_mask = np.isnan(derivative)
            # Filter out NaN elements using the mask
            derivative = derivative[~nan_mask]
            position_min = np.argmin(abs(derivative))
            delta_x = 1/1000*x_coord[position_min]
            position_label = np.abs(x_coord - delta_x).argmin()
            delta_x = x_coord[position_label]
            delta_y = y_coord[position_label]
            label_angle = np.arctan(derivative[position_label])
        #For signals calculated on the fly: user. Just do dummy vector
        if label == 'Your curve':
            x_coord = 10**np.linspace(-18,21,100)
            y_coord = np.array([ 1E-200 for _ in range(100) ])

        return Data(x_coord, y_coord, color, linewidth, linestyle, opacity, depth, label, physics_category, curve_category, comment, delta_x, delta_y, label_angle, label_color, label_size)  # Pass the category to Data initialization

def load_and_categorize_data(detector_data, theoretical_bounds_data, signal_data):
    #global hc_cosmic_strings
    #hc_cosmic_strings = interpolate_cosmic_strings(signal_data)
    data_instances = {}
    physics_category_dict = {
        'Existing': [],
        'Ongoing': [],
        'Proposed': [],
        'TheoreticalBounds': [],
        'Signals_Envelope': [],
        'Signals_Individual': []
    }
    curve_category_dict = {
        'Lines': [],
        'Curves': [],
        'Areas': [],
        'SingleFreq': [],
        'Points': []
    }



    #For detector_data
    for file_path, label, physics_category, curve_category, color, linewidth, linestyle, opacity, depth, comment, delta_x, delta_y, label_angle, label_color, label_size in detector_data:
        data_instances[label] = Data.load_data(file_path, color, linewidth, linestyle, opacity, depth, label, physics_category, curve_category, comment, delta_x, delta_y, label_angle, label_color, label_size)

        if physics_category == 'Existing':
            physics_category_dict['Existing'].append(label)
        elif physics_category == 'Ongoing':
            physics_category_dict['Ongoing'].append(label)
        elif physics_category == 'Proposed':
            physics_category_dict['Proposed'].append(label)

        if curve_category == 'Lines':
            curve_category_dict['Lines'].append(label)
        elif curve_category == 'Curves':
            curve_category_dict['Curves'].append(label)
        elif curve_category == 'Areas':
            curve_category_dict['Areas'].append(label)
        elif curve_category == 'SingleFreq':
            curve_category_dict['SingleFreq'].append(label)

    #For theoretical_bounds_data
    for file_path, label, physics_category, curve_category, color, linewidth, linestyle, opacity, depth, comment, delta_x, delta_y, label_angle, label_color, label_size in theoretical_bounds_data:
        data_instances[label] = Data.load_data(file_path, color, linewidth, linestyle, opacity, depth, label, physics_category, curve_category, comment, delta_x, delta_y, label_angle, label_color, label_size)

        if physics_category == 'Theoretical Bound':
            physics_category_dict['TheoreticalBounds'].append(label)

        if curve_category == 'Lines':
            curve_category_dict['Lines'].append(label)
        elif curve_category == 'Curves':
            curve_category_dict['Curves'].append(label)
        elif curve_category == 'Areas':
            curve_category_dict['Areas'].append(label)
        elif curve_category == 'SingleFreq':
            curve_category_dict['SingleFreq'].append(label)
        elif curve_category == 'Points':
            curve_category_dict['Points'].append(label)

    #For signal_data
    for file_path, label, physics_category, curve_category, color, linewidth, linestyle, opacity, depth, comment, delta_x, delta_y, label_angle, label_color, label_size in signal_data:
        data_instances[label] = Data.load_data(file_path, color, linewidth, linestyle, opacity, depth, label, physics_category, curve_category, comment, delta_x, delta_y, label_angle, label_color, label_size)

        if physics_category == 'Signals_Envelope':
            physics_category_dict['Signals_Envelope'].append(label)
        elif physics_category == 'Signals_Individual':
            physics_category_dict['Signals_Individual'].append(label)

        if curve_category == 'Lines':
            curve_category_dict['Lines'].append(label)
        elif curve_category == 'Curves':
            curve_category_dict['Curves'].append(label)
        elif curve_category == 'Areas':
            curve_category_dict['Areas'].append(label)
        elif curve_category == 'SingleFreq':
            curve_category_dict['SingleFreq'].append(label)
        elif curve_category == 'Points':
            curve_category_dict['Points'].append(label)



    return data_instances, physics_category_dict, curve_category_dict

# Create plot sliders, and button for h vs Omega

def create_sliders(fig,  Shmin, Shmax):
    range_slider_x = RangeSlider(
        title=" Adjust frequency range",
        start=-18.,
        end=20.,
        step=1,
        value=(np.log10(float(fig.x_range.start)), np.log10(float(fig.x_range.end))),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(0))")
    )



    # range_slider_y = RangeSlider(
    #     title=r" Adjust $$h_c$$ range",
    #     start=-39.,
    #     end=-10.,
    #     step=1,
    #     value=(np.log10(float(fig.y_range.start)), np.log10(float(fig.y_range.end))),
    #     format=CustomJSTickFormatter(code="return ((Math.pow(10.,tick)).toExponential(0))")
    # )


    # range_slider_y_Omega = RangeSlider(
    #     title=r" Adjust $$\Omega$$ range",
    #     start=-40.,
    #     end=40.,
    #     step=1,
    #     value=(np.log10(float(Omegamin)), np.log10(float(Omegamax))),
    #     format=CustomJSTickFormatter(code="return ((Math.pow(10.,tick)).toExponential(0))")
    # )


    range_slider_y = RangeSlider(
        title=r" Adjust $$\Omega h^2$$ range",
        start=-30.,
        end=20.,
        step=1,
        value=(np.log10(float(Shmin)), np.log10(float(Shmax))),
        format=CustomJSTickFormatter(code="return ((Math.pow(10.,tick)).toExponential(0))")
    )


    slider_width = Slider(title="Adjust plot width", start=320, end=1920, step=10, value=int(1.61803398875*600))


    slider_height = Slider(title="Adjust plot height", start=240, end=1080, step=10, value=600)

    # Sliders for Phase Transition

    slider_pt_temp = Slider(
        title=" Phase transition temperature (GeV)",
        start=-3.,
        end=16.,
        step=0.05,
        value = np.log10(Tstar0),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    slider_pt_alpha = Slider(
        title=r" $$\alpha$$",
        start=-5.,
        end=3.,
        step=0.05,
        value = np.log10(alpha0),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    slider_pt_betaOverH = Slider(
        title=r" $$\beta/H$$",
        start=-6.,
        end=1.,
        step=0.05,
        value = np.log10(betaOverH0),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    slider_pt_vw = Slider(
        title=r" $$v_w$$",
        start=0.05,
        end=0.99,
        step=0.04,
        value = vw0
        #format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    # Code for h vs Omega button


    # Create a RadioButtonGroup widget
    h_vs_Omega_buttons = RadioButtonGroup(labels=[r"Plot energy fraction h²Ω", r"Plot characteristic strain h꜀"], active=0)


    user_color_picker = ColorPicker(title = "Line Color", color = 'darkred')

    user_label_input = TextInput(title = "Label", value = "My curve")

    user_label_size = TextInput(title = "Label Size", value = "9pt")

    user_label_x = Slider(
        title=" x coordinate of label",
        start=-18.,
        end=20.,
        step=0.1,
        value=-18,
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(0))"))


    user_label_y = Slider(
        title=" y coordinate of label",
        start=-47.,
        end=20.,
        step=0.1,
        value=-30,
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(0))"))


    user_label_angle = Slider(
        title=" Angle of label (degrees)",
        start=-np.pi,
        end=np.pi,
        step=0.01,
        value=0.,
        format=CustomJSTickFormatter(code="""return (tick * 180 / Math.PI).toFixed(0) + "\\u00B0";""")
    )





    return range_slider_x, range_slider_y,  slider_width, slider_height,  h_vs_Omega_buttons, slider_pt_temp, slider_pt_alpha, slider_pt_betaOverH, slider_pt_vw, user_color_picker, user_label_input, user_label_size, user_label_x, user_label_y, user_label_angle  # return the sliders if needed

# Create dictionary of curves and annotations
def create_curves_dict(data_instances, physics_category_dict, curve_category_dict, Smax):
    curves_dict = {}
    curves_dict_hc = {}
    maxLengthCurves = 1
    maxLengthAreas = 1
    maxLengthPoints = 1
    #First identify max lengths
    for label, data_instance in data_instances.items():
        category = None
        for cat, labels in curve_category_dict.items():
            if label in labels:
                category = cat
                break
        if (category == 'Curves'):
            maxLengthCurves = max(maxLengthCurves, len(data_instance.x_coord))
        if (category == 'Areas'):
            maxLengthAreas = max(maxLengthAreas, len(data_instance.x_coord))
        if (category == 'Points'):
            maxLengthPoints = max(maxLengthPoints, len(data_instance.x_coord))


    for label, data_instance in data_instances.items():
        #Extract common keys for simplicity
        color_key = f'color_{label}'
        linewidth_key = f'linewidth_{label}'
        linestyle_key = f'linestyle_{label}'
        opacity_key = f'opacity_{label}'
        depth_key = f'depth_{label}'
        annotation_x_key= f'annotation_x_{label}'  # New key for delta_x
        annotation_y_key = f'annotation_y_{label}'  # New key for delta_y
        label_angle_key = f'label_angle_{label}'
        label_color_key = f'label_color_{label}'
        label_size_key = f'label_size_{label}'

        # Determine the category of the curve
        category = None
        for cat, labels in curve_category_dict.items():
            if label in labels:
                category = cat
                break



        #If ProjBoundsCurves or SignalCurves, we plot line segments
        if (category == 'Curves'):
            x_key = f'xCurve_{label}'
            y_key = f'yCurve_{label}'
            xaux = data_instance.x_coord
            yaux = data_instance.y_coord
            testcommentx = data_instance.delta_x
            if (testcommentx):
                annotation_x_aux =  data_instance.delta_x
                annotation_y_aux =  data_instance.delta_y
            else:
                annotation_x_aux =  xaux[0]
                annotation_y_aux =  yaux[0]
            xlength = len(xaux)
            nextra = maxLengthCurves - len(xaux)
            if nextra==0:
                yaux_h = yaux
                annotation_y_aux_h = annotation_y_aux
                curves_dict[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
            else:
                xextra = np.array([ xaux[xlength-1] for _ in range(nextra) ])
                yextra = np.array([ yaux[xlength-1] for _ in range(nextra) ])
                xaux = np.concatenate([xaux,xextra])
                yaux = np.concatenate([yaux,yextra])
                yaux_h = yaux
                annotation_y_aux_h = annotation_y_aux
                curves_dict[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}

            #Data for hc=8.93368/f Sqrt[h^2 Omega]
            yaux = 8.93368e-19/(xaux)*np.sqrt(yaux)
            annotation_y_aux = 8.93368e-19/(annotation_x_aux)*np.sqrt(annotation_y_aux)
            #print(' yaux: ',yaux)
            curves_dict_hc[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}


        elif (category == 'Areas'):
        #Here we plot current bounds, shaded areas
            x_key = f'x_{label}'
            y_key = f'y_{label}'
            y2_key = f'y2_{label}'
            xaux = data_instance.x_coord
            yaux = data_instance.y_coord
            y2aux = np.array([1E100 for _ in range(len(data_instance.y_coord))])
            testcommentx = data_instance.delta_x
            if (testcommentx):
                annotation_x_aux =  data_instance.delta_x
                annotation_y_aux =  data_instance.delta_y
            else:
                annotation_x_aux =  xaux[0]
                annotation_y_aux =  yaux[0]
            #Might have to add extra
            xlength = len(xaux)
            nextra = maxLengthAreas - len(xaux)
            if nextra==0:
                yaux_h = yaux
                y2aux_h = y2aux
                annotation_y_aux_h = annotation_y_aux
                curves_dict[label] = {x_key: xaux, y_key: yaux,  y2_key: y2aux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
            else:
                xextra = np.array([ xaux[xlength-1] for _ in range(nextra) ])
                yextra = np.array([ yaux[xlength-1] for _ in range(nextra) ])
                y2extra = np.array([ y2aux[xlength-1] for _ in range(nextra) ])
                xaux = np.concatenate([xaux,xextra])
                yaux = np.concatenate([yaux,yextra])
                y2aux = np.concatenate([y2aux,y2extra])
                curves_dict[label] = {x_key: xaux, y_key: yaux,  y2_key: y2aux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}

            #Data for hc=8.93368/f Sqrt[h^2 Omega]
            yaux = 8.93368e-19/(xaux)*np.sqrt(yaux)
            y2aux = 8.93368e-19/(xaux)*np.sqrt(y2aux)
            annotation_y_aux = 8.93368e-19/(annotation_x_aux)*np.sqrt(annotation_y_aux)
            #print(' yaux: ',yaux)
            curves_dict_hc[label] = {x_key: xaux, y_key: yaux,  y2_key: y2aux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}


        #If category is SingleFreq, we plot vertical line
        elif (category == 'SingleFreq'):
            x_key = f'x_{label}'
            y_key = f'y_{label}'
            y2_key = f'y2_{label}'
            xaux = data_instance.x_coord
            yaux = data_instance.y_coord
            y2aux = np.array([1.0E100])
            testcommentx = data_instance.delta_x
            if (testcommentx):
                annotation_x_aux =  data_instance.delta_x
                annotation_y_aux =  data_instance.delta_y
            else:
                annotation_x_aux =  2.0*xaux
                annotation_y_aux =  0.4*yaux
            #print(label,' x=', xaux)
            curves_dict[label] = {x_key: xaux, y_key: yaux, y2_key: y2aux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity,  depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}

            #Data for hc=8.93368/f Sqrt[h^2 Omega]
            yaux = 8.93368e-19/(xaux)*np.sqrt(yaux)
            y2aux = 8.93368e-19/(xaux)*np.sqrt(y2aux)
            annotation_y_aux = 8.93368e-19/(annotation_x_aux)*np.sqrt(annotation_y_aux)
            #print(' yaux: ',yaux)
            curves_dict_hc[label] = {x_key: xaux, y_key: yaux, y2_key: y2aux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity,  depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}

        #If Points, we plot line points
        elif (category == 'Points'):
            x_key = f'x_{label}'
            y_key = f'y_{label}'
            xaux = data_instance.x_coord
            yaux = data_instance.y_coord
            testcommentx = data_instance.delta_x
            if (testcommentx):
                annotation_x_aux =  data_instance.delta_x
                annotation_y_aux =  data_instance.delta_y
            else:
                annotation_x_aux =  xaux[0]
                annotation_y_aux =  yaux[0]
            xlength = len(xaux)
            nextra = maxLengthPoints - len(xaux)
            if nextra==0:
                annotation_y_aux_h = annotation_y_aux
                curves_dict[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
            else:
                xextra = np.array([ xaux[xlength-1] for _ in range(nextra) ])
                yextra = np.array([ yaux[xlength-1] for _ in range(nextra) ])
                xaux = np.concatenate([xaux,xextra])
                yaux = np.concatenate([yaux,yextra])
                curves_dict[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}

            #Data for hc=8.93368/f Sqrt[h^2 Omega]
            yaux = 8.93368e-19/(xaux)*np.sqrt(yaux)
            annotation_y_aux = 8.93368e-19/(annotation_x_aux)*np.sqrt(annotation_y_aux)
            #print(' yaux: ',yaux)
            curves_dict_hc[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}





    return curves_dict,  curves_dict_hc



# Defines plot data with curves and annotations, plots them invisibly
def add_curves_to_plot(fig, curves_dict, curves_dict_hc, physics_category_dict, curve_category_dict, what_to_plot, plot_source_curves, plot_source_areas, plot_source_lollipops, plot_source_points,  annotation_source):

    """"
    Always starts assuming one is plotting strain Sh, and so uses curves_dict
    """

    if what_to_plot == 0:
        curves_dict_to_use = curves_dict
    else:
        curves_dict_to_use = curves_dict_hc

    #Ratio to convert angles
    fmin = fig.x_range.start
    fmax = fig.x_range.end
    Shmin = fig.y_range.start
    Shmax = fig.y_range.end
    ratio = ((np.log10(Shmax)-np.log10(Shmin))/(np.log10(fmax)-np.log10(fmin)))*fig.width/fig.height


    angle_factor = 0.9



    for label, data in curves_dict_to_use.items():
        # Determine the category of the curve
        physics_category = None
        curve_category = None
        for cat, labels in curve_category_dict.items():
            if label in labels:
                curve_category = cat
                break
        for cat, labels in physics_category_dict.items():
            if label in labels:
                physics_category = cat
                break
        color_key = f'color_{label}'
        linewidth_key = f'linewidth_{label}'
        linestyle_key = f'linestyle_{label}'
        opacity_key = f'opacity_{label}'
        depth_key = f'depth_{label}'

        # Generate keys for delta_x and delta_y dynamically based on the label
        annotation_x_key = f'annotation_x_{label}'  # Adjusted to use the dynamic key
        annotation_y_key = f'annotation_y_{label}'  # Adjusted to use the dynamic key
        label_text_key = f'annotation_text_{label}'
        label_angle_key = f'label_angle_{label}'
        label_color_key = f'label_color_{label}'
        label_size_key = f'label_size_{label}'








        label_text = f"{label}"

        #Correct label angle with aspect ratios

        label_angle = np.arctan(angle_factor/ratio*np.tan(data.get(label_angle_key, 0)))# Defaulting to 0 if not present
        # Retrieve delta_x and delta_y using the dynamically generated keys
        annotation_x = data.get(annotation_x_key, 0)  # Defaulting to 0 if not present
        annotation_y = data.get(annotation_y_key, 0)  # Defaulting to 0 if not present
        label_color = data.get(label_color_key, 'black')# Defaulting to black if not present
        label_size = data.get(label_size_key, '9pt')# Defaulting to 9 if not present

        annotation_source.add([annotation_x], annotation_x_key)
        annotation_source.add([annotation_y], annotation_y_key)
        annotation_source.add([label_angle], label_angle_key)
        annotation_source.add([label_text], label_text_key)
        annotation_source.add([label_color], label_color_key)
        annotation_source.add([label_size], label_size_key)



        

        # If the category is found, apply the corresponding style
        if curve_category:
            if (curve_category == 'Curves'):
                #also line plot but use different names
                x_key = f'xCurve_{label}'
                y_key = f'yCurve_{label}'
                data_x = data[x_key]
                data_y = data[y_key]
                plot_source_curves.add(data_x, x_key)
                plot_source_curves.add(data_y, y_key)
                #if 'Your curve' in label:
                #    isvisible = True
                #else:
                isvisible = False
                fig.line(x = x_key, y = y_key, source= plot_source_curves,  color = data[color_key], line_width = data[linewidth_key], line_dash = data[linestyle_key], line_alpha = data[opacity_key], level = data[depth_key], name = label, visible=isvisible)

            elif (curve_category == 'Areas'):
                x_key = f'x_{label}'
                y_key = f'y_{label}'
                y2_key = f'y2_{label}'
                plot_source_areas.add(data[x_key], x_key)
                plot_source_areas.add(data[y_key], y_key)
                plot_source_areas.add(data[y2_key], y2_key)
                fig.varea(x = x_key, y1 = y_key, y2=y2_key, source= plot_source_areas,  color = data[color_key], alpha = data[opacity_key], level = data[depth_key], name = label, visible=False)#legend_label=label,

            elif (curve_category == 'SingleFreq'):
                x_key = f'x_{label}'
                y_key = f'y_{label}'
                y2_key = f'y2_{label}'
                plot_source_lollipops.add(data[x_key], x_key)
                plot_source_lollipops.add(data[y_key], y_key)
                plot_source_lollipops.add(data[y2_key], y2_key)
                #plot vertical segment
                fig.segment(x0 = x_key, y0 = y_key, x1 = x_key, y1=y2_key, source= plot_source_lollipops,  color = data[color_key], line_width = data[linewidth_key], line_dash = data[linestyle_key], alpha = data[opacity_key], level = data[depth_key], name = label, visible=False)
                #plot circle
                fig.scatter(x = x_key, y = y_key, source = plot_source_lollipops, size=5, color = data[color_key], fill_alpha = data[opacity_key], level = data[depth_key], name = f"lollipop_{label}", visible=False)

            elif (curve_category == 'Points'):
                x_key = f'x_{label}'
                y_key = f'y_{label}'
                plot_source_points.add(data[x_key], x_key)
                plot_source_points.add(data[y_key], y_key)
                fig.scatter(x = x_key, y = y_key,  source= plot_source_points,  color = data[color_key], alpha = data[opacity_key], level = data[depth_key], name = label, visible=False)#legend_label=label,



        # Create and add the LabelSet for the annotation
        annotation = LabelSet(x= annotation_x_key, y= annotation_y_key, text=label_text_key, x_offset=0, y_offset=0, source=annotation_source,text_font_size= label_size_key, visible=False, name=f"annotation_{label}", text_color = label_color_key, angle = label_angle_key)  # Unique name
        fig.add_layout(annotation)




    return  fig, plot_source_curves, plot_source_areas, plot_source_lollipops, plot_source_points,  annotation_source








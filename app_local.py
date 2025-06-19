#app.py

# Import all the relevant libraries and packages


from aux.imports import *


from aux.data_files import detector_data, theoretical_bounds_data, signal_data
from aux.aux_functions import load_and_categorize_data
from aux.aux_functions import create_sliders
from aux.aux_functions import create_curves_dict
from aux.aux_functions import add_curves_to_plot

from aux.aux_functions import Tstar0, alpha0, betaOverH0, vw0, gstar0

from aux.signal_functions import OmegaPT

# Create a Blueprint
Omegaplot = Blueprint('Omegaplot', __name__, static_folder='Omegaplot/static', template_folder='Omegaplot/templates')









# Suppress specific Bokeh warning
warnings.filterwarnings("ignore", message="ColumnDataSource's columns must be of the same length")





# Initialize app
app = Flask(__name__)
app.secret_key = 'George127!Lana#:Hubi47_Grabwoski!'
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



## Load detector curves

# Load data into Data class instances collected in the dictionary data_instances
# Create a dictionary category_dict containing the experiment labels divided into categories (Indirect bounds, Direct bounds, Projected bounds and others)
data_instances, physics_category_dict, curve_category_dict = load_and_categorize_data(detector_data, theoretical_bounds_data, signal_data)
## Define app section

@Omegaplot.before_request
def assign_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')


@Omegaplot.route('/get_comments')
def get_comments():
    label = request.args.get('label')
    data_instance = data_instances.get(label, None)
    comment = data_instance.comment if data_instance and data_instance.comment not in [None, ''] else None

    return jsonify({'comment': comment})

@Omegaplot.route('/upload', methods=['POST'])
def upload():
    file = request.files['csvfile']
    if file and file.filename.endswith('.csv'):
        user_id = session.get("user_id")
        path = os.path.join(UPLOAD_FOLDER, f"{user_id}.csv")
        file.save(path)
    return '', 204  # No Content; prevents browser refresh



# Flask route to serve the HTML template with the initial Bokeh plot
@Omegaplot.route('/')
def index():
    session_id = session.get("user_id")
    script_bokeh_plot =  server_document(url=f"http://localhost:5006/Omegaplotworkers/plot", arguments={"session_id": session_id})#url=f"http://localhost:37629/Omegaplotworkers/plot"#url=f"https://incandenza-01.zdv.uni-mainz.de/Omegaplotworkers/plot") #CHANGE FOR SERVER



    return render_template(
        'index.html',
        script_bokeh_plot = script_bokeh_plot,
        bokeh_css=INLINE.render_css(),
        bokeh_js=INLINE.render_js(),
        physics_category_dict= physics_category_dict,
        curve_category_dict= curve_category_dict
    )



#Bokeh app for all
def bokeh_plot_app(doc):


    args = doc.session_context.request.arguments
    #print("ARGS:", args)
    session_id = args.get("session_id", [b"default"])[0].decode()
    csv_path = os.path.join(UPLOAD_FOLDER, f"{session_id}.csv")
    #print(f"[DEBUG] session_id from server_document: {session_id}")
    print(f'csv_path: {csv_path}')
    last_modified = None  # Track the last file change time


    #Global variables that can be seen by all users, even if they are fed different plots
    #global  data_instances, physics_category_dict, curves_category_dict, curves_dict, curves_dict_hc

    what_to_plot = 0
    #Phase transition variables only defined in app, not globally, matching initial values
    Tstar = Tstar0
    alpha = alpha0
    betaOverH = betaOverH0
    vw = vw0
    gstar = gstar0

    #Variables for Total energy fraction in GWs
    h2OmegaGW = 0.
    dRBoundViolation = "Unknown"

    # Global ColumnDataSource objects to manage plot data



    plot_source_curves = ColumnDataSource(data=dict(), name='plot_source_curves')
    plot_source_areas = ColumnDataSource(data=dict(), name='plot_source_areas')
    plot_source_lollipops = ColumnDataSource(data=dict(), name='plot_source_lollipops')
    plot_source_points = ColumnDataSource(data=dict(), name='plot_source_points')
    #plot_source_polygons = ColumnDataSource(data=dict(), name='plot_source_polygons')
    # Annotations object
    annotation_source = ColumnDataSource(data=dict(), name='annotation_source')



    # Set up the figure

    #Global parameters for range, width and height


    #Omegah2min = 10.**-40
    #Omegah2max = 10.**-19
    hmin = 10.**-45.
    hmax = 10.**-10.
    Omegah2min = 10**-28.
    Omegah2max = 10**18

    Shrangechanged = 0
    #fmin = 10**10.
    #fmax = 10**19.
    fmin = 10**0.5
    fmax = 10**19.5
    frangechanged = 0
    plot_width = int(900)
    plot_width_changed = 0
    plot_height = 600 #(added 80 points for the legend height: 3itmes*(20 glyph+10 padding)+2*(10padding))
    legend_height = 0
    plot_height_changed = 0
    xrange = (fmin, fmax)
    yrange = (Omegah2min, Omegah2max)
    #custom_major_ticker = LogTicker(base=10, min_interval=1, num_minor_ticks=10)  # Major ticks at each decade
    #custom_minor_ticker = LogTicker(base=10, mantissas=[2, 3, 4, 5, 6, 7, 8, 9])  # Minor ticks


    fig = figure(background_fill_color='white',
    border_fill_color='black',
    border_fill_alpha=0.0,
    height= plot_height,
    width= plot_width,
    x_axis_label=r'GW frequency $$f\,\,[{\rm Hz}]$$',
    x_axis_type='log',
    x_axis_location='below',
    x_range=xrange,
    y_axis_label=r'Energy spectrum of grav. waves $$h^2\Omega_{\rm GW}$$',
    y_axis_type='log',
    y_axis_location='left',
    y_range=yrange,
    toolbar_location='below',
    tools='save',name = 'HFGWPlotter_stochastic')
    fig.output_backend = "svg"
    fig.xgrid.level = 'image'
    fig.ygrid.level = 'image'
    # Add an extra logarithmic axis on the top
    log_axis_top = LogAxis()
    fig.add_layout(log_axis_top, 'above')

    # Add an extra logarithmic axis on the right
    log_axis_right = LogAxis()
    fig.add_layout(log_axis_right, 'right')


    custom_ticks_xaxis= [10**i for i in range(-19,21)]
    custom_ticks_yaxis= [10**i for i in range(-50,20)]
    custom_ticks_minor_xaxis = [j * 10**i for i in range(-19, 21) for j in range(2,10)]
    custom_ticks_minor_yaxis = [j * 10**i for i in range(-50, 20) for j in range(2,10)]
    fig.xaxis.ticker = FixedTicker(ticks=custom_ticks_xaxis, minor_ticks=custom_ticks_minor_xaxis)
    fig.yaxis.ticker = FixedTicker(ticks=custom_ticks_yaxis, minor_ticks=custom_ticks_minor_yaxis)
    # Use MathText for LaTeX-like formatting
    #fig.yaxis.formatter = CustomJSTickFormatter(code="""
    #const power = Math.log10(tick);
    #if (power % 2 === 0) {
    #    return "10" +
    #    (Math.log10(tick).toString()
    #     .split('')
    #     .map(function(d) {
    #        return d === '-' ? '⁻' : '⁰¹²³⁴⁵⁶⁷⁸⁹'[+d];
    #     })
    #     .join(''));
    #} else {
    #    return "";
    #}
    #""")


    fig.yaxis.major_label_overrides = {
    1e-47: r"",
    1e-45: r"",
    1e-43: r"",
    1e-41: r"",
    1e-39: r"",
    1e-37: r"",
    1e-35: r"",
    1e-33: r"",
    1e-31: r"",
    1e-29: r"",
    1e-27: r"",
    1e-25: r"",
    1e-23: r"",
    1e-21: r"",
    1e-19: r"",
    1e-17: r"",
    1e-15: r"",
    1e-13: r"",
    1e-11: r"",
    1e-9: r"",
    1e-7: r"",
    1e-5: r"",
    1e-3: r"",
    1e-1: r"",
    1e1: r"",
    1e3: r"",
    1e5: r"",
    1e7: r"",
    1e9: r"",
    1e11: r"",
    1e13: r"",
    1e15: r"",
    1e17: r"",
    }

    # Allow rendering of HTML in labels
    #fig.yaxis.axis_label_text_font_style = "normal"

    # Customize tick label sizes
    fig.xaxis.major_label_text_font_size = "12pt"  # Change x-axis tick label size
    fig.yaxis.major_label_text_font_size = "12pt"  # Change y-axis tick label size

    fig.xaxis.axis_label_text_font_size = "12pt"  # Change x-axis label size
    fig.yaxis.axis_label_text_font_size = "12pt"  # Change y-axis label size
    #fig.title.title_text_font_size = "12pt"  # Change y-axis label size

    #Label right-down corner
    watermark = Label(x=fig.width-265, y=15, x_units = 'screen', y_units = 'screen', text=r"HFGWPlotter",  text_font_size="12pt", text_color="gray", text_font_style="bold", background_fill_color="white",background_fill_alpha=1, name="watermark")
    #Label upper right
    #label = Label(x=585, y=450, x_units = 'screen', y_units = 'screen', text=r"Aggarwal et al. 2025",  text_font_size="12pt", text_color="gray", text_font_style="bold", background_fill_color="white",
    #background_fill_alpha=1)
    # Add the Label to the plot
    fig.add_layout(watermark)
    #fig.log_axis_top.ticker = FixedTicker(ticks=custom_ticks_xaxis)
    #fig.xaxis.ticker.num_minor_ticks = 10

    #fig.title = Title(text=r"$$\text{Interferometers and resonant mass detectors}$$", text_font_size="12pt", align="center")




    # Set up the sliders

    slider_x, slider_y, slider_width,  slider_height,  h_vs_Omega_buttons, slider_pt_temp, slider_pt_alpha, slider_pt_betaOverH, slider_pt_vw, user_color_picker, user_label_input, user_label_size, user_label_x, user_label_y, user_label_angle  = create_sliders(fig, Omegah2min, Omegah2max)


    # Create dictionary of curves

    curves_dict, curves_dict_hc = create_curves_dict(data_instances, physics_category_dict, curve_category_dict, Omegah2max)

    #print(curves_dict)

    # Link curves to a chart
    fig, plot_source_curves, plot_source_areas, plot_source_lollipops, plot_source_points,  annotation_source = add_curves_to_plot(fig, curves_dict, curves_dict_hc , physics_category_dict, curve_category_dict, what_to_plot, plot_source_curves, plot_source_areas, plot_source_lollipops, plot_source_points,  annotation_source)


    #Add legend at this stage
    # Retrieve renderers by their name
    renderer_current = fig.select(name="LIGO")
    renderer_ongoing = fig.select(name="DMRadio-GUT")
    renderer_ongoing_res = fig.select(name="DMRadio-GUT-res")
    renderer_proposed =  fig.select(name="Mag. Weber bars")
    renderer_proposed_res =  fig.select(name="Mag. Weber bars (res)")
    renderer_theo_line =  fig.select(name="BBN")
    renderer_theo_dot =  fig.select(name="Astro")
    renderer_signal = fig.select(name = "CGMB")
    renderer_signal_2 = fig.select(name = 'Oscillons')
    renderer_signal_3 = fig.select(name = 'Met. strings')


    # Add a dummy glyph for intermediate text
    dummy_line = fig.line([], [], line_alpha=0)  # Invisible line for the "header"
    # Create a custom legend
    legend = Legend(items=[
        (r"Current exp.", [renderer_current[0]]),  # Access the first matching renderer
        (r"Exp. in development (solid: broad, dotted: res.)", [renderer_ongoing[0],renderer_ongoing_res[0]]),
        (r"Proposed exp. (solid: broad, dotted: res.)", [renderer_proposed[0],renderer_proposed_res[0]]),
        (r"Astrophysical bounds", [renderer_theo_line[0], renderer_theo_dot[0]]),
        (r"Potential stochastic signals", [renderer_signal[0], renderer_signal_2[0], renderer_signal_3[0]])
    ],
    glyph_height=20,  # Glyph height in points
    glyph_width=20,   # Glyph width in points
    spacing=10,       # Spacing between items in points
    padding=100        # Padding inside the legend box in points
    )
    # Customize the font size of the legend labels
    legend.ncols = 2   # Simulates multi-column rows
    legend.label_text_font_size = "11pt"  # Set the font size for the legend labels
    legend.location = (10, 10)  # Custom (x, y) position in plot space
    legend.border_line_color = None  # Hide the frame
    legend.background_fill_alpha = 0.5  # Set background transparency (50%)
    # Add the legend to the figure
    fig.add_layout(legend, 'center')
    # Create a separate figure to hold the legend
    #legend_fig = figure(height=200, width=400, toolbar_location=None, outline_line_color=None)

    # Add dummy glyphs to represent legend items
    #line_ongoing_dummy = legend_fig.line([0,1], [0,1], line_width=2, color="rebeccapurple", visible = False)  # Same style as in the main plot
    #line_proposed_dummy = legend_fig.line([0,1], [0,1], line_width=2, color="darkcyan", visible = False)
    #Dummy glyph for area
    #area_current_dummy =legend_fig.patch(
    #x=[0, 1, 1, 0],  # Example rectangle coordinates
    #y=[0, 0, 1, 1],
    #fill_color="darkorange",
    #fill_alpha=0.4,
    #line_color=None, visible = False # Match style of the area plot
    #)

    # Create a custom legend
    #legend = Legend(items=[
    #    ("Current bounds", [area_current_dummy]),  # Access the first matching renderer
    #    ("Experiments in active development", [line_ongoing_dummy]),
    #    ("Proposed experiments", [line_proposed_dummy])
    #])

    # Remove axes, gridlines, and other visuals from the dummy figure
    #legend_fig.xaxis.visible = False
    #legend_fig.yaxis.visible = False
    #legend_fig.grid.visible = False
    #legend_fig.outline_line_color = None

    #legend_fig.add_layout(legend, 'center')


    #Text boxes for DarkRadiation
    divOmegaGW = Div(text=f"<b>Energy fraction in GWs:</b> {h2OmegaGW:.4f}")
    divDRBound = Div(text=f"<b>Compliance with DR bound:</b> {dRBoundViolation}")

    #Main plot with range/size sliders
    layout = column(h_vs_Omega_buttons, fig)
    #Sliders for range/size
    layout_size = column(Div(text="<h1>Plot range and size</h1>"), slider_x, slider_y,   slider_width, slider_height)
    layout_phase_transition = column(Div(text="<h1>Phase transition parameters</h1>"), slider_pt_temp, slider_pt_alpha, slider_pt_betaOverH, slider_pt_vw, visible = False, name = "panel_1st-order p.t.")
    layout_user = column(Div(text="<h1>Customize your curve</h1>"), user_color_picker, user_label_input, user_label_size, user_label_x, user_label_y, user_label_angle, divOmegaGW, divDRBound, visible = False, name = "panel2_Your curve")










    #Function that updates annotation_angles and positions
    def update_annotation_angles(curves_dict, curves_dict_hc, what_to_plot, annotation_source, fig, fmin, fmax, Omegah2min, Omegah2max):

        nonlocal hmin,hmax, user_label_angle

        # To reduce individual changes (communications with server) update main variable only once, so we use first copy
        new_data_annotation = dict(annotation_source.data)

        #curves_dict_to_use = curves_dict

        if what_to_plot == 0:
            curves_dict_to_use = curves_dict
        elif what_to_plot == 1:
            curves_dict_to_use = curves_dict_hc




        #Update plot_sources

        for label, data in curves_dict_to_use.items():
            # Generate keys for delta_x and delta_y dynamically based on the label
            annotation_x_key = f'annotation_x_{label}'  # Adjusted to use the dynamic key
            annotation_y_key = f'annotation_y_{label}'  # Adjusted to use the dynamic key
            label_angle_key  = f'label_angle_{label}'

            x_label = data.get(annotation_x_key, 0)
            y_label = data.get(annotation_y_key, 0)

            new_data_annotation[annotation_x_key] = [x_label]  # Change the x position
            new_data_annotation[annotation_y_key] = [y_label]  # Change the x position


            #Change label angles for selected curves when going from hc to Omega
            label_angle = data.get(label_angle_key, 0)

            #if what_to_plot == 1 and  (label_angle) != 0:
            #    ratio = ((np.log10(Omegamax)-np.log10(Omegamin))/(np.log10(fmax)-np.log10(fmin)))*fig.width/fig.height
            #    new_label_angle = np.arctan(1/ratio*(2.+2.*np.tan(label_angle)))
            #    new_data_annotation[label_angle_key] = [new_label_angle]

            #if what_to_plot == 0 and  (label_angle) != 0:
            #    ratio = ((np.log10(hmax)-np.log10(hmin))/(np.log10(fmax)-np.log10(fmin)))*fig.width/fig.height
            #    new_label_angle = np.arctan(0.9/ratio*(np.tan(label_angle)))
            #    new_data_annotation[label_angle_key] = [new_label_angle]

            #If plotting Omegah2
            if what_to_plot == 0:
                ratio = ((np.log10(Omegah2max)-np.log10(Omegah2min))/(np.log10(fmax)-np.log10(fmin)))*fig.width/(fig.height-legend_height)
                new_label_angle = np.arctan(1/ratio*(np.tan(label_angle)))
                new_data_annotation[label_angle_key] = [new_label_angle]
            #If plotting hc
            if what_to_plot == 1:
                ratio = ((np.log10(hmax)-np.log10(hmin))/(np.log10(fmax)-np.log10(fmin)))*fig.width/(fig.height-legend_height)
                new_label_angle = np.arctan(1/ratio*(-1+1/2*np.tan(label_angle)))
                new_data_annotation[label_angle_key] = [new_label_angle]
            #For user curve, change slider position
            if label == 'Your curve':
                user_label_angle.value = new_label_angle



        return new_data_annotation




    # Update plot data when changing between Omega and h- ColumnDataSources and annotations
    def update_plot_data(curves_dict, curves_dict_hc, curve_category_dict,  what_to_plot):


        nonlocal plot_source_curves
        nonlocal plot_source_areas
        nonlocal plot_source_lollipops
        nonlocal plot_source_points
        nonlocal annotation_source
        nonlocal fig
        nonlocal hmin, hmax, Omegah2min, Omegah2max
        # To reduce individual changes (communications with server) update main variable only once, so we use first copy
        new_data_rectangles = {}
        new_data_curves = {}
        new_data_areas = {}
        new_data_lollipops = {}
        new_data_points = {}


        new_data_annotation  =  update_annotation_angles(curves_dict, curves_dict_hc, what_to_plot, annotation_source, fig, fmin, fmax, Omegah2min, Omegah2max)


        if what_to_plot == 0:
            curves_dict_to_use = curves_dict
        elif what_to_plot == 1:
            curves_dict_to_use = curves_dict_hc
        #Update plot_sources


        for label, data in curves_dict_to_use.items():
            # Determine the category of the curve
            curve_category = None
            for cat, labels in curve_category_dict.items():
                if label in labels:
                    curve_category = cat
                    break


            # If the category is found, apply the corresponding style
            if curve_category:
                if (curve_category == 'Curves'):
                    x_key = f'xCurve_{label}'
                    y_key = f'yCurve_{label}'
                    new_data_curves[x_key] = data[x_key]
                    new_data_curves[y_key] = data[y_key]

                elif (curve_category == 'Areas'):
                    x_key = f'x_{label}'
                    y_key = f'y_{label}'
                    y2_key = f'y2_{label}'
                    new_data_areas[x_key] = data[x_key]
                    new_data_areas[y_key] = data[y_key]
                    new_data_areas[y2_key] = data[y2_key]

                elif (curve_category == 'SingleFreq'):
                    x_key = f'x_{label}'
                    y_key = f'y_{label}'
                    y2_key = f'y2_{label}'
                    new_data_lollipops[x_key] = data[x_key]
                    new_data_lollipops[y_key] = data[y_key]
                    new_data_lollipops[y2_key] = data[y2_key]

                elif (curve_category == 'Points'):
                    x_key = f'x_{label}'
                    y_key = f'y_{label}'
                    new_data_points[x_key] = data[x_key]
                    new_data_points[y_key] = data[y_key]


        plot_source_curves.data = new_data_curves
        plot_source_areas.data = new_data_areas
        plot_source_lollipops.data = new_data_lollipops
        plot_source_points.data = new_data_points
        annotation_source.data = new_data_annotation


    #Define a callback function for the what_to_plot_button
    def h_vs_Omega_button_handler(new, curves_dict, curves_dict_hc, curve_category_dict):
        nonlocal plot_source_areas
        nonlocal plot_source_curves
        nonlocal plot_source_lollipops
        nonlocal plot_source_points
        nonlocal fig
        nonlocal what_to_plot
        nonlocal hmin, hmax, Omegah2min, Omegah2max
        nonlocal yrange
        what_to_plot = new
        nonlocal user_label_x, user_label_y, user_label_angle
        #print('what_to_plot = ',what_to_plot)
        #Update ranges
        if what_to_plot == 0:
            slider_y.value = (np.log10(float(Omegah2min)), np.log10(float(Omegah2max)))
            slider_y.start = -30
            slider_y.end = 20
            slider_y.title = r" Adjust $$\Omega h^2$$ range"
            fig.y_range.start = Omegah2min
            fig.y_range.end = Omegah2max
            fig.yaxis[0].axis_label = r'Energy spectrum of grav. waves $$h^2\Omega_{\rm GW}$$'
            old_label_x = 10**(user_label_x.value)
            old_label_y = 10**(user_label_y.value)
            #old_label_angle = user_label_angle.value
            #Convert slider positions from hc to h2Omega
            user_label_y.value = np.log10(1.25297e36*(old_label_x**2)*(old_label_y**2))
            #user_label_angle.value = np.arctan(2+2*np.tan(old_label_angle))

        elif what_to_plot == 1:
            slider_y.value = (np.log10(float(hmin)), np.log10(float(hmax)))
            slider_y.start = -47
            slider_y.end = -8
            slider_y.title = r" Adjust $$h_c$$ range"
            fig.y_range.start = hmin
            fig.y_range.end = hmax
            fig.yaxis[0].axis_label = r'Characteristic strain $$h_c$$'
            old_label_x = 10.**user_label_x.value
            old_label_y = 10.**user_label_y.value
            #old_label_angle = user_label_angle.value
            #Convert slider position from h2Omega to hc
            user_label_y.value = np.log10(8.93368e-19/(old_label_x)*np.sqrt(old_label_y))
            #user_label_angle.value = np.arctan(-1+1/2*np.tan(old_label_angle))
        # Call the update_plot_data function and update new_data
        update_plot_data(curves_dict, curves_dict_hc, curve_category_dict, what_to_plot)



    h_vs_Omega_buttons.on_change('active', lambda attr, old, new:  h_vs_Omega_button_handler(new, curves_dict, curves_dict_hc, curve_category_dict))



    #Define a callback function for plot size, and update annotation angles, for example after changing range which affects aspect ratio
    def update_frange(new, curves_dict, curves_dict_hc):

        nonlocal fig
        nonlocal annotation_source
        nonlocal fmin
        nonlocal fmax

        fmin = 10.**new[0]
        fmax = 10.**new[1]
        fig.x_range.start  = fmin
        fig.x_range.end = fmax

        annotation_source.data = update_annotation_angles(curves_dict, curves_dict_hc, what_to_plot, annotation_source, fig, fmin, fmax, Omegah2min, Omegah2max)


    slider_x.on_change('value', lambda attr, old, new: update_frange(new, curves_dict, curves_dict_hc))

    def update_yrange(new, curves_dict, curves_dict_hc):

        nonlocal fig
        nonlocal annotation_source
        nonlocal Omegah2min, Omegah2max, hmin, hmax


        if what_to_plot == 0:

            Omegah2min = 10.**new[0]
            Omegah2max = 10.**new[1]
            fig.y_range.start = Omegah2min
            fig.y_range.end = Omegah2max

        elif what_to_plot == 1:

            hmin = 10.**new[0]
            hmax = 10.**new[1]
            fig.y_range.start = hmin
            fig.y_range.end = hmax

        annotation_source.data =  update_annotation_angles(curves_dict, curves_dict_hc, what_to_plot, annotation_source, fig, fmin, fmax, Omegah2min, Omegah2max)






    slider_y.on_change('value', lambda attr, old, new: update_yrange(new, curves_dict, curves_dict_hc))



    def update_width(new, curves_dict, curves_dict_hc):

        nonlocal fig
        nonlocal annotation_source
        nonlocal watermark

        new_width = slider_width.value;
        fig.width = new_width;

        #watermark = fig.select(dict(name="watermark"))[0]
        watermark.x = new_width-265;


        annotation_source.data =  update_annotation_angles(curves_dict, curves_dict_hc, what_to_plot, annotation_source, fig, fmin, fmax, Omegah2min, Omegah2max)



    slider_width.on_change('value', lambda attr, old, new: update_width(new, curves_dict, curves_dict_hc))


    def update_height(new, curves_dict, curves_dict_hc):

        nonlocal fig
        nonlocal annotation_source

        fig.height = slider_height.value;
        annotation_source.data =  update_annotation_angles(curves_dict, curves_dict_hc, what_to_plot, annotation_source, fig, fmin, fmax, Omegah2min, Omegah2max)

    slider_height.on_change('value',  lambda attr, old, new: update_height(new, curves_dict, curves_dict_hc))

    ##################################################
    ##################################################
    ##################################################
    #update user curve

    def update_user_color(attr, old, new):
        nonlocal annotation_source
        label = 'Your curve'
        line = fig.select(name=label)[0]  # get first match
        line.glyph.line_color = new

        new_data_annotation = dict(annotation_source.data)
        label = 'Your curve'
        label_color_key = f'label_color_{label}'

        new_data_annotation[label_color_key ] = [new]  # Change the x position
        annotation_source.data = new_data_annotation

        #labelset = fig.select(name=f'annotation_{label}')[0]  # Get LabelSet by name
        #labelset.text_color = new


    user_color_picker.on_change('color', update_user_color)

    def update_user_label(new):
        nonlocal annotation_source
        ## To reduce individual changes (communications with server) update main variable only once, so we use first copy
        new_data_annotation = dict(annotation_source.data)
        label = 'Your curve'
        label_text_key = f'annotation_text_{label}'

        new_data_annotation[label_text_key] = [new]  # Change the x position
        annotation_source.data = new_data_annotation


    user_label_input.on_change('value',  lambda attr, old, new: update_user_label(new))

    def update_user_label_size(new):
        nonlocal annotation_source
        ## To reduce individual changes (communications with server) update main variable only once, so we use first copy
        new_data_annotation = dict(annotation_source.data)
        label = 'Your curve'
        label_size_key = f'label_size_{label}'

        new_data_annotation[label_size_key] = [new]  # Change the x position
        annotation_source.data = new_data_annotation


    user_label_size.on_change('value',  lambda attr, old, new: update_user_label_size(new))

    def update_user_label_x(new):
        nonlocal annotation_source
        nonlocal curves_dict
        nonlocal curves_dict_hc
        label = 'Your curve'
        annotation_x_key = f'annotation_x_{label}'  # Adjusted to use the dynamic key
        #Update curves dict (necessary for jumps between h2Omega and hc)
        curves_dict[label][annotation_x_key] = 10.**new
        curves_dict_hc[label][annotation_x_key] = 10.**new

        ## To reduce individual changes (communications with server) update main variable only once, so we use first copy
        new_data_annotation = dict(annotation_source.data)

        new_data_annotation[annotation_x_key] = [10.**new]  # Change the x position
        annotation_source.data = new_data_annotation

    user_label_x.on_change('value',  lambda attr, old, new: update_user_label_x(new))

    def update_user_label_y(new):
        nonlocal annotation_source
        nonlocal curves_dict
        nonlocal curves_dict_hc
        nonlocal what_to_plot
        label = 'Your curve'
        #Need both x,y to convert between h2Omega, hc
        annotation_x_key = f'annotation_x_{label}'  # Adjusted to use the dynamic key
        annotation_y_key = f'annotation_y_{label}'  # Adjusted to use the dynamic key
        annotation_x_aux = curves_dict[label][annotation_x_key]
        annotation_y_aux = 10.**new
        if what_to_plot == 0:# We are plotting h2Omega
            curves_dict[label][annotation_y_key] = annotation_y_aux
            #Convert to hc
            annotation_y_aux = 8.93368e-19/(annotation_x_aux)*np.sqrt(annotation_y_aux)
            curves_dict_hc[label][annotation_y_key] = annotation_y_aux
        else: #We are plotting hc
            curves_dict_hc[label][annotation_y_key] = annotation_y_aux
            #Convert to h2Omega
            annotation_y_aux = 1.25297e36*(annotation_x_aux**2)*(annotation_y_aux**2)
            curves_dict[label][annotation_y_key] = annotation_y_aux

        ## To reduce individual changes (communications with server) update main variable only once, so we use first copy
        new_data_annotation = dict(annotation_source.data)


        new_data_annotation[annotation_y_key] = [10.**new]  # Change the x position
        annotation_source.data = new_data_annotation

    user_label_y.on_change('value',  lambda attr, old, new: update_user_label_y(new))

    def update_user_label_angle(new):
        nonlocal annotation_source
        nonlocal curves_dict
        nonlocal curves_dict_hc
        nonlocal what_to_plot
        nonlocal fmin, fmax, hmin, hmax, Omegah2min, Omegah2max
        label = 'Your curve'
        label_angle_key  = f'label_angle_{label}'

        ## To reduce individual changes (communications with server) update main variable only once, so we use first copy
        new_data_annotation = dict(annotation_source.data)
        new_data_annotation[label_angle_key] = [new]  # Change the Angle directly in annotation

        #Save angle to dictionary (needed for change between hc/h2Omega), correct for ratio
        #Angle is not changed between dictionaries
        if what_to_plot == 0:
                ratio = ((np.log10(Omegah2max)-np.log10(Omegah2min))/(np.log10(fmax)-np.log10(fmin)))*fig.width/(fig.height-legend_height)
                new_label_angle_dict = np.arctan(ratio*(np.tan(new)))

        #If plotting hc
        if what_to_plot == 1:
                ratio = ((np.log10(hmax)-np.log10(hmin))/(np.log10(fmax)-np.log10(fmin)))*fig.width/(fig.height-legend_height)
                new_label_angle_dict = np.arctan(2*(1+ratio*np.tan(new)))

        curves_dict[label][label_angle_key] = new_label_angle_dict
        curves_dict_hc[label][label_angle_key] = new_label_angle_dict


        annotation_source.data = new_data_annotation

    user_label_angle.on_change('value',  lambda attr, old, new: update_user_label_angle(new))



 #Update plot when external csv loaded
    def update_from_external_csv():


        nonlocal plot_source_curves
        nonlocal what_to_plot
        nonlocal curves_dict
        nonlocal curves_dict_hc
        nonlocal last_modified
        nonlocal fig

        #Reset h2OMegaGW, dR
        #h2OmegaGW = 0
        #dRBoundViolation = "Unknown"


        if os.path.exists(csv_path):
            stat = os.stat(csv_path)
            if last_modified is None or stat.st_mtime > last_modified:
                last_modified = stat.st_mtime
                print("Reloading file:", csv_path)
                try:
                    df = pd.read_csv(csv_path,  header=None, names=['x', 'y'])

                    # Sort by x in ascending order
                    df = df.sort_values(by='x', ascending=True).reset_index(drop=True)


                    if 'x' in df.columns and 'y' in df.columns:
                        #new_data_curves[x_key] = df['x']
                        #new_data_curves[y_key] = df['y']
                        xuser = df['x']
                        yuser = df['y']
                        ####FIRST THING. ESTIMATE Integrated energy

                        try:
                            # Create interpolator for inside the range
                            interp_func = interp1d(xuser, yuser, kind='cubic', bounds_error=False, fill_value="extrapolate")
                            fit_points = min(5, int(len(yuser)/4))
                            if (fit_points)>1:
                                def power_law(x, a, b):
                                    return a * x**b
                                # Fit power-law to the left boundary
                                x_left = xuser[:fit_points]
                                y_left = yuser[:fit_points]
                                popt_left, _ = curve_fit(power_law, x_left, y_left, maxfev=10000)


                                # Fit power-law to the right boundary
                                x_right = xuser[-fit_points:]
                                y_right = yuser[-fit_points:]
                                popt_right, _ = curve_fit(power_law, x_right, y_right, maxfev=10000)


                                def interpolator_with_extrapolation(x_new):
                                    x_new = np.array(x_new)
                                    y_new = np.empty_like(x_new, dtype=float)

                                    # Masks
                                    mask_left = x_new < xuser[0]
                                    mask_right = x_new > xuser[len(xuser)-1]
                                    mask_middle = ~ (mask_left | mask_right)

                                    # Apply interpolation and extrapolation
                                    y_new[mask_middle] = interp_func(x_new[mask_middle])
                                    y_new[mask_left] = power_law(x_new[mask_left], *popt_left)
                                    y_new[mask_right] = power_law(x_new[mask_right], *popt_right)

                                    return y_new

                                ##Create array of frequencies
                                logxuserintegral = np.linspace(-18,19,num = 1000)
                                #print('logxuserintegral: ',logxuserintegral)
                                dlogxuserintegral = logxuserintegral[1]-logxuserintegral[0]
                                #print('dlogxuserintegral: ',dlogxuserintegral)
                                yuserintegral = interpolator_with_extrapolation(10**logxuserintegral)

                                #print('yuserintegral: ',yuserintegral)

                                h2OmegaGW = dlogxuserintegral*np.sum(yuserintegral)
                                dRBound = curves_dict['BBN']['yCurve_BBN'][0]
                                print('dRBound= ',dRBound)
                                dRBoundViolation = True if (h2OmegaGW <= dRBound) else False
                                divOmegaGW.text = f"<b>Energy fraction in GWs:</b> {h2OmegaGW}"
                                divDRBound.text = f"<b>Compliance with DR bound:</b> {dRBoundViolation}"
                        except Exception as ee:
                            h2OmegaGW = "Unknown"
                            dRBoundViolation = "Unknown"
                            divOmegaGW.text = f"<b>Energy fraction in GWs:</b> {h2OmegaGW}"
                            divDRBound.text = f"<b>Compliance with DR bound:</b> {dRBoundViolation}"
                            print(f"Error estimating energy fraction: {ee}")




                        lenCSV = len(xuser)
                        label = 'Your curve'
                        lenDict = len(curves_dict[label][f'xCurve_{label}'])
                        #If length of CSV < current max length, just refill user data
                        if lenDict >= lenCSV:
                            nextra = lenDict - lenCSV
                            x_key = f'xCurve_{label}'
                            y_key = f'yCurve_{label}'
                            if nextra > 0:
                                xextra = np.array([ xuser[lenCSV-1] for _ in range(nextra) ])
                                yextra = np.array([ yuser[lenCSV-1] for _ in range(nextra) ])
                                xuser = np.concatenate([xuser,xextra])
                                yuser = np.concatenate([yuser,yextra])
                            #Update curves dict. Assume data is for h2Omega
                            curves_dict[label][x_key] = xuser
                            curves_dict[label][y_key] = yuser
                            #If we are plotting h2Omega, update source
                            if what_to_plot == 0:
                                plot_source_curves.data[x_key] = xuser
                                plot_source_curves.data[y_key] = yuser
                            #Data for hc=8.93368/f Sqrt[h^2 Omega]
                            yuser = 8.93368e-19/(xuser)*np.sqrt(yuser)
                            curves_dict_hc[label][x_key] = xuser
                            curves_dict_hc[label][y_key] = yuser
                            #If we are plotting hc, update source
                            if what_to_plot == 1:
                                plot_source_curves.data[x_key] = xuser
                                plot_source_curves.data[y_key] = yuser
                        #If length of CSV > current max length, need to refill all other curves in "Curves" category
                        #To avoid too many calls to change plot_source_curves, we use dict new_data_curves and update source in the end
                        else:
                            new_data_curves = {}
                            nextra =  lenCSV - lenDict
                            for label, data in curves_dict.items():
                                # Determine the category of the curve
                                category = None
                                for cat, labels in curve_category_dict.items():
                                    if label in labels:
                                        category = cat
                                        break
                                if category == 'Curves':
                                    if 'Your curve' not in label:
                                        x_key = f'xCurve_{label}'
                                        y_key = f'yCurve_{label}'
                                        ###Read curves dict and modify
                                        xaux = data[x_key]
                                        yaux = data[y_key]
                                        #print(f'{label}: xaux: {xaux}')
                                        #print(f'{label}: yaux: {yaux}')
                                        xextra = np.array([ xaux[lenDict-1] for _ in range(nextra) ])
                                        yextra = np.array([ yaux[lenDict-1] for _ in range(nextra) ])
                                        xaux = np.concatenate([xaux,xextra])
                                        yaux = np.concatenate([yaux,yextra])
                                        curves_dict[label][x_key] = xaux
                                        curves_dict[label][y_key] = yaux
                                        #If we are plotting h2Omega, update new data
                                        if what_to_plot == 0:
                                            new_data_curves[x_key] = xaux
                                            new_data_curves[y_key] = yaux
                                        ####Update curces_dict_hc
                                        yaux = 8.93368e-19/(xaux)*np.sqrt(yaux)
                                        curves_dict_hc[label][x_key] = xaux
                                        curves_dict_hc[label][y_key] = yaux
                                        #If we are plotting hc, update source
                                        if what_to_plot == 1:
                                            new_data_curves[x_key] = xaux
                                            new_data_curves[y_key] = yaux
                                    if label == 'Your curve': #Now we are in user data, no need to concatenate
                                        x_key = f'xCurve_{label}'
                                        y_key = f'yCurve_{label}'
                                        #Update curves dict. Assume data is for h2Omega
                                        curves_dict[label][x_key] = xuser
                                        curves_dict[label][y_key] = yuser
                                        #If we are plotting h2Omega, update source
                                        if what_to_plot == 0:
                                            new_data_curves[x_key] =  xuser
                                            new_data_curves[y_key] =  yuser
                                        #Data for hc=8.93368/f Sqrt[h^2 Omega]
                                        yuser = 8.93368e-19/(xuser)*np.sqrt(yuser)
                                        curves_dict_hc['Your curve'][x_key] = xuser
                                        curves_dict_hc['Your curve'][y_key] = yuser
                                        #If we are plotting hc, update source
                                        if what_to_plot == 1:
                                            new_data_curves[x_key] =  xuser
                                            new_data_curves[y_key] =  yuser


                            plot_source_curves.data = new_data_curves
                            #print(f'Data length for csv_path {csv_path}: {len(plot_source_curves.data['xCurve_Your curve'])}')
                            #Update annotation visibility
                            #labelset = fig.select(name='Your curve')[0]  # Get LabelSet by name
                            #labelset.visible = True   # Toggle visibility
                            #paco f"annotation_{label}"


                        #We use this method to only have one call to change plot_source (as opposed to changing x and changing y with 2 statments)
                        #plot_source_curves.data = new_data_curves
                        print(f"CSV loaded for session {session_id}")
                except Exception as e:
                    print(f"Error reading CSV: {e}")


    # Check every 2 seconds
    doc.add_periodic_callback(update_from_external_csv, 2000)

    def cleanup_session(session_context):
        try:
            if os.path.exists(csv_path):
                os.remove(csv_path)
                print(f"[CLEANUP] Removed file for session {session_id}")
        except Exception as e:
            print(f"[ERROR] Failed to delete file for session {session_id}: {e}")

    doc.on_session_destroyed(cleanup_session)



    #####################################################################################
    #####################################################################################
    #####################################################################################
    #####################################################################################
    ######################################################################################


    #Handling changes in phase transition parameters: Simply change plot sources. Future: Do it only if active?
    def update_plot_phase_transition():

        nonlocal plot_source_curves
        nonlocal annotation_source



        x_coord = curves_dict['1st-order p.t.']['xCurve_1st-order p.t.']
        y_coord = np.array(OmegaPT(Tstar, alpha, betaOverH, vw, gstar, x_coord))
        #For 1st-order p.t. we compute label position and angle near peak
        derivative = np.gradient(np.log10(y_coord), np.log10(x_coord))
        nan_mask = np.isnan(derivative)
        # Filter out NaN elements using the mask
        derivative = derivative[~nan_mask]
        if len(derivative)>0:
            position_min = np.argmin(abs(derivative))
            delta_x = 1/1000*x_coord[position_min]
            position_label = np.abs(x_coord - delta_x).argmin()
            delta_x = x_coord[position_label]
            delta_y = y_coord[position_label]
            label_angle = np.arctan(derivative[position_label])
        else:
            #If curve seems problematic, take delta_x delta_y out of plot, label angle 0
            delta_x = 1.e-5*fmin
            delta_y = 1.e-5*min(hmin,Omegah2min)
            label_angle = 0.

        y_coord_h = y_coord
        delta_y_h = delta_y
        delta_x_h = delta_x

        curves_dict['1st-order p.t.']['yCurve_1st-order p.t.'] = y_coord
        curves_dict['1st-order p.t.']['annotation_x_1st-order p.t.'] = delta_x
        curves_dict['1st-order p.t.']['annotation_y_1st-order p.t.'] = delta_y
        curves_dict['1st-order p.t.']['label_angle_1st-order p.t.'] = label_angle


        #Coords for hc=8.93368e-19/f Sqrt[h^2 Omega]
        y_coord = 8.93368e-19/(x_coord)*np.sqrt(y_coord)
        delta_y = 8.93368e-19/(delta_x)*np.sqrt(delta_y)


        curves_dict_hc['1st-order p.t.']['yCurve_1st-order p.t.'] = y_coord
        curves_dict_hc['1st-order p.t.']['annotation_x_1st-order p.t.'] = delta_x
        curves_dict_hc['1st-order p.t.']['annotation_y_1st-order p.t.'] = delta_y
        curves_dict_hc['1st-order p.t.']['label_angle_1st-order p.t.'] = label_angle


        if what_to_plot == 0:
            plot_source_curves.data['yCurve_1st-order p.t.'] = curves_dict['1st-order p.t.']['yCurve_1st-order p.t.']
        elif what_to_plot == 1:
            plot_source_curves.data['yCurve_1st-order p.t.'] = curves_dict_hc['1st-order p.t.']['yCurve_1st-order p.t.']


        annotation_source.data = update_annotation_angles(curves_dict, curves_dict_hc, what_to_plot, annotation_source, fig, fmin, fmax, Omegah2min, Omegah2max)




    # Define a callback function for the phase transition sliders
    def update_tstar(attr, old, new):
        nonlocal Tstar
        Tstar = 10**slider_pt_temp.value
        update_plot_phase_transition()
    def update_alpha(attr, old, new):
        nonlocal alpha
        alpha = 10**slider_pt_alpha.value
        update_plot_phase_transition()
    def update_betaOverH(attr, old, new):
        nonlocal betaOverH
        betaOverH = 10**slider_pt_betaOverH.value
        update_plot_phase_transition()
    def update_vw(attr, old, new):
        nonlocal vw
        vw = slider_pt_vw.value
        update_plot_phase_transition()

    # Attach the Python function to the 'value' change event of the slider
    slider_pt_temp.on_change('value', update_tstar)
    slider_pt_alpha.on_change('value', update_alpha)
    slider_pt_betaOverH.on_change('value', update_betaOverH)
    slider_pt_vw.on_change('value', update_vw)




    # Add the layout to the Bokeh document
    final_layout = column(layout,  Div(text="<div style='height: 10px; background-color: black; width: 100%;'></div>"), row(layout_size,Div(text="<div style='width: 10px; background-color: black; height: 100%;'></div>"),  Div(text="<div style='width: 10px; background-color: black; height: 100%;'></div>"),layout_phase_transition, Div(text="<div style='width: 10px; background-color: black; height: 100%;'></div>"), layout_user), sizing_mode="scale_both")
    doc.add_root(final_layout)



plot_app = Application(FunctionHandler(bokeh_plot_app))







# if __name__ == '__main__':
#     print('Opening Bokeh application on http://localhost:5006/')
#     #server.io_loop.add_callback(server.show, "/")
#     server.io_loop.start()
#     #print('Opening Bokeh application on http://localhost:5007/')
#     #server2.io_loop.start()
#     # Join threads
#     flask_thread.join()

app.register_blueprint(Omegaplot, url_prefix='/Omegaplot')

###########################################
##CODE TO RUN WITH FLASK INTEGRATED SERVER
###########################################
# Start Flask app in a separate thread
flask_thread = Thread(target=lambda: app.run(debug=True, port=5003, use_reloader=False))
flask_thread.start()

# Create and start a single Bokeh server with the different apps with different urls
server = Server({'/plot': plot_app}, prefix="/Omegaplotworkers", io_loop=IOLoop.current(), allow_websocket_origin=["*","localhost:5006","127.0.0.1:5006","localhost:5003","127.0.0.1:5003"], port=5006)
server.start()



if __name__ == '__main__':
     server.io_loop.start()
     flask_thread.join()




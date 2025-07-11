import numpy as np
from matplotlib import pyplot as plt
#some basic colors
clearer='#fd94aeff'
darker='#da76a2ff'
kblue='#569bd2ff'
color_current = 'darkorange'
color_current_2 = 'orange'
color_current_3 = 'peru'
color_current_4 = 'sienna'
color_current_5 = 'orange'
color_current_6 = 'navajowhite'
color_ongoing = 'rebeccapurple'
color_ongoing_2 = 'blueviolet'
color_ongoing_3 = 'mediumpurple'
color_ongoing_4 = 'darkmagenta'
color_ongoing_5 = 'orchid'
color_proposed = 'darkcyan'
color_proposed_2 = 'darkturquoise'
color_proposed_3 = 'cadetblue'
color_proposed_4 = 'cyan'

color_signal_1 = 'rosybrown'
color_signal_2 = 'lightcoral'
color_signal_3 = 'indianred'
color_signal_4 = 'brown'
color_signal_5 = 'firebrick'
color_signal_6 = 'maroon'
color_signal_7 = 'darkred'
color_signal_8 = 'orangered'
color_signal_9 = 'chocolate'
color_signal_10 = 'salmon'
color_signal_11 = 'tomato'
color_signal_12 = 'darksalmon'
color_signal_13 = 'coral'
color_signal_14 = 'crimson'



# data_files.py
#matplotlib default colors
#hc -> (8.54826*10^-19 Sqrt[Omega])/f
prop_cycle = plt.rcParams['axes.prop_cycle']
mplcolors = prop_cycle.by_key()['color']

#Each row gives filename, short name, type (Direct bound/projected bound/projected curve/ indirect bound), color, depth level in plot
detector_data = [
    # Direct bounds. They are plotted as shaded areas, so line width and dash style will be ignored
    #(file, label, category, color, linewidth,linestyle, opacity, depth level, comment, x-shift of label, y-shift of label, angle of label, label color, label size)
    #LC Resonators
    ('Curves/DetectorCurves/PLS_DMRadioGUT_res.csv', 'DMRadio-GUT-res', 'Ongoing', 'Curves', color_ongoing_2, 3, 'dotted', 1,'glyph', None, 1.E-200, 1.E-200, -1.1*np.pi/2.8, color_ongoing, '11pt' ),
    ('Curves/DetectorCurves/PLS_DMRadioGUT.csv', 'DMRadio-GUT', 'Ongoing', 'Curves', color_ongoing_2, 2, 'solid', 1,'glyph', None, 3e7, 2.e12, 0., color_ongoing_2, '11pt' ),
    #Magnetic Weber bars
    ('Curves/DetectorCurves/PLS_MWB.csv', 'Mag. Weber bars', 'Proposed', 'Curves', color_proposed_2, 2, 'solid', 1,'glyph', None, 2E5,  2.e-1, 1.25*np.pi/4, color_proposed_2, '11pt' ),
    ('Curves/DetectorCurves/PLS_MWBDMR_res.csv', 'Mag. Weber bars (res)', 'Proposed', 'Curves', color_proposed_2, 3, 'dotted', 1,'glyph', None, 1E-100, 1E-100, -3.6*np.pi/8, color_proposed_2, '11pt' ),
    #MAGO
    ('Curves/DetectorCurves/PLS_MAGO.csv', 'MAGO', 'Ongoing', 'Curves', color_ongoing, 2, 'solid', 1,'glyph', None, 1.5E4, 1E8,  1.7*np.pi/4, color_ongoing, '11pt' ),
    ('Curves/DetectorCurves/PLS_MAGO_res.csv', 'MAGO (res)', 'Ongoing', 'Curves', color_ongoing, 3, 'dotted', 1,'glyph', None, 1E-100, 1E-100, -np.pi/2.8, color_ongoing, '11pt' ),
    #HELIOSCOPES
    ('Curves/DetectorCurves/PLS_IAXOLF.csv', 'LF IAXO-SPD', 'Proposed', 'Curves', color_proposed, 2, 'solid', 1,'glyph', None, 5E9, 2E1, 0., color_proposed, '11pt' ),
    ('Curves/DetectorCurves/PLS_IAXOLFVar.csv', 'LF IAXO-Var', 'Proposed', 'Curves', color_proposed, 2, 'dashed', 1,'glyph', None, 1E-100, 1E-100, 0, color_proposed, '11pt' ),
    ('Curves/DetectorCurves/PLS_IAXO.csv', 'IAXO', 'Ongoing', 'Curves', color_ongoing, 2, 'solid', 0.5, 'underlay', None, 2e18, 1E9, 0, color_ongoing, '11pt' ),
    ('Curves/DetectorCurves/PLS_CAST.csv', 'CAST', 'Existing', 'Areas', color_current, 2, 'solid', 0.6,'underlay', None, 1.2E18,  1E14, np.pi/2, 'white', '11pt' ),
    #GW INTERFEROMETERS
    ('Curves/DetectorCurves/PLS_LIGO.csv', 'LIGO', 'Existing', 'Areas', color_current, 2, 'solid', 0.6, 'underlay', None, 4e1, 1e11, np.pi/2, 'white', '11pt' ),
    #LIGHT SHINING THROUGH WALL
    ('Curves/DetectorCurves/PLS_DALI.csv', 'DALI II', 'Proposed', 'Curves', color_proposed, 2, 'solid', 1,'glyph', None, 1E10, 2e12, 0.6, color_proposed, '11pt' ),
    ('Curves/DetectorCurves/PLS_ALPS.csv', 'ALPS II', 'Ongoing', 'Curves', color_ongoing, 2, 'solid', 1, 'underlay', None, 1E13, 1E8, 0, color_ongoing, '11pt' ),
    ('Curves/DetectorCurves/PLS_OSQAR.csv', 'OSQAR II', 'Existing', 'Areas', color_current, 2, 'solid', 0.6, 'underlay', None, 1.5E15, 1e16, 0, color_current, '11pt' ),
    #Madmax
     ('Curves/DetectorCurves/PLS_Madmax.csv', 'Madmax', 'Ongoing', 'Curves', color_ongoing_4, 2, 'solid', 1,'glyph', None, 1e9, 1E16, 0.3, color_ongoing_4, '11pt' ),
     ('Curves/DetectorCurves/PLS_Madmax_res.csv', 'Madmax (res)', 'Ongoing', 'Curves', color_ongoing_4, 3, 'dotted', 1,'glyph', None,  1E-100,1E-100,-np.pi/4.2, color_ongoing_4, '11pt' ),
     #Holometer
     ('Curves/DetectorCurves/PLS_Holometer.csv', 'Holometer', 'Existing', 'Areas', color_current, 2, 'solid', 0.6,'underlay', None, 3E6, 2.E11, np.pi/2, 'white', '11pt' ),
     #Levitated sensors
     ('Curves/DetectorCurves/PLS_LS_res.csv', 'Lev. sens. 100m', 'Proposed', 'Curves', color_proposed_3, 3, 'dotted', 1,'glyph', None, 1e5, 1e3, 1.6*np.pi/4, color_proposed_3, '11pt' ),
     #Levitated superconductors
     ('Curves/DetectorCurves/PLS_LevSup.csv', 'Lev. SC 1g', 'Proposed', 'Curves', color_proposed, 2, 'solid', 1,'glyph', None, 2E4, 2.E3, 1.7*np.pi/4, color_proposed, '11pt' )
]



theoretical_bounds_data = [#(file, label, category, color, linewidth,linestyle, opacity, depth level, comment, x-shift of label, y-shift of label, angle of label, label color, label size)
     ('Curves/TheoreticalBoundsCurves/DR.txt', 'BBN', 'Theoretical Bound',  'Curves', 'royalblue', 2, 'dashed', 1, 'glyph', None, 3E17, 1.5E-6, 0, 'royalblue', '11pt'),
     ('Curves/TheoreticalBoundsCurves/Galactic_Data.csv', 'Astro','Theoretical Bound', 'Points',  'royalblue', 2, None, 1, 'glyph', None, 1E16, 1E14, -1.5*np.pi/4, 'royalblue', '11pt')]


signal_data = [
    #(file, label, category, color, linewidth,linestyle, opacity, depth level, comment, x-shift of label, y-shift of label, angle of label, label color, label size)
    ###Global strings (envelope)
    ####PBHs (envelope)
    ('Curves/SignalCurves/CosmologicalSources/PBHs_envelope_h2Omega.csv', 'PBHs', 'Signals_Envelope', 'Curves', color_signal_2, 3, 'solid', 1, 'glyph', 'Comment on PBH : ', 3E17, 1.5E-8, -0.1,  color_signal_2, '11pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/Inflation-EFT_h2Omega.csv', 'Inflation-EFT', 'Signals_Envelope', 'Curves', color_signal_3, 3, 'solid', 1, 'glyph', None, 1E3, 7E-13, 0.2, color_signal_3, '11pt'),
    ('Curves/SignalCurves/CosmologicalSources/Inflation-scalar-perturbations_h2Omega.csv', 'Inflation-scalar pert.', 'Signals_Envelope', 'Curves', color_signal_4, 3, 'solid', 1, 'glyph', None, 7E0, 1E-9, -0.05, color_signal_4, '11pt'),
    ('Curves/SignalCurves/CosmologicalSources/Inflation-extra-species_h2Omega.csv', 'Inflation-extra species', 'Signals_Envelope', 'Curves', color_signal_5, 3, 'solid', 1, 'glyph', None, 7E0, 1E-15, 0,color_signal_5, '11pt'),
    ###
    ('Curves/SignalCurves/CosmologicalSources/Oscillons_h2Omega.csv', 'Oscillons', 'Signals_Envelope', 'Curves', color_signal_7, 3, 'solid', 0.6, 'glyph', None, 2E6, 1E-13, np.pi/2, color_signal_7, '11pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/Metastable_strings_h2Omega.csv', 'Met. strings',  'Signals_Envelope', 'Curves', color_signal_8, 3, 'solid', 1, 'overlay', None, 1e3, 2e-6, 0, color_signal_8, '11pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/Local_strings_h2Omega.csv', 'Cosmic strings', 'Signals_Envelope', 'Curves', mplcolors[6], 3, 'solid', 1, 'underlay', None, 1E7, 1.e-9, 0, mplcolors[6], '11pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/Gauge_textures_h2Omega.csv', 'Gauge text.', 'Signals_Envelope', 'Curves', color_signal_9, 3, 'solid', 1, 'glyph', None, 4E6, 2E-20, 0.875*np.pi/2, color_signal_9, '11pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/PT_envelope_h2Omega.csv', 'Phase transitions', 'Signals_Envelope', 'Curves', color_signal_10, 3, 'solid', 1, 'glyph', None, 1E7, 2E-6, 0, color_signal_10, '11pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/CGMB_SM_1e16_h2Omega.csv', 'CGMB (env.)', 'Signals_Envelope', 'Curves', color_signal_11, 3, 'solid', 1, 'glyph', None, 3E11, 2E-11, -0.97*np.pi/2, color_signal_11, '11pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/Preheating_Quadratic_h2Omega.csv', 'Preheating 1', 'Signals_Envelope', 'Curves', color_signal_13, 3, 'solid', 1, 'glyph', None, 3E6, 2.5E-12, 0, color_signal_13, '11pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/Preheating_Quartic_h2Omega.csv', 'Preheating 2', 'Signals_Envelope', 'Curves', color_signal_12, 3, 'solid', 1, 'glyph', None, 1E9, 2E-15,  0, color_signal_12, '11pt'),
    ##
    (' ','1st-order p.t.',  'Signals_Individual', 'Curves', color_signal_14, 2, 'solid', 1, 'glyph', None, None, None, np.pi/4, color_signal_14, '9pt'),
    ##
    ('Curves/SignalCurves/CosmologicalSources/CGMB_SM_Mp_h2Omega.csv', 'CGMB', 'Signals_Individual', 'Curves', 'orangered', 2, 'solid', 1, 'glyph', None, 3E11, 2E-11, -0.97*np.pi/2, 'orangered', '11pt'),
    ##
    (' ','Your curve',  'Signals_Individual', 'Curves', color_signal_7, 3, 'solid', 1, 'glyph', None, None, None, 0, color_signal_7, '9pt')
    ]


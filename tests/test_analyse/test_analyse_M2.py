# test M2 fitting

import laser_beam as lb

#from matplotlib import units
import pint

import numpy as np
import matplotlib.pyplot as plt

import xarray as xr

#data_set = 1 # from 08.04.2026 with Femtoeasy, didn't work
# data_set = 2 # from 09.04.2026 with Ophir, MP 0% pump, DFM optimized for MP 0% pump
#data_set = 3 # from 09.04.2026 with Ophir, MP 100% pump, DFM optimized for MP 0% pump
#data_set = 4 # from 09.04.2026 with Ophir, MP 100% pump, DFM optimized for MP 100% pump

data_set = 4

match data_set:
    case 1:
        titel = "faulty measurement: MP 0% pump, DFM optimized for MP 0% pump"
        width_x = np.array([1285, 1198, 1059, 928, 719, 530, 433, 318, 295, 309, 300, 374, 410, 553, 721, 882])
        width_y = np.array([1056, 985, 884, 780, 629, 460, 397, 287, 237, 262, 244, 334, 380, 525, 639, 897])
        position = np.array([-11, 1, 27, 50, 75, 100, 126, 142, 162, 175, 181, 201, 221, 243, 262, 289])

    case 2:
        titel = "MP 0% pump, DFM optimized for MP 0% pump"
        position = np.array([14, 30, 40, 54, 67, 82, 87, 93, 96, 101, 106, 113, 121, 135, 150, 160, 171, 181, 200])
        width_x = np.array([872, 705, 631, 509, 402, 292, 266, 237, 205, 197, 189, 191, 210, 310, 402, 474, 580, 668, 838])
        width_y = np.array([698, 593, 513, 427, 326, 238, 236, 221, 212, 208, 208, 228, 247, 320, 420, 489, 570, 625, 788])

    case 3:
        titel = "MP 100% pump, DFM optimized for MP 0% pump"
        position = np.array([19, 32, 44, 61, 79, 92, 103, 113, 124, 134, 145, 155, 170, 184, 199, 220])
        width_x = np.array([1160, 1000, 970, 690, 560, 419, 372, 260, 218, 212, 221, 286, 357, 495, 611, 813])
        width_y = np.array([753, 696, 639, 472, 353, 271, 242, 219, 203, 256, 276, 351, 444, 533, 641, 819])

    case 4:
        titel = "MP:10mJ"
        position = np.array([11, 25, 40, 54, 69, 85, 100, 110, 114, 119, 124, 128, 134, 144, 155, 170, 186, 201, 215])
        width_x = np.array([925, 838, 700, 630, 500, 414, 246, 199, 182, 177, 183, 186, 197, 243, 327, 447, 589, 707, 822])
        width_y = np.array([909, 795, 728, 570, 451, 355, 252, 212, 195, 191, 200, 187, 216, 241, 278, 387, 534, 652, 750])

    case 5:
        titel = "MP: 430mJ (1)"
        position = np.array([15, 23, 36, 44, 44, 57, 70, 87, 100, 111, 119, 126, 130, 135, 145, 155, 169, 189, 205, 220, 227])
        width_x = np.array([1084, 1112, 984, 761, 875, 770, 537, 399, 274, 239, 183, 185, 184, 190, 247, 303, 413, 642, 839, 957, 1038])
        width_y = np.array([953, 946, 851, 725, 740, 659, 499, 377, 283, 222, 202, 201, 190, 210, 284, 353, 438, 616, 756, 865, 922])

    case 6:
        titel = "MP: 430mJ (2)"
        position = np.array([15, 23, 36, 45, 58, 71, 87, 100, 111, 126, 130, 135, 141, 149, 156, 166, 180, 204, 219, 234])
        width_x = np.array([1254, 1168, 1041, 964, 810, 633, 503, 379, 285, 191, 171, 165, 180, 230, 257, 344, 491, 750, 880, 1066])
        width_y = np.array([1058, 1023, 894, 812, 665, 576, 460, 351, 276, 207, 188, 178, 191, 212, 257, 333, 461, 708, 829, 962])



radius_x = width_x / 2
radius_y = width_y / 2


width_units = 'μm'
width_units = 'micrometer'
position_units = 'mm'


# --- setup beam objects 
beam_x = xr.DataArray(
    data = radius_x,
    dims=['Position'],
    coords={
        'Position': (['Position'], position, {'units': position_units}),
    },
    name='Radius',
    attrs={'units': width_units,
            'label': 'X',
    },
)

beam_y = xr.DataArray(
    data = radius_y,
    dims=['Position'],
    coords={
        'Position': (['Position'], position, {'units': position_units}),
    },
    name='Radius',
    attrs={'units': width_units,
            'label': 'Y',
    },
)

# --- fitting ---
fit_m2_x = lb.fit_m2(beam_x, wavelength=1030e-9)
fit_m2_y = lb.fit_m2(beam_y, wavelength=1030e-9)



# --- print results ---
lb.print_m2_result(fit_m2_x)
lb.print_m2_result(fit_m2_y)

# --- plotting ---
fig,ax = plt.subplots(1)

# color stuff
color1 = '#ec0868'
color2 = '#fc2f00'
color3 = '#ec7d10'
color4 = '#ffbc0a'

color_a = color2
color_b = color4

styles = [lb.STYLE_POINTS| {"color": color_a},
                lb.STYLE_POINTS| {"color": color_b},
                lb.STYLE_FIT| {"color": color_a},
                lb.STYLE_FIT| {"color": color_b},
                ]

# plot data and fits
ax = lb.plot_1D([beam_x,beam_y,fit_m2_x,fit_m2_y],
    title=titel,
    plot_styles=styles,
    overlays_label_show=False,
    legend_kwargs= {'loc': 'upper center', 'ncol': 2},
    )


plt.tight_layout()
plt.show()
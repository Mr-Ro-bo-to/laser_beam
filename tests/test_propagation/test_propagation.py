# test propagete.py module

import numpy as np

import matplotlib.pyplot as plt

import laser_beam as lb

# define beam
beam_I_NF = lb.create_beam_xy(
    name = "Input",
    #type='SuperGaussSquare',
    type='Gauss',
    func_params={
        'width_x': 50,
        'width_y': 60,
    },
    axis_unit='mm',
)

# do the math
beam_E_NF = np.sqrt(beam_I_NF)
beam_E_NF.attrs['beam_name'] = 'Square Root'
beam_E_NF.name = 'E-Field'

beam_E_FF = lb.fft_2d(beam_E_NF)

# --- Figures ---


fig,ax = plt.subplots(1, 3,figsize=(12,4))

lb.plot_2D(beam_I_NF,ax=ax[0])

lb.plot_2D(beam_E_NF,ax=ax[1])

lb.plot_2D(beam_E_FF,ax=ax[2])

# plt.tight_layout()
plt.show()
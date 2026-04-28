#from laser_beam.utils import hello_world

import pint_xarray

import matplotlib.pyplot as plt


import laser_beam as lb

lb.hello_world()

ureg = pint_xarray.unit_registry


beam = lb.create_beam_xy()

beam.plot()


plt.show()
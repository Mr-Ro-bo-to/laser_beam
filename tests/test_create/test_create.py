import matplotlib.pyplot as plt

import laser_beam as lb

beam = lb.create_beam_xy(
    func_params={
        'width_x': 10,
        'width_y': 15,
    }
)

beam.plot()

plt.tight_layout()
plt.show()


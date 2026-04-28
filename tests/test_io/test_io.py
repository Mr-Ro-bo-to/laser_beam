import matplotlib.pyplot as plt

import laser_beam as lb

beam = lb.create_beam_xy(
    func_params={
        'width_x': 10,
        'width_y': 15,
    }
)

lb.save_dataarray_as_png(beam,file_name="Test.png")
beam = lb.load_image_as_dataarray(file_name="Test.png")

lb.plot_2D(beam)

plt.tight_layout()
plt.show()
import laser_beam as lb

import matplotlib.pyplot as plt

center_x = 0.5
center_y = -1
width_x = 0.5
width_y = 0.5

beam = lb.create_beam_xy(
    type="Gauss",
    name="Near Field",
    variable_name = 'Intensity',
    func_params={
        'width_x': width_x,
        'width_y': width_y,
        'x0': center_x,
        'y0': center_y,
    },
    axis_unit="px",
    axis_pixelsize=0.05,
    axis_x_N=101,
    axis_y_N=101,
)

# --- Check stats

beam_2 = lb.set_statistics(beam)
print(f"center input(x,y): ({center_x}), {center_y})")
print(f"center(x,y): {beam_2.coords['x'].attrs['center']},{beam_2.coords['y'].attrs['center']}")

print(f"width input: ({width_x}), {width_y}) (D(1/e2) = 4*std for Gauss)")
print(f"std(x,y): {beam_2.coords['x'].attrs['spread']}, {beam_2 .coords['y'].attrs['spread']}")

    
# -- Figures

fig, ax = plt.subplots()
lb.plot_2D(beam_2, ax=ax)

plt.show()
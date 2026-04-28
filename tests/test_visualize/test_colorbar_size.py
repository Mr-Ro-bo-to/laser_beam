import numpy as np
import xarray as xr

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import laser_beam as lb

pixel_size = 1
N_x = 150
N_y = 100

x = pixel_size * (np.arange(N_x) - (N_x - 1) / 2)
y = pixel_size * (np.arange(N_y) - (N_y - 1) / 2)

# define extent correctly
dx = x[1] - x[0]
dy = y[1] - y[0]
extent = [x[0]-dx/2, x[-1]+dx/2, y[0]-dy/2, y[-1]+dy/2]

# create meshgrid
X, Y = np.meshgrid(x, y,indexing='ij')  # note the indexing='ij' for x,y order

data = lb.gauss_2D(X, Y, width_x=10.0, width_y=10.0)

da = xr.DataArray(
    data,
    dims=("x", "y"),
    coords={"x": x, "y": y},
    name="intensity"
)

# plot figure, default
fig1, ax1 = plt.subplots(figsize=(6,6))
im1 = ax1.imshow(data, 
    cmap='jet',
    extent=extent,  # Show requested extent
    origin='lower', # set origin of y-axis to bottom (top by default, such confusion)
    aspect='equal',
)
ax1.set_xlabel("x (px)")
ax1.set_ylabel("y (px)")
ax1.set_title("Default colorbar (may not align)")
cbar = plt.colorbar(im1)
cbar.set_label("Intensity (a.u.)")




fig2, ax2 = plt.subplots(figsize=(6,6))

im2 = ax2.imshow(data.T,
                 cmap='jet',
                 extent=extent,
                 origin='lower',
                 aspect='equal')  # preserves pixel aspect

ax2.set_xlabel("x (px)")
ax2.set_ylabel("y (px)")
ax2.set_title("Aligned colorbar")

# Create colorbar aligned exactly to the image
divider = make_axes_locatable(ax2)
cax = divider.append_axes("right", size="5%", pad=0.1)  # 5% width, 0.05 padding
cbar = plt.colorbar(im2, cax=cax)
cbar.set_label("Intensity (a.u.)")



# now with subplot
fig3, axes = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns

# Top: default colorbar (approximate)
ax1 = axes[0]
im1 = ax1.imshow(data.T, cmap='jet', extent=extent, origin='lower')
ax1.set_title("Default colorbar")
ax1.set_xlabel("x (px)")
ax1.set_ylabel("y (px)")
cbar = plt.colorbar(im1, ax=ax1)  # default placement
cbar.set_label("Intensity (a.u.)")

# Bottom: aligned colorbar
ax2 = axes[1]
im2 = ax2.imshow(data.T, cmap='jet', extent=extent, origin='lower', aspect='equal')
ax2.set_title("Aligned colorbar")
ax2.set_xlabel("x (px)")
ax2.set_ylabel("y (px)")
divider = make_axes_locatable(ax2)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbar = plt.colorbar(im2, cax=cax)
cbar.set_label("Intensity (a.u.)")




# try with da.plot()

fig4, ax = plt.subplots(figsize=(6,6))


quad = da.plot(
    ax=ax,
    cmap="jet",
    add_colorbar=False  # important!
)

ax.set_aspect("equal")
ax.set_title("xarray plot with aligned colorbar")

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

cbar = plt.colorbar(quad, cax=cax)
cbar.set_label("Intensity (a.u.)")

plt.tight_layout()
plt.show()
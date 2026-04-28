# attempt at parametrically generate cerated aperture

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.path import Path


# 

Length = 30
N_e = 10.1



N_c = 5
R = 20
depth = -3

# pitch_e = (Length-2*R) / N_e
# pitch_c = np.pi * R / N_c
# alpha = 2 * np.pi / 4 / N_c / 2 # 90deg/ N, half of that

# print(f"Edge: pitch={pitch_e}, N={N_e}")
# print(f"Corner: pitch={pitch_c}, N={N_c}")
# print(f"angle: {np.rad2deg(alpha)}")

# # edge (bottom)
# edge = np.ones((2 * N_e + 1, 2))

# for i in range(2 * N_e + 1):
#     #outside
#     if np.mod(i,2)==0:
#         y = -depth/2
#     #inside
#     if np.mod(i,2) == 1:
#         y = depth/2

#     x = i * pitch_e/2
#     x = x - (Length/2 - R)    # shift to 0
    
#     edge[i,0] = x #x
#     edge[i,1] = y #y


# # corner
# corner = np.ones((2 * N_c + 1, 2))

# for i in range(2 * N_c+1):
#     #outside
#     if np.mod(i,2)==0:
#         R_mod = R + depth/2
#     #inside
#     if np.mod(i,2) == 1:
#         R_mod = R - depth/2
    
#     corner[i,0] = R_mod * np.sin(alpha * i) #x
#     corner[i,1] = -R_mod* np.cos(alpha * i) #y

# # patch stuff together:
# M_rot = np.array([[0, 1],
#               [-1,  0]])

# edge_shift = Length/2
# corner_shfit = Length/2-R

# # edges
# edge_2 = edge @ M_rot
# edge_3 = edge_2 @ M_rot
# edge_4 = edge_3 @ M_rot

# edge_1 = edge + np.array([0,-edge_shift])   # bottom
# edge_2 = edge_2 + np.array([edge_shift,0])  # right
# edge_3 = edge_3 + np.array([0,edge_shift])  # top
# edge_4 = edge_4 + np.array([-edge_shift,0]) # left

# #corner
# corner_2 = corner @ M_rot
# corner_3 = corner_2 @ M_rot
# corner_4 = corner_3 @ M_rot

# corner_1 = corner + np.array([corner_shfit,-corner_shfit])      # bottom right
# corner_2 = corner_2 + np.array([corner_shfit,corner_shfit])     # top right
# corner_3 = corner_3 + np.array([-corner_shfit,corner_shfit])    # top left
# corner_4 = corner_4 + np.array([-corner_shfit,-corner_shfit])   # bottom left


# points = np.vstack((edge_1, corner_1,
#                          edge_2, corner_2,
#                          edge_3, corner_3,
#                          edge_4, corner_4))

def serrated_aperture_points(size=Length, n_e=N_e, n_c=N_c, r=R, depth=depth):
    """
    Generates a set of (x, y) coordinates defining a serrated square aperture
    with rounded corners.
    
    The shape is constructed by defining one quadrant (one edge and one corner)
    and rotating it four times. The serrations are created by alternating 
    offsets relative to the nominal boundary.

    Parameters
    ----------
    size : float
        The side length of the square aperture (edge to edge).
    n_e : int
        Number of serration "teeth" along each straight edge. 
        Will be cast to an integer.
    n_c : int
        Number of serration "teeth" along each 90-degree corner arc.
        Will be cast to an integer.
    r : float
        The nominal radius of the corners. If r=0, corners are sharp.
        If r=size/2, the aperture becomes a serrated circle.
    depth : float
        The peak-to-peak depth of the serrations. A positive value 
        creates teeth alternating between +/- depth/2.

    Returns
    -------
    points : ndarray
        An (N, 2) array of coordinates defining the closed path of the 
        aperture, suitable for use with matplotlib.path or cv2.fillPoly.

    Raises
    ------
    ValueError
        If n_e or n_c are negative.
    """

    # some validation
    if n_e < 0:
        raise ValueError(f"Number of points (n_e={n_e}) must be non-negative.")
    if n_c < 0:
        raise ValueError(f"Number of points (n_c={n_c}) must be non-negative.")
    
    # Cast to int to ensure array sizing works
    n_e, n_c = int(n_e), int(n_c)


    # 1. Create the alternating "serration" offsets
    # Using tile to create [depth/2, -depth/2, depth/2, ...]
    edge_offsets = np.tile([depth/2, -depth/2], n_e + 1)[:2 * n_e + 1]
    corner_offsets = np.tile([-depth/2, depth/2], n_c + 1)[:2 * n_c + 1]

    # 2. Build the bottom edge (Edge 1)
    x_e = np.linspace(-(size/2 - r), (size/2 - r), 2 * n_e + 1)
    edge_template = np.column_stack((x_e, -size/2 + edge_offsets))

    # 3. Build the bottom-right corner (Corner 1)
    # Angle spans 0 to 90 degrees (pi/2)
    angles = np.linspace(0, np.pi/2, 2 * n_c + 1)
    r_coords = r + corner_offsets
    
    # Center of the corner arc is at (size/2 - r, -size/2 + r)
    cx, cy = (size/2 - r), -(size/2 - r)
    corner_template = np.column_stack((
        cx + r_coords * np.sin(angles),
        cy - r_coords * np.cos(angles)
    ))

    # 4. Combine into one side (Quadrant)
    side = np.vstack((edge_template, corner_template))

    # 5. Rotate and collect
    # 90-degree rotation matrix
    m_rot = np.array([[0, 1], [-1, 0]])
    
    all_points = []
    current_side = side
    for _ in range(4):
        all_points.append(current_side)
        current_side = current_side @ m_rot
        
    return np.vstack(all_points)

points = serrated_aperture_points()
#points = np.vstack((edge_1))
# points = np.vstack((corner_1))


# --- make mask ---
# 1. Create a meshgrid from scratch
x_mask = np.linspace(-Length, Length, 1000)
y_mask = np.linspace(-Length, Length, 1000)
# 'ij' indexing matches (rows, columns) logic
xx, yy = np.meshgrid(x_mask, y_mask, indexing='ij')

# 3. Generate the mask
# Flatten the grid to a list of (x, y) pairs
coords = np.column_stack((xx.flatten(), yy.flatten()))

# Create the Path and test points

# Small test data

poly_path = Path(points)
mask = poly_path.contains_points(coords).reshape(xx.shape)


# Figures
x = points[:, 0]
y = points[:, 1]

fig1, (ax0, ax1) = plt.subplots(1, 2)


# --- Left Plot: The Points ---
ax0.plot(x, y)
ax0.set_xlabel("x")
ax0.set_ylabel("y")
ax0.set_title("Created Aperture (Points)")
ax0.set_aspect('equal') # Forces 1:1 ratio
ax0.grid(True, linestyle='--', alpha=0.6)

# --- Right Plot: The Mask ---
# 'extent' maps the image to your actual coordinate values: [xmin, xmax, ymin, ymax]
extent = [x_mask.min(), x_mask.max(), y_mask.min(), y_mask.max()]

im = ax1.imshow(mask, origin='lower', extent=extent, cmap='viridis', aspect='equal')
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_title("Created Aperture (Mask)")

# Add a colorbar that fits nicely next to the mask


plt.tight_layout()
plt.show()
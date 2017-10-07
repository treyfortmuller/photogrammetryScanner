# Parse the json file created by SfM algorithm into a numpy array then run operations to determine the maximum
# door open angle without hitting a point in the cloud
# Trey Fortmuller

import numpy as np
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Rectangle, Circle

# CONSTANTS
z_upper_thresh = 30  # top of the door
z_lower_thresh = -60  # bottom of the door
door_sweep_radius = 60  # we center our circle of door sweep at the origin
max_open_angle = 80  # the maximum open angle of the door, the open angle when there are no collision points
safety_margin_deg = 3  # how many degrees to leave before we collide with the first point
safe_open_ang = 0  # default safe open angle in degrees

# VARIABLES
points = np.array([])
collision_points = np.array([])  # points that the door will hit along its sweep
no_collision_points = np.array([])  # points that the door will not hit along its sweep
collision_ratios = np.array([])  # ratio of y / x for collision points, the min is the the point we hit first


def inside_door_sweep_circle(x_point, y_point, radius):  # the x and y coords of the point, the radius of the door swing
    # points inside or on a circle satisfy (x - center_x)^2 + (y - center_y)^2 <= radius^2
    if x_point ** 2 + y_point ** 2 <= radius ** 2:
        return True
    else:
        return False


def add_to_list_of_lists(np_array, value):
    # BUG: A ARISES HERE WHEN THERE IS ONLY ONE POINT B/C THE DEPTH OF THE ARRAY IS INCORRECT

    # first append then continue by vstacking
    if len(np_array) == 0:
        np_array = np.append(np_array, [value])
    else:
        np_array = np.vstack((np_array, value))
    return np_array


def get_x_coords(full_coords):
    x_coords = np.array([])
    for coord in full_coords:
        x_coords = np.append(x_coords, coord[0])
    return x_coords.tolist()


def get_y_coords(full_coords):
    y_coords = np.array([])
    for coord in full_coords:
        y_coords = np.append(y_coords, coord[1])
    return y_coords.tolist()


def get_z_coords(full_coords):
    z_coords = np.array([])
    for coord in full_coords:
        z_coords = np.append(z_coords, coord[2])
    return z_coords.tolist()


def calc_safety_margin(open_deg):
    # if the open angle should be 0 or the maximum then the safety factor should not be factored in
    # otherwise, apply the safety factor to undershoot a collision
    if open_deg == 0 or open_deg == max_open_angle:
        return open_deg
    else:
        return open_deg - safety_margin_deg


def rad_to_deg(rad):
    deg = (rad / np.pi) * 180
    return deg


def deg_to_rad(deg):
    rad = (deg / 180.0) * np.pi
    return rad


# PARSE THE JSON FILE INTO COORDINATES
with open('/home/trey.fortmuller/Desktop/sfm/sfm_test/sfm_out/sfm_reconstruction/point_cloud.json') as json_file:
    data = json.load(json_file)
    for point in data["structure"]:
        coord = point["value"]["X"]  # get the coordinates into a list of lists like [[x1, y1, z1], [x2, y2, z2]]
        points = add_to_list_of_lists(points, coord)

# split the points array into two, points the door collides with and points it doesn't
for point in points:

    x = point[0]
    y = point[1]
    z = point[2]

    if z_upper_thresh > z > z_lower_thresh and inside_door_sweep_circle(x, y, door_sweep_radius):
        collision_points = add_to_list_of_lists(collision_points, point)
    else:
        no_collision_points = add_to_list_of_lists(no_collision_points, point)

# if there are no collision points we can open the door to the max angle, otherwise we have to compute the open angle
if len(collision_points) == 0:
    open_ang_deg = max_open_angle
    safe_open_ang = calc_safety_margin(open_ang_deg)
    print("SAFE OPEN ANGLE TO COMMAND: " + str(safe_open_ang) + " (MAX)")

# otherwise we need to compute the open angle we should command to the door
else:
    # # protect against an edge case bug where the depth of the array is incorrect when there is only one point
    # if type(collision_points[0]) == np.float64:  # if the list is not a list of lists...
    #     collision_points = np.array([collision_points])

    # sort the collision points by ratio of y / x, the point with the minimum is the point we collide with first
    for point in collision_points:
        x = point[0]
        y = point[1]

        # protect against edge cases
        if y <= 0:
            collision_ratio = 0  # an object is already touching the door (or is inside the door somehow)
        if x == 0:  # avoid a divide by zero error
            # this is python's float for positive infinity, np.arctan handles this appropriately and outputs pi/2 rads
            collision_ratio = float("inf")
        else:
            collision_ratio = y / x
            if collision_ratio < 0:  # only collision ratios greater than 0 are valid
                # do nothing
                continue
            else:
                collision_ratios = np.append(collision_ratios, collision_ratio)

    if len(collision_ratios) == 0:  # if all of the collision ratios were less than 0 so none were kept
        open_ang_deg = max_open_angle
        safe_open_ang = calc_safety_margin(open_ang_deg)
        print("SAFE OPEN ANGLE TO COMMAND: " + str(safe_open_ang) + " (MAX)")
    else:
        min_col_ratio = np.min(collision_ratios)  # the minimum collision ratio
        # SET THE OPEN ANGLE OF THE DOOR
        open_ang_rad = np.arctan(min_col_ratio)
        open_ang_deg = rad_to_deg(open_ang_rad)  # this is the open angle at which we will collide with the first point

        safe_open_ang = calc_safety_margin(open_ang_deg)  # apply the safety factor if it necessary to apply it

        print("SAFE OPEN ANGLE TO COMMAND: " + str(safe_open_ang))

# PLOTTING
# initialize a 3d plot with matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim3d(-25, 65)  # arbitrarily chosen points to maintain the scale between axis
ax.set_ylim3d(-10, 80)
ax.set_zlim3d(-50, 50)

# plot the hinge axis as a vertical line
ax.plot([0, 0], [0, 0], [z_lower_thresh, z_upper_thresh], c='black', linewidth=3.0)

# plot the door as a rectangle in the closed position
# (x, y) - lower left corner, width, height
rect = Rectangle((0, z_lower_thresh), door_sweep_radius, z_upper_thresh - z_lower_thresh, alpha=.1)
ax.add_patch(rect)
art3d.pathpatch_2d_to_3d(rect, z=0, zdir="y")  # 'zdir' is the normal vector

# draw a circle representing the door swing radius
# (x, y) - center, radius
circ = Circle((0, 0), door_sweep_radius, alpha=.1)
ax.add_patch(circ)
art3d.pathpatch_2d_to_3d(circ, z=z_lower_thresh, zdir="z")  # 'zdir' is the normal vector

# plot the points we won't collide with in blue
ax.scatter(get_x_coords(no_collision_points),
           get_y_coords(no_collision_points),
           get_z_coords(no_collision_points),
           c='b',
           marker='o')

# plot the points we will collide with in red
ax.scatter(get_x_coords(collision_points),
           get_y_coords(collision_points),
           get_z_coords(collision_points),
           c='r',
           marker='o')

ax.set_xlabel('Door')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')

# plot the door at "safe_open_angle"
# the x and y coordinates of the outside edge of the door in its open angle to plot rect with vertices
outer_edge_x = door_sweep_radius * np.cos(deg_to_rad(safe_open_ang))
outer_edge_y = door_sweep_radius * np.sin(deg_to_rad(safe_open_ang))

# all the x, y, and z coords of the vertices, there are 4 verts in a rectangle
# vertices in order clockwise starting from the bottom left
x = [0, 0, outer_edge_x, outer_edge_x]
y = [0, 0, outer_edge_y, outer_edge_y]
z = [z_lower_thresh, z_upper_thresh, z_upper_thresh, z_lower_thresh]
verts = [zip(x, y, z)]

collection = Poly3DCollection(verts, linewidths=1, alpha=0.5)
face_color = [0, 1, 0]  # the rgb face color for the moved door, this must be set in order to get an alpha
collection.set_facecolor(face_color)  # set the face color
ax.add_collection3d(collection)  # add the moved door to the plot

plt.show()

import bpy
import math
from mathutils import Vector

# Convenience function to animate Bezier points and handles
def animate_bezier_point(point, frame, location):
    bpy.context.scene.frame_set(frame)
    point.co = location
    point.keyframe_insert(data_path="co")

# Clear existing objects in the scene
if bpy.context.active_object:
    bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Set up the curve
curve_data = bpy.data.curves.new('knot_curve', 'CURVE')
curve_data.dimensions = '3D'
curve_data.fill_mode = 'FULL'
curve_data.bevel_depth = 0.02  # Adjust the thickness of the cord
curve_object = bpy.data.objects.new('KnotObject', curve_data)
bpy.context.collection.objects.link(curve_object)

# Create a spline in the curve
spline = curve_data.splines.new('BEZIER')
spline.use_cyclic_u = False

# Add the points for the knot
num_points = 4
spline.bezier_points.add(num_points - 1)
for point in spline.bezier_points:
    point.handle_left_type = 'AUTO'
    point.handle_right_type = 'AUTO'

# Define start and end points
start_point = spline.bezier_points[0]
end_point = spline.bezier_points[-1]
start_point.co = Vector((0, 0, 0))
end_point.co = Vector((0, 0, 2))

# Initial animation: everything is straight
for point in spline.bezier_points:
    animate_bezier_point(point, 1, point.co)

# Animation: Tie the knot
frames_per_step = 20
current_frame = 1

# Step 1: Create a loop in the middle
current_frame += frames_per_step
mid_point_1 = spline.bezier_points[1]
mid_point_2 = spline.bezier_points[2]
animate_bezier_point(mid_point_1, current_frame, Vector((1, 0, 0.5)))
animate_bezier_point(mid_point_2, current_frame, Vector((-1, 0, 1.5)))

# Step 2: Cross over
current_frame += frames_per_step
animate_bezier_point(mid_point_1, current_frame, Vector((1, 0, 1.5)))
animate_bezier_point(mid_point_2, current_frame, Vector((-1, 0, 0.5)))

# Step 3: Pull tight to form the knot
current_frame += frames_per_step
animate_bezier_point(mid_point_1, current_frame, Vector((0.5, 0, 1)))
animate_bezier_point(mid_point_2, current_frame, Vector((-0.5, 0, 1)))

# Set scene frame range
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = current_frame

print("Animated knot created.")

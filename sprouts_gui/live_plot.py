import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from SH_diff import PolygonClipper
import torch
from util import check_polygon_self_intersection
from grad_utils import polygon_area_torch, angle_range_loss, intersection_closeness_loss


def plot_polygon(ax, polygon_tensor, color='r'):
    if polygon_tensor.shape[0] == 0:
        return
    # Convert the torch tensor to a numpy array
    polygon_np = polygon_tensor.detach().numpy()
    # Plot the polygon
    ax.plot(np.append(polygon_np[:, 0], polygon_np[0, 0]), np.append(polygon_np[:, 1], polygon_np[0, 1]), color+'-')


# Function to update the plot at each iteration
def update(frame, ax, subject_polygon, clipping_polygons, optim, is_point_fixed, should_include, clipping_poly_area):
    x_min, x_max = -3, 15
    y_min, y_max = -3, 15
    # Clear the previous plot
    ax.clear()

    # Plot the updated polygon and clipping polygon
    plot_polygon(ax, subject_polygon, 'r')
    for clipping_polygon in clipping_polygons:
        plot_polygon(ax, clipping_polygon, 'b')

    update_polygon_nodes(subject_polygon, clipping_polygons, ax, optim, is_point_fixed, should_include, clipping_poly_area)

    # Set plot limits according to your needs
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

def apply_gradient_descent_self_intersect(polygon, delta = 0.01):
    # Ensure the polygon has a gradient
    assert polygon.requires_grad, "Polygon tensor must have the grad attribute set."
    
    # Clone the polygon for manipulation
    new_polygon = polygon.clone().detach().requires_grad_(True)
    
    # Iterate over each point in the polygon
    for i in range(new_polygon.shape[0]):
       
        # Apply the gradient to the point with the learning rate delta
        new_polygon.data[i] -= delta * polygon.grad[i]
        
        # Check for self-intersection
        if check_polygon_self_intersection(new_polygon):
            # Zero out the gradient and revert the change if self-intersection occurs
            new_polygon.data[i] += 2*delta * polygon.grad[i]  # Revert the change
        else:
            # Keep the change and continue
            continue
    
    # Update the original polygon
    polygon.data = new_polygon.data


def update_polygon_nodes(subject_polygon, clipping_polygons, ax, optim, is_point_fixed, should_include, clipping_poly_area):
    loss = torch.tensor(0.0)
    for i,clipping_polygon in enumerate(clipping_polygons):
        clip = PolygonClipper()
        clipped_polygon = clip(subject_polygon,clipping_polygon)
        if clipped_polygon.shape[0] == 0:
            continue
        plot_polygon(ax, clipped_polygon, 'g')

        # Calculate the area loss - if polygon should be inside loss is area - area_inside
        # if polygon should be outside loss is area_inside
        if should_include[i]:
            area_loss = clipping_poly_area[i] - polygon_area_torch(clipped_polygon)
        else:
            area_loss = polygon_area_torch(clipped_polygon)
        print(f'Area loss: {area_loss}')
        loss += area_loss
    
    angle_loss = 0.1*angle_range_loss(subject_polygon)
    intersect_loss = intersection_closeness_loss(subject_polygon)
    print(f'Angle loss: {angle_loss}')
    print(f'Intersect loss: {intersect_loss}')
    loss += angle_loss + intersect_loss
    loss.backward()

    # Set the gradient of the fixed points to zero
    for i in range(subject_polygon.shape[0]):
        if is_point_fixed[i]:
            subject_polygon.grad[i] = 0
    optim.step()
    optim.zero_grad()



subject_polygon = [(1.9, 0.7),(2.2, 4.3),(5.2, 6.3),(8, 7),(10.6, 6.7),(12.6, 5.8),(13.6, 4.8),(13.5, 3.1),(11.4, 0.5),(7.8, 0.9),(4.2, 0.3)]
is_point_fixed = [True, False, False, False, False, False, False, False, False, False, True]
points1 = [(8.5, 5.7),
           (11.2, 8.2),
           (12.5, 4.9)]
points2 = [(10, 4.3),
           (13.7, 2.1),
           (10.6, 2.2)]
points3 = [(2, 6),
           (5.5, 7.7),
           (5.9, 3.3)]
should_include = [True, True, False]



subject_polygon = torch.tensor(subject_polygon).float()
clipping_polygons = [torch.tensor(points1).float(), torch.tensor(points2).float(), torch.tensor(points3).float()]
optim = torch.optim.Adam([subject_polygon], lr = 0.05)

for cp in clipping_polygons:
    cp.requires_grad = True
subject_polygon.requires_grad = True

clip_poly_area = [polygon_area_torch(cp).detach() for cp in clipping_polygons]

# Create a figure and axis
fig, ax = plt.subplots()

# Create the animation
animation = FuncAnimation(fig, update, frames=range(100), fargs=(ax, subject_polygon, clipping_polygons, optim, is_point_fixed, should_include, clip_poly_area), interval=1)

# Show the plot
plt.show()

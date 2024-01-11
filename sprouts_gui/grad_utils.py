import torch
from util import point_to_line_segment_distance, calculate_angle

def polygon_area_torch(polygon_tensor):
    if polygon_tensor.shape[0] == 0:
        return 0.0
    # Add the first point to the end to close the polygon
    polygon_tensor = torch.cat((polygon_tensor, polygon_tensor[0].unsqueeze(0)), dim=0)

    # Calculate the area using the shoelace formula
    area = 0.5 * torch.abs(torch.sum(polygon_tensor[:-1, 0] * polygon_tensor[1:, 1] - polygon_tensor[1:, 0] * polygon_tensor[:-1, 1]))

    return area

def angle_range_loss(polygon, min_angle=30, max_angle=150):
    # Ensure the polygon is a 2D tensor
    assert polygon.dim() == 2 and polygon.size(1) == 2, "Polygon must be a nx2 tensor"
    
    n = polygon.size(0)
    loss = 0.0

    for i in range(n):
        a = polygon[i - 1]  # Previous vertex
        b = polygon[i]      # Current vertex
        c = polygon[(i + 1) % n]  # Next vertex

        # Calculate the interior angle at vertex b
        angle = calculate_angle(a, b, c)

        # If the angle is smaller than the min_angle, add to the loss the exp of the difference
        if angle < min_angle:
            diff = min_angle - angle
            loss += torch.exp(diff*0.05)
        # If the angle is larger than the max_angle, add to the loss
        elif angle > max_angle:
            diff = angle - max_angle
            loss += torch.exp(diff*0.05)

    return loss

def intersection_closeness_loss(polygon, distance_bound = 0.5, epsilon=1e-6):
    loss = 0.0
    n_points = polygon.shape[0]
    
    # Iterate over each point in the polygon
    for i in range(n_points):
        P = polygon[i]
        
        # Iterate over each side of the polygon
        for j in range(n_points):
            # Skip adjacent sides
            if i == j or i == (j + 1) % n_points or (i + 1) % n_points == j:
                continue
            
            A = polygon[j]
            B = polygon[(j + 1) % n_points]
            
            # Calculate the distance from the point to the current side
            distance = point_to_line_segment_distance(P, A, B)
            
            # If the distance is less than the bound, add the penalty to the loss
            if distance < distance_bound:
                # Add a penalty term that increases as the distance decreases
                loss += 1.0 / (distance + epsilon)
    
    return loss

import torch

def ccw(A, B, C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def on_segment(p, q, r):
    """Given three collinear points p, q, and r, check if point q lies on line segment 'pr'"""
    return (q[0] < max(p[0], r[0]) and q[0] > min(p[0], r[0]) and
            q[1] < max(p[1], r[1]) and q[1] > min(p[1], r[1]))

def is_collinear(p, q, r):
    """Check if points p, q, and r are collinear."""
    return (q[1] - p[1]) * (r[0] - q[0]) == (q[0] - p[0]) * (r[1] - q[1])

def intersect(A, B, C, D):
    """Check if line segments AB and CD intersect or overlap."""
    # Check for general intersection
    if (ccw(A, C, D) != ccw(B, C, D)) and (ccw(A, B, C) != ccw(A, B, D)):
        return True

    # Check for collinearity and overlap excluding endpoints
    if is_collinear(A, B, C):
        if on_segment(A, C, B) or on_segment(A, D, B):
            return True
    if is_collinear(A, B, D):
        if on_segment(C, A, D) or on_segment(C, B, D):
            return True

    return False

def test_intersect():
    # Test non-intersecting segments
    assert not intersect((0, 0), (1, 1), (1, 0), (2, 1)), "Test failed: Non-intersecting segments"
    
    # Test intersecting segments
    assert intersect((0, 0), (2, 2), (2, 0), (0, 2)), "Test failed: Intersecting segments"
    
    # Test collinear segments that overlap
    assert intersect((0, 0), (3, 3), (1, 1), (2, 2)), "Test failed: Collinear overlapping segments"
    
    # Test collinear segments that do not overlap
    assert not intersect((0, 0), (1, 1), (2, 2), (3, 3)), "Test failed: Collinear non-overlapping segments"
    
    # Test one segment being a single point
    assert not intersect((0, 0), (0, 0), (1, 1), (2, 2)), "Test failed: One segment is a point"
    
    # Test both segments being a single point
    assert not intersect((0, 0), (0, 0), (0, 0), (0, 0)), "Test failed: Both segments are points"

    # Test endpoint touching
    assert not intersect((0, 0), (1, 1), (1, 1), (2, 2)), "Test failed: Endpoint touching should not be considered intersecting"

    print("All tests passed test_intersect!")

def check_polygon_self_intersection(points : torch.Tensor):
    """Check if a polygon defined by a tensor (n x 2) of points has self-intersection."""
    n = points.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            # Check for intersection between non-adjacent edges
            if abs(i - j) > 1 and not (i == 0 and j == n - 1):
                if intersect(points[i], points[(i + 1) % n], points[j], points[(j + 1) % n]):
                    return True
    return False

def point_to_line_segment_distance(P: torch.Tensor, A : torch.Tensor, B : torch.Tensor):
    # Compute the squared distance from A to B
    AB_squared = torch.sum((B - A) ** 2)
    if AB_squared == 0:
        # A and B are the same point
        return torch.norm(P - A)
    
    # Compute the dot product of vectors AP and AB, 
    # and the normalized "distance" along AB where the perpendicular projection of P falls
    AP = P - A
    AB = B - A
    t = torch.dot(AP, AB) / AB_squared
    
    # If t is between 0 and 1, the projection falls on the segment.
    # Clamp t to the closest endpoint if it falls outside the segment.
    t = torch.clamp(t, 0, 1)
    
    # Find the projection point
    P_prime = A + t * AB
    
    # Compute the distance from P to P_prime
    distance = torch.norm(P - P_prime)
    return distance

def test_point_to_line_segment_distance():
    # Segment and random point whose projection is on the segment
    assert abs(point_to_line_segment_distance(torch.tensor([12.0, 7.0]), torch.tensor([11.0, 3.0]), torch.tensor([15.0, 6.0])) - 2.6) < 1e-6, "Test failed: Point to line segment distance"
    # Same segment and random point whose projection is on the segment but A B are reversed
    assert abs(point_to_line_segment_distance(torch.tensor([12.0, 7.0]), torch.tensor([15.0, 6.0]), torch.tensor([11.0, 3.0])) - 2.6) < 1e-6, "Test failed: Point to line segment distance"
    # Segment and random point whose projection is not on the segment
    assert abs(point_to_line_segment_distance(torch.tensor([7.74, 1.83]), torch.tensor([11.0, 3.0]), torch.tensor([15.0, 6.0])) - 3.4635) < 1e-3, "Test failed: Point projection not on line segment"
    # Same segment and random point whose projection is not on the segment but A B are reversed
    assert abs(point_to_line_segment_distance(torch.tensor([7.74, 1.83]), torch.tensor([15.0, 6.0]), torch.tensor([11.0, 3.0])) - 3.4635) < 1e-3, "Test failed: Point projection not on line segment"
    # Segment and random point that is one of the endpoints
    assert abs(point_to_line_segment_distance(torch.tensor([15.0, -3.0]), torch.tensor([15.0, -3.0]), torch.tensor([-7.32, 1.324])) - 0.0) < 1e-6, "Test failed: Point is one of the endpoints"
    # Point is on the segment
    assert abs(point_to_line_segment_distance(torch.tensor([0, 0]), torch.tensor([-1.0, -1.0]), torch.tensor([1.0, 1.0])) - 0.0) < 1e-6, "Test failed: Point on segment"
    print("All tests passed test_point_to_line_segment_distance!")
    

def calculate_angle(a, b, c):
    # Calculate the vectors ab and bc
    ab = b - a
    bc = b - c
    # Compute the dot product and the magnitudes of ab and bc
    dot_product = torch.sum(ab * bc, dim=-1)
    norm_product = torch.norm(ab, dim=-1) * torch.norm(bc, dim=-1)
    # Use the clamp function to make sure the cosine value is between -1 and 1
    cosine_angle = torch.clamp(dot_product / norm_product, -1.0, 1.0)
    # Compute the angle using the arccos function
    angle = torch.acos(cosine_angle)
    # Convert the angle to degrees
    angle = torch.rad2deg(angle)
    return angle
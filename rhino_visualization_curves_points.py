import clr
clr.AddReference('RhinoCommon')
from Rhino.Geometry import Point3d, Line

def get_element_geometry(doc, element_id):
    """
    Retrieves the geometry of a Revit element as Rhino geometry.
    Returns a list of Rhino geometry objects (e.g., curves, points).
    """
    try:
        element = doc.GetElement(ElementId(element_id))
        
        if not element:
            return []
        
        geometry = []
        
        # Extract location (if applicable)
        if hasattr(element, "Location") and element.Location:
            if hasattr(element.Location, "Curve"):
                curve = element.Location.Curve
                start_point = curve.GetEndPoint(0)
                end_point = curve.GetEndPoint(1)
                line = Line(
                    Point3d(start_point.X, start_point.Y, start_point.Z),
                    Point3d(end_point.X, end_point.Y, end_point.Z)
                )
                geometry.append(line)
            elif hasattr(element.Location, "Point"):
                point = element.Location.Point
                geometry.append(Point3d(point.X, point.Y, point.Z))
        
        return geometry
    
    except Exception as e:
        print(f"Error retrieving geometry for element {element_id}: {e}")
        return []

def assign_geometry_to_layers(geometry, layer_name):
    """
    Assigns Rhino geometry to a specific layer.
    Returns a list of tuples containing geometry and its associated layer name.
    """
    return [(geo, layer_name) for geo in geometry]

def visualize_changes_in_rhino(doc, added_ids, removed_ids, modified_ids):
    """
    Visualizes changes in Rhino by assigning added, removed, and modified elements to layers.
    """
    # Define layer names for visualization
    added_layer = "Added"
    removed_layer = "Removed"
    modified_layer = "Modified"
    
    # Store geometry with layer assignments
    layered_geometry = []
    
    # Process added elements
    for element_id in added_ids:
        geometry = get_element_geometry(doc, element_id)
        layered_geometry.extend(assign_geometry_to_layers(geometry, added_layer))
    
    # Process removed elements
    for element_id in removed_ids:
        geometry = get_element_geometry(doc, element_id)
        layered_geometry.extend(assign_geometry_to_layers(geometry, removed_layer))
    
    # Process modified elements
    for element_id in modified_ids:
        geometry = get_element_geometry(doc, element_id)
        layered_geometry.extend(assign_geometry_to_layers(geometry, modified_layer))
    
    # Output the layered geometry for Grasshopper
    OUT = layered_geometry
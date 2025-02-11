import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import Options, GeometryElement, Solid, Face

clr.AddReference('RhinoCommon')
from Rhino.Geometry import Brep

def get_3d_geometry(doc, element_id):
    """
    Retrieves the 3D geometry of a Revit element as Rhino Breps.
    Returns a list of Rhino Breps.
    """
    try:
        element = doc.GetElement(ElementId(element_id))
        
        if not element:
            return []
        
        # Create geometry options
        geom_options = Options()
        geom_options.ComputeReferences = True
        geom_options.IncludeNonVisibleObjects = False
        
        # Get the geometry of the element
        geom_element = element.get_Geometry(geom_options)
        breps = []
        
        for geom_obj in geom_element:
            # Handle solids
            if isinstance(geom_obj, Solid) and geom_obj.Volume > 0:
                faces = [geom_obj.Faces[i] for i in range(geom_obj.Faces.Size)]
                for face in faces:
                    brep = Brep.TryConvertBrep(face.ToRhino())
                    if brep:
                        breps.append(brep)
            
            # Handle other geometry types (e.g., meshes)
            elif hasattr(geom_obj, "ToRhino"):
                rhino_geom = geom_obj.ToRhino()
                if isinstance(rhino_geom, Brep):
                    breps.append(rhino_geom)
        
        return breps
    
    except Exception as e:
        print(f"Error retrieving 3D geometry for element {element_id}: {e}")
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
    Uses 3D geometry (Breps) for visualization.
    """
    # Define layer names for visualization
    added_layer = "Added"
    removed_layer = "Removed"
    modified_layer = "Modified"
    
    # Store geometry with layer assignments
    layered_geometry = []
    
    # Process added elements
    for element_id in added_ids:
        geometry = get_3d_geometry(doc, element_id)
        layered_geometry.extend(assign_geometry_to_layers(geometry, added_layer))
    
    # Process removed elements
    for element_id in removed_ids:
        geometry = get_3d_geometry(doc, element_id)
        layered_geometry.extend(assign_geometry_to_layers(geometry, removed_layer))
    
    # Process modified elements
    for element_id in modified_ids:
        geometry = get_3d_geometry(doc, element_id)
        layered_geometry.extend(assign_geometry_to_layers(geometry, modified_layer))
    
    # Output the layered geometry for Grasshopper
    OUT = layered_geometry
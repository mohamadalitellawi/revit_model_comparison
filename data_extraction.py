import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    BuiltInCategory,
    ElementId,
    BuiltInParameter
)

import logging

def get_element_data(doc, categories):
    """
    Extracts element data from a Revit document for the specified categories.
    Returns a dictionary where keys are element IDs and values are element properties.
    """
    element_data = {}
    
    for category in categories:
        try:
            elements = FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType()
            
            for element in elements:
                element_id = element.Id.IntegerValue
                
                # Extract common properties
                element_name = element.Name if hasattr(element, "Name") else "Unnamed"
                element_type = element.GetType().Name
                
                # Extract location (if applicable)
                location = None
                if hasattr(element, "Location") and element.Location:
                    if hasattr(element.Location, "Curve"):
                        location = element.Location.Curve.GetEndPoint(0)  # Start point
                    elif hasattr(element.Location, "Point"):
                        location = element.Location.Point
                
                # Extract length (if applicable)
                length = None
                if element.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH):
                    length = element.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH).AsDouble()
                
                # Store element data
                element_data[element_id] = {
                    "Category": category.ToString(),
                    "Name": element_name,
                    "Type": element_type,
                    "Length": length,
                    "Location": location
                }
        
        except Exception as e:
            logging.error(f"Error extracting data for category {category}: {e}")
    
    return element_data
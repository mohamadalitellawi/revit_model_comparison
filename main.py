import clr
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

from logging_config import configure_logging
from data_extraction import get_element_data
from comparison import compare_elements

# Configure logging
configure_logging()

# Get the current Revit documents
doc1 = DocumentManager.Instance.CurrentDBDocument  # First model
doc2 = __doc2__  # Placeholder for second model (you need to pass this)

# Define categories to compare
categories_to_compare = [
    BuiltInCategory.OST_Walls,
    BuiltInCategory.OST_Floors,
    BuiltInCategory.OST_Roofs,
    BuiltInCategory.OST_StructuralColumns,
    BuiltInCategory.OST_StructuralFraming,
    BuiltInCategory.OST_StructuralFoundation
]

try:
    # Extract element data from both models
    logging.info("Extracting data from the first model...")
    elements_doc1 = get_element_data(doc1, categories_to_compare)
    
    logging.info("Extracting data from the second model...")
    elements_doc2 = get_element_data(doc2, categories_to_compare)
    
    # Compare element data
    logging.info("Comparing element data...")
    added, removed, modified = compare_elements(elements_doc1, elements_doc2)
    
    # Prepare outputs for Grasshopper
    added_ids = list(added.keys())
    removed_ids = list(removed.keys())
    modified_ids = list(modified.keys())
    
    # Output results
    OUT = added_ids, removed_ids, modified_ids

except Exception as e:
    logging.error(f"An error occurred during the comparison process: {e}")
    OUT = [], [], []
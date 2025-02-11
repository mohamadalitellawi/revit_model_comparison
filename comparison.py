def compare_elements(elements1, elements2):
    """
    Compares two sets of element data and identifies changes.
    Returns three dictionaries: added, removed, and modified elements.
    """
    added = {id: elements2[id] for id in elements2 if id not in elements1}
    removed = {id: elements1[id] for id in elements1 if id not in elements2}
    modified = {}

    for id in elements1:
        if id in elements2:
            if elements1[id] != elements2[id]:
                modified[id] = {
                    "Old": elements1[id],
                    "New": elements2[id]
                }

    return added, removed, modified
import bpy

# from https://blender.stackexchange.com/questions/146685/how-to-obtain-the-parent-of-a-collection-using-python

def get_parent_collection_names(collection, parent_names):
  for parent_collection in bpy.data.collections:
        if collection.name in parent_collection.children.keys():
            parent_names.append(parent_collection.name)
            get_parent_collection_names(parent_collection, parent_names)
            return


def turn_collection_hierarchy_into_path(obj):
    parent_collection = obj.users_collection[0]
    parent_names      = []
    parent_names.append(parent_collection.name)
    get_parent_collection_names(parent_collection, parent_names)
    parent_names.reverse()
    return '\\'.join(parent_names)

def mark_selected(for_export = True):
    for obj in bpy.context.selected_objects:
        if for_export:
            obj.ExportEnum = 'export_recursive' #Set for export
            obj.exportFolderName = "".join(turn_collection_hierarchy_into_path(obj).split())
        else: 
            obj.ExportEnum = 'auto' #Set not for exporting
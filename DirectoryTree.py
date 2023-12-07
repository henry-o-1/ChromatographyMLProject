import os
import logging
import fnmatch
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)


class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

def buildFileTree(root_path):
    root_node = TreeNode(os.path.basename(root_path))
    if os.path.isdir(root_path):
        # If directory:
        for item in os.listdir(root_path): # iterate through items in directory
            item_path = os.path.join(root_path, item) # get full path of item
            child_node = buildFileTree(item_path) # define child node by recursively calling this function
            # the each child node becomes the root as this is called, and go on
            # if a text file (or non directory) --> child/root node is returned
            root_node.children.append(child_node)
    return root_node

def displayFileTree(node, indent=0):
    print('  ' * indent + node.name)
    for child in node.children:
        displayFileTree(child, indent + 1)




# Example usage:
root_directory = r'C:\Users\odonnh\VSCode\ChromatographyMLProject\Source\Group 10 Spring 19'

file_tree = buildFileTree(root_directory)
displayFileTree(file_tree)
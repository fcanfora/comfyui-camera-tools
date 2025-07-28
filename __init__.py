# In file: comfyui-camera-tools/__init__.py

from .camera_nodes import NODE_CLASS_MAPPINGS as camera_mappings, NODE_DISPLAY_NAME_MAPPINGS as camera_display_mappings
from .nodes_load_3d_advanced import NODE_CLASS_MAPPINGS as load3d_mappings, NODE_DISPLAY_NAME_MAPPINGS as load3d_display_mappings

# This new variable tells ComfyUI where to find your JavaScript files
WEB_DIRECTORY = "js"

# Combine the mappings from all your node files
NODE_CLASS_MAPPINGS = {**camera_mappings, **load3d_mappings}
NODE_DISPLAY_NAME_MAPPINGS = {**camera_display_mappings, **load3d_display_mappings}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

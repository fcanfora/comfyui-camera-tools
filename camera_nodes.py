import json
import os

class LoadCameraFromFile:
    """
    A node that loads camera data (position, target, zoom) from a specified JSON file.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_path": ("STRING", {"default": "D:/camera.json", "multiline": False}),
            }
        }

    RETURN_TYPES = ("CAMERA_INFO",)
    FUNCTION = "load_camera"
    CATEGORY = "3D Camera"

    def load_camera(self, json_path):
        # Default camera data in case the file doesn't load
        camera_info = {
            "position": [0.0, 0.0, -10.0],
            "target": [0.0, 0.0, 0.0],
            "zoom": 1.0
        }

        try:
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    data = json.load(f)
                    # Update camera_info with data from the file, if keys exist
                    camera_info["position"] = data.get("position", camera_info["position"])
                    camera_info["target"] = data.get("target", camera_info["target"])
                    camera_info["zoom"] = data.get("zoom", camera_info["zoom"])
                    print(f"Successfully loaded camera data from {json_path}")
            else:
                print(f"Warning: Camera file not found at {json_path}. Using default values.")
        except Exception as e:
            print(f"Error loading camera file: {e}. Using default values.")

        return (camera_info,)

# --- Node Mappings ---
# At the end of the file, we'll register our nodes.
# We will add the second node here later.
NODE_CLASS_MAPPINGS = {
    "LoadCameraFromFile": LoadCameraFromFile
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadCameraFromFile": "Load Camera From File"
}
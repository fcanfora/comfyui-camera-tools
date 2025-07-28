import nodes
import folder_paths
import os

from comfy.comfy_types import IO
# from comfy_api.input_impl import VideoFromFile # --- DISABLED FOR DEBUGGING ---

from pathlib import Path


def normalize_path(path):
    return path.replace('\\', '/')

class Load3D_Adv():
    @classmethod
    def INPUT_TYPES(s):
        input_dir = os.path.join(folder_paths.get_input_directory(), "3d")

        os.makedirs(input_dir, exist_ok=True)

        input_path = Path(input_dir)
        base_path = Path(folder_paths.get_input_directory())

        files = [
            normalize_path(str(file_path.relative_to(base_path)))
            for file_path in input_path.rglob("*")
            if file_path.suffix.lower() in {'.gltf', '.glb', '.obj', '.fbx', '.stl'}
        ]

        return {"required": {
            "model_file": (sorted(files), {"file_upload": True}),
            # --- Widget type is now LOAD_3D ---
            "image": ("LOAD_3D", {}),
            "width": ("INT", {"default": 1024, "min": 1, "max": 4096, "step": 1}),
            "height": ("INT", {"default": 1024, "min": 1, "max": 4096, "step": 1}),
        }}

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "IMAGE", "IMAGE", "LOAD3D_CAMERA", IO.VIDEO)
    RETURN_NAMES = ("image", "mask", "mesh_path", "normal", "lineart", "camera_info", "recording_video")

    FUNCTION = "process"
    EXPERIMENTAL = True

    CATEGORY = "3d"

    def process(self, model_file, image, **kwargs):
        # The 'image' input is now a dictionary from our JS widget
        # For now, we are just passing through placeholder data
        # In the future, the JS widget will generate real images and send their paths
        image_path = folder_paths.get_annotated_filepath(image['image'])
        mask_path = folder_paths.get_annotated_filepath(image['mask'])
        normal_path = folder_paths.get_annotated_filepath(image['normal'])
        lineart_path = folder_paths.get_annotated_filepath(image['lineart'])

        load_image_node = nodes.LoadImage()
        # This will fail until the JS widget saves real images, but the node will load
        try:
            output_image, ignore_mask = load_image_node.load_image(image=image_path)
            ignore_image, output_mask = load_image_node.load_image(image=mask_path)
            normal_image, ignore_mask2 = load_image_node.load_image(image=normal_path)
            lineart_image, ignore_mask3 = load_image_node.load_image(image=lineart_path)
        except Exception as e:
            print(f"Could not load placeholder images: {e}")
            # Return None for all image types if they fail to load
            return (None, None, model_file, None, None, image['camera_info'], None)


        video = None
        # if image['recording'] != "":
        #     recording_video_path = folder_paths.get_annotated_filepath(image['recording'])
        #     video = VideoFromFile(recording_video_path)

        return output_image, output_mask, model_file, normal_image, lineart_image, image['camera_info'], video


class Load3DAnimation_Adv():
    @classmethod
    def INPUT_TYPES(s):
        input_dir = os.path.join(folder_paths.get_input_directory(), "3d")

        os.makedirs(input_dir, exist_ok=True)

        input_path = Path(input_dir)
        base_path = Path(folder_paths.get_input_directory())

        files = [
            normalize_path(str(file_path.relative_to(base_path)))
            for file_path in input_path.rglob("*")
            if file_path.suffix.lower() in {'.gltf', '.glb', '.fbx'}
        ]

        return {"required": {
            "model_file": (sorted(files), {"file_upload": True}),
            # --- Widget type is now LOAD_3D_ANIMATION ---
            "image": ("LOAD_3D_ANIMATION", {}),
            "width": ("INT", {"default": 1024, "min": 1, "max": 4096, "step": 1}),
            "height": ("INT", {"default": 1024, "min": 1, "max": 4096, "step": 1}),
        }}

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "IMAGE", "LOAD3D_CAMERA", IO.VIDEO)
    RETURN_NAMES = ("image", "mask", "mesh_path", "normal", "camera_info", "recording_video")

    FUNCTION = "process"
    EXPERIMENTAL = True

    CATEGORY = "3d"

    def process(self, model_file, image, **kwargs):
        image_path = folder_paths.get_annotated_filepath(image['image'])
        mask_path = folder_paths.get_annotated_filepath(image['mask'])
        normal_path = folder_paths.get_annotated_filepath(image['normal'])

        load_image_node = nodes.LoadImage()
        try:
            output_image, ignore_mask = load_image_node.load_image(image=image_path)
            ignore_image, output_mask = load_image_node.load_image(image=mask_path)
            normal_image, ignore_mask2 = load_image_node.load_image(image=normal_path)
        except Exception as e:
            print(f"Could not load placeholder images: {e}")
            return (None, None, model_file, None, image['camera_info'], None)

        video = None
        # if image['recording'] != "":
        #     recording_video_path = folder_paths.get_annotated_filepath(image['recording'])
        #     video = VideoFromFile(recording_video_path)

        return output_image, output_mask, model_file, normal_image, image['camera_info'], video


class Preview3D_Adv():
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "model_file": ("STRING", {"default": "", "multiline": False}),
        },
        "optional": {
            "camera_info": ("LOAD3D_CAMERA", {})
        }}

    OUTPUT_NODE = True
    RETURN_TYPES = ()

    CATEGORY = "3d"

    FUNCTION = "process"
    EXPERIMENTAL = True

    def process(self, model_file, **kwargs):
        camera_info = kwargs.get("camera_info", None)

        return {
            "ui": {
                "result": [model_file, camera_info]
            }
        }

class Preview3D_AdvAnimation_Adv():
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "model_file": ("STRING", {"default": "", "multiline": False}),
        },
        "optional": {
            "camera_info": ("LOAD3D_CAMERA", {})
        }}

    OUTPUT_NODE = True
    RETURN_TYPES = ()

    CATEGORY = "3d"

    FUNCTION = "process"
    EXPERIMENTAL = True

    def process(self, model_file, **kwargs):
        camera_info = kwargs.get("camera_info", None)

        return {
            "ui": {
                "result": [model_file, camera_info]
            }
        }

# Corrected Node Registration Block
NODE_CLASS_MAPPINGS = {
    "Load3D_Adv": Load3D_Adv,
    "Load3DAnimation_Adv": Load3DAnimation_Adv,
    "Preview3D_Adv": Preview3D_Adv,
    "Preview3D_AdvAnimation_Adv": Preview3D_AdvAnimation_Adv
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Load3D_Adv": "Load 3D",
    "Load3DAnimation_Adv": "Load 3D - Animation",
    "Preview3D_Adv": "Preview 3D",
    "Preview3D_AdvAnimation_Adv": "Preview 3D - Animation"
}

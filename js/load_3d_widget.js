import { app } from "/scripts/app.js";

// Adds a 3D viewer widget to a node
function get3DViewer(node, name) {
    const widget = {
        type: name, // The type of the widget
        name: name,
        size: [128, 128], // The size of the widget
        draw: function (ctx, _, widget, y, w) {
            // Draw a placeholder rectangle
            ctx.fillStyle = "#222";
            ctx.fillRect(0, y, w, this.size[1]);
            ctx.fillStyle = "#888";
            ctx.font = "12px Arial";
            ctx.textAlign = "center";
            ctx.fillText("3D Viewer Placeholder", w / 2, y + this.size[1] / 2);
        },
        computeSize: function(width) {
            return [width, 128]; // Calculate the size of the widget
        },
        value: {
            // Default values that the widget will send to the backend
            image: "default_image.png",
            mask: "default_mask.png",
            normal: "default_normal.png",
            lineart: "default_lineart.png",
            recording: "",
            camera_info: {
                position: [0, 0, -10],
                target: [0, 0, 0],
                zoom: 1.0,
            },
        }
    };
    node.addCustomWidget(widget);
    return widget;
}

// Register the custom node with ComfyUI
app.registerExtension({
    name: "Comfy.3D.Load3DWidget",
    nodeCreated(node) {
        // Check if the node is one of our custom 3D nodes
        if (node.comfyClass === "Load3D_Adv") {
            // Find the widget by its name (as defined in the Python code)
            const imageWidget = node.widgets.find((w) => w.name === "image");
            if (imageWidget) {
                // Replace the temporary string widget with our new 3D viewer
                imageWidget.type = "LOAD_3D";
                // We will add the three.js viewer logic here later
            }
        }
        if (node.comfyClass === "Load3DAnimation_Adv") {
            const imageWidget = node.widgets.find((w) => w.name === "image");
            if (imageWidget) {
                imageWidget.type = "LOAD_3D_ANIMATION";
                // We will add the three.js viewer logic here later
            }
        }
    },
});

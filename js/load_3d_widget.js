import { app } from "/scripts/app.js";

// Dynamically import three.js and necessary loaders from a CDN
async function loadThreeJS() {
    if (window.THREE) return window.THREE;

    const THREE = await import("https://cdn.jsdelivr.net/npm/three@0.126.0/build/three.module.js");
    const { OrbitControls } = await import("https://cdn.jsdelivr.net/npm/three@0.126.0/examples/jsm/controls/OrbitControls.js");
    const { GLTFLoader } = await import("https://cdn.jsdelivr.net/npm/three@0.126.0/examples/jsm/loaders/GLTFLoader.js");
    const { OBJLoader } = await import("https://cdn.jsdelivr.net/npm/three@0.126.0/examples/jsm/loaders/OBJLoader.js");
    const { FBXLoader } = await import("https://cdn.jsdelivr.net/npm/three@0.126.0/examples/jsm/loaders/FBXLoader.js");
    const { STLLoader } = await import("https://cdn.jsdelivr.net/npm/three@0.126.0/examples/jsm/loaders/STLLoader.js");

    THREE.OrbitControls = OrbitControls;
    THREE.GLTFLoader = GLTFLoader;
    THREE.OBJLoader = OBJLoader;
    THREE.FBXLoader = FBXLoader;
    THREE.STLLoader = STLLoader;
    
    window.THREE = THREE;
    return THREE;
}


// The main extension logic
app.registerExtension({
    name: "Comfy.3D.Load3DWidget",
    async nodeCreated(node) {
        if (node.comfyClass === "Load3D_Adv" || node.comfyClass === "Load3DAnimation_Adv") {
            
            const THREE = await loadThreeJS();
            if (!THREE) {
                console.error("Three.js failed to load.");
                return;
            }

            // Find the widget that we will replace with our 3D viewer
            const widget = node.widgets.find((w) => w.name === "image");
            if (!widget) return;

            // --- Basic Scene Setup ---
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x2a2a2a);
            const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setPixelRatio(window.devicePixelRatio);
            
            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            camera.position.z = 5;

            // Add some lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
            scene.add(ambientLight);
            const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
            directionalLight.position.set(1, 1, 1);
            scene.add(directionalLight);

            // Add a grid helper
            const gridHelper = new THREE.GridHelper(10, 10);
            scene.add(gridHelper);

            let currentModel = null;

            // --- Model Loading Logic ---
            const loadModel = (path) => {
                if (currentModel) {
                    scene.remove(currentModel);
                }
                if (!path) return;

                const fullPath = `/view?filename=${encodeURIComponent(path)}&type=input&subfolder=3d`;
                const extension = path.split('.').pop().toLowerCase();
                let loader;

                if (extension === 'gltf' || extension === 'glb') {
                    loader = new THREE.GLTFLoader();
                } else if (extension === 'obj') {
                    loader = new THREE.OBJLoader();
                } else if (extension === 'fbx') {
                    loader = new THREE.FBXLoader();
                } else if (extension === 'stl') {
                    loader = new THREE.STLLoader();
                } else {
                    console.error("Unsupported model format:", extension);
                    return;
                }

                loader.load(fullPath, (model) => {
                    currentModel = extension === 'gltf' || extension === 'glb' ? model.scene : model;
                    scene.add(currentModel);
                }, undefined, (error) => {
                    console.error("An error happened while loading the model:", error);
                });
            };

            // --- Animation Loop ---
            function animate() {
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
            }
            animate();

            // --- Hijack the original widget ---
            const originalDraw = widget.draw;
            widget.draw = function(ctx, node, w, y) {
                // originalDraw?.apply(this, arguments); // We don't need the original draw anymore
                const [width, height] = this.size;
                renderer.setSize(width, height);
                camera.aspect = width / height;
                camera.updateProjectionMatrix();

                // Append the renderer's canvas to the document if it's not already there
                if (!renderer.domElement.parentNode) {
                    document.body.appendChild(renderer.domElement);
                    renderer.domElement.style.position = 'absolute';
                    renderer.domElement.style.zIndex = '99'; // Ensure it's on top
                }

                // Position the canvas over the widget area
                const graphCanvas = app.graph.list_of_graphcanvas[0];
                const transform = new DOMMatrix(graphCanvas.canvas.style.transform);
                const nodePos = node.pos;
                const widgetY = this.last_y;
                
                const canvasRect = graphCanvas.canvas.getBoundingClientRect();

                renderer.domElement.style.left = `${canvasRect.left + (nodePos[0] + 15) * transform.a}px`;
                renderer.domElement.style.top = `${canvasRect.top + (nodePos[1] + widgetY) * transform.d}px`;
            };

            // --- Watch for model changes ---
            const modelWidget = node.widgets.find((w) => w.name === "model_file");
            if (modelWidget) {
                const originalCallback = modelWidget.callback;
                modelWidget.callback = function(value) {
                    loadModel(value);
                    if (originalCallback) {
                        return originalCallback.apply(this, arguments);
                    }
                };
                // Load initial model
                loadModel(modelWidget.value);
            }
            
            node.onRemoved = function() {
                // Cleanup when the node is removed
                if (renderer.domElement.parentNode) {
                    renderer.domElement.parentNode.removeChild(renderer.domElement);
                }
            };
        }
    },
});

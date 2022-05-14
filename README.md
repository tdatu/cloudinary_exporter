# cloudinary_exporter
A simple Blender add-on to directly push 3D scene to Cloudinary Programmable Media


## Requirements
- Mac system, (Windows should works too - let me know if there's issue).
- Blender 3+ 
- This Add-on
- [Cloudinary Programmable Media](https://cloudinary.com/products/programmable_media) Account (free)

![Cloudinary Exporter](https://github.com/tdatu/cloudinary_exporter/blob/main/media/demo.mp4?raw=true)

## Steps  
1. Clone this repo: `git clone https://github.com/tdatu/cloudinary_exporter.git .`
2. In Blender, install the Add-on: Blender preferences > Add-ons, press Install button then locate cloudinary_settings.py
3. In 3D Model View, press n key to bring the Cloudinary Panel. 
4. Fill the fields with your Cloud Name, API Key, Upload Preset, Public ID, and Tag (optional) 


__Notes:__  
* It only supports exporting glTF format. For more info about this format, go to: https://www.khronos.org/api/index_2017/gltf
* Public ID only supports alphabet, integers, hypen, and underscore. 


## TODO: 
1. Support forward slash character in the Public ID field.  
2. Persist config, reload config.  


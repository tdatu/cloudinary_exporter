# cloudinary_exporter
A simple Blender add-on to directly push 3D scene to Cloudinary Programmable Media


## Requirements
- Mac system, (Windows should works too - let me know if there's issue).
- Blender 3+ 
- This Add-on
- [Cloudinary Programmable Media](https://cloudinary.com/products/programmable_media) Account (free)

![Cloudinary Exporter](https://res.cloudinary.com/tdatupersonal/image/upload/v1652572300/blender/screenshot_mmcnpd.png)

https://user-images.githubusercontent.com/1905383/168451855-9c01b763-8cb9-4241-9afe-ca039b116ecc.mp4

https://codesandbox.io/s/stoic-driscoll-m6lvgi

## Steps  
1. Clone this repo: `git clone https://github.com/tdatu/cloudinary_exporter.git .`
2. In Blender, install the Add-on: Blender preferences > Add-ons, press Install button then locate cloudinary_settings.py
3. In 3D Model View, press n key to bring the Cloudinary Panel. 
4. Fill the fields with your Cloud Name, API Key, Upload Preset, Public ID, and Tag (optional) 


__Notes:__  
* ~~It only supports exporting glTF format.~~ It now supports GLTZ and USDZ formats. For more info about this format, go to: https://www.khronos.org/api/index_2017/gltf
* Public ID only supports alphabet, integers, hypen, and underscore.
* If the Cloudinary Panel **does not appear**, create the Cloudinary3D folder in ~/Documents


## New Features
1. Load previous config.  Useful especially when closing Blender so no
   need to type all of the needed environment variables. 
2. In addition to default GLTZ, USDZ 3D file format is now added. 
3. Allow blank Public ID field and it will generate a random
  12 alpha-numeric characters. 


## TODO: 
1. Support forward slash character in the Public ID field.  
2. ~~Persist config, reload config.~~  




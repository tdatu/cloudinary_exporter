import bpy
import os
import requests
import shutil
import configparser

bl_info = {
    "name": "Cloudinary Uploader",
    "description": "A Simple direct exporter to Cloudinary",
    "blender": (3, 0, 0),
    "category": "Import-Export",
    "author": "Anthony Datu",
    "doc_url":
    "https://github.com/tdatu/cloudinary_exporter/blob/main/README.md",
    "support": "COMMUNITY"
}


class CloudinaryProperty(bpy.types.PropertyGroup):
    cloud_name: bpy.props.StringProperty(
        name="Cloud Name",
        description=
        "Cloud Name is the last value after the @ in the environment variable",
        maxlen=40)
    api_key: bpy.props.StringProperty(
        name="API Key",
        description="Get API Key from Cloudinary Dashboard",
        maxlen=15)
    upload_preset: bpy.props.StringProperty(
        name="Upload Preset",
        description="Upload Preset defined in Cloudinary Settings",
        maxlen=25)
    public_id: bpy.props.StringProperty(
        name="Public ID",
        description=
        "Public ID is the media asset identifier name in Cloudinary",
        maxlen=60)
    tags: bpy.props.StringProperty(name="Tags", maxlen=60)


class CLOUDINARY_PT_main_panel(bpy.types.Panel):
    bl_label = "Cloudinary Settings"
    bl_idname = "CLOUDINARY_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Cloudinary"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        cld_prop = scene.cld_prop

        #load existing config
        config = self.load_config(context)

        #cld_prop.api_key = config["CLOUDINARY"]["API_KEY"]
        #cld_prop.cloud_name = config["CLOUDINARY"]["CLOUD_NAME"]
        #cld_prop.upload_preset = config["CLOUDINARY"]["UPLOAD_PRESET"]

        #create fields to panel
        layout.prop(cld_prop, "cloud_name")
        layout.prop(cld_prop, "api_key")
        layout.prop(cld_prop, "upload_preset")
        layout.prop(cld_prop, "public_id")
        layout.prop(cld_prop, "tags")

        layout.operator("cloudinary.oper")

    def load_config(self, context):

        root = os.getcwd()
        home_dir = os.path.expanduser('~')
        dest = home_dir + os.sep + "Documents" + os.sep + "Cloudinary3D"

        os.chdir(dest)
        config = configparser.ConfigParser()
        config.read(".ini")

        #self.report({"INFO"}, "API KEY: {}".format(config["CLOUDINARY"]["API_KEY"]))

        os.chdir(root)

        return config


class CLOUDINARY_OT_operator(bpy.types.Operator):

    bl_label = "Upload"
    bl_idname = "cloudinary.oper"

    def save_config(self, dest, cld_prop):

        #Go to directory
        root = os.getcwd()
        os.chdir(dest)
        os.chdir("..")

        #if os.path.exists(".ini") == False:

        config = configparser.ConfigParser()
        config["CLOUDINARY"] = {}
        config["CLOUDINARY"]["API_KEY"] = str(cld_prop.api_key)
        config["CLOUDINARY"]["CLOUD_NAME"] = str(cld_prop.cloud_name)
        config["CLOUDINARY"]["UPLOAD_PRESET"] = str(cld_prop.upload_preset)

        with open(".ini", "w") as configfile:
            config.write(configfile)

        #Go back to original directory
        os.chdir(root)

    def upload(self, dest, cld_prop):

        api_url = "https://api.cloudinary.com/v1_1/{}/image/upload".format(
            cld_prop.cloud_name)

        #Go to directory
        root = os.getcwd()
        os.chdir(dest)
        os.chdir("..")

        zipfile = "{}.zip".format(cld_prop.public_id)

        payload = {}
        files = [('file', ('file', open(zipfile,
                                        'rb'), 'application/octet-stream'))]
        payload["upload_preset"] = cld_prop.upload_preset
        payload["public_id"] = cld_prop.public_id
        payload["api_key"] = cld_prop.api_key
        payload["tags"] = cld_prop.tags

        #Send the file
        sess = requests.Session()
        sess.headers.update({"User-Agent": "Blender-python/0.1.0"})
        res = sess.post(api_url, data=payload, files=files)

        #output return
        if res.status_code == 200:
            self.report({"INFO"}, res.text)
        else:
            self.report({"ERROR"}, res.text)

        #Go back to original directory
        os.chdir(root)

    def zip_dir(self, dest, public_id):

        #Go to Cloudinary3D path
        root = os.getcwd()
        os.chdir(dest)
        os.chdir("..")
        shutil.make_archive(public_id, "zip", public_id)

        os.chdir(root)

        #self.report({"INFO"}, "This is zip_dir method")
        #self.report({"INFO"}, "Current Directory: {}".format(os.getcwd()))

    def execute(self, context):
        scene = context.scene
        cld_prop = scene.cld_prop

        cloud_name = cld_prop.cloud_name
        upload_preset = cld_prop.upload_preset
        public_id = cld_prop.public_id

        self.report({"INFO"}, "cloud name: {}".format(cloud_name))
        self.report({"INFO"}, "upload preset: {}".format(upload_preset))
        self.report({"INFO"}, "public id: {}".format(public_id))

        check = 0

        if len(cloud_name) > 2:
            check += 1

        if len(upload_preset) > 2:
            check += 1

        if len(public_id) > 2:
            check += 1

        self.report({"INFO"}, "check value: {}".format(check))

        #export the scene
        if check == 3:
            home_dir = os.path.expanduser('~')
            dest = home_dir + os.sep + "Documents" + os.sep + "Cloudinary3D" + os.sep + "{}".format(
                public_id)
            export_file = dest + os.sep + "{}".format(public_id)

            if os.path.exists(dest) == False:
                #create the destination folder
                os.makedirs(dest)

            bpy.ops.export_scene.gltf("EXEC_DEFAULT",
                                      filepath=export_file,
                                      export_format="GLTF_SEPARATE")

            #zip directory
            self.zip_dir(dest, public_id)

            #upload file
            self.upload(dest, cld_prop)

            #make config persistent
            self.save_config(dest, cld_prop)

        return {"FINISHED"}


classes = [
    CloudinaryProperty, CLOUDINARY_PT_main_panel, CLOUDINARY_OT_operator
]


def setup_storage_dir():
    curdir = os.getcwd()
    storage_dir = os.path.expanduser(
        "~") + os.sep + "Documents" + os.sep + "Cloudinary3D"
    try:
        os.makedirs(storage_dir)
        result = True
    except FileExistsError:
        result = False

    return result


def register():
    result = setup_storage_dir()
    if result:
        print("storage setup is successful.")
    else:
        print("storage setup is unsuccessful.")

    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.cld_prop = bpy.props.PointerProperty(
            type=CloudinaryProperty)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.cld_prop


if __name__ == "__main__":
    register()

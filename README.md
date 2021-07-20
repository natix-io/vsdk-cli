**vsdkx-cli** is a cli tool to facilitate the usage of **vsdkx**. you can
add/remove any *vsdkx addons* or *vsdkx models* to your project.

###How to install
To install this client you can easily use *pip*.
```
pip install git+https://gitlab+deploy-token-485942:VJtus51fGR59sMGhxHUF@gitlab.com/natix/cvison/vsdkx/vsdkx-core.git
pip install git+https://gitlab+deploy-token-488366:iCjAsvbmVEMd_xeayAh-@gitlab.com/natix/cvison/vsdkx/vsdkx-cli
```
After this you can use **vsdkx-cli** which is installed in the *PATH*

###How to use
To install *vsdkx models* you can use easily go to your project and run 
```
vsdkx-cli model add {model_name} {weight_name}
#or to remove any model you can use remove instead of add
``` 
currently these models and weights are available

|Model|Weights|
|---|---|
|yolo-torch|default.pt, best.pt|
|yolo-tflite|default.pt, best.pt|
|yolo-facemask|default.pt, best.pt|
|bayesian|default.pt, best.pt|
|resnet|default.pt, best.pt|
|mobilenet|default.pt, best.pt|
To add any addon to your project you can use:
```
vsdkx-cli addon add {addon_name}
#or to remove any addon you can use remove instead of add
```
currently these addons are available:
* zoning
* distant
* tracking

To set new configuration for the repo that vsdk-cli is searching for the models
and addons you can use:
```
vsdkx-cli repo
```
**Notice:** *You should run all the vsdkx-cli command inside your project 
directory*

To clean all the things you have done with this cli just do this:
```
vsdkx-cli clean
```

---
After everything is installed inside your project now you should have these 
directories inside your project
```
|-- project
|   |-- vsdkx
|       |-- model
|           |-- profile.yaml
|       |-- weight
|           |-- weight files according to your models
```
the `profile.yaml` contains information about the model and which model uses 
which weight file. you can either manually change that file or you can use:
```
vsdkx-cli set {model_name} {weight_name}
```

Now for final step you only need to config the app with this:
```
vsdkx-cli app init
```
This will create `settings.yaml` file and `vsdkx-run.py` inside your project 
and in the vsdkx folder according the models and addons you added before. you 
can also change the addons and models with previous commands but if you want 
to update `settings.yaml` with new models and addons you can reconfigure the 
app with:
```
vsdkx-cli app config
```

now to use the `vsdkx-run.py` you can run `python vsdkx-run.py -h` to see 
the usage

You can also configure the drawing properties for debug mode by useing:
```
vsdkx-cli app draw
```

You can see the list of models and addons in you project by using:
```
vsdkx-cli app list
```

### Hidden Files
This cli will create two hidden files `.secret` which has the credential 
information for the registry that we are using to download wieght files 
and other data, and `.config` file which stores the list of `addons` and 
`model-drivers` for this project.

### Profile
`profile.yaml` is a file inside `visionx/model` and we can configure the model 
that we are going to use with its attributes. it should have 
following structure.
```yaml
profile-name:
# All the required parameter for that specific model
  classes_len: 
  input_shape:
  model_path: # path to weight file
  ...
    
```
We can have multiple profiles and we can pass `profile-name` to the driver to 
use that specific values.

### Settings
`settings.yaml` is a file inside `visionx` directory and has 
following structure.
```yaml
addons:
    addon-name:
      class:  # the class of the addon, each addon has a specific class, it will be added automatically if you use cli to add addons to your project
      ... # other properties required by that addon like distance_threshold, max_disappeared, etc that we need to use for tracking addon
model:
    class: # this is the class of the model driver we want to use for this project, it will be added automatically if you use cli to add model-driver to your project
    debug: # If this value is true it will show debug window with some simple drawings, like zonings, bboxes and etc.
    profile: # the name of the profile we want to use for our model driver
    settings:
      ... # all other dynamic settings the we can pass to our model driver
drawing: # this is optional if we want to have debug window with minimal drawing feature, this dictionary will also be passed to addons and model-drivers so if developers need to debug something there they can set drawing configs here.
  box_font_scale: 0.8
  box_thickness: 3
  group_color: !!python/tuple
  - 135
  - 206
  - 235
  rectangle_color: !!python/tuple
  - 60
  - 179
  - 113
  text_color: !!python/tuple
  - 255
  - 255
  - 255
  text_fontscale: 1
  text_thickness: 1
  zone_thickness: 3
  zones:
  - - - 538
      - 226
    - - 837
      - 213
    - - 877
      - 656
    - - 589
      - 674
    - - 538
      - 226
  zones_color: !!python/tuple
  - 153
  - 50
  - 204

# we can pass this yaml file through gRPC to our project or via command line
```

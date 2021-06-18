**vsdkx-cli** is a cli tool to facilitate the usage of **vsdkx**. you can
add/remove any *vsdkx addons* or *vsdkx models* to your project.

###How to install
To install this client you can easily use *pip*.
```
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
|yolo-bayesian|default.pt, best.pt|
|yolo-resnet|default.pt, best.pt|
|yolo-mobilenet|default.pt, best.pt|
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
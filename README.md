# Unfolder [Blender addon]

This addon helps to unfold / unwrap meshes. Could be useful for laser cutter model preprocessing.

## Installation

`Warning!` This addon heavily uses [Shapely](https://pypi.org/project/Shapely/). You have to install Shapely before useing this addon.

```
pip3 install --user shapely
```

Addon installation:
- download [addon](unfolder.zip)
- install addon from file in Blender - follow this [manual](https://docs.blender.org/manual/en/latest/preferences/addons.html)
![installation](https://github.com/demeter-macik/blender-unfolder/blob/develop/docs/images/unfolder-install.gif)

## Usage

- select mesh and press `Test` button to check if this mesh has not flat faces (faces that has more then 3 vertices):
![testing mesh](https://github.com/demeter-macik/blender-unfolder/blob/develop/docs/images/test-mesh.gif)

- press `Unfold` to break mesh by faces into separate mashes and align them to the XY plane:
![unfold](https://github.com/demeter-macik/blender-unfolder/blob/develop/docs/images/unfold-all.gif)

- unfold only selected faces:
![unfold selected](https://github.com/demeter-macik/blender-unfolder/blob/develop/docs/images/unfold-selected.gif)

- it will fail if you're trying to unfold not flat faces ( these faces will be shown as selected in edit mode). Yuo should selected flat faces only and try again:
![unfold not flat](https://github.com/demeter-macik/blender-unfolder/blob/develop/docs/images/unfold-selected-1.gif)

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

## Usage

- select mesh and press `Test` button to check if this mesh has not flat faces (faces that has more then 3 vertices)

- change options if you need

- press `Unfold` to break mesh by faces into separate mashes and align them to the XY plane

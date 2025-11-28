# GMF2 Tools

> [!NOTE]  
> See [here](https://sevonj.github.io/ghm_docs/formats/) for documentation on how data is stored in the game files.

Uses code from https://github.com/sevonj/nmh_reverse

A [Blender](https://www.blender.org) extension that allows Blender to import GMF2 files.

## Requirements
- Blender version 4.5.3 or higher

## Installation
- Download the extension version you want from the Releases tab on the right (don't unzip!)
- Open the Extensions tab in Blender (Edit > Preferences > Get Extensions)
- Click the small arrow in the top right of the tab
- Click 'Install from Disk'
- Select the .zip file
- The extension is installed!

## Supported Games
Games that are currently supported by the extension are:
- No More Heroes
- No More Heroes 2: Desperate Struggle

Other games that use the GMF2 model format might have support added in the future.

## Known Issues
- Addon fails when attemping to import a model with an armature if another model with an armature was imported previously
- ~~Addon crashes when importing textures without models~~ (fixed in upcoming release)
- Vertex groups are very inaccurate
- Models with a 0x96 code will not have any vertices (e.x NMH1 sunglasses)
- Textures compressed using RGB5A3 or RGBA32 will never import
- Models with extremely large positional values will fail to import
- Certain models (usually stages/maps) appear with an invalid positional offset
- Some models will fail to import due to the addon reading an incorrect number of tristrips
- Normals are reversed in certain models (e.x. Parts of NMH1 Travis's hair)

If you have noticed an error that is not on this list, please report it!

## Feature Checklist
- ~~Vertices~~
- ~~Indices~~
- ~~Object Hierarchy~~
- ~~Object Origins~~
- ~~Object Rotations~~
- ~~UVs~~
- ~~Normals~~
- ~~Armature~~
- ~~Materials~~
- ~~Textures~~
- Weight Data
- Animations
- Blood+ support

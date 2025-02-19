# GMF2 Tools

> [!NOTE]  
> See [here](https://sevonj.github.io/ghm_docs/formats/) for documentation on how data is stored in the game files.

Uses code from https://github.com/sevonj/nmh_reverse

A [Blender](https://www.blender.org) extension that allows Blender to import GMF2 files.

## Requirements
- Blender version 4.2 or higher

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
- Normals will occasionally fail to import on map models
- ~~Objects from NMH2 will not import armature positions correctly~~ (Fixed in upcoming release)
- ~~Meshes parented to armature bones don't appear in the correct position~~ (Fixed in upcoming release)
- Some objects import with a slightly incorrect position (e.x. the Tsubaki MKIII)
- Some models will fail to import due to the program reading an incorrect number of tristrips
- Models have a different order in the hierarchy than they should
- Unknown error causing some models to not import (e.x. the Jacob's Ladder)
- Some map models have an unknown position/rotation error
- Some normals are reversed in certain models (e.x. Parts of NMH1 Travis's hair)

## Feature Checklist
- ~~Vertices~~
- ~~Indices~~
- ~~Object Hierarchy~~
- ~~Object Origins~~
- ~~Object Rotations~~
- ~~UVs~~
- ~~Normals~~
- Armature
- Weight Data
- Materials
- Textures
- Animations
- Blood+ support

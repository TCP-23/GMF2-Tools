# GMF2 Tools

> [!NOTE]  
> See [here](https://sevonj.github.io/ghm_docs/formats/) for documentation on how data is stored in the game files.

Uses code from https://github.com/sevonj/nmh_reverse

A [Blender](https://www.blender.org) extension that allows Blender to import GMF2 files.

## UV Mirroring

As of 0.4.1, UVs currently need to be manually mirrored for them to look right.
I'm working on automating this process, but for now use this method:

- Open the UVs of your object in a UV editor window
- Open the texture that the object uses in the UV editor window as well
- Set your Blender cursor to the center of the texture (Default shortcut: Shift + C)
- Change your Rotation/Scale pivot mode to use the Blender Cursor
- Select all the UVs of your object while tabbed into the UV editor window (Default shortcut: A)
- Scale the UVs by -1 on the Y axis (S > Y > -1)
- Your UVs should now be mirrored properly

## Requirements:
- Blender version 4.2 or higher

## Installation:
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

## Feature Checklist:
- ~~Vertices~~
- ~~Indices~~
- ~~Object Hierarchy~~
- ~~Object Origins~~
- ~~Object Rotations~~
- ~~UVs~~
- Armature
- Materials
- Normals
- Textures

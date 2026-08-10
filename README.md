# GMF2 Tools

> [!NOTE]  
> See [here](https://sevonj.github.io/ghm_docs/formats/) for documentation on how data is stored in the game files.

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

Games that are only supported experimentally are:
- No More Heroes 2: Desperate Struggle
- BLOOD+: One Night Kiss

Other games that use the GMF2 model format might have support added in the future.

## Known Issues
- Addon fails when attemping to import a model with an armature if another model with an armature was imported previously
- Vertex groups are very inaccurate
- Models with a 0x96 code will not have any vertices (e.x NMH1 sunglasses)
- Models with extremely large positional values will fail to import
- Normals are reversed in certain models (e.x. Parts of NMH1 Travis's hair)

If you have noticed an error that is not on this list, please report it!

## Credits
Thanks to [sevonj](https://github.com/sevonj) for the basis of the GMF2 parser

Thanks to TravisTchDown (fdgsz) for providing the basis of the BLOOD+ GMF2 parser

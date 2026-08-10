from dataclasses import dataclass

from .gmf2b import Gmf2b

@dataclass
class BloodVertexGroupInfo:
    data_object = Gmf2b.WorldObject.Surface.SkinningData
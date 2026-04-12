from dataclasses import dataclass

from .flcg import Flcg

def create_minfo_from_wobjects(wobjs: Flcg.WObject):
    info_list = []

    return info_list

@dataclass
class CollisionModelObjectInfo:
    data_object: Flcg.WObject

    name: str

    parent: CollisionModelObjectInfo
    first_child: CollisionModelObjectInfo
    prev: CollisionModelObjectInfo
    next: CollisionModelObjectInfo

    has_children = parent is not None

from dataclasses import dataclass

from .gmf2b import Gmf2b

@dataclass
class BloodModelObjectInfo:
    data_object: Gmf2b.WorldObject

    name: str

    parent: 'BloodModelObjectInfo'
    first_child: 'BloodModelObjectInfo'
    prev: 'BloodModelObjectInfo'
    next: 'BloodModelObjectInfo'

    @property
    def is_child(self):
        """Does the object have a parent?"""
        return self.parent is not None
    
    @property
    def has_children(self):
        """Does the object have any children?"""
        return self.first_child is not None
    

def create_minfo_from_wobjects(wobjs: list[Gmf2b.WorldObject]):
    info_dict: dict[int, BloodModelObjectInfo] = {}

    for wobj in wobjs:
        new_minfo = BloodModelObjectInfo(wobj, wobj.name, None, None, None, None)
        info_dict[wobj.offset] = new_minfo
    
    for minfo in info_dict.values():
        if minfo.data_object.off_parent is not 0:
            minfo.parent = info_dict[minfo.data_object.off_parent]
        if minfo.data_object.off_first_child is not 0:
            minfo.first_child = info_dict[minfo.data_object.off_first_child]
        if minfo.data_object.off_prev is not 0:
            minfo.prev = info_dict[minfo.data_object.off_prev]
        if minfo.data_object.off_next is not 0:
            minfo.next = info_dict[minfo.data_object.off_next]
    
    return list(info_dict.values())

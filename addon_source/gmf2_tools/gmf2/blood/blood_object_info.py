import math
from dataclasses import dataclass

import bpy
import mathutils

from .gmf2b import Gmf2b

@dataclass
class BloodModelObjectInfo:
    data_object: Gmf2b.WorldObject

    name: str

    parent: 'BloodModelObjectInfo'
    first_child: 'BloodModelObjectInfo'
    prev: 'BloodModelObjectInfo'
    next: 'BloodModelObjectInfo'

    root: 'BloodModelObjectInfo'

    local_matrix: mathutils.Matrix
    global_matrix: mathutils.Matrix

    @property
    def unique_name_string(self) -> str:
        return f"{self.name}_MODELNAME_{self.data_object.offset}"

    @property
    def is_child(self) -> bool:
        """Does the object have a parent?"""
        return self.parent is not None
    
    @property
    def has_children(self) -> bool:
        """Does the object have any children?"""
        return self.first_child is not None
    
    @property
    def has_model_data(self) -> bool:
        """Does the object have any mesh data?"""
        return self.data_object.off_surfaces is not 0
    
    @property
    def is_bone(self) -> bool:
        # """Is the object an armature bone?"""
        # if self.has_model_data:
        #     return False
        
        # if self.name is not "ROOT":
        #     if self.root is not self and not self.root.is_bone:
        #         return False
        
        # return True
        return self.data_object.flags == 0x11
    

def create_minfo_from_wobjects(wobjs: list[Gmf2b.WorldObject]):
    info_dict: dict[int, BloodModelObjectInfo] = {}

    for wobj in wobjs:
        pos_matrix = mathutils.Matrix.Translation((wobj.position.x, wobj.position.y, wobj.position.z))

        new_minfo = BloodModelObjectInfo(wobj, wobj.name, None, None, None, None, None, pos_matrix.copy(), pos_matrix.copy())
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
    
    # Set the root in a seperate loop to ensure that all parents have been properly set
    for minfo in info_dict.values():
        root_obj = minfo
        root_found = False
        while root_found is False:
            if root_obj.is_child:
                root_obj = root_obj.parent
            else:
                root_found = True
        minfo.root = root_obj

        if minfo.is_child:
            minfo.global_matrix = minfo.parent.global_matrix @ minfo.local_matrix
    
    return list(info_dict.values())

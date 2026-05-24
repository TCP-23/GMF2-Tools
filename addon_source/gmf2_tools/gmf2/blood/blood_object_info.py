from dataclasses import dataclass

@dataclass
class BloodModelObjectInfo:

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
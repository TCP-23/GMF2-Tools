class ProcessedObject:
    obj = None
    parent_obj = None
    first_child_obj = None
    prev_obj = None
    next_obj = None

    is_first_child = False

    def __init__(self, _obj, _parent_obj, _first_child_obj, _prev_obj, _next_obj):
        self.obj = _obj
        self.parent_obj = _parent_obj
        self.first_child_obj = _first_child_obj
        self.prev_obj = _prev_obj
        self.next_obj = _next_obj

        if self.parent_obj is not None and self.parent_obj.off_parent == 0:
            self.is_first_child = True


def process_objects(unprocessed_objects):
    processed_objects = []

    # Loop through every object in the provided list
    for i, obj_data in unprocessed_objects.items():
        parent, first_child, prev_obj, next_obj = None, None, None, None

        # Get references to linked objects
        if obj_data.off_parent in unprocessed_objects:
            parent = unprocessed_objects[obj_data.off_parent]
        if obj_data.off_first_child in unprocessed_objects:
            first_child = unprocessed_objects[obj_data.off_first_child]
        if obj_data.off_prev in unprocessed_objects:
            prev_obj = unprocessed_objects[obj_data.off_prev]
        if obj_data.off_next in unprocessed_objects:
            next_obj = unprocessed_objects[obj_data.off_next]

        # Create a ProcessedObject
        new_obj = ProcessedObject(obj_data, parent, first_child, prev_obj, next_obj)
        processed_objects.append(new_obj)

    return processed_objects


class DataObjInfo:
    data_obj = None
    obj_name = "NONE"

    is_child_obj = False


class ModelObjInfo:
    pass


class AnimObjInfo:
    anim_obj = None
    obj_name = "NONE"
    has_anim_data = False
    has_pos = False
    has_rot = False
    is_child_obj = False

    pos_x_block = None
    pos_y_block = None
    pos_z_block = None
    rot_x_block = None
    rot_y_block = None
    rot_z_block = None

    def __init__(self, _anim_obj, _is_first_child):
        self.anim_obj = _anim_obj
        self.obj_name = self.anim_obj.name

        if self.anim_obj.obj_anim_data is not None:
            self.has_anim_data = True

            if self.anim_obj.off_parent != 0 and not _is_first_child:
                self.is_child_obj = True

            if self.anim_obj.obj_anim_data.block_count == 6:
                # If an object has both position and rotation data, the position data will always come first.

                self.pos_x_block = self.anim_obj.obj_anim_data.pos_x_block
                self.pos_y_block = self.anim_obj.obj_anim_data.pos_y_block
                self.pos_z_block = self.anim_obj.obj_anim_data.pos_z_block
                self.rot_x_block = self.anim_obj.obj_anim_data.rot_x_block
                self.rot_y_block = self.anim_obj.obj_anim_data.rot_y_block
                self.rot_z_block = self.anim_obj.obj_anim_data.rot_z_block

                self.has_pos = True
                self.has_rot = True
            else:
                # An object can't have only one or two channels in a set.
                # Because of this, we only need to check for one block in a set.

                if self.anim_obj.obj_anim_data.pos_x_block.block_id == 0:
                    self.pos_x_block = self.anim_obj.obj_anim_data.pos_x_block
                    self.pos_y_block = self.anim_obj.obj_anim_data.pos_y_block
                    self.pos_z_block = self.anim_obj.obj_anim_data.pos_z_block

                    self.has_pos = True
                else:
                    self.rot_x_block = self.anim_obj.obj_anim_data.pos_x_block
                    self.rot_y_block = self.anim_obj.obj_anim_data.pos_y_block
                    self.rot_z_block = self.anim_obj.obj_anim_data.pos_z_block

                    self.has_rot = True


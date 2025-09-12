class DataObjInfo:
    def __init__(self, _data_obj, _parent_obj, _first_child_obj, _prev_obj, _next_obj):
        self.data_obj = _data_obj
        self.obj_name = self.data_obj.name

        self.parent_obj = _parent_obj
        self.is_child_obj = False
        if self.parent_obj is not None:
            self.is_child_obj = True
        self.first_child_obj = _first_child_obj
        self.has_children = False
        if self.first_child_obj is not None:
            self.has_children = True
        self.prev_obj = _prev_obj
        self.next_obj = _next_obj

    @staticmethod
    def process_object_info(unprocessed_obj_info):
        processed_obj_info = []

        # Loop through every object in the provided list
        for i, obj_info in unprocessed_obj_info.items():
            parent, first_child, prev_obj, next_obj = None, None, None, None

            # Get references to linked objects
            if obj_info.off_parent in unprocessed_obj_info:
                parent = unprocessed_obj_info[obj_info.off_parent]
            if obj_info.off_first_child in unprocessed_obj_info:
                first_child = unprocessed_obj_info[obj_info.off_first_child]
            if obj_info.off_prev in unprocessed_obj_info:
                prev_obj = unprocessed_obj_info[obj_info.off_prev]
            if obj_info.off_next in unprocessed_obj_info:
                next_obj = unprocessed_obj_info[obj_info.off_next]

            # Create a DataObjInfo
            new_obj_info = DataObjInfo(obj_info, parent, first_child, prev_obj, next_obj)
            processed_obj_info.append(new_obj_info)

        return processed_obj_info


class ModelObjInfo(DataObjInfo):
    bone_m_infos = []

    def __init__(self, _data_obj, _parent_obj, _first_child_obj, _prev_obj, _next_obj):
        super().__init__(_data_obj, _parent_obj, _first_child_obj, _prev_obj, _next_obj)

        self.has_model_data = False
        self.is_bone = False
        self.is_child_of_bone = False
        self.is_parent_of_bone = False

        if self.data_obj.surfaces is not None:
            self.has_model_data = True
        elif self.obj_name == "ROOT" and not self.has_model_data:
            self.is_bone = True
            ModelObjInfo.bone_m_infos.append(self.data_obj)
        elif self.parent_obj in ModelObjInfo.bone_m_infos:
            self.is_child_of_bone = True
            self.is_bone = True
            ModelObjInfo.bone_m_infos.append(self.data_obj)

        if self.first_child_obj in ModelObjInfo.bone_m_infos:
            self.is_parent_of_bone = True

        self.vertices = []
        self.indices = []
        self.uvs = []
        self.normals = []
        self.mat_offsets = []
        self.skin_names = []

    @staticmethod
    def process_object_info(unprocessed_obj_info):
        model_obj_info = []

        for i, obj_info in unprocessed_obj_info.items():
            parent, first_child, prev_obj, next_obj = None, None, None, None

            # Get references to linked objects
            if obj_info.off_parent in unprocessed_obj_info:
                parent = unprocessed_obj_info[obj_info.off_parent]
            if obj_info.off_first_child in unprocessed_obj_info:
                first_child = unprocessed_obj_info[obj_info.off_first_child]
            if obj_info.off_prev in unprocessed_obj_info:
                prev_obj = unprocessed_obj_info[obj_info.off_prev]
            if obj_info.off_next in unprocessed_obj_info:
                next_obj = unprocessed_obj_info[obj_info.off_next]

            # Create a ModelObjInfo
            new_model_obj_info = ModelObjInfo(obj_info, parent, first_child, prev_obj, next_obj)
            model_obj_info.append(new_model_obj_info)

        ModelObjInfo.bone_m_infos.clear()

        return model_obj_info


class AnimObjInfo(DataObjInfo):
    def __init__(self, _data_obj, _parent_obj, _first_child_obj, _prev_obj, _next_obj):
        super().__init__(_data_obj, _parent_obj, _first_child_obj, _prev_obj, _next_obj)

        if self.data_obj.obj_anim_data is not None:
            self.has_anim_data = True

            if self.data_obj.obj_anim_data.block_count == 6:
                # If an object has both position and rotation data, the position data will always come first.

                self.pos_x_block = self.data_obj.obj_anim_data.pos_x_block
                self.pos_y_block = self.data_obj.obj_anim_data.pos_y_block
                self.pos_z_block = self.data_obj.obj_anim_data.pos_z_block
                self.rot_x_block = self.data_obj.obj_anim_data.rot_x_block
                self.rot_y_block = self.data_obj.obj_anim_data.rot_y_block
                self.rot_z_block = self.data_obj.obj_anim_data.rot_z_block

                self.has_pos = True
                self.has_rot = True
            else:
                # An object can't have only one or two channels in a set.
                # Because of this, we only need to check for one block in a set.

                if self.data_obj.obj_anim_data.pos_x_block.block_id == 0:
                    self.pos_x_block = self.data_obj.obj_anim_data.pos_x_block
                    self.pos_y_block = self.data_obj.obj_anim_data.pos_y_block
                    self.pos_z_block = self.data_obj.obj_anim_data.pos_z_block

                    self.has_pos = True
                else:
                    self.rot_x_block = self.data_obj.obj_anim_data.pos_x_block
                    self.rot_y_block = self.data_obj.obj_anim_data.pos_y_block
                    self.rot_z_block = self.data_obj.obj_anim_data.pos_z_block

                    self.has_rot = True

    @staticmethod
    def process_object_info(unprocessed_obj_info):
        anim_obj_info = []

        # evil way to do this but whatever
        data_obj_info = super().process_object_info(unprocessed_obj_info)
        for data_info in data_obj_info:
            new_anim_obj_info = AnimObjInfo(data_info.data_obj, data_info.parent_obj, data_info.first_child_obj,
                                            data_info.prev_obj, data_info.next_obj)
            anim_obj_info.append(new_anim_obj_info)

        return anim_obj_info

from __future__ import annotations

from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.property_object import PropertyObject
from py_teststand.property.property_object_file import PropertyObjectFile
from py_teststand.users.user import User, UserGroup


class UsersFile(PropertyObjectFile):
    @property
    @ts_interface
    def user_group_list(self) -> PropertyObject:
        return PropertyObject(self._com_obj.UserGroupList, self._engine_ref)

    @property
    @ts_interface
    def user_list(self) -> PropertyObject:
        return PropertyObject(self._com_obj.UserList, self._engine_ref)

    @property
    @ts_interface
    def user_profile_list(self) -> PropertyObject:
        return PropertyObject(self._com_obj.UserProfileList, self._engine_ref)

    @ts_interface
    def as_property_object_file(self) -> PropertyObjectFile:
        return PropertyObjectFile(self._com_obj.AsPropertyObjectFile(), self._engine_ref)

    @ts_interface
    def reload_from_disk(self) -> None:
        self._com_obj.ReloadFromDisk()

    @ts_interface
    def set_user_list(self, user_list: PropertyObject) -> None:
        raw_list = getattr(user_list, "_com_obj", user_list)
        self._com_obj.SetUserList(raw_list)

    def get_users(self) -> list[User]:
        users = []
        user_list = self.user_list
        num_users = user_list.get_num_elements()
        for i in range(num_users):
            com_user = user_list.get_property_object_by_offset(i)
            if com_user:
                users.append(User(com_user._com_obj, self._engine_ref))
        return users

    def get_user_groups(self) -> list[UserGroup]:
        groups = []
        group_list = self.user_group_list
        num_groups = group_list.get_num_elements()
        for i in range(num_groups):
            com_group = group_list.get_property_object_by_offset(i)
            if com_group:
                groups.append(UserGroup(com_group._com_obj, self._engine_ref))
        return groups

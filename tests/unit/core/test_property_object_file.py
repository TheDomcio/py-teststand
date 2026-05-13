from __future__ import annotations

from unittest.mock import MagicMock, PropertyMock

from py_teststand import PropertyObjectFile, TypeUsageList


def test_property_object_file_path():

    mock_com = MagicMock()

    type(mock_com).Path = PropertyMock(return_value="mock.ini")

    pof = PropertyObjectFile(mock_com, None)

    assert pof.path == "mock.ini"


def test_property_object_file_path_setter():

    mock_com = MagicMock()

    pof = PropertyObjectFile(mock_com, None)

    pof.path = "new.ini"

    assert mock_com.Path == "new.ini"


def test_property_object_file_locked():

    mock_com = MagicMock()

    type(mock_com).Locked = PropertyMock(return_value=True)

    pof = PropertyObjectFile(mock_com, None)

    assert pof.locked is True


def test_property_object_file_is_modified():

    mock_com = MagicMock()

    type(mock_com).IsModified = PropertyMock(return_value=False)

    pof = PropertyObjectFile(mock_com, None)

    assert pof.is_modified is False


def test_property_object_file_is_disk_file_read_only():

    mock_com = MagicMock()

    type(mock_com).IsDiskFileReadOnly = PropertyMock(return_value=True)

    pof = PropertyObjectFile(mock_com, None)

    assert pof.is_disk_file_read_only is True


def test_property_object_file_type():

    mock_com = MagicMock()

    type(mock_com).FileType = PropertyMock(return_value=1)

    pof = PropertyObjectFile(mock_com, None)

    assert pof.file_type == 1


def test_property_object_file_read_file():

    mock_com = MagicMock()

    mock_com.ReadFile.return_value = True

    pof = PropertyObjectFile(mock_com, None)

    result = pof.read_file(1)

    mock_com.ReadFile.assert_called_once_with(1)

    assert result is True


def test_property_object_file_read_file_default():

    mock_com = MagicMock()

    mock_com.ReadFile.return_value = True

    pof = PropertyObjectFile(mock_com, None)

    pof.read_file()

    mock_com.ReadFile.assert_called_once_with(1)


def test_property_object_file_write_file():

    mock_com = MagicMock()

    pof = PropertyObjectFile(mock_com, None)

    pof.write_file()

    mock_com.WriteFile.assert_called_once_with(1)


def test_property_object_file_write_file_format():

    mock_com = MagicMock()

    pof = PropertyObjectFile(mock_com, None)

    pof.write_file(3)

    mock_com.WriteFile.assert_called_once_with(3)


def test_property_object_file_lock():

    mock_com = MagicMock()

    pof = PropertyObjectFile(mock_com, None)

    pof.lock("secret")

    mock_com.Lock.assert_called_once_with("secret")


def test_property_object_file_unlock():

    mock_com = MagicMock()

    pof = PropertyObjectFile(mock_com, None)

    pof.unlock("secret")

    mock_com.Unlock.assert_called_once_with("secret")


def test_property_object_file_handle_type_conflicts():

    mock_com = MagicMock()

    mock_com.HandleTypeConflicts.return_value = True

    pof = PropertyObjectFile(mock_com, None)

    result = pof.handle_type_conflicts(0)

    mock_com.HandleTypeConflicts.assert_called_once_with(0)

    assert result is True


def test_property_object_file_save_file_if_modified():

    mock_com = MagicMock()

    mock_com.SaveFileIfModified.return_value = True

    pof = PropertyObjectFile(mock_com, None)

    result = pof.save_file_if_modified()

    mock_com.SaveFileIfModified.assert_called_once_with(True)

    assert result is True


def test_property_object_file_version():

    mock_com = MagicMock()

    type(mock_com).Version = PropertyMock(return_value="1.0")

    pof = PropertyObjectFile(mock_com, None)

    assert pof.version == "1.0"


def test_type_usage_list_num_types():

    mock_com = MagicMock()

    type(mock_com).NumTypes = PropertyMock(return_value=5)

    tul = TypeUsageList(mock_com, None)

    assert tul.num_types == 5


def test_type_usage_list_len():

    mock_com = MagicMock()

    type(mock_com).NumTypes = PropertyMock(return_value=3)

    tul = TypeUsageList(mock_com, None)

    assert len(tul) == 3


def test_type_usage_list_get_type_definition():

    mock_com = MagicMock()

    mock_type = MagicMock()

    mock_com.GetTypeDefinition.return_value = mock_type

    tul = TypeUsageList(mock_com, None)

    result = tul.get_type_definition(0)

    mock_com.GetTypeDefinition.assert_called_once_with(0)

    assert result._com_obj is mock_type


def test_type_usage_list_get_type_index():

    mock_com = MagicMock()

    mock_com.GetTypeIndex.return_value = 2

    tul = TypeUsageList(mock_com, None)

    assert tul.get_type_index("MyType") == 2

    mock_com.GetTypeIndex.assert_called_once_with("MyType")


def test_type_usage_list_union():

    mock_com = MagicMock()

    mock_com.Union.return_value = True

    mock_other_com = MagicMock()

    tul = TypeUsageList(mock_com, None)

    other = TypeUsageList(mock_other_com, None)

    result = tul.union(other)

    mock_com.Union.assert_called_once_with(mock_other_com)

    assert result is True


def test_type_usage_list_move_type():

    mock_com = MagicMock()

    tul = TypeUsageList(mock_com, None)

    tul.move_type(0, 2)

    mock_com.MoveType.assert_called_once_with(0, 2)


def test_type_usage_list_remove_type():

    mock_com = MagicMock()

    mock_removed = MagicMock()

    mock_com.RemoveType.return_value = mock_removed

    tul = TypeUsageList(mock_com, None)

    result = tul.remove_type(1)

    mock_com.RemoveType.assert_called_once_with(1)

    assert result._com_obj is mock_removed

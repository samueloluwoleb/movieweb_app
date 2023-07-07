import pytest
from datamanager.json_data_manager import JSONDataManager

data_manager_obj = JSONDataManager('movies_database.json')


def test_file_path_json():
    assert data_manager_obj._file_path == "movies_database.json"


pytest.main()

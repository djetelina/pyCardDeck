import pytest
import os
import shutil


@pytest.fixture(scope="session", autouse=True)
def temp_dir(request):
    os.mkdir(os.getcwd() + "/tests/temp")

    def after_tests():
        shutil.rmtree(os.getcwd() + "/tests/temp")
    request.addfinalizer(after_tests)

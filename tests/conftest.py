import pytest
import os
import shutil


@pytest.fixture(scope="session", autouse=True)
def temp_dir(request):
    os.makedirs(os.getcwd() + "/tests/temp", exist_ok=True)

    def after_tests():
        shutil.rmtree(os.getcwd() + "/tests/temp")

    request.addfinalizer(after_tests)

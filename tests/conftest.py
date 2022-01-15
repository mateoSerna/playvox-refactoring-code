import os

import boto3
import pytest
from moto import mock_sns, mock_ssm

os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_REGION_NAME"] = "testing"

os.environ["FILE_PATH"] = "tests/fixtures/profileDB_id.txt"


@pytest.fixture()
def ssm_mock():
    ssm_params = {
        "username": "root",
        "password": "123",
        "host": "localhost",
        "port": "6603",
        "database": "backendtest",
    }

    with mock_ssm():
        ssm_client = boto3.client("ssm")

        for param, value in ssm_params.items():
            ssm_client.put_parameter(
                Name=f"/mysql/{param}", Value=value, Type="SecureString"
            )
        yield ssm_client


@pytest.fixture()
def sns_mock():
    with mock_sns():
        sns_client = boto3.client("sns")
        yield sns_client

import json
import os
from enum import Enum
from typing import Optional

import boto3

from orm import Orm

# I'd use environment variables to store this kind of information,
# in this case, the AWS credentials or any credentials never should be hard coded.
sns_client = boto3.client(
    "sns",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name=os.environ["AWS_REGION_NAME"],
)

# I'd use enumerations to make definitions and constants that are easy
# to read and mantain.
class Types(Enum):
    INFORMATION_ACCOUNT = "info"


# I'd create reusable classes that help to accomplish the DRY principle.
class Message(Orm):
    def __init__(self, users: list) -> None:
        super().__init__()
        self.users = users

    @staticmethod
    def send_to_sns(message: str, phone_number: str) -> None:
        """Sends a notification using the SNS service to a phone number (SMS).
        
        I'd use docstrings to improve documentation."""
        try:
            sns_client.publish(PhoneNumber=phone_number, Message=message)
        except Exception as e:
            # I'd use more specific exceptions.
            raise Exception(f"There was an error publishing the message to AWS: {e}")

    def send_messages(self) -> None:
        for user in self.__get_users():
            numbers = json.loads(user["phone_numbers"])
            phone_number = self.__get_phone_number(numbers.values())

            if message := self.__get_message(user):
                self.send_to_sns(message, phone_number)

    # I'd use the access modifiers to identify what methods can only be
    # used in the class instance and what others are public, etc.
    def __get_users(self) -> list:
        try:
            user_fields = [
                "profile",
                "first_name",
                "last_name",
                "phone_numbers",
                "service_link",
            ]
            users_ids = [str(user["profile"]) for user in self.users]
            user_where = {"profile": users_ids}
            users = self.select_in(table="users", fields=user_fields, where=user_where)

            if users:
                return [user for user in users]
        except Exception as e:
            # I'd use more specific exceptions.
            raise Exception(f"Error getting users: {e}")
        return []

    def __get_phone_number(self, numbers: dict) -> dict:
        try:
            phone_fields = ["number"]
            phone_where = {"phone_id": numbers}
            phone_number = self.select_in(
                table="phone_numbers",
                fields=phone_fields,
                where=phone_where,
                only_first=True,
            )

            if phone_number:
                return phone_number["number"]
        except Exception as e:
            # I'd use more specific exceptions.
            raise Exception(f"Error getting user: {e}")
        return {}

    def __get_message(self, user: dict) -> Optional[str]:
        message = None
        membership, type_message = next(
            (
                (user_info["membership"], user_info["type"])
                for user_info in self.users
                if str(user_info["profile"]) == str(user["profile"])
            ),
            None,
        )

        # I'd use the advantages of each feature of python: for example the f strings
        # to do better and easier concatenations, the walrus operator (:=) or the addition
        # of the new `match case` statement in python 3.10.
        match type_message:
            case Types.INFORMATION_ACCOUNT.value:
                message = (
                    f"Hey {user['first_name']} {user['last_name']} we have some information "
                    f"about your {membership} account, please go to {user['service_link']} "
                    f"to get more details."
                )

        return message

"""Send message to users read in a file

This script reads the content of a file and send a message to each user. The file
should be a .txt with a semicolon separated value format.

Finally, the message is sent using the SNS from AWS.
"""
# I'd use tools such as isort and black that help to guarantee and standardize
# the code style guide.
import asyncio
import logging
import os

import aiofiles

from message import Message, Types

# I'd use environment variables to store information
# such as where the file is located and the number of
# messages desired to process per batch.
FILE_PATH = os.environ["FILE_PATH"]
CHUNK_SIZE = os.environ.get("CHUNK_SIZE", 1)


# I'd use an asynchronous approach to improve the performance
# of the reading and processing of the file.
async def main():
    users = []
    async with aiofiles.open(FILE_PATH, mode="r") as file:
        async for line in file:
            try:
                # I think is better to process the file in batches, with this
                # the number of similar queries to the database is reduced to just
                # one per batch.
                user_membership, profile, *_ = line.strip().split(";")
                membership = user_membership.split(" ")[-1]
                users.append(
                    {
                        "profile": profile,
                        "membership": membership,
                        "type": Types.INFORMATION_ACCOUNT.value,
                    }
                )

                if len(users) == CHUNK_SIZE:
                    try:
                        # I'd separate the logic of reading the file and processing
                        # the content. And in this case I'd create a reusable class
                        # to manage Messages to users.
                        message = Message(users=users)
                        message.send_messages()
                    except Exception as e:
                        # I'd add error handling that helps to control the workflow and
                        # help to understand what happened in case of any error.
                        logging.error(
                            f"There was an error sending the message to some user(s): {e}"
                        )
                    finally:
                        users = []
            except Exception as e:
                logging.error(f"There was an error reading the file: {e}")


if __name__ == "__main__":
    asyncio.run(main())

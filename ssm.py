import boto3

ssm = boto3.client("ssm")

# I'd create helpers to easily access to services such as SSM from Amazon.
def get(name=None, with_decryption=True):
    try:
        parameter = ssm.get_parameter(Name=name, WithDecryption=with_decryption)
        return parameter["Parameter"]["Value"]
    except Exception:
        # I'd use more specific exceptions.
        raise Exception(f"Unable to get SSM parameter {name}")

import os
import argparse
import logging
import boto3
import botocore
import json

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

import urllib.parse

parser = argparse.ArgumentParser("Run the LambdaPy project.")
parser.add_argument('-v','--verbose', help="Run with log.level=Info", action='store_true')
args = parser.parse_args()


def handler(event, context):
    print('##EVENT')
    print(event)

    if 'Records' in event:
        bucket = event['Records'][0]['s3']['bucket']['name']
        s3_file_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding="utf-8")
        print(f"Trying to parse file:{s3_file_key}")
        try:
            s3 = boto3.client('s3','eu-central-1', config=botocore.config.Config(connect_timeout=5, s3={'addressing_style':'path'}))
            s3_object = s3.get_object(Bucket=bucket, Key=s3_file_key)
            print(f"CONTENT TYPE:"+s3_object["ContentType"])
            json_content = json.loads(s3_object['Body'].read().decode('utf-8'))
            print(f"JSON_CONTENT:{json_content}")
        except Exception as e:
            print(e)
            print(f"Error getting object {s3_file_key} from bucket {bucket}")
            return

        try:
            s3 = boto3.client('s3', 'eu-central-1',  config=botocore.config.Config(connect_timeout=5, s3={'addressing_style':'path'}))
            new_key = s3_file_key.replace("new", "processed")
            s3.put_object(Body=f"{json_content}", Bucket=bucket, Key=new_key)
            print(f"Copied with the new key {new_key}")
        except Exception as e:
            print(e)
            print(f"We couldn't put the new key:{new_key}")


if __name__ == "__main__":
    if len(logging.getLogger().handlers) > 0:
        # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
        # `.basicConfig` does not execute. Thus we set the level directly.
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose:
        logging.basicConfig(
            level=logging.INFO,
            format=f'%(asctime)s %(levelname)s %(message)s',
            force=True
        )
    else:
        logging.basicConfig(
            level=logging.ERROR,
            format=f'%(asctime)s %(levelname)s %(message)s',
            force=True
        )
    logger = logging.getLogger()
    handler(False, False)



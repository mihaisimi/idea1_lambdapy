#This is a python code deployed as a lambda container, this is the support codebase for the 
##For any information please contact us, you can find more details on our company's site: [Ideahub] ( https://www.ideahub.ro/#/home )


##Overview
This is a demo for the video located here:

##Setup 
```bash
pip3.9 install -r requirements.txt
```

###Building the docker image and pushing it to ECR


###Services provided
####Use the /buildAndDeploy.sh to build and push a new image to ECR< please make sure you change you profile and the ECR URI. 
####Usage: ./buildAndDeploy.sh -a <numerical_aws_id> -r <aws_region eg. eu-central-1> -p <aws_profile eg. default>
####You can find the numerical_aws_id associated to your IAM by clicking on your name in the AWS GUI, it should be AccountId:, please put only the numbers in here (should be 12 digits)

```shell
./buildAndDeploy.sh -a <numerical_aws_id> -r eu-central-1 -p default
```



###Run locally as docker then the code will be located inside  /var/task/src/
###run it with the web server
`docker run -it --rm -p 9000:8080 idea1_lambdapy:latest`

##this is how an S3 trigger event looks like:
```json
{
  "Records": [
    {
      "s3": {
        "name": "lambdapy-test",
        "object": {
          "key": "test.json"
        }
      }
    }
  ]
}
```


```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations"      -d  '{"Records":[{"s3":{"name":"lambdapy-test","object":{"key":"test.json"}}}]}'
```

#To test remotely you can put a file on the s3 trigger folder
aws s3 cp resources/test.json s3://lambdapy-test/new/ --profile YOUR_PROFILE

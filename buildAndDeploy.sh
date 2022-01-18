#!/bin/sh

display_help() {
    echo "Usage: $0 -a <numerical_aws_id> -r <aws_region eg. eu-central-1> -p <aws_profile eg. default> " >&2
    exit 1
}

while getopts a:r:p: flag
do
    case "${flag}" in
        a) awsid=${OPTARG};;
        r) region=${OPTARG};;
        p) profile=${OPTARG};;
        *) display_help;exit 1;;
    esac
done

echo "Building image idea1_lambdapy to $awsid.dkr.ecr.$region.amazonaws.com using the profile: $profile "

docker buildx build -t idea1_lambdapy . --platform linux/amd64
aws ecr get-login-password --region $region --profile $profile | docker login --username AWS --password-stdin $awsid.dkr.ecr.$region.amazonaws.com
docker tag idea1_lambdapy:latest $awsid.dkr.ecr.$region.amazonaws.com/idea1_lambdapy:latest
docker push $awsid.dkr.ecr.$region.amazonaws.com/idea1_lambdapy:latest

#!/bin/bash
FROM public.ecr.aws/lambda/python:3.8

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

#set the working directory inside the container
COPY . ${LAMBDA_TASK_ROOT}/

WORKDIR ${LAMBDA_TASK_ROOT}/idea1_lambdapy

CMD [ "src.app.handler" ]

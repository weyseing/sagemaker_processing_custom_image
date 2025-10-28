#!/bin/bash
set -e

# load env
if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

# image tag
IMAGE_TAG="latest"

# build
echo "Building Docker image..."
docker build -t $AWS_ECR_ENDPOINT:$IMAGE_TAG -f Dockerfile_sagemaker .

# login to ECR
echo "Logging into ECR..."
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ECR_ENDPOINT

# push image
echo "Pushing to ECR..."
docker push $AWS_ECR_ENDPOINT:$IMAGE_TAG

echo "Done! Image pushed to: $AWS_ECR_ENDPOINT:$IMAGE_TAG"
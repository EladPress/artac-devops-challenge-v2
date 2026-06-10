# MY ASSESSMENT

## DEPENDENCIES

### scikit-learn 1.8.0 | Type: bugfix
"[DECISIONS.md](DECISIONS.md)" explains under "Dependencies" that the package "scikit-learn" is locked to v1.6.1 because of stability and API breaking in later versions.
I disagree with this decision because the model was "pickled" with scikit-learn v1.8.0, so the package being too old was breaking the application.
My solution was to raise the version in "[requirements.txt](requirements.txt)" to v1.8.0

LATER NOTE: This also fixed the "Run Tests" Job in our CI process.

## Docker Image

### Health Checks | Type: needs improvement
"[DECISIONS.md](DECISIONS.md)" explains under "Docker Image" that both `/health` and `ready` return 200 so either works. That's true for now, because the model loading is baked inside the startup of the server's startup, so it will immediately become ready as soon as it becomes alive. 

I switched the health checks to poll `/ready` because it's the actual condition of the application being ready for use, and it makes the image more robust if further changes to the application separate the startup logic.

### Base image | Type: intentional tradeoff
"[DECISIONS.md](DECISIONS.md)" explains under "Docker Image" that the base image is python:3.12 because the slim was causing issues with some native dependencies during `pip install`. I did not experience any issues, the slim image works just fine. In any case, the reduction in image size is significant and in my opinion is worth a bit of debugging, or a multi stage build.

LATER NOTE: This also seemed to remove a CRITICAL vulnerability in the project. The slimmer image simply did not include it.

### .dockerignore | Type: needs improvement
A .dockerignore file was missing, which caused a lot of needless file to be copied into the image, so a "[.dockerignore](.dockerignore)" file was added

### Single-stage build | Type: intentional tradeoff
This is not actually a trade off, the image should not be built with another stage, as there isn't anything that needs to be compiled or built before copying everything into the final image.
Building the project as a whl or any equivalent seems unnecessary because the project is very small and distributing the code itself is not relevant.

## CI/CD

### Image pushed before testing | Type: bug
The CI process pushed the Docker image before testing/security checks could verify the image is safe to deploy.
I fixed this by building the image, uploading it as an artifact, downloading it for the security-scan stage, and only after verifying all tests and scans passed the image will be given tags and pushed.

### Normalize image registry/image-name | Type: bug
The registry and image name values in "[ci.yml](ci.yml)" accepted uppercase letters, which ghcr does not. I fixed this by normalizing these values

### Upgrading actions versions | Type: needs improvement
The CI results showed warnings that the actions used had Node20 which was getting deprecated from use in GitHub Actions. I upgraded these actions' versions and validated the CI process still works.

### Locking Trivy version | Type: needs improvement
The Trivy job in "[ci.yml](ci.yml)" was watching the action's master branch, which keeps getting new versions, and this is a risk because breaking changes can appear that we are not aware of. As a solution, I locked the Trivy version to 0.36.0 which is as of writing the latest.

### Non Existent Smoke Test | Type: needs improvement
"[DECISIONS.md](DECISIONS.md)" mentions a "CI smoke test" but it didn't really exist in "[ci.yml](ci.yml)". There is of course the "Run Tests" job but it doesn't really qualify, as it only runs the python code, instead of testing the entire stack, which includes deploying the Docker Image. I added a smoke test job that deploys the image and checks all three endpoints.

### Trivy ignores all severity vulnerabilities | Type: intentional tradeoff
"[DECISIONS.md](DECISIONS.md)" mentions that Trivy was intentionally being made to ignore all vulnerabilities. This is a temporary fix only to pass the build, so I fixed this.
I believed HIGH and CRITICAL vulnerabilities should automatically fail the build and LOW and MEDIUM should pass the build but be reported.
Because Trivy can't have a different exit code for different severities of vulnerabilities I divided the Trivy scan to two portions: one that does a full scan and uploads an artifact with the full results, and a second one that fails the build if a HIGH or CRITICAL vulnerability exists.
I kept ignoring unfixed vulnerabilities, because these can't be actioned upon. This is a tradeoff I made for now, this is not set in stone, of course a vulnerability can be avoided instead of fixed.

### Fixed HIGH vulnerability | Type: bug
While stopping Trivy from ignoring HIGH and CRITICAL vulnerabilities, a HIGH severity vulnerability was found in "starlette" which fastapi uses. As a fix, I upgraded fastapi to a version high enough that includes a fixed version of "starlette". I could have chosen the latest version of fastapi but I chose a more conservative version, as I felt this was outside the scope of the assignment.

### Image naming convention | Type: Needs improvement
This is an architecture choice of mine. I feel commit hashes as image tags are not human readable. Using Semantic Release, each release/prerelease image will have their semantic version as a tag which of course matches the git tag. All images will also have the tag: {BRANCH_NAME-BUILD_INCREMENT} and will have the label: org.opencontainers.image.revision=${commit_hash}

### Image only built for amd64 | Type: intentional tradeoff
While the images are mostly running on amd64, A lot of developers use ARM based Macs, so I thought it important to include an amd64 native image along with the standard amd64 image.
But I decided to keep only building amd64 images because I reached the conclusion that the changed needed to make two images would mean a large change of the CI process, which I decided was outside of the scope of this mission.
The reason the tradeoff is valid in my opinion is the production environments run on amd64 anyway, and Macs can run amd64 images via emulation (A simple flag in the docker run command allows Macs to run amd64 images).

### Stubbed deploy job | Type: bug
The `deploy` job in "[ci.yml](ci.yml)" was a no-op stub. "[DECISIONS.md](DECISIONS.md)" acknowledges it was left unwired. On top of being unimplemented, its comment said it should "SSH into the EC2 instance" — which contradicts the infrastructure work, since I removed SSH and moved instance access to AWS SSM Session Manager.
I implemented the deploy job and made it look up the EC2 instance (if there is none nothing will be deployed), replace the image deployed with the one the build created, and makes sure the container is running and ready.

## Infrastructure

### Choice of deploying on EC2 | Type: intentional tradeoff
This project is deployed on EC2, which to me seemed weird as we're deploying a Docker image, why not deploy using AWS ECS?
I reached the conclusion that ECS may be overkill for this assignment, and for a single application an EC2 instance that runs Docker is good enough.

### AMI deprecated | Type: bug
The AMI image specified for the EC2 instance in "[main.tf](terraform/main.tf)" was deprecated.
A fix was irrelevant because of the next change:

### Region-agnostic AMI | Type: needs improvement
In "[main.tf](terraform/main.tf)" the AMI ID was hardcoded, while the AWS region wasn't. This works when not changing region from "us-east-1" but because of AMIs being region-specific, switching regions would not work.
My solution was to get the ID of the Ubuntu image we require (same locked version in each region) and then use it in the EC2 instance.

### Key pair handling | Type: needs improvement
In order to deploy the application using Terraform, a key pair had to exist before. I think a good practice to handle this specifically would have been creating a key pair with this Terraform project.
Instead I removed the key pair because the solution to the next problem makes this solution irrelevant:

### SSH ingress open wide | Type: bug
The security group in "[main.tf](terraform/main.tf)" allowed SSH (port 22) from `0.0.0.0/0`. "[DECISIONS.md](DECISIONS.md)" admits SSH was left open. Instead of narrowing down the CIDR, I removed SSH access and moved to accessing the instance using AWS SSM Session Manager

### App port left open | Type: intentional tradeoff
After closing SSH, port 8080 (the application) remains reachable from `0.0.0.0/0`. This is intentional: it is a public API and locking it to a single IP would defeat its purpose, unlike SSH which has no legitimate public need. I made the allowed range a variable (`app_allowed_cidrs`, default `0.0.0.0/0`) so it can be scoped down per environment without a code change.

### Instance type unsupported in newer regions | Type: needs improvement
When switching regions I noticed `t2.micro` didn't exist in the newer `il-central-1` region. In order to allow the application to run on more regions I changed the instance type to `t3.micro`.

### Root volume oversized and unencrypted | Type: needs improvement
The `root_block_device` in "[main.tf](terraform/main.tf)" requested a 20 GB volume and was not encrypted.
I right-sized the root volume to 10 GB, and added `encrypted = true` for at-rest encryption.

### Local Terraform state | Type: intentional tradeoff
"[DECISIONS.md](DECISIONS.md)" mentions that a remote state is overkill for now. I will correct that adding a DynamoDB for file locking is not needed anymore, as S3 now features file locking, so we only need to bootstrap an S3 bucket for remote state, but I agree that this is overkill for this mission, and if multiple people will work on a project, a remote state is very important and easy to implement.
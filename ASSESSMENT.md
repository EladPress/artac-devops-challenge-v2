# MY ASSESSMENT

## DEPENDENCIES

### scikit-learn 1.8.0 | Type: bugfix
"[DECISIONS.md](DECISIONS.md)" explains under "Dependencies" that the package "scikit-learn" is locked to v1.6.1 because of stability and API breaking in later versions.
I disagree with this descision because the model was "pickled" with scikit-learn v1.8.0, so the package being too old was breaking the application.
My solution was to raise the version in "[requirements.txt](requirements.txt)" to v1.8.0

LATER NOTE: This also fixed the the "Run Tests" Job in our CI process.

## Docker Image

# Health Checks | Type: needs improvement
"[DECISIONS.md](DECISIONS.md)" explains under "Docker Image" that both `/health` and `ready` return 200 so either works. That's true for now, because the model loading is baked inside the startup of the server's startup, so it will immediately become ready as soon as it becomes alive. 

I switched the health checks to poll `/ready` because it's the actual condition of the application being ready for use, and it makes the image more robust if further changes to the application separate the startup logic.

# Base image | Type: intentional tradeoff
"[DECISIONS.md](DECISIONS.md)" explains under "Docker Image" that the base image is python:3.12 because the slim was causing issues with some native dependencies during `pip install`. I did not experience any issues the the slim image works just fine. In any case, the reduction in image size is significant and in my opinion is worth a bit of debugging, or a multi stage build.

LATER NOTE: This also seemed to remove a CRITICAL vulnerability in the project. The slimmer image simply did not include it.

# .dockerignore | Type: needs improvement
A .dockerignore file was missing, which caused a lot of needless file to be copied into the image, so a "[.dockerignore](.dockerignore)" file was added

# Single-stage build | Type: intentional tradeoff
This is not actually a trade off, the image should not be built with another stage, as there isn't anything that needs to be compiled or built before copying everything into the final image.
Building the project as a whl or any equivalent seems unneccessary because the project is very small and distributing the code itself is not relevant.

## CI/CD

# Image pushed before testing | Type: bug
The CI process pushed the Docker image before testing/security checks could verify the image is safe to deploy.
I fixed this by building the image, uploading it as an artifact, downloading it for the security-scan stage, and only after verifying all tests and scans passed the image will be given tags and pushed.

# Upgrading actions versions | Type: needs improvement
The CI results showed warnings that the actions used had Node20 which was getting deprecated from use in GitHub Actions. I upgraded these actions' versions and validated the CI process still works.

# Locking Trivy version | Type: needs improvement
The Trivy job in "[ci.yml](ci.yml)" was watching the action's master branch, which keeps getting new versions, and this is a risk because breaking changes can appear that we are not aware of. As a solution, I locked the Trivy version to 0.36.0 which is as of writing the latest.

# Non Existent Smoke Test | Type: needs improvement
"[DECISIONS.md](DECISIONS.md)" mentions a "CI smoke test" but it didn't really exist in "[ci.yml](ci.yml)". There is of course the "Run Tests" job but it doesn't really qualify, as it only runs the python code, instead of testing the entire stack, which includes deploying the Docker Image. I added a smoke test job that deploys the image and checks all three endpoints.

# Trivy ignores all severity vulnerabilies | Type: intentional tradeoff
"[DECISIONS.md](DECISIONS.md)" mentions that Trivy was intentionally being made to ignore all vulnerabilites. This is a temporary fix only to pass the build, so I fixed this.
I believed HIGH and CRITICAL vulnerabilities should automatically fail the build and LOW and MEDIUM should pass the build but be reported.
Because Trivy can't have a different exit code for different severities of vulnerabilities I divided the Trivy scan to two portions: one that does a full scan and uploads an artifact with the full results, and a second one that fails the build if a HIGH or CRITICAL vulnerability exists.
I kept ignoring unfixed vulnerabilities, because these can't be actioned upon. This is a tradeoff I made for now, this is not set in stone, of course a vulnerability can be avoided instead of fixed.

# Fixed HIGH vulnerability | Type: bug
While stopping Trivy from ignoring HIGH and CRITICAL vulnerabilites, a HIGH severity vulnerability was found in "starlette" which fastapi uses. As a fix, I upgraded fastapi to a version high enough that includes a fixed version of "starlette". I could have chosen the latest version of fastapi but I chose a more conservative version, as I felt this was outside the scope of the assignment.

# Image naming convention | Type: Needs improvement
This is an architecture choice of mine. I feel commit hashes as image tags are not human readable. Using Semantic Release, each release/prerelease iamge will have their semantic version as a tag which of course matches the git tag. All images will also have the tag: {BRANCH_NAME-BUILD_INCREMENT} and will have the label: org.opencontainers.image.revision=${commit_hash}
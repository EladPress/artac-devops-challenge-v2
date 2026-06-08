# MY ASSESSMENT

## DEPENDENCIES

### scikit-learn 1.8.0 | Type: bugfix
"[DECISIONS.md](DECISIONS.md)" explains under "Dependencies" that the package "scikit-learn" is locked to v1.6.1 because of stability and API breaking in later versions.
I disagree with this descision because the model was "pickled" with scikit-learn v1.8.0, so the package being too old was breaking the application.
My solution was to raise the version in "[requirements.txt](requirements.txt)" to v1.8.0

## Docker Image

# Health Checks | Type: needs improvement
"[DECISIONS.md](DECISIONS.md)" explains under "Docker Image" that both `/health` and `ready` return 200 so either works. That's true for now, because the model loading is baked inside the startup of the server's startup, so it will immediately become ready as soon as it becomes alive. 

I switched the health checks to poll `/ready` because it's the actual condition of the application being ready for use, and it makes the image more robust if further changes to the application separate the startup logic.

# Base image | Type: intentional tradeoff
"[DECISIONS.md](DECISIONS.md)" explains under "Docker Image" that the base image is python:3.12 because the slim was causing issues with some native dependencies during `pip install`. I did not experience any issues the the slim image works just fine. In any case, the reduction in image size is significant and in my opinion is worth a bit of debugging, or a multi stage build.

# .dockerignore | Type: needs improvement
A .dockerignore file was missing, which caused a lot of needless file to be copied into the image, so a "[.dockerignore](.dockerignore)" file was added

# Single-stage build | Type: intentional tradeoff
This is not actually a trade off, the image should not be built with another stage, as there isn't anything that needs to be compiled or built before copying everything into the final image.
Building the project as a whl or any equivalent seems unneccessary because the project is very small and distributing the code itself is not relevant.
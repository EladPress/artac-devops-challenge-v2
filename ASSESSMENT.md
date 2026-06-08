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
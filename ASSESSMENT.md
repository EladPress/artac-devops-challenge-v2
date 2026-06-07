# MY ASSESSMENT

## DEPENDENCIES

### scikit-learn 1.8.0 | Type: bugfix
"[DECISIONS.md](DECISIONS.md)" explains under "DEPENDENCIES" that the package "scikit-learn" is locked to v1.6.1 because of stability and API breaking in later versions.
I disagree with this descision because the model was "pickled" with scikit-learn v1.8.0, so the package being too old was breaking the application.
My solution was to raise the version in "[requirements.txt](requirements.txt)" to v1.8.0
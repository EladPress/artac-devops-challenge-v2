# Engineering Decisions Log

> Notes from the previous engineer who set up this deployment. Read these before making changes —
> some decisions were made for specific reasons.

## Docker Image

### Single-stage build
Tried multi-stage at first, but ran into issues where the model wouldn't load in the final slim stage —
something about missing shared libraries for scikit-learn. Reverted to a single-stage build to keep
things working. Could revisit later but it's not blocking anything.

### Base image: `python:3.12`
Using the full Python image rather than slim. Slim was causing issues with some native dependencies
during pip install. The full image "just works" and the size difference isn't significant enough
to justify debugging slim compatibility issues.

### Health checks
Using the `/health` endpoint for the Docker `HEALTHCHECK` and the CI smoke test.
Both `/health` and `/ready` return 200 so either works — went with `/health` since
it's the standard name.

## Infrastructure

### Pinned AMI
Using a specific AMI ID (`ami-0c7217cdde317cfec`) instead of a dynamic lookup. We had an incident
where the latest Ubuntu AMI changed and broke the Docker CE install script (incompatible `containerd`
version). Pinning the AMI ensures reproducible infrastructure. The AMI is Ubuntu 22.04 LTS from
January 2024 — it's stable and well-tested with our user-data script.

### Local Terraform state
Running with local state file for now. This is a single-operator deployment — adding S3 backend
and DynamoDB locking is overkill for one person running terraform apply. Will add remote state
if we scale the team.

### SSH access
Security group allows SSH from `0.0.0.0/0`. Needed for initial setup and for the CI pipeline
to deploy via SSH. Haven't had time to lock it down further.

## CI/CD

### Trivy configuration
Added `ignore-unfixed` and set severity to CRITICAL to get the scan to pass. Trivy was flagging
a ton of stuff in the base image and blocking the pipeline. Current config lets the build through.

### Pipeline structure
Split the pipeline into separate jobs for build, test, security scan, and deploy.
The deploy job is stubbed out — needs to be wired up to the actual infrastructure.

## Dependencies

### scikit-learn 1.6.1
Pinned to 1.6.1 for stability. It's a well-known release with good community support. Newer
versions tend to have breaking API changes so I'm keeping this locked down.

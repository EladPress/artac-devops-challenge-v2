# Sentiment Analysis API

A FastAPI service that serves a pre-trained scikit-learn sentiment classifier, packaged as a
container image and deployed to AWS via Terraform.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict` | POST | Accepts `{"text": "..."}`, returns `{"sentiment": "positive/negative", "confidence": 0.92}` |
| `/health` | GET | Liveness probe — returns 200 if the server process is running |
| `/ready` | GET | Readiness probe — returns 200 only after the model is loaded and ready to serve |

The service listens on port **8080**.

---

## Repository layout

| Path | Purpose |
|------|---------|
| `app/` | Application source (FastAPI app + model loading) — unmodified |
| `models/` | Pre-trained scikit-learn model — unmodified |
| `tests/` | Unit tests for the API and model |
| `Dockerfile` | Production container image |
| `.dockerignore` | Build-context exclusions |
| `.github/workflows/ci.yml` | CI/CD pipeline (release → build → test/scan/smoke → push → deploy) |
| `terraform/` | AWS infrastructure (EC2 + security group + SSM access) |
| `requirements.txt` | Python dependencies |
| `ASSESSMENT.md` | Assessment of the inherited codebase |
| `AI_WORKFLOW.md` | AI tooling usage documentation |

---

## Run locally (without Docker)

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Then exercise the endpoints:

```bash
curl http://localhost:8080/health
curl http://localhost:8080/ready
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "this movie was fantastic"}'
```

## Run the tests

```bash
pytest tests/ -v
```

---

## Run with Docker

Build the image:

```bash
docker build -t sentiment-api .
```

Run the container:

```bash
docker run -d --name sentiment-api -p 8080:8080 sentiment-api
```

> **Apple Silicon (ARM) Macs:** the published images are built for `linux/amd64` (see
> [ASSESSMENT.md](ASSESSMENT.md)). To run a published image on an ARM Mac, add
> `--platform linux/amd64` to the `docker run` command; Docker Desktop runs it under emulation.

The container has a built-in `HEALTHCHECK` that polls `/ready`, so `docker ps` reports the
container as healthy only once the model is loaded.

---

## Container images

Images are published to GitHub Container Registry by the CI pipeline:

```
ghcr.io/eladpress/artac-devops-challenge-v2
```

Each build is tagged with its semantic version (e.g. `:1.2.0`) and a
`{branch}-{run-number}` tag, and carries an `org.opencontainers.image.revision` label pointing at
the source commit. See the *Image naming convention* finding in [ASSESSMENT.md](ASSESSMENT.md).

---

## Deploy to AWS (Terraform)

The Terraform configuration in [`terraform/`](terraform/) provisions:

- An **EC2 instance** that installs Docker via user-data and runs the container image with a
  `restart unless-stopped` policy.
- A **security group** exposing only the application port (8080). SSH is intentionally not open —
  instance access is via **AWS SSM Session Manager**.
- An **IAM role + instance profile** granting `AmazonSSMManagedInstanceCore` so the instance is
  reachable through SSM.
- An encrypted, right-sized (10 GB, gp3) root volume.

### Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.5.0
- AWS credentials configured (e.g. `aws configure` or environment variables) with permission to
  manage EC2, IAM, and security groups
- The [Session Manager plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)
  for the AWS CLI (only needed to open a shell on the instance)

### Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `aws_region` | `us-east-1` | Region to deploy to (AMI is resolved per-region automatically) |
| `project_name` | `sentiment-api` | Prefix used for resource naming |
| `instance_type` | `t2.micro` | EC2 instance type |
| `app_port` | `8080` | Port the application listens on |
| `docker_image` | *(required)* | Full image reference to deploy, e.g. `ghcr.io/<owner>/<repo>:1.2.0` |
| `app_allowed_cidrs` | `["0.0.0.0/0"]` | CIDRs allowed to reach the application port |

`docker_image` has no default, so a `terraform.tfvars` file (or `-var`) is required. An example:

```hcl
aws_region    = "il-central-1"
instance_type = "t3.micro"
app_port      = 8080
docker_image  = "ghcr.io/eladpress/artac-devops-challenge-v2:1.2.0"
```

### Apply

```bash
cd terraform
terraform init
terraform plan      # validated output committed as terraform/plan-output.txt
terraform apply
```

After `apply`, Terraform prints the relevant outputs:

| Output | Description |
|--------|-------------|
| `app_url` | `http://<public-dns>:8080` — the live application URL |
| `instance_public_ip` / `instance_public_dns` | Instance network addresses |
| `instance_id` | EC2 instance ID |
| `ssm_command` | Ready-to-run `aws ssm start-session` command for shell access |

> If the image is private on GHCR, make it public or configure the instance with registry
> credentials before the user-data `docker pull` will succeed.

### Connect to the instance

There is no SSH and no open port 22. Open a shell via SSM using the `ssm_command` output:

```bash
aws ssm start-session --target <instance-id> --region <aws_region>
```

### Tear down

```bash
terraform destroy
```

---

## CI/CD

The pipeline ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) runs on every push and PR:

1. **release** — semantic-release computes the next version from conventional commits.
2. **build** — builds the image once and uploads it as an artifact.
3. **test / security-scan / smoke-test** — run the unit tests, run a Trivy scan (fails on
   HIGH/CRITICAL, reports the rest), and start the container to verify all three endpoints respond.
4. **push** — only after the above pass, tags and pushes the image to GHCR.
5. **deploy** — gated to `main`; currently a documented placeholder (see [ASSESSMENT.md](ASSESSMENT.md)).

See [ASSESSMENT.md](ASSESSMENT.md) for the rationale behind each pipeline decision and
[AI_WORKFLOW.md](AI_WORKFLOW.md) for how AI tooling was used during this work.
</content>
</invoke>

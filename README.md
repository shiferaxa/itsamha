# itsamha.com

Personal portfolio site — [itsamha.com](https://itsamha.com). Static site on AWS
(S3 + CloudFront), provisioned with Terraform, deployed automatically by GitHub
Actions.

## How it works

- **Site** — plain HTML/CSS/JS in [`website/`](website/). Dark, minimal, no
  frameworks.
- **Certifications** — pulled from
  [Credly](https://www.credly.com/users/amha-shiferaw) at build time by
  [`scripts/fetch_certifications.py`](scripts/fetch_certifications.py), which
  writes `website/certifications.json`. Certs that aren't on Credly (e.g.
  Microsoft Learn) live in [`data/extra-certs.json`](data/extra-certs.json) and
  get merged in. Credly badges marked `Certification` are featured; training
  badges render as a secondary strip.
- **Contact form** — posts to an existing Lambda behind API Gateway
  (see [`lambda/`](lambda/) and [`terraform/`](terraform/)).
- **CI/CD** — [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)
  runs on every push to `main`, on a weekly schedule (so new Credly badges
  appear without a code change), and on manual dispatch. It fetches
  certifications, syncs `website/` to S3, and invalidates CloudFront.

## Deploying

Push to `main`. That's it.

Requires two GitHub Actions secrets (Settings → Secrets and variables →
Actions):

| Secret | Value |
| --- | --- |
| `AWS_ACCESS_KEY_ID` | Access key for the `github-actions-itsamha` IAM user |
| `AWS_SECRET_ACCESS_KEY` | Its secret key |

The IAM user is scoped to exactly two things: syncing the `itsamha.com` bucket
and invalidating the site's CloudFront distribution.

## Local preview

```bash
python scripts/fetch_certifications.py   # refresh certifications.json
cd website && python -m http.server 8000
```

## Infrastructure

Provisioned with Terraform in [`terraform/`](terraform/): S3 (private, OAC),
CloudFront, Route 53, Lambda + API Gateway for the contact form.

```bash
cd terraform
terraform init && terraform plan
```

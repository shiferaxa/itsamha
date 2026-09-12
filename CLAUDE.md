# itsamha.com

Static portfolio site for Amha Shiferaw. HTML, CSS, and vanilla JS in `website/`, served from S3 behind CloudFront, contact form via API Gateway and Lambda. Infrastructure is Terraform.

## Warnings

- `website/certifications.json` is generated. Do not hand edit it. Regenerate with `python scripts/fetch_certifications.py`.
- Amha runs Terraform and AWS CLI commands himself in WSL. Explain them, do not run them, unless asked.
- Every push to `main` deploys the site. There is no staging. Check the diff before pushing.
- Terraform state is remote (S3 bucket `itsamha-tfstate`). Never run `terraform` with a local backend here.
- No em dashes in site copy or commit messages. Commit messages never mention AI.

## Architecture

Visitor -> Route 53 -> CloudFront -> private S3 bucket (`website/`). Contact form -> API Gateway -> Lambda (`lambda/contact-form`) -> SES email.

- `website/index.html` main page, sections for about, architecture diagram, certifications, contact
- `website/resume.html` resume page with a hand written cert list
- `website/script.js` fetches `certifications.json` and renders the featured grid and training badges row, handles the contact form
- `scripts/fetch_certifications.py` pulls badges from Credly at build time and writes `website/certifications.json`
- `data/extra-certs.json` certs not on Credly (Microsoft Learn), merged in by the script
- `lambda/contact-form` contact form handler
- `terraform/` S3, CloudFront, ACM, API Gateway, Lambda, IAM
- `.github/workflows/deploy.yml` fetch certs, sync `website/` to S3, invalidate CloudFront. Runs on push to `main` and weekly.
- `.github/workflows/terraform.yml` plan on PR, apply on `main`, via OIDC role

## Commands

- Preview locally: open `website/index.html` in a browser, or `python -m http.server` from `website/`
- Refresh certs: `python scripts/fetch_certifications.py`
- Deploy: push to `main`
- Terraform (Amha runs these in WSL): `terraform plan` and `terraform apply` from `terraform/`

## Conventions

- Featured cert order is pinned by the `PRIORITY` list in the fetch script: CKA, CKAD, AWS SAA, GCP ACE, Azure Administrator, CCNA, then the rest newest first.
- The `DEMOTE` list forces certs to the very end regardless of date. KCNA is there on purpose, Amha does not want it highlighted. Put other entry level certs there instead of reordering by hand.
- Credly badges typed `Certification` go in the featured grid, everything else goes in the training badges row.
- Dates are not shown on the site, they only drive sort order.
- When adding a cert, also append it to the list in `website/resume.html`. Low priority certs go at the bottom there too.

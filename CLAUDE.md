# itsamha.com

Static portfolio site in `website/`, deployed to S3 + CloudFront by `.github/workflows/deploy.yml` on every push to `main`. Infrastructure is Terraform in `terraform/` (separate `terraform.yml` workflow). Amha runs Terraform and AWS CLI commands himself in WSL, so explain commands instead of running them unless asked.

## Certifications

- `website/certifications.json` is generated, do not hand edit it. Run `python scripts/fetch_certifications.py` to regenerate after any change.
- The script pulls badges from Credly (`credly.com/users/amha-shiferaw`) at build time. Badges typed `Certification` go in the featured grid, everything else goes in the training badges row.
- Certs not on Credly (Microsoft Learn) live in `data/extra-certs.json` and get merged in.
- Featured order is pinned by the `PRIORITY` list in the script: CKA, CKAD, AWS SAA, GCP ACE, Azure Administrator, CCNA, then the rest newest first.
- The `DEMOTE` list in the script forces certs to the very end regardless of date. KCNA is there on purpose, Amha does not want it highlighted. Add other entry level certs there rather than reordering by hand.
- Dates are not displayed on the site, they only drive sort order.
- `website/resume.html` has its own hand written cert list. Keep it in sync when adding a cert, new low priority certs go at the bottom.

## Writing style

No em dashes or en dashes anywhere in site copy or commit messages. Plain language, no AI sounding phrasing. Commit messages never mention Claude or AI.

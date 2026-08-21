#!/usr/bin/env python3
"""One-time setup: create a least-privilege IAM user for GitHub Actions deploys.

Creates user `github-actions-itsamha` that can ONLY:
  - sync objects in s3://itsamha.com
  - create invalidations on the site's CloudFront distribution

Run with admin/root credentials in your environment, then put the printed
key pair into the repo's GitHub Actions secrets (AWS_ACCESS_KEY_ID /
AWS_SECRET_ACCESS_KEY). After that, delete your root access keys — CI never
needs them.

Usage:
  AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... python scripts/setup_deploy_iam.py
"""

import json
import sys

import boto3

USER = "github-actions-itsamha"
BUCKET = "itsamha.com"
ACCOUNT_ID = "825988191458"
DISTRIBUTION_ID = "E1RT76ETYBB5J6"

POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "SyncBucket",
            "Effect": "Allow",
            "Action": ["s3:ListBucket"],
            "Resource": f"arn:aws:s3:::{BUCKET}",
        },
        {
            "Sid": "WriteObjects",
            "Effect": "Allow",
            "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
            "Resource": f"arn:aws:s3:::{BUCKET}/*",
        },
        {
            "Sid": "Invalidate",
            "Effect": "Allow",
            "Action": ["cloudfront:CreateInvalidation"],
            "Resource": f"arn:aws:cloudfront::{ACCOUNT_ID}:distribution/{DISTRIBUTION_ID}",
        },
    ],
}


def main():
    iam = boto3.client("iam")
    try:
        iam.create_user(UserName=USER, Tags=[
            {"Key": "purpose", "Value": "github-actions-deploy-itsamha.com"},
        ])
        print(f"Created IAM user {USER}")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"IAM user {USER} already exists")

    iam.put_user_policy(
        UserName=USER,
        PolicyName="deploy-itsamha-site",
        PolicyDocument=json.dumps(POLICY),
    )
    print("Attached inline policy deploy-itsamha-site")

    existing = iam.list_access_keys(UserName=USER)["AccessKeyMetadata"]
    if existing:
        answer = input(f"{len(existing)} access key(s) exist — delete and recreate? [y/N] ")
        if answer.lower() != "y":
            print("Keeping existing keys; nothing else to do.")
            return 0
        for key in existing:
            iam.delete_access_key(UserName=USER, AccessKeyId=key["AccessKeyId"])
            print("Deleted old key", key["AccessKeyId"])

    key = iam.create_access_key(UserName=USER)["AccessKey"]
    print("\nAdd these to GitHub → repo Settings → Secrets and variables → Actions:\n")
    print(f"  AWS_ACCESS_KEY_ID={key['AccessKeyId']}")
    print(f"  AWS_SECRET_ACCESS_KEY={key['SecretAccessKey']}")
    print("\n(This is the only time the secret is shown.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

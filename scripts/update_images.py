#!/usr/bin/env python3
"""Update Localshops environment images using immutable OCI digests."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
IMAGE = re.compile(r"^[a-zA-Z0-9._:/-]+$")
REVISION = re.compile(r"^[0-9a-f]{40}$")


def replace_image(path: Path, name: str, image: str, digest: str) -> None:
    lines = path.read_text().splitlines()
    found = False
    in_target = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped == f"- name: {name}":
            in_target = True
            found = True
            continue
        if in_target and stripped.startswith("- name:"):
            in_target = False
        if in_target and stripped.startswith("newName:"):
            indentation = line[: len(line) - len(line.lstrip())]
            lines[index] = f"{indentation}newName: {image}"
        if in_target and stripped.startswith("digest:"):
            indentation = line[: len(line) - len(line.lstrip())]
            lines[index] = f"{indentation}digest: {digest}"
            in_target = False
    if not found:
        raise ValueError(f"image {name!r} not found in {path}")
    path.write_text("\n".join(lines) + "\n")


def update_production_migration(
    path: Path, image: str, digest: str, source_revision: str
) -> None:
    content = path.read_text()
    content, name_count = re.subn(
        r"(\n  name: localshops-migrate-)[a-z0-9]+",
        rf"\g<1>{source_revision[:7]}",
        content,
        count=1,
    )
    content, image_count = re.subn(
        r"(\n          image: )[a-zA-Z0-9._:/-]+@sha256:[0-9a-f]{64}",
        rf"\g<1>{image}@{digest}",
        content,
        count=1,
    )
    if name_count != 1 or image_count != 1:
        raise ValueError(f"production migration markers not found in {path}")
    path.write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", choices=("dev", "production"), required=True)
    parser.add_argument("--api-image", required=True)
    parser.add_argument("--api-digest", required=True)
    parser.add_argument("--web-image", required=True)
    parser.add_argument("--web-digest", required=True)
    parser.add_argument("--source-revision", required=True)
    args = parser.parse_args()

    for value in (args.api_image, args.web_image):
        if not IMAGE.fullmatch(value):
            raise ValueError(f"invalid OCI image name: {value}")
    for value in (args.api_digest, args.web_digest):
        if not DIGEST.fullmatch(value):
            raise ValueError(f"invalid OCI digest: {value}")
    if not REVISION.fullmatch(args.source_revision):
        raise ValueError("source revision must be a full Git SHA")

    root = Path(__file__).resolve().parents[1]
    if args.environment == "production":
        production = root / "apps" / "localshops" / "production"
        kustomization = production / "kustomization.yaml"
        replace_image(kustomization, "localshops-api", args.api_image, args.api_digest)
        replace_image(kustomization, "localshops-web", args.web_image, args.web_digest)
        update_production_migration(
            production / "migration.yaml",
            args.api_image,
            args.api_digest,
            args.source_revision,
        )
        return

    overlay = root / "apps" / "localshops" / "overlays" / args.environment
    replace_image(overlay / "migration" / "kustomization.yaml", "localshops-api", args.api_image, args.api_digest)
    replace_image(overlay / "application" / "kustomization.yaml", "localshops-api", args.api_image, args.api_digest)
    replace_image(overlay / "application" / "kustomization.yaml", "localshops-web", args.web_image, args.web_digest)

    release = overlay / "application" / "release.yaml"
    content = release.read_text()
    content, count = re.subn(
        r"(source-revision:\s*)['\"]?[0-9a-f]+['\"]?",
        rf'\g<1>"{args.source_revision}"',
        content,
    )
    if count != 1:
        raise ValueError(f"source-revision marker not found in {release}")
    release.write_text(content)


if __name__ == "__main__":
    main()

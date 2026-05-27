#!/usr/bin/env python3
"""Write the Axiom repository config used by axiom push."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def ttl_string(value: str) -> str:
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )
    return f'"{escaped}"'


def ttl_bool(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return "True"
    if normalized in {"0", "false", "no", "n", "off"}:
        return "False"
    raise ValueError(f"Expected a boolean value, got {value!r}")


def required(name: str) -> str:
    value = env(name)
    if not value:
        raise ValueError(f"{name} is required")
    return value


def main() -> None:
    repository = required("AXIOM_REPOSITORY")
    endpoint = required("AXIOM_REPOSITORY_ENDPOINT")
    username = required("AXIOM_USERNAME")
    password = required("AXIOM_PASSWORD")
    insecure = ttl_bool(env("AXIOM_INSECURE", "false"))
    tls_verify = ttl_bool(env("AXIOM_TLS_VERIFY", "true"))

    config_dir = Path.home() / ".config" / "axiom"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "repository.ttl"

    subject = f"http://example.com/axiom/repository/{quote(repository, safe='')}"
    content = f"""@prefix adms: <http://www.w3.org/ns/adms#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix v: <http://www.w3.org/2006/vcard/ns#> .

<{subject}> a dcat:Catalog ;
    adms:identifier {ttl_string(repository)} ;
    dct:title {ttl_string(repository)} ;
    dct:description "OCI registry configured by the Axiom GitHub Action." ;
    dct:publisher [
        a foaf:Agent ;
        v:fn "GitHub Actions"
    ] ;
    dcat:contactPoint [
        a v:Kind ;
        v:fn "GitHub Actions" ;
        v:hasEmail "actions@github.com"
    ] ;
    dcat:accessURL {ttl_string(endpoint)} ;
    dct:username {ttl_string(username)} ;
    dct:password {ttl_string(password)} ;
    dct:insecure {ttl_string(insecure)} ;
    dct:tls {ttl_string(tls_verify)} .
"""

    config_file.write_text(content, encoding="utf-8")
    print(f"Wrote Axiom repository config to {config_file}")


if __name__ == "__main__":
    main()

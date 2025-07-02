#!/usr/bin/env python3
"""Zedec data sync automation for Debian 12.

This script parses zedec_config.yml and performs the following:
- Fetches sources (git clone or HTTP download).
- Distributes fetched data to additional volumes.
- Pushes data to object storage using rclone if available.
- Generates a JSON manifest.
- Optionally posts manifest details to Codex endpoints.
"""

import os
import subprocess
import sys
import yaml
import json
import uuid
import shutil
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

CONFIG_FILE = Path(__file__).with_name("zedec_config.yml")


def run(cmd):
    """Run shell command and return CompletedProcess."""
    print(f"[cmd] {cmd}")
    return subprocess.run(cmd, shell=True, text=True, capture_output=True)


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def fetch_git(source, target, method):
    ensure_dir(Path(target).parent)
    if method == "clone":
        run(f"git clone {source} {target}")
    else:
        run(f"git {method} {source} {target}")


def fetch_http(source, target, extract=False):
    ensure_dir(target)
    filename = source.split("/")[-1] or "download.tmp"
    temp_path = Path(target) / filename
    run(f"wget -O {temp_path} '{source}'")
    if extract:
        if temp_path.suffix in {".zip"}:
            run(f"unzip -o {temp_path} -d {target}")
        elif temp_path.suffix in {".tar", ".gz", ".tgz", ".bz2"}:
            run(f"tar -xf {temp_path} -C {target}")


def distribute_volume(src, dst):
    src_path = Path(src)
    dst_path = Path(dst)
    ensure_dir(dst_path)
    if src_path.is_dir():
        run(f"rsync -a {src_path}/ {dst_path}/")
    elif src_path.is_file():
        shutil.copy2(src_path, dst_path)


def push_object(source, remote):
    if shutil.which("rclone"):
        run(f"rclone copy {source} {remote}")
    else:
        print("rclone not installed; skipping object push for", source)


def create_manifest(manifest_file, fields):
    data = fields.copy()
    if data.get("cid") == "auto":
        data["cid"] = str(uuid.uuid4())
    ensure_dir(Path(manifest_file).parent)
    with open(manifest_file, "w") as f:
        json.dump(data, f, indent=2)
    return data


def post_codex(manifest_data, codex_cfg):
    if not requests:
        print("requests library not available; skipping codex upload")
        return
    ingest_url = codex_cfg.get("ingest_url")
    declare_url = codex_cfg.get("declare_url")
    payload = codex_cfg.get("payload", {}).copy()
    if payload.get("CID") == "auto":
        payload["CID"] = manifest_data.get("cid")
    if codex_cfg.get("ingest") and ingest_url:
        try:
            resp = requests.post(ingest_url, json=manifest_data)
            print("ingest status", resp.status_code)
        except Exception as e:
            print("ingest failed", e)
    if declare_url:
        try:
            resp = requests.post(declare_url, json=payload)
            print("declare status", resp.status_code)
        except Exception as e:
            print("declare failed", e)


def main():
    if not CONFIG_FILE.exists():
        print("Config file not found:", CONFIG_FILE)
        sys.exit(1)
    with open(CONFIG_FILE) as f:
        cfg = yaml.safe_load(f)
    zedec = cfg.get("zedec", {})

    # fetch sources
    for item in zedec.get("fetch", []):
        if item.get("type") == "git":
            fetch_git(item["source"], item["target"], item.get("method", "clone"))
        elif item.get("type") == "http":
            fetch_http(item["source"], item["target"], item.get("extract", False))

    # distribute volumes
    for vol in zedec.get("distribute", {}).get("volumes", []):
        distribute_volume(vol["from"], vol["to"])

    # object storage push
    obj_push = zedec.get("storage", {}).get("object_push", {})
    for tgt in obj_push.get("targets", []):
        push_object(tgt["source"], tgt["remote"])

    # manifest generation
    manifest_cfg = zedec.get("manifest", {})
    manifest_data = create_manifest(manifest_cfg.get("file", "manifest.json"), manifest_cfg.get("fields", {}))

    # codex upload
    codex_cfg = zedec.get("codex", {})
    post_codex(manifest_data, codex_cfg)


if __name__ == "__main__":
    main()

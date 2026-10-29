# AI381 Lab 2: Bring Your Own Model – Container + CI

![CI](https://github.com/aliayman38/ai381-lab2/actions/workflows/ci.yml/badge.svg)

Containerized FastAPI machine learning inference service built with a multi-stage, non-root `Dockerfile`, automated `pytest` suite, Trivy vulnerability scanning, and automated publishing to GitHub Container Registry (GHCR).

## One-Command Quickstart

Build and start the containerized service on port `8000` with a single command:

```bash
docker build -t ai381-lab2 . && docker run --rm -p 8000:8000 ai381-lab2
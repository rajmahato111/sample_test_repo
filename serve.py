"""
Application entrypoint (fixture).

Intended for static inspection by repo analysis tooling. Runtime execution requires
vLLM and suitable GPU drivers; CI should not depend on running this module.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml
from vllm import LLM, SamplingParams


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    cfg = load_config(Path(__file__).resolve().parent / "config.yaml")
    model_id = cfg["model"]["id"]
    vllm_cfg = cfg["vllm"]

    llm = LLM(
        model=model_id,
        tensor_parallel_size=int(vllm_cfg["tensor_parallel_size"]),
        max_model_len=int(vllm_cfg["max_model_len"]),
        gpu_memory_utilization=float(vllm_cfg["gpu_memory_utilization"]),
        dtype=vllm_cfg.get("dtype", "auto"),
    )
    _ = SamplingParams(temperature=0.7, max_tokens=256)

    print(f"listen {args.host}:{args.port}")


if __name__ == "__main__":
    main()

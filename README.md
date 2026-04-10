# qwen-chat-demo

Small vLLM-based serving layout: one Hugging Face chat model, configuration in YAML, and a Python entrypoint. Intended as a minimal reference for tooling that inspects GitHub repositories (file tree and contents).

## Repository layout

| File | Role |
|------|------|
| `config.yaml` | Model id, vLLM engine settings, and HTTP bind host/port. |
| `Dockerfile` | Image based on `vllm/vllm-openai:v0.4.0`; installs Python deps, copies `config.yaml` and `serve.py`, exposes port 8000. |
| `requirements.txt` | Runtime libraries: `vllm`, `ray[serve]`, `pydantic`, `pyyaml`. |
| `serve.py` | Loads `config.yaml`, builds a vLLM `LLM` instance from `model.id` and the `vllm.*` block, accepts `--host` / `--port`. |

## `config.yaml`

- **`model.id`**: `Qwen/Qwen2-7B-Instruct` (Hugging Face model identifier).
- **`model.trust_remote_code`**: `false`.
- **`vllm`**: `tensor_parallel_size` (1), `max_model_len` (16384), `gpu_memory_utilization` (0.92), `dtype` (`bfloat16`).
- **`server`**: listen address and port (aligned with the container `EXPOSE` / `CMD`).

## `Dockerfile`

Multi-step image: install from `requirements.txt`, copy application config and `serve.py`, set `MODEL_CONFIG=/app/config.yaml`, default command runs `serve.py` on `0.0.0.0:8000`.

## `requirements.txt`

Pins a compatible `vllm` minor range and pulls Ray Serve, Pydantic v2, and PyYAML for config parsing in `serve.py`.

## `serve.py`

Reads `config.yaml` from the application directory, constructs `vllm.LLM` using the YAML `model` and `vllm` sections, and defines CLI overrides for host and port. Running this module requires a GPU-capable environment with vLLM installed; use the Dockerfile or an equivalent CUDA stack for execution.

## Run (optional)

```bash
docker build -t qwen-chat-demo .
docker run --gpus all -p 8000:8000 qwen-chat-demo
```

Adjust GPU flags and drivers to match your host. If you only need a static copy for analysis tools, cloning or mirroring these files without building is sufficient.

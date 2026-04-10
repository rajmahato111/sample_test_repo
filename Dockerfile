# vLLM OpenAI-compatible base image (fixture for repo analysis)
FROM vllm/vllm-openai:v0.4.0

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config.yaml serve.py ./

ENV MODEL_CONFIG=/app/config.yaml

EXPOSE 8000

CMD ["python", "serve.py", "--host", "0.0.0.0", "--port", "8000"]

./bin/ollama serve &
pid=$!

while ! timeout 1 bash -c "echo > /dev/tcp/localhost/11434" 2>/dev/null; do
    echo "Waiting for Ollama to start..."
    sleep 1
done
echo "Ollama started."

echo "Pulling model $LLM_MODEL..."
ollama pull $LLM_MODEL
echo "$LLM_MODEL pulled."

wait $pid

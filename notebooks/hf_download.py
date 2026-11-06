from huggingface_hub import snapshot_download

path = snapshot_download(
    repo_id="shrijayan/gov_myscheme",
    repo_type="dataset",
    local_dir="data/raw/myscheme",
)
print("Downloaded to:", path)
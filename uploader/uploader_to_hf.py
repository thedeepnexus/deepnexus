from huggingface_hub import HfApi

api = HfApi()
api.upload_folder(
    folder_path="./docker",
    repo_id="dasomaru/docker-api",
    repo_type="space",
    token="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"   
)
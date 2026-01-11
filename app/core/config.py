from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    #Environment
    env:str = Field(default="development" , env = "ENV")

    #hf tokens and keys
    hf_api_token: str = Field(..., env ="HF_API_TOKEN")
    hf_base_url: str = Field(
        default="https://router.huggingface.co/v1" ,
        env="HF_BASE_URL"
    )
    hf_model_id: str = Field(
        default="meta-llama/Llama-3.1-8B-Instruct",
        env = "HF_MODEL_ID"
    )

    #cohere
    cohere_api_key: str = Field(..., env="COHERE_API_KEY")

    #pinecone key
    pinecone_api_key: str = Field(..., env="PINECONE_API_KEY")
    pinecone_environment: str = Field(..., env="PINECONE_ENVIRONMENT")
    pinecone_index_name: str = Field(..., env="PINECONE_INDEX_NAME")

    class Config:
        env_file = ".env",
        extra = "ignore"

settings = Settings()
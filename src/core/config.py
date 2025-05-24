#!/usr/bin/env python3
"""
設定管理モジュール
"""

import os
from typing import Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # API Keys
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    tavily_api_key: str = Field(..., env="TAVILY_API_KEY")
    weather_api_key: str = Field(..., env="WEATHER_API_KEY")
    
    # LLM Configuration
    default_model: str = Field("gpt-4", env="DEFAULT_MODEL")
    temperature: float = Field(0.7, env="TEMPERATURE")
    max_tokens: int = Field(2000, env="MAX_TOKENS")
    
    # Application Settings
    debug: bool = Field(False, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    output_dir: str = Field("./outputs", env="OUTPUT_DIR")
    
    # Web UI Settings
    streamlit_server_port: int = Field(8501, env="STREAMLIT_SERVER_PORT")
    streamlit_server_headless: bool = Field(True, env="STREAMLIT_SERVER_HEADLESS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()

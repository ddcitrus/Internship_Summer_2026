"""
全局配置模块
使用 pydantic-settings 管理所有配置项，支持从 .env 文件和环境变量读取
加载优先级：环境变量（系统级别）> .env 文件 > 代码中的默认值
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用全局配置"""

    # ---------- 应用基础配置 ----------
    APP_NAME: str = "RSOD Agent Platform"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # ---------- PostgreSQL 数据库配置 ----------
    # 直接使用统一连接字符串（优先级最高）
    DATABASE_URL: Optional[str] = None

    # 分解配置（若 DATABASE_URL 未设置，则由这些字段组装）
    DB_HOST: str = "localhost"
    DB_PORT: int = 5658          # 与 docker-compose 映射端口一致
    DB_NAME: str = "agent"       # docker-compose 中 POSTGRES_DB
    DB_USER: str = "admin"       # docker-compose 中 POSTGRES_USER
    DB_PASSWORD: str = "ltz78911"  # docker-compose 中 POSTGRES_PASSWORD

    @property
    def database_url(self) -> str:
        """返回最终使用的数据库连接字符串"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # ---------- Redis 配置 ----------
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None  # 默认无密码
    REDIS_DB: int = 0

    @property
    def redis_url(self) -> str:
        """构造 Redis 连接字符串"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # ---------- MinIO 对象存储配置 ----------
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "rsod-images"   # 与 .env 一致
    MINIO_SECURE: bool = False          # 开发环境关闭 TLS

    # ---------- LLM 相关配置 ----------
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"

    # Qwen (DashScope)
    QWEN_API_KEY: Optional[str] = None
    QWEN_API_URL: str = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    QWEN_BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    # Ollama (本地)
    USE_LOCAL_LLM: bool = False
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:7b"

    # ---------- JWT 认证配置 ----------
    JWT_SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ---------- CORS 配置 ----------
    ALLOWED_ORIGINS: str = (
        "http://localhost:3000,http://localhost:5173,http://localhost:8080"
    )

    @property
    def cors_origins_list(self) -> list:
        """将 CORS 配置字符串转为列表"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        """Pydantic 配置"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        # 允许额外字段，便于未来扩展
        extra = "ignore"


# 创建全局单例，其他模块直接 import 使用
settings = Settings()
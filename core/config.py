from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import AnyHttpUrl,field_validator,Field
from typing import List,Union


class Settings(BaseSettings):
    project_name:str="AI Integrated Content Manager"
    version:str="v1.0"
    ai_v1_str:str="/api/v1"

    allowed_origins:List[AnyHttpUrl]=Field(... ,validation_alias="ALLOWED_ORIGINS")
    anthropic_api_key:str=Field(... , validation_alias="ANTHROPIC_API_KEY")

    database_url:str=Field(... , validation_alias="DATABASE_URL")
    secret_key:str=Field(... ,validation_alias="SECRET_KEY")
    production:bool=False

    @field_validator("allowed_origins",mode="before")
    @classmethod
    def validation_origin(cls,value:Union[str,List[str]])->List[str]:
        if isinstance(value,list):
            return value
        if isinstance(value,str):
            if value.startswith("[") and value.endswith("]"):
                return[item.strip("'/") for item in value[1:-1].split(",")]
            return[value.strip()]
        raise ValueError("data inserted is invalid")
    
    model_config=SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    ) 
settings=Settings()              
                          
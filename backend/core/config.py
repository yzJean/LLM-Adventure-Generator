from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

# map environment variables to python through the Settings class attributes. This allows us to easily manage configuration settings for our application. For example, if there's a new variable in .env but it is not specified in the Settings class attributes, it will be ignored and won't cause any issues in the application. This is useful for maintaining a clean and organized configuration management system, as we can easily add or remove settings without affecting the overall functionality of the application. Additionally, using Pydantic's BaseSettings allows us to take advantage of features like type validation and default values, which can help prevent errors and improve the robustness of our application.
class Settings(BaseSettings):
    API_PREFIX: str = "/api" # default prefix for all API endpoints, e.g., /api/generate-story
    DEBUG: bool = False
    DATABASE_URL: str
    ALLOWED_ORIGINS: str = ""
    OPENAI_API_KEY: str
    GEMINI_API_KEY: str
    # parse the ALLOWED_ORIGINS string from the .env file into a list of origins because .env doesn't support list type, so we need to parse it manually. The field_validator decorator is used to define a validation function for the ALLOWED_ORIGINS field. This function takes the string value from the .env file, splits it by commas, and returns a list of origins. If the string is empty, it returns an empty list. This allows us to easily manage CORS settings in our application by simply updating the ALLOWED_ORIGINS variable in the .env file.
    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return v.split(",") if v else []

    class Config:
        env_file = ".env" # specify the .env file to load environment variables from
        env_file_encoding = "utf-8" # specify the encoding of the .env file
        case_sensitive = True # make environment variable names case-sensitive
        
settings = Settings() # create an instance of the Settings class to access the configuration settings throughout the application
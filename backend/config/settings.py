from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY : str = "28h49r4024hf248hf0g84t79gygrfhbnrweiqujh0q83390u2qhn0821jsq"
    ALGORITHM : str= "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 60
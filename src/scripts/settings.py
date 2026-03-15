from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path
import yaml
from functools import lru_cache
from typing import Annotated
from fastapi import Depends

class WindowsSettings(BaseModel):
    host: str = '127.0.0.1'
    port: int = 8000

class LinuxSettings(BaseModel):
    socket:str = '/tmp/moris/maldc.sock'

class ApiSettings(BaseModel):
    use_uds: bool = False
    linux: LinuxSettings = LinuxSettings()
    windows: WindowsSettings = WindowsSettings()

class RandomSpritesWeightSettings(BaseModel):
    common: int = 4
    uncommon: int = 3
    rare: int = 1

class MatrixSettings(BaseModel):
    rows: int = 8
    columns: int = 8
    random_sprites_before_sleep: int = 3
    random_sprite_interval_sec: int = 5
    random_sprites_weights: RandomSpritesWeightSettings = RandomSpritesWeightSettings()
    flip_every_other_row: bool = True
    spritesheet_framerate: float = 0.1
    brightness: float = 0.2
    sprites_folder: str = "storage/sprites"
    
class BuzzerSettings(BaseModel):
    pin: int = 23

class LCDSettings(BaseModel):
    line_count: int = 2
    line_length: int = 16
    backlight_enabled_by_default: bool = False
    long_wait_list: list[str] = [",", ".", "?", "!", ":", "\n"]
    wait_time: float = 0.05
    long_wait_time: float = 0.1
    next_screen_wait_time: float = 1


class Settings(BaseSettings):
    api: ApiSettings = ApiSettings()
    matrix: MatrixSettings = MatrixSettings()
    buzzer: BuzzerSettings = BuzzerSettings()
    lcd: LCDSettings = LCDSettings()

@lru_cache()
def load_settings(path_to_settings: Path = None) -> Settings:
    config_path = path_to_settings
    if not path_to_settings: 
        config_path = Path(__file__).resolve().parents[2] / "config.yaml"
    
    if not config_path.exists():
        settings = Settings()     
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            yaml.dump(settings.model_dump(), f, default_flow_style=False)

    with open(config_path, "r") as f:
        config_dict = yaml.safe_load(f)
    
    return Settings(**config_dict)

SettingsDep = Annotated[Settings, Depends(load_settings)]
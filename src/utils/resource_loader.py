import os
import configparser
from pathlib import Path
from src.core import PetState


def load_animation(state):
    """加载指定状态的动画序列"""
    print(state)
    animation_dir = Path("assets/animations")

    state_dirs = {
        PetState.IDLE: "idle",
        PetState.WALKING: "walk",
        PetState.SLEEPING: "sleep",
        PetState.EATING: "eat",
        PetState.TALK:"talk",
        PetState.FALL_ASLEEP: "fall_asleep",
    }
    
    if state not in state_dirs:
        return []
    
    state_dir = animation_dir / state_dirs[state]
    if not state_dir.exists():
        return []
    
    # 获取目录中的所有图片文件并按文件名排序
    frames = sorted(
        [str(f) for f in state_dir.iterdir() if f.is_file() and f.suffix in [".png", ".gif"]],
        key=lambda x: os.path.basename(x)
    )
    return frames

def load_config():
    """加载配置文件"""
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    # 设置默认值
    if not config.has_section("General"):
        config.add_section("General")
        config.set("General", "start_hidden", "False")
        config.set("General", "animation_speed", "100")
    
    return config
"""
Утилиты для загрузки конфигураций
"""
import yaml
import os
from typing import Dict, Any, Optional
from pathlib import Path
from loguru import logger


class ConfigLoader:
    """Загрузчик конфигураций из YAML файлов"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        if not self.config_dir.exists():
            raise FileNotFoundError(f"Директория конфигураций не найдена: {config_dir}")
    
    def load_agents_config(self) -> Dict[str, Any]:
        """Загрузить конфигурацию агентов"""
        config_file = self.config_dir / "agents_config.yaml"
        
        if not config_file.exists():
            raise FileNotFoundError(f"Файл конфигурации агентов не найден: {config_file}")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            logger.info(f"Загружена конфигурация агентов из {config_file}")
            return config
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке конфигурации агентов: {e}")
            raise
    
    def load_interactions_config(self) -> Dict[str, Any]:
        """Загрузить конфигурацию взаимодействий"""
        config_file = self.config_dir / "interactions.yaml"
        
        if not config_file.exists():
            raise FileNotFoundError(f"Файл конфигурации взаимодействий не найден: {config_file}")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            logger.info(f"Загружена конфигурация взаимодействий из {config_file}")
            return config
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке конфигурации взаимодействий: {e}")
            raise
    
    def load_all_configs(self) -> Dict[str, Any]:
        """Загрузить все конфигурации"""
        return {
            "agents": self.load_agents_config(),
            "interactions": self.load_interactions_config()
        }
    
    def save_config(self, config: Dict[str, Any], filename: str) -> None:
        """Сохранить конфигурацию в файл"""
        config_file = self.config_dir / filename
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            
            logger.info(f"Конфигурация сохранена в {config_file}")
            
        except Exception as e:
            logger.error(f"Ошибка при сохранении конфигурации: {e}")
            raise


def get_api_key() -> Optional[str]:
    """Получить API ключ из переменных окружения"""
    # Проверяем различные варианты переменных окружения
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not api_key:
        logger.warning("API ключ не найден в переменных окружения")
        return None
    
    return api_key 
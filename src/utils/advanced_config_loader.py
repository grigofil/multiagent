"""
Расширенный загрузчик конфигураций с поддержкой различных LLM провайдеров
"""
import yaml
import os
from typing import Dict, Any, Optional, List
from pathlib import Path
from pydantic import BaseModel, Field, validator
from loguru import logger


class ModelConfig(BaseModel):
    """Конфигурация модели LLM"""
    provider: str
    model_name: str
    temperature: float = Field(ge=0.0, le=2.0, default=0.1)
    max_tokens: int = Field(ge=1, le=32000, default=4000)
    top_p: float = Field(ge=0.0, le=1.0, default=0.9)
    frequency_penalty: float = Field(ge=-2.0, le=2.0, default=0.0)
    presence_penalty: float = Field(ge=-2.0, le=2.0, default=0.0)


class AgentConfig(BaseModel):
    """Расширенная конфигурация агента"""
    name: str
    role: str
    description: str
    model: ModelConfig
    system_prompt: str
    prompt_template: Optional[str] = None
    capabilities: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    
    @validator('prompt_template')
    def validate_prompt_template(cls, v):
        if v is not None:
            valid_templates = [
                "data_analysis", "code_generation", "code_review",
                "project_management", "idea_generation", "quality_assessment"
            ]
            if v not in valid_templates:
                raise ValueError(f"Неизвестный шаблон промпта: {v}")
        return v


class ProviderConfig(BaseModel):
    """Конфигурация провайдера LLM"""
    name: str
    models: List[str]
    api_base: str
    api_key_env: str = "OPENAI_API_KEY"


class SecurityConfig(BaseModel):
    """Конфигурация безопасности"""
    max_input_length: int = 10000
    max_output_length: int = 8000
    content_filtering: bool = True
    rate_limiting: Dict[str, int] = Field(default_factory=dict)


class AdvancedConfigLoader:
    """Расширенный загрузчик конфигураций"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        if not self.config_dir.exists():
            raise FileNotFoundError(f"Директория конфигураций не найдена: {config_dir}")
        
        self._agents_config = None
        self._interactions_config = None
        self._providers_config = None
        self._security_config = None
    
    def load_agents_config(self) -> Dict[str, Any]:
        """Загрузить и валидировать конфигурацию агентов"""
        if self._agents_config is None:
            config_file = self.config_dir / "agents_config.yaml"
            
            if not config_file.exists():
                raise FileNotFoundError(f"Файл конфигурации агентов не найден: {config_file}")
            
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    raw_config = yaml.safe_load(f)
                
                # Валидируем конфигурацию агентов
                agents = {}
                for agent_id, agent_data in raw_config.get("agents", {}).items():
                    try:
                        agent_config = AgentConfig(**agent_data)
                        agents[agent_id] = agent_config.dict()
                    except Exception as e:
                        logger.error(f"Ошибка валидации агента {agent_id}: {e}")
                        raise
                
                # Загружаем дополнительные настройки
                self._agents_config = {
                    "agents": agents,
                    "default_settings": raw_config.get("default_settings", {}),
                    "supported_providers": raw_config.get("supported_providers", {}),
                    "security": raw_config.get("security", {})
                }
                
                logger.info(f"Загружена расширенная конфигурация агентов из {config_file}")
                logger.info(f"Валидировано агентов: {len(agents)}")
                
            except Exception as e:
                logger.error(f"Ошибка при загрузке конфигурации агентов: {e}")
                raise
        
        return self._agents_config
    
    def load_interactions_config(self) -> Dict[str, Any]:
        """Загрузить конфигурацию взаимодействий"""
        if self._interactions_config is None:
            config_file = self.config_dir / "interactions.yaml"
            
            if not config_file.exists():
                raise FileNotFoundError(f"Файл конфигурации взаимодействий не найден: {config_file}")
            
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    self._interactions_config = yaml.safe_load(f)
                
                logger.info(f"Загружена конфигурация взаимодействий из {config_file}")
                
            except Exception as e:
                logger.error(f"Ошибка при загрузке конфигурации взаимодействий: {e}")
                raise
        
        return self._interactions_config
    
    def get_provider_config(self, provider_name: str) -> Optional[ProviderConfig]:
        """Получить конфигурацию провайдера"""
        agents_config = self.load_agents_config()
        providers = agents_config.get("supported_providers", {})
        
        if provider_name not in providers:
            logger.warning(f"Провайдер '{provider_name}' не найден в конфигурации")
            return None
        
        try:
            provider_data = providers[provider_name]
            return ProviderConfig(
                name=provider_data.get("name", provider_name),
                models=provider_data.get("models", []),
                api_base=provider_data.get("api_base", ""),
                api_key_env=provider_data.get("api_key_env", f"{provider_name.upper()}_API_KEY")
            )
        except Exception as e:
            logger.error(f"Ошибка при создании конфигурации провайдера {provider_name}: {e}")
            return None
    
    def get_security_config(self) -> SecurityConfig:
        """Получить конфигурацию безопасности"""
        if self._security_config is None:
            agents_config = self.load_agents_config()
            security_data = agents_config.get("security", {})
            
            try:
                self._security_config = SecurityConfig(**security_data)
            except Exception as e:
                logger.error(f"Ошибка при создании конфигурации безопасности: {e}")
                # Используем значения по умолчанию
                self._security_config = SecurityConfig()
        
        return self._security_config
    
    def validate_agent_config(self, agent_id: str) -> bool:
        """Валидировать конфигурацию конкретного агента"""
        try:
            agents_config = self.load_agents_config()
            agents = agents_config.get("agents", {})
            
            if agent_id not in agents:
                logger.error(f"Агент '{agent_id}' не найден в конфигурации")
                return False
            
            agent_data = agents[agent_id]
            
            # Проверяем наличие обязательных полей
            required_fields = ["name", "role", "model", "system_prompt"]
            for field in required_fields:
                if field not in agent_data:
                    logger.error(f"Поле '{field}' отсутствует в конфигурации агента {agent_id}")
                    return False
            
            # Проверяем конфигурацию модели
            model_config = agent_data["model"]
            if "provider" not in model_config or "model_name" not in model_config:
                logger.error(f"Некорректная конфигурация модели для агента {agent_id}")
                return False
            
            # Проверяем поддержку провайдера
            provider_name = model_config["provider"]
            provider_config = self.get_provider_config(provider_name)
            if provider_config is None:
                logger.error(f"Провайдер '{provider_name}' не поддерживается для агента {agent_id}")
                return False
            
            # Проверяем поддержку модели
            model_name = model_config["model_name"]
            if model_name not in provider_config.models:
                logger.warning(f"Модель '{model_name}' может не поддерживаться провайдером '{provider_name}'")
            
            logger.info(f"Конфигурация агента '{agent_id}' валидна")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка валидации агента {agent_id}: {e}")
            return False
    
    def get_agent_capabilities(self, agent_id: str) -> List[str]:
        """Получить возможности агента"""
        agents_config = self.load_agents_config()
        agents = agents_config.get("agents", {})
        
        if agent_id not in agents:
            logger.warning(f"Агент '{agent_id}' не найден")
            return []
        
        return agents[agent_id].get("capabilities", [])
    
    def get_agent_limitations(self, agent_id: str) -> List[str]:
        """Получить ограничения агента"""
        agents_config = self.load_agents_config()
        agents = agents_config.get("agents", {})
        
        if agent_id not in agents:
            logger.warning(f"Агент '{agent_id}' не найден")
            return []
        
        return agents[agent_id].get("limitations", [])
    
    def get_supported_providers(self) -> List[str]:
        """Получить список поддерживаемых провайдеров"""
        agents_config = self.load_agents_config()
        return list(agents_config.get("supported_providers", {}).keys())
    
    def get_provider_models(self, provider_name: str) -> List[str]:
        """Получить список моделей провайдера"""
        provider_config = self.get_provider_config(provider_name)
        if provider_config is None:
            return []
        
        return provider_config.models
    
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
    
    def validate_all_configs(self) -> Dict[str, bool]:
        """Валидировать все конфигурации"""
        results = {}
        
        try:
            # Валидируем конфигурацию агентов
            agents_config = self.load_agents_config()
            agents = agents_config.get("agents", {})
            
            for agent_id in agents.keys():
                results[f"agent_{agent_id}"] = self.validate_agent_config(agent_id)
            
            # Валидируем конфигурацию взаимодействий
            interactions_config = self.load_interactions_config()
            workflows = interactions_config.get("workflows", {})
            
            for workflow_id in workflows.keys():
                results[f"workflow_{workflow_id}"] = True  # Простая проверка наличия
            
            logger.info(f"Валидация завершена: {sum(results.values())}/{len(results)} проверок прошли успешно")
            
        except Exception as e:
            logger.error(f"Ошибка при валидации конфигураций: {e}")
            results["validation_error"] = False
        
        return results 
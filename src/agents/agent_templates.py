"""
Система шаблонов для быстрого создания новых агентов
Позволяет легко добавлять новые роли агентов через конфигурацию
"""
from typing import Dict, Any, List, Optional, Type
from dataclasses import dataclass
from abc import ABC, abstractmethod
import yaml
from pathlib import Path
from loguru import logger

from .base_agent import BaseAgent, AgentConfig


@dataclass
class AgentTemplate:
    """Шаблон для создания агента"""
    name: str
    base_type: str
    description: str
    customizations: Dict[str, Any]
    required_capabilities: List[str]
    optional_capabilities: List[str]
    dependencies: List[str] = None


class AgentTemplateManager:
    """Менеджер шаблонов агентов"""
    
    def __init__(self, templates_dir: str = "config/templates"):
        self.templates_dir = Path(templates_dir)
        self.templates: Dict[str, AgentTemplate] = {}
        self.load_templates()
    
    def load_templates(self) -> None:
        """Загрузить шаблоны из файлов"""
        if not self.templates_dir.exists():
            self.templates_dir.mkdir(parents=True, exist_ok=True)
            self.create_default_templates()
        
        for template_file in self.templates_dir.glob("*.yaml"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = yaml.safe_load(f)
                
                template = AgentTemplate(
                    name=template_data['name'],
                    base_type=template_data['base_type'],
                    description=template_data['description'],
                    customizations=template_data.get('customizations', {}),
                    required_capabilities=template_data.get('required_capabilities', []),
                    optional_capabilities=template_data.get('optional_capabilities', []),
                    dependencies=template_data.get('dependencies', [])
                )
                
                # Используем имя файла без расширения как ключ
                template_key = template_file.stem
                self.templates[template_key] = template
                logger.info(f"Загружен шаблон агента: {template.name}")
                
            except Exception as e:
                logger.error(f"Ошибка загрузки шаблона {template_file}: {e}")
    
    def create_default_templates(self) -> None:
        """Создать шаблоны по умолчанию"""
        default_templates = {
            "junior_analyst": {
                "name": "Junior Data Analyst",
                "base_type": "analyst",
                "description": "Младший аналитик данных для базовых задач",
                "customizations": {
                    "temperature": 0.1,
                    "max_tokens": 2000,
                    "capabilities": ["basic_data_analysis", "simple_reporting"]
                },
                "required_capabilities": ["data_analysis"],
                "optional_capabilities": ["visualization", "statistical_analysis"]
            },
            "senior_developer": {
                "name": "Senior Software Developer",
                "base_type": "coder",
                "description": "Старший разработчик с архитектурными навыками",
                "customizations": {
                    "temperature": 0.1,
                    "max_tokens": 8000,
                    "capabilities": ["architecture_design", "system_design", "mentoring"]
                },
                "required_capabilities": ["code_generation", "code_review"],
                "optional_capabilities": ["performance_optimization", "security_review"]
            },
            "security_expert": {
                "name": "Security Expert",
                "base_type": "security",
                "description": "Эксперт по кибербезопасности",
                "customizations": {
                    "temperature": 0.05,
                    "max_tokens": 5000,
                    "capabilities": ["penetration_testing", "compliance_audit", "incident_response"]
                },
                "required_capabilities": ["security_analysis"],
                "optional_capabilities": ["threat_modeling", "vulnerability_assessment"]
            }
        }
        
        for template_name, template_data in default_templates.items():
            template_file = self.templates_dir / f"{template_name}.yaml"
            with open(template_file, 'w', encoding='utf-8') as f:
                yaml.dump(template_data, f, default_flow_style=False, allow_unicode=True)
    
    def get_template(self, template_name: str) -> Optional[AgentTemplate]:
        """Получить шаблон по имени"""
        return self.templates.get(template_name)
    
    def list_templates(self) -> List[str]:
        """Получить список доступных шаблонов"""
        return list(self.templates.keys())
    
    def create_agent_from_template(self, template_name: str, custom_config: Dict[str, Any] = None) -> AgentConfig:
        """Создать конфигурацию агента из шаблона"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Шаблон {template_name} не найден")
        
        # Базовая конфигурация
        base_config = self._get_base_config(template.base_type)
        
        # Применяем кастомизации шаблона
        config = self._apply_template_customizations(base_config, template.customizations)
        
        # Применяем дополнительные кастомизации
        if custom_config:
            config = self._apply_custom_config(config, custom_config)
        
        return AgentConfig(**config)
    
    def _get_base_config(self, base_type: str) -> Dict[str, Any]:
        """Получить базовую конфигурацию для типа агента"""
        # Загружаем базовую конфигурацию из основного файла
        config_file = Path("config/extended_agents_config.yaml")
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
                return config_data['agents'].get(base_type, {})
        
        # Fallback конфигурация
        return {
            "name": f"{base_type.title()} Agent",
            "role": f"{base_type.title()}",
            "description": f"Агент типа {base_type}",
            "model": {
                "provider": "openai",
                "model_name": "gpt-4",
                "temperature": 0.2,
                "max_tokens": 4000,
                "top_p": 0.9
            },
            "system_prompt": f"Ты агент типа {base_type}.",
            "capabilities": [],
            "limitations": []
        }
    
    def _apply_template_customizations(self, base_config: Dict[str, Any], customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Применить кастомизации шаблона к базовой конфигурации"""
        config = base_config.copy()
        
        # Обновляем модель
        if 'model' in customizations:
            config['model'].update(customizations['model'])
        
        # Обновляем возможности
        if 'capabilities' in customizations:
            config['capabilities'] = customizations['capabilities']
        
        # Обновляем другие параметры
        for key, value in customizations.items():
            if key not in ['model', 'capabilities']:
                config[key] = value
        
        return config
    
    def _apply_custom_config(self, config: Dict[str, Any], custom_config: Dict[str, Any]) -> Dict[str, Any]:
        """Применить пользовательские кастомизации"""
        result = config.copy()
        
        # Глубокое слияние конфигураций
        for key, value in custom_config.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key].update(value)
            else:
                result[key] = value
        
        return result


class DynamicAgentCreator:
    """Создатель динамических агентов"""
    
    def __init__(self, template_manager: AgentTemplateManager):
        self.template_manager = template_manager
        self.agent_registry: Dict[str, Type[BaseAgent]] = {}
    
    def register_agent_type(self, agent_type: str, agent_class: Type[BaseAgent]) -> None:
        """Зарегистрировать новый тип агента"""
        self.agent_registry[agent_type] = agent_class
        logger.info(f"Зарегистрирован тип агента: {agent_type}")
    
    def create_dynamic_agent(self, agent_config: AgentConfig, api_key: str = None) -> BaseAgent:
        """Создать агента динамически на основе конфигурации"""
        # Пробуем найти по роли
        agent_type = agent_config.role.lower().replace(" ", "_")
        
        if agent_type in self.agent_registry:
            agent_class = self.agent_registry[agent_type]
            return agent_class(agent_config, api_key)
        
        # Пробуем найти по имени
        agent_name = agent_config.name.lower().replace(" ", "_")
        if agent_name in self.agent_registry:
            agent_class = self.agent_registry[agent_name]
            return agent_class(agent_config, api_key)
        
        # Если тип не зарегистрирован, создаем универсального агента
        return UniversalAgent(agent_config, api_key)
    
    def create_agent_from_template(self, template_name: str, custom_config: Dict[str, Any] = None, api_key: str = None) -> BaseAgent:
        """Создать агента из шаблона"""
        agent_config = self.template_manager.create_agent_from_template(template_name, custom_config)
        return self.create_dynamic_agent(agent_config, api_key)


class UniversalAgent(BaseAgent):
    """Универсальный агент для новых типов"""
    
    async def process(self, input_data: Any) -> str:
        """Универсальная обработка входных данных"""
        if isinstance(input_data, dict):
            # Используем конфигурацию агента для определения обработки
            context = input_data.get("context", "Универсальная обработка")
            requirements = input_data.get("requirements", "Обработай данные согласно роли агента")
            
            template_vars = {
                "input_data": input_data,
                "context": context,
                "requirements": requirements,
                "agent_role": self.config.role,
                "agent_capabilities": self.config.capabilities
            }
            
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "input_data": input_data,
                "context": "Универсальная обработка",
                "requirements": "Обработай данные согласно роли агента",
                "agent_role": self.config.role,
                "agent_capabilities": self.config.capabilities
            }
            
            return await self._generate_response("", template_vars)


class AgentRoleManager:
    """Менеджер ролей агентов"""
    
    def __init__(self):
        self.roles: Dict[str, Dict[str, Any]] = {}
        self.role_hierarchy: Dict[str, List[str]] = {}
        self.load_role_definitions()
    
    def load_role_definitions(self) -> None:
        """Загрузить определения ролей"""
        role_file = Path("config/agent_roles.yaml")
        if role_file.exists():
            with open(role_file, 'r', encoding='utf-8') as f:
                role_data = yaml.safe_load(f)
                self.roles = role_data.get('roles', {})
                self.role_hierarchy = role_data.get('hierarchy', {})
    
    def get_role_requirements(self, role: str) -> Dict[str, Any]:
        """Получить требования для роли"""
        return self.roles.get(role, {})
    
    def get_role_hierarchy(self, role: str) -> List[str]:
        """Получить иерархию ролей"""
        return self.role_hierarchy.get(role, [])
    
    def validate_agent_for_role(self, agent: BaseAgent, role: str) -> bool:
        """Проверить, подходит ли агент для роли"""
        role_requirements = self.get_role_requirements(role)
        required_capabilities = role_requirements.get('required_capabilities', [])
        
        for capability in required_capabilities:
            if capability not in agent.config.capabilities:
                return False
        
        return True
    
    def suggest_agent_improvements(self, agent: BaseAgent, role: str) -> List[str]:
        """Предложить улучшения для агента в контексте роли"""
        role_requirements = self.get_role_requirements(role)
        required_capabilities = role_requirements.get('required_capabilities', [])
        suggested_capabilities = role_requirements.get('suggested_capabilities', [])
        
        improvements = []
        
        # Проверяем недостающие обязательные возможности
        for capability in required_capabilities:
            if capability not in agent.config.capabilities:
                improvements.append(f"Добавить обязательную возможность: {capability}")
        
        # Предлагаем дополнительные возможности
        for capability in suggested_capabilities:
            if capability not in agent.config.capabilities:
                improvements.append(f"Рассмотреть добавление возможности: {capability}")
        
        return improvements 
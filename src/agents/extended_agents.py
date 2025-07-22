"""
Расширенные специализированные агенты для Итерации №4
Дополнительные роли агентов с различными специализациями
"""
from typing import Any, Dict, List, Optional
from .base_agent import BaseAgent, AgentConfig
from loguru import logger


class DatabaseAgent(BaseAgent):
    """Агент для работы с базами данных"""
    
    async def process(self, input_data: Any) -> str:
        """Обработка запросов к базам данных"""
        if isinstance(input_data, dict):
            template_vars = {
                "query_type": input_data.get("query_type", "select"),
                "table": input_data.get("table", ""),
                "columns": input_data.get("columns", "*"),
                "conditions": input_data.get("conditions", ""),
                "database_type": input_data.get("database_type", "postgresql"),
                "context": input_data.get("context", "Общий запрос к БД")
            }
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "query_type": "select",
                "table": "unknown",
                "columns": "*",
                "conditions": "",
                "database_type": "postgresql",
                "context": "Запрос к базе данных"
            }
            return await self._generate_response("", template_vars)


class ImageAnalysisAgent(BaseAgent):
    """Агент для анализа изображений"""
    
    async def process(self, input_data: Any) -> str:
        """Анализ изображений и извлечение информации"""
        if isinstance(input_data, dict):
            template_vars = {
                "image_url": input_data.get("image_url", ""),
                "analysis_type": input_data.get("analysis_type", "general"),
                "features": input_data.get("features", ["objects", "text", "faces"]),
                "context": input_data.get("context", "Общий анализ изображения"),
                "requirements": input_data.get("requirements", "Опиши содержимое изображения")
            }
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "image_url": str(input_data),
                "analysis_type": "general",
                "features": ["objects", "text", "faces"],
                "context": "Анализ изображения",
                "requirements": "Опиши содержимое изображения"
            }
            return await self._generate_response("", template_vars)


class APIAgent(BaseAgent):
    """Агент для работы с внешними API"""
    
    async def process(self, input_data: Any) -> str:
        """Взаимодействие с внешними API"""
        if isinstance(input_data, dict):
            template_vars = {
                "api_endpoint": input_data.get("api_endpoint", ""),
                "method": input_data.get("method", "GET"),
                "parameters": input_data.get("parameters", {}),
                "headers": input_data.get("headers", {}),
                "context": input_data.get("context", "API запрос"),
                "expected_response": input_data.get("expected_response", "json")
            }
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "api_endpoint": str(input_data),
                "method": "GET",
                "parameters": {},
                "headers": {},
                "context": "API запрос",
                "expected_response": "json"
            }
            return await self._generate_response("", template_vars)


class MachineLearningAgent(BaseAgent):
    """Агент для машинного обучения"""
    
    async def process(self, input_data: Any) -> str:
        """Работа с ML моделями и алгоритмами"""
        if isinstance(input_data, dict):
            template_vars = {
                "task_type": input_data.get("task_type", "classification"),
                "algorithm": input_data.get("algorithm", "random_forest"),
                "data_description": input_data.get("data_description", ""),
                "hyperparameters": input_data.get("hyperparameters", {}),
                "evaluation_metrics": input_data.get("evaluation_metrics", ["accuracy"]),
                "context": input_data.get("context", "ML задача")
            }
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "task_type": "classification",
                "algorithm": "random_forest",
                "data_description": str(input_data),
                "hyperparameters": {},
                "evaluation_metrics": ["accuracy"],
                "context": "ML задача"
            }
            return await self._generate_response("", template_vars)


class SecurityAgent(BaseAgent):
    """Агент для анализа безопасности"""
    
    async def process(self, input_data: Any) -> str:
        """Анализ безопасности кода и систем"""
        if isinstance(input_data, dict):
            template_vars = {
                "security_type": input_data.get("security_type", "code_analysis"),
                "target": input_data.get("target", ""),
                "vulnerability_types": input_data.get("vulnerability_types", ["sql_injection", "xss"]),
                "severity_level": input_data.get("severity_level", "medium"),
                "context": input_data.get("context", "Анализ безопасности"),
                "recommendations": input_data.get("recommendations", True)
            }
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "security_type": "code_analysis",
                "target": str(input_data),
                "vulnerability_types": ["sql_injection", "xss"],
                "severity_level": "medium",
                "context": "Анализ безопасности",
                "recommendations": True
            }
            return await self._generate_response("", template_vars)


class DevOpsAgent(BaseAgent):
    """Агент для DevOps задач"""
    
    async def process(self, input_data: Any) -> str:
        """Автоматизация DevOps процессов"""
        if isinstance(input_data, dict):
            template_vars = {
                "devops_task": input_data.get("devops_task", "deployment"),
                "platform": input_data.get("platform", "kubernetes"),
                "environment": input_data.get("environment", "production"),
                "tools": input_data.get("tools", ["docker", "helm"]),
                "context": input_data.get("context", "DevOps задача"),
                "automation_level": input_data.get("automation_level", "full")
            }
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "devops_task": "deployment",
                "platform": "kubernetes",
                "environment": "production",
                "tools": ["docker", "helm"],
                "context": "DevOps задача",
                "automation_level": "full"
            }
            return await self._generate_response("", template_vars)


class DocumentationAgent(BaseAgent):
    """Агент для создания документации"""
    
    async def process(self, input_data: Any) -> str:
        """Создание и обновление документации"""
        if isinstance(input_data, dict):
            template_vars = {
                "doc_type": input_data.get("doc_type", "api_documentation"),
                "content": input_data.get("content", ""),
                "format": input_data.get("format", "markdown"),
                "audience": input_data.get("audience", "developers"),
                "context": input_data.get("context", "Создание документации"),
                "style": input_data.get("style", "technical")
            }
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "doc_type": "api_documentation",
                "content": str(input_data),
                "format": "markdown",
                "audience": "developers",
                "context": "Создание документации",
                "style": "technical"
            }
            return await self._generate_response("", template_vars)


class TestingAgent(BaseAgent):
    """Агент для тестирования"""
    
    async def process(self, input_data: Any) -> str:
        """Создание и выполнение тестов"""
        if isinstance(input_data, dict):
            template_vars = {
                "test_type": input_data.get("test_type", "unit_test"),
                "target": input_data.get("target", ""),
                "framework": input_data.get("framework", "pytest"),
                "coverage": input_data.get("coverage", 80),
                "context": input_data.get("context", "Создание тестов"),
                "assertions": input_data.get("assertions", True)
            }
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "test_type": "unit_test",
                "target": str(input_data),
                "framework": "pytest",
                "coverage": 80,
                "context": "Создание тестов",
                "assertions": True
            }
            return await self._generate_response("", template_vars)


class ResearchAgent(BaseAgent):
    """Агент для исследований и анализа"""
    
    async def process(self, input_data: Any) -> str:
        """Проведение исследований и анализ информации"""
        if isinstance(input_data, dict):
            template_vars = {
                "research_topic": input_data.get("research_topic", ""),
                "research_type": input_data.get("research_type", "market_analysis"),
                "sources": input_data.get("sources", []),
                "depth": input_data.get("depth", "comprehensive"),
                "context": input_data.get("context", "Исследование"),
                "output_format": input_data.get("output_format", "report")
            }
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "research_topic": str(input_data),
                "research_type": "market_analysis",
                "sources": [],
                "depth": "comprehensive",
                "context": "Исследование",
                "output_format": "report"
            }
            return await self._generate_response("", template_vars)


class CommunicationAgent(BaseAgent):
    """Агент для коммуникации и презентаций"""
    
    async def process(self, input_data: Any) -> str:
        """Создание презентаций и коммуникационных материалов"""
        if isinstance(input_data, dict):
            template_vars = {
                "communication_type": input_data.get("communication_type", "presentation"),
                "topic": input_data.get("topic", ""),
                "audience": input_data.get("audience", "stakeholders"),
                "format": input_data.get("format", "slides"),
                "context": input_data.get("context", "Коммуникация"),
                "key_points": input_data.get("key_points", [])
            }
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "communication_type": "presentation",
                "topic": str(input_data),
                "audience": "stakeholders",
                "format": "slides",
                "context": "Коммуникация",
                "key_points": []
            }
            return await self._generate_response("", template_vars)


# Расширенная фабрика агентов
class ExtendedAgentFactory:
    """Расширенная фабрика для создания специализированных агентов"""
    
    @staticmethod
    def create_agent(agent_type: str, config: AgentConfig, api_key: str = None) -> BaseAgent:
        """Создать агента указанного типа"""
        
        # Базовые агенты
        base_agent_classes = {
            "analyst": "DataAnalystAgent",
            "coder": "CodeDeveloperAgent", 
            "reviewer": "CodeReviewerAgent",
            "manager": "TaskManagerAgent",
            "ideator": "IdeaGeneratorAgent",
            "assessor": "QualityAssessorAgent"
        }
        
        # Новые расширенные агенты
        extended_agent_classes = {
            "database": DatabaseAgent,
            "image_analysis": ImageAnalysisAgent,
            "api": APIAgent,
            "ml": MachineLearningAgent,
            "security": SecurityAgent,
            "devops": DevOpsAgent,
            "documentation": DocumentationAgent,
            "testing": TestingAgent,
            "research": ResearchAgent,
            "communication": CommunicationAgent
        }
        
        # Объединяем все типы агентов
        all_agent_classes = {**base_agent_classes, **extended_agent_classes}
        
        if agent_type not in all_agent_classes:
            raise ValueError(f"Неизвестный тип агента: {agent_type}")
        
        agent_class = all_agent_classes[agent_type]
        
        # Если это строка (базовый агент), импортируем из specialized_agents
        if isinstance(agent_class, str):
            from .specialized_agents import AgentFactory
            return AgentFactory.create_agent(agent_type, config, api_key)
        
        # Иначе создаем новый расширенный агент
        return agent_class(config, api_key)
    
    @staticmethod
    def get_available_agent_types() -> List[str]:
        """Получить список всех доступных типов агентов"""
        return [
            # Базовые агенты
            "analyst", "coder", "reviewer", "manager", "ideator", "assessor",
            # Расширенные агенты
            "database", "image_analysis", "api", "ml", "security", 
            "devops", "documentation", "testing", "research", "communication"
        ]
    
    @staticmethod
    def get_agent_categories() -> Dict[str, List[str]]:
        """Получить категории агентов"""
        return {
            "analysis": ["analyst", "research", "image_analysis"],
            "development": ["coder", "reviewer", "testing", "documentation"],
            "management": ["manager", "communication"],
            "specialized": ["database", "api", "ml", "security", "devops"],
            "creative": ["ideator", "assessor"]
        } 
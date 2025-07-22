"""
Специализированные агенты для различных задач
"""
from typing import Any, Dict, List
from .base_agent import BaseAgent, AgentConfig
from loguru import logger


class DataAnalystAgent(BaseAgent):
    """Агент-аналитик данных"""
    
    async def process(self, input_data: Any) -> str:
        """Обработка данных для анализа"""
        if isinstance(input_data, dict):
            # Используем шаблон промпта для анализа данных
            template_vars = {
                "data": input_data,
                "context": input_data.get("context", "Общий анализ данных"),
                "requirements": input_data.get("requirements", "Предоставь структурированный анализ с выводами")
            }
            return await self._generate_response("", template_vars)
        else:
            # Если строковые данные
            template_vars = {
                "data": input_data,
                "context": "Анализ текстовых данных",
                "requirements": "Предоставь структурированный анализ с выводами и рекомендациями"
            }
            return await self._generate_response("", template_vars)


class CodeDeveloperAgent(BaseAgent):
    """Агент-программист"""
    
    async def process(self, input_data: Any) -> str:
        """Генерация кода на основе описания задачи"""
        if isinstance(input_data, dict) and "task" in input_data:
            # Используем шаблон промпта для генерации кода
            template_vars = {
                "task": input_data["task"],
                "requirements": input_data.get("requirements", "Следуй лучшим практикам Python"),
                "language": input_data.get("language", "Python"),
                "version": input_data.get("version", "3.8+"),
                "style": input_data.get("style", "PEP 8"),
                "context": input_data.get("context", "Нет дополнительного контекста")
            }
            return await self._generate_response("", template_vars)
        else:
            # Если строковые данные
            template_vars = {
                "task": input_data,
                "requirements": "Следуй лучшим практикам Python",
                "language": "Python",
                "version": "3.8+",
                "style": "PEP 8",
                "context": "Нет дополнительного контекста"
            }
            return await self._generate_response("", template_vars)


class CodeReviewerAgent(BaseAgent):
    """Агент-ревьюер кода"""
    
    async def process(self, input_data: Any) -> str:
        """Ревью кода"""
        if isinstance(input_data, dict) and "code" in input_data:
            # Используем шаблон промпта для ревью кода
            template_vars = {
                "code": input_data["code"],
                "language": input_data.get("language", "python"),
                "context": input_data.get("context", "Общий ревью кода"),
                "criteria": input_data.get("criteria", "Качество, читаемость, эффективность, безопасность")
            }
            return await self._generate_response("", template_vars)
        else:
            # Если строковые данные
            template_vars = {
                "code": input_data,
                "language": "python",
                "context": "Общий ревью кода",
                "criteria": "Качество, читаемость, эффективность, безопасность"
            }
            return await self._generate_response("", template_vars)


class TaskManagerAgent(BaseAgent):
    """Агент-менеджер задач"""
    
    async def process(self, input_data: Any) -> str:
        """Управление задачами и проектами"""
        if isinstance(input_data, dict):
            project_info = input_data.get("project", "")
            tasks = input_data.get("tasks", [])
            
            management_prompt = f"""
            Проанализируй проект и задачи:
            
            Проект: {project_info}
            Задачи: {tasks}
            
            Предоставь:
            1. План выполнения задач
            2. Приоритизацию
            3. Оценку времени
            4. Рекомендации по управлению
            """
        else:
            management_prompt = f"""
            Помоги с управлением задачами:
            {input_data}
            
            Предоставь структурированный план действий.
            """
        
        return await self._generate_response(management_prompt)


class IdeaGeneratorAgent(BaseAgent):
    """Агент-генератор идей"""
    
    async def process(self, input_data: Any) -> str:
        """Генерация идей"""
        if isinstance(input_data, dict):
            # Используем шаблон промпта для генерации идей
            template_vars = {
                "domain": input_data.get("domain", input_data),
                "context": input_data.get("context", "Общий контекст"),
                "constraints": input_data.get("constraints", "Нет специальных ограничений"),
                "audience": input_data.get("audience", "Общая аудитория")
            }
            return await self._generate_response("", template_vars)
        else:
            # Если строковые данные
            template_vars = {
                "domain": input_data,
                "context": "Общий контекст",
                "constraints": "Нет специальных ограничений",
                "audience": "Общая аудитория"
            }
            return await self._generate_response("", template_vars)


class QualityAssessorAgent(BaseAgent):
    """Агент-оценщик качества"""
    
    async def process(self, input_data: Any) -> str:
        """Оценка качества"""
        if isinstance(input_data, dict):
            # Используем шаблон промпта для оценки качества
            template_vars = {
                "content": input_data.get("content", input_data),
                "criteria": input_data.get("criteria", "Качество, точность, полнота, полезность"),
                "context": input_data.get("context", "Общая оценка качества"),
                "target_audience": input_data.get("target_audience", "Общая аудитория")
            }
            return await self._generate_response("", template_vars)
        else:
            # Если строковые данные
            template_vars = {
                "content": input_data,
                "criteria": "Качество, точность, полнота, полезность",
                "context": "Общая оценка качества",
                "target_audience": "Общая аудитория"
            }
            return await self._generate_response("", template_vars)


# Фабрика для создания агентов
class AgentFactory:
    """Фабрика для создания специализированных агентов"""
    
    @staticmethod
    def create_agent(agent_type: str, config: AgentConfig, api_key: str = None) -> BaseAgent:
        """Создать агента указанного типа"""
        
        # Базовые агенты
        agent_classes = {
            "analyst": DataAnalystAgent,
            "coder": CodeDeveloperAgent,
            "reviewer": CodeReviewerAgent,
            "manager": TaskManagerAgent,
            "ideator": IdeaGeneratorAgent,
            "assessor": QualityAssessorAgent
        }
        
        # Проверяем базовые типы
        if agent_type in agent_classes:
            agent_class = agent_classes[agent_type]
            return agent_class(config, api_key)
        
        # Если не найден в базовых типах, пробуем расширенные агенты
        try:
            from .extended_agents import ExtendedAgentFactory
            extended_factory = ExtendedAgentFactory()
            return extended_factory.create_agent(agent_type, config, api_key)
        except ImportError:
            raise ValueError(f"Неизвестный тип агента: {agent_type}")
    
    @staticmethod
    def get_available_agent_types() -> List[str]:
        """Получить список всех доступных типов агентов"""
        base_types = [
            "analyst", "coder", "reviewer", "manager", "ideator", "assessor"
        ]
        
        # Добавляем расширенные типы
        try:
            from .extended_agents import ExtendedAgentFactory
            extended_types = ExtendedAgentFactory.get_available_agent_types()
            return base_types + extended_types
        except ImportError:
            return base_types 
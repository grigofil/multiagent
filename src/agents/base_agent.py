"""
Базовый класс для всех агентов в мультиагентной системе
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from loguru import logger

try:
    from ..prompts import PromptTemplates
except ImportError:
    from prompts import PromptTemplates


class AgentConfig(BaseModel):
    """Конфигурация агента"""
    name: str
    role: str
    description: str
    model: Dict[str, Any]
    system_prompt: str
    prompt_template: Optional[str] = None
    capabilities: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class AgentState(BaseModel):
    """Состояние агента"""
    messages: List[BaseMessage] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    iteration: int = 0


class BaseAgent(ABC):
    """
    Базовый класс для всех агентов
    """
    
    def __init__(self, config: AgentConfig, api_key: Optional[str] = None):
        self.config = config
        self.api_key = api_key
        self.state = AgentState()
        
        # Инициализация LLM
        self.llm = ChatOpenAI(
            model=config.model["model_name"],
            temperature=config.model["temperature"],
            max_tokens=config.model.get("max_tokens", 4000),
            top_p=config.model.get("top_p", 0.9),
            openai_api_key=api_key
        )
        
        # Создание базового промпта
        self.base_prompt_template = ChatPromptTemplate.from_messages([
            ("system", config.system_prompt),
            ("human", "{input}")
        ])
        
        # Инициализация шаблона промпта если указан
        self.prompt_template = None
        if config.prompt_template:
            try:
                self.prompt_template = PromptTemplates.get_template(config.prompt_template)
                logger.info(f"Загружен шаблон промпта: {config.prompt_template}")
            except Exception as e:
                logger.warning(f"Не удалось загрузить шаблон промпта {config.prompt_template}: {e}")
        
        logger.info(f"Инициализирован агент: {config.name} ({config.role})")
        logger.info(f"Возможности: {config.capabilities}")
        logger.info(f"Ограничения: {config.limitations}")
    
    def add_message(self, message: BaseMessage) -> None:
        """Добавить сообщение в историю агента"""
        self.state.messages.append(message)
    
    def get_context(self) -> Dict[str, Any]:
        """Получить текущий контекст агента"""
        return self.state.context
    
    def set_context(self, context: Dict[str, Any]) -> None:
        """Установить контекст агента"""
        self.state.context.update(context)
    
    @abstractmethod
    async def process(self, input_data: Any) -> str:
        """
        Основной метод обработки входных данных
        Должен быть реализован в каждом конкретном агенте
        """
        pass
    
    async def _generate_response(self, input_text: str, template_vars: Dict[str, Any] = None) -> str:
        """Генерация ответа с помощью LLM"""
        try:
            # Если есть шаблон промпта, используем его
            if self.prompt_template and template_vars:
                try:
                    rendered_prompt = self.prompt_template.render(**template_vars)
                    prompt = ChatPromptTemplate.from_messages([
                        ("system", self.config.system_prompt),
                        ("human", rendered_prompt)
                    ])
                except Exception as e:
                    logger.warning(f"Ошибка рендеринга шаблона промпта: {e}")
                    # Используем базовый промпт
                    prompt = self.base_prompt_template
                    input_text = str(template_vars)
            else:
                # Используем базовый промпт
                prompt = self.base_prompt_template
            
            # Формируем промпт
            formatted_prompt = prompt.format(input=input_text)
            
            # Получаем ответ от LLM
            response = await self.llm.ainvoke(formatted_prompt)
            
            # Добавляем сообщения в историю
            self.add_message(HumanMessage(content=input_text))
            self.add_message(AIMessage(content=response.content))
            
            logger.debug(f"Агент {self.config.name} сгенерировал ответ")
            return response.content
            
        except Exception as e:
            logger.error(f"Ошибка при генерации ответа агентом {self.config.name}: {e}")
            raise
    
    def has_capability(self, capability: str) -> bool:
        """Проверить наличие возможности у агента"""
        return capability in self.config.capabilities
    
    def get_capabilities(self) -> List[str]:
        """Получить список возможностей агента"""
        return self.config.capabilities.copy()
    
    def get_limitations(self) -> List[str]:
        """Получить список ограничений агента"""
        return self.config.limitations.copy()
    
    def reset_state(self) -> None:
        """Сбросить состояние агента"""
        self.state = AgentState()
        logger.info(f"Состояние агента {self.config.name} сброшено")
    
    def get_info(self) -> Dict[str, Any]:
        """Получить информацию об агенте"""
        return {
            "name": self.config.name,
            "role": self.config.role,
            "description": self.config.description,
            "model": self.config.model,
            "prompt_template": self.config.prompt_template,
            "capabilities": self.config.capabilities,
            "limitations": self.config.limitations,
            "messages_count": len(self.state.messages),
            "iteration": self.state.iteration
        } 
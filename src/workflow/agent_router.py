"""
Механизм маршрутизации сообщений между агентами
"""
import asyncio
from typing import Dict, Any, List, Optional, Callable, Union
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from loguru import logger

from ..agents import BaseAgent, AgentFactory
from ..utils.advanced_config_loader import AdvancedConfigLoader


class MessageType(Enum):
    """Типы сообщений между агентами"""
    TASK = "task"
    RESULT = "result"
    ERROR = "error"
    CONTROL = "control"
    DATA = "data"


class RoutingStrategy(Enum):
    """Стратегии маршрутизации"""
    SEQUENTIAL = "sequential"  # Последовательная обработка
    PARALLEL = "parallel"      # Параллельная обработка
    CONDITIONAL = "conditional"  # Условная маршрутизация
    BROADCAST = "broadcast"    # Широковещательная рассылка


@dataclass
class Message:
    """Сообщение между агентами"""
    id: str
    sender: str
    recipients: List[str]
    message_type: MessageType
    content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 0
    
    def __post_init__(self):
        if isinstance(self.message_type, str):
            self.message_type = MessageType(self.message_type)


@dataclass
class RoutingRule:
    """Правило маршрутизации"""
    condition: Callable[[Message], bool]
    target_agents: List[str]
    strategy: RoutingStrategy
    priority: int = 0
    description: str = ""


class AgentRouter:
    """Маршрутизатор сообщений между агентами"""
    
    def __init__(self, config_loader: AdvancedConfigLoader, api_key: str = None):
        self.config_loader = config_loader
        self.api_key = api_key
        self.agents: Dict[str, BaseAgent] = {}
        self.routing_rules: List[RoutingRule] = []
        self.message_history: List[Message] = []
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.is_running = False
        
        # Статистика маршрутизации
        self.stats = {
            "messages_processed": 0,
            "messages_routed": 0,
            "errors": 0,
            "avg_processing_time": 0.0
        }
        
        logger.info("Инициализирован маршрутизатор агентов")
    
    async def initialize_agents(self, agent_ids: List[str] = None) -> None:
        """Инициализация агентов"""
        try:
            agents_config = self.config_loader.load_agents_config()
            available_agents = agents_config.get("agents", {})
            
            if agent_ids is None:
                agent_ids = list(available_agents.keys())
            
            for agent_id in agent_ids:
                if agent_id not in available_agents:
                    logger.warning(f"Агент {agent_id} не найден в конфигурации")
                    continue
                
                agent_config_dict = available_agents[agent_id]
                # Создаем объект AgentConfig из словаря
                from ..agents import AgentConfig
                agent_config = AgentConfig(**agent_config_dict)
                
                agent = AgentFactory.create_agent(
                    agent_id, 
                    agent_config, 
                    self.api_key
                )
                self.agents[agent_id] = agent
                logger.info(f"Инициализирован агент: {agent_id}")
            
            logger.info(f"Инициализировано агентов: {len(self.agents)}")
            
        except Exception as e:
            logger.error(f"Ошибка при инициализации агентов: {e}")
            raise
    
    def add_routing_rule(self, rule: RoutingRule) -> None:
        """Добавить правило маршрутизации"""
        self.routing_rules.append(rule)
        # Сортируем по приоритету (высокий приоритет первым)
        self.routing_rules.sort(key=lambda x: x.priority, reverse=True)
        logger.info(f"Добавлено правило маршрутизации: {rule.description}")
    
    def add_default_routing_rules(self) -> None:
        """Добавить правила маршрутизации по умолчанию"""
        
        # Правило для анализа данных
        def is_data_analysis(message: Message) -> bool:
            return (message.message_type == MessageType.TASK and 
                   any(keyword in str(message.content).lower() 
                       for keyword in ["анализ", "данные", "статистика", "тренды"]))
        
        self.add_routing_rule(RoutingRule(
            condition=is_data_analysis,
            target_agents=["analyst"],
            strategy=RoutingStrategy.SEQUENTIAL,
            priority=10,
            description="Анализ данных -> Data Analyst"
        ))
        
        # Правило для генерации кода
        def is_code_generation(message: Message) -> bool:
            return (message.message_type == MessageType.TASK and 
                   any(keyword in str(message.content).lower() 
                       for keyword in ["код", "программа", "функция", "класс", "алгоритм"]))
        
        self.add_routing_rule(RoutingRule(
            condition=is_code_generation,
            target_agents=["coder"],
            strategy=RoutingStrategy.SEQUENTIAL,
            priority=10,
            description="Генерация кода -> Code Developer"
        ))
        
        # Правило для ревью кода
        def is_code_review(message: Message) -> bool:
            return (message.message_type == MessageType.TASK and 
                   any(keyword in str(message.content).lower() 
                       for keyword in ["ревью", "проверка", "код", "качество"]))
        
        self.add_routing_rule(RoutingRule(
            condition=is_code_review,
            target_agents=["reviewer"],
            strategy=RoutingStrategy.SEQUENTIAL,
            priority=9,
            description="Ревью кода -> Code Reviewer"
        ))
        
        # Правило для управления проектами
        def is_project_management(message: Message) -> bool:
            return (message.message_type == MessageType.TASK and 
                   any(keyword in str(message.content).lower() 
                       for keyword in ["проект", "план", "управление", "задачи", "сроки"]))
        
        self.add_routing_rule(RoutingRule(
            condition=is_project_management,
            target_agents=["manager"],
            strategy=RoutingStrategy.SEQUENTIAL,
            priority=8,
            description="Управление проектами -> Project Manager"
        ))
        
        # Правило для генерации идей
        def is_idea_generation(message: Message) -> bool:
            return (message.message_type == MessageType.TASK and 
                   any(keyword in str(message.content).lower() 
                       for keyword in ["идея", "инновация", "креатив", "решение"]))
        
        self.add_routing_rule(RoutingRule(
            condition=is_idea_generation,
            target_agents=["ideator"],
            strategy=RoutingStrategy.SEQUENTIAL,
            priority=7,
            description="Генерация идей -> Idea Generator"
        ))
        
        # Правило для оценки качества
        def is_quality_assessment(message: Message) -> bool:
            return (message.message_type == MessageType.TASK and 
                   any(keyword in str(message.content).lower() 
                       for keyword in ["качество", "оценка", "проверка", "аудит"]))
        
        self.add_routing_rule(RoutingRule(
            condition=is_quality_assessment,
            target_agents=["assessor"],
            strategy=RoutingStrategy.SEQUENTIAL,
            priority=6,
            description="Оценка качества -> Quality Assessor"
        ))
        
        # Правило для комплексных задач (несколько агентов)
        def is_complex_task(message: Message) -> bool:
            return (message.message_type == MessageType.TASK and 
                   len(str(message.content)) > 200)  # Длинные задачи считаем комплексными
        
        self.add_routing_rule(RoutingRule(
            condition=is_complex_task,
            target_agents=["analyst", "coder", "reviewer"],
            strategy=RoutingStrategy.SEQUENTIAL,
            priority=5,
            description="Комплексные задачи -> Analyst -> Coder -> Reviewer"
        ))
        
        logger.info("Добавлены правила маршрутизации по умолчанию")
    
    async def send_message(self, message: Message) -> None:
        """Отправить сообщение в очередь"""
        await self.message_queue.put(message)
        logger.debug(f"Сообщение {message.id} добавлено в очередь")
    
    async def route_message(self, message: Message) -> List[Message]:
        """Маршрутизация сообщения согласно правилам"""
        routed_messages = []
        
        try:
            # Находим подходящие правила
            matching_rules = [
                rule for rule in self.routing_rules 
                if rule.condition(message)
            ]
            
            if not matching_rules:
                logger.warning(f"Не найдено правил маршрутизации для сообщения {message.id}")
                return routed_messages
            
            # Берем правило с наивысшим приоритетом
            rule = matching_rules[0]
            logger.info(f"Применено правило: {rule.description}")
            
            # Фильтруем доступных агентов
            available_agents = [
                agent_id for agent_id in rule.target_agents 
                if agent_id in self.agents
            ]
            
            if not available_agents:
                logger.warning(f"Нет доступных агентов для правила: {rule.description}")
                return routed_messages
            
            # Создаем сообщения для агентов согласно стратегии
            if rule.strategy == RoutingStrategy.SEQUENTIAL:
                # Последовательная обработка
                for i, agent_id in enumerate(available_agents):
                    agent_message = Message(
                        id=f"{message.id}_to_{agent_id}",
                        sender=message.sender,
                        recipients=[agent_id],
                        message_type=message.message_type,
                        content=message.content,
                        metadata={
                            **message.metadata,
                            "step": i + 1,
                            "total_steps": len(available_agents),
                            "previous_results": [msg.content for msg in routed_messages]
                        },
                        priority=message.priority
                    )
                    routed_messages.append(agent_message)
                    
            elif rule.strategy == RoutingStrategy.PARALLEL:
                # Параллельная обработка
                for agent_id in available_agents:
                    agent_message = Message(
                        id=f"{message.id}_to_{agent_id}",
                        sender=message.sender,
                        recipients=[agent_id],
                        message_type=message.message_type,
                        content=message.content,
                        metadata={
                            **message.metadata,
                            "parallel": True,
                            "agent_id": agent_id
                        },
                        priority=message.priority
                    )
                    routed_messages.append(agent_message)
                    
            elif rule.strategy == RoutingStrategy.BROADCAST:
                # Широковещательная рассылка
                for agent_id in self.agents.keys():
                    agent_message = Message(
                        id=f"{message.id}_broadcast_{agent_id}",
                        sender=message.sender,
                        recipients=[agent_id],
                        message_type=message.message_type,
                        content=message.content,
                        metadata={
                            **message.metadata,
                            "broadcast": True
                        },
                        priority=message.priority
                    )
                    routed_messages.append(agent_message)
            
            self.stats["messages_routed"] += len(routed_messages)
            logger.info(f"Сообщение {message.id} маршрутизировано к {len(routed_messages)} агентам")
            
        except Exception as e:
            logger.error(f"Ошибка при маршрутизации сообщения {message.id}: {e}")
            self.stats["errors"] += 1
        
        return routed_messages
    
    async def process_message(self, message: Message) -> Message:
        """Обработка сообщения агентом"""
        start_time = datetime.now()
        
        try:
            agent_id = message.recipients[0]
            agent = self.agents.get(agent_id)
            
            if not agent:
                logger.error(f"Агент {agent_id} не найден")
                raise ValueError(f"Агент {agent_id} не найден")
            
            # Обрабатываем сообщение агентом
            result = await agent.process(message.content)
            
            # Создаем ответное сообщение
            response = Message(
                id=f"response_{message.id}",
                sender=agent_id,
                recipients=[message.sender] if message.sender != "system" else [],
                message_type=MessageType.RESULT,
                content=result,
                metadata={
                    "original_message_id": message.id,
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "agent_capabilities": agent.get_capabilities(),
                    "agent_limitations": agent.get_limitations()
                },
                priority=message.priority
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            self.stats["avg_processing_time"] = (
                (self.stats["avg_processing_time"] * self.stats["messages_processed"] + processing_time) /
                (self.stats["messages_processed"] + 1)
            )
            self.stats["messages_processed"] += 1
            
            logger.info(f"Сообщение {message.id} обработано агентом {agent_id} за {processing_time:.2f}с")
            return response
            
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщения {message.id}: {e}")
            self.stats["errors"] += 1
            
            # Создаем сообщение об ошибке
            error_response = Message(
                id=f"error_{message.id}",
                sender=message.recipients[0] if message.recipients else "system",
                recipients=[message.sender] if message.sender != "system" else [],
                message_type=MessageType.ERROR,
                content=f"Ошибка обработки: {str(e)}",
                metadata={
                    "original_message_id": message.id,
                    "error_type": type(e).__name__,
                    "processing_time": (datetime.now() - start_time).total_seconds()
                },
                priority=message.priority
            )
            return error_response
    
    async def start_processing(self) -> None:
        """Запуск обработки сообщений"""
        self.is_running = True
        logger.info("Запущена обработка сообщений")
        
        while self.is_running:
            try:
                # Получаем сообщение из очереди
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                
                # Добавляем в историю
                self.message_history.append(message)
                
                # Маршрутизируем сообщение
                routed_messages = await self.route_message(message)
                
                # Обрабатываем маршрутизированные сообщения
                if routed_messages:
                    if any(msg.metadata.get("parallel", False) for msg in routed_messages):
                        # Параллельная обработка
                        tasks = [self.process_message(msg) for msg in routed_messages]
                        responses = await asyncio.gather(*tasks, return_exceptions=True)
                        
                        for response in responses:
                            if isinstance(response, Exception):
                                logger.error(f"Ошибка в параллельной обработке: {response}")
                            else:
                                self.message_history.append(response)
                    else:
                        # Последовательная обработка
                        for msg in routed_messages:
                            response = await self.process_message(msg)
                            self.message_history.append(response)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Ошибка в цикле обработки сообщений: {e}")
                self.stats["errors"] += 1
    
    async def stop_processing(self) -> None:
        """Остановка обработки сообщений"""
        self.is_running = False
        logger.info("Остановлена обработка сообщений")
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику маршрутизатора"""
        return {
            **self.stats,
            "agents_count": len(self.agents),
            "rules_count": len(self.routing_rules),
            "queue_size": self.message_queue.qsize(),
            "history_size": len(self.message_history)
        }
    
    def get_message_history(self, limit: int = 100) -> List[Message]:
        """Получить историю сообщений"""
        return self.message_history[-limit:] if limit else self.message_history
    
    def clear_history(self) -> None:
        """Очистить историю сообщений"""
        self.message_history.clear()
        logger.info("История сообщений очищена") 
"""
Мультиагентные рабочие процессы с использованием LangGraph
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from loguru import logger
import asyncio

from ..agents import BaseAgent, AgentFactory, AgentConfig
from ..utils import ConfigLoader


class WorkflowState(BaseModel):
    """Состояние рабочего процесса"""
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    current_step: int = 0
    max_iterations: int = 5
    workflow_name: str = ""
    agents_info: Dict[str, Any] = Field(default_factory=dict)


class MultiAgentWorkflow:
    """
    Управление мультиагентными рабочими процессами
    """
    
    def __init__(self, config_loader: ConfigLoader, api_key: Optional[str] = None):
        self.config_loader = config_loader
        self.api_key = api_key
        self.agents: Dict[str, BaseAgent] = {}
        self.workflows: Dict[str, StateGraph] = {}
        
        # Загружаем конфигурации
        self.agents_config = config_loader.load_agents_config()
        self.interactions_config = config_loader.load_interactions_config()
        
        # Инициализируем агентов
        self._initialize_agents()
        
        # Создаем рабочие процессы
        self._create_workflows()
    
    def _initialize_agents(self) -> None:
        """Инициализация агентов из конфигурации"""
        for agent_id, agent_config in self.agents_config["agents"].items():
            try:
                # Создаем конфигурацию агента
                config = AgentConfig(
                    name=agent_config["name"],
                    role=agent_config["role"],
                    model=agent_config["model"],
                    system_prompt=agent_config["system_prompt"]
                )
                
                # Определяем тип агента по ID
                agent_type = agent_id
                
                # Создаем агента через фабрику
                agent = AgentFactory.create_agent(agent_type, config, self.api_key)
                self.agents[agent_id] = agent
                
                logger.info(f"Инициализирован агент: {agent_id} ({config.name})")
                
            except Exception as e:
                logger.error(f"Ошибка при инициализации агента {agent_id}: {e}")
                raise
    
    def _create_workflows(self) -> None:
        """Создание рабочих процессов из конфигурации"""
        for workflow_id, workflow_config in self.interactions_config["workflows"].items():
            try:
                workflow = self._create_single_workflow(workflow_id, workflow_config)
                self.workflows[workflow_id] = workflow
                
                logger.info(f"Создан рабочий процесс: {workflow_id}")
                
            except Exception as e:
                logger.error(f"Ошибка при создании рабочего процесса {workflow_id}: {e}")
                raise
    
    def _create_single_workflow(self, workflow_id: str, workflow_config: Dict[str, Any]) -> StateGraph:
        """Создание отдельного рабочего процесса"""
        
        # Создаем граф состояний
        workflow = StateGraph(WorkflowState)
        
        # Добавляем узлы для каждого шага
        for step in workflow_config["flow"]:
            step_num = step["step"]
            agent_id = step["agent"]
            
            # Создаем функцию для обработки шага
            async def process_step(state: WorkflowState, agent_id=agent_id, step=step) -> WorkflowState:
                """Обработка одного шага рабочего процесса"""
                
                try:
                    # Получаем агента
                    agent = self.agents[agent_id]
                    
                    # Подготавливаем входные данные
                    input_data = self._prepare_input_data(state, step)
                    
                    # Обрабатываем через агента
                    result = await agent.process(input_data)
                    
                    # Обновляем состояние
                    state.messages.append({
                        "step": step_num,
                        "agent": agent_id,
                        "input": input_data,
                        "output": result,
                        "timestamp": asyncio.get_event_loop().time()
                    })
                    
                    state.current_step = step_num
                    state.context[step["output"]] = result
                    
                    logger.info(f"Шаг {step_num} выполнен агентом {agent_id}")
                    
                except Exception as e:
                    logger.error(f"Ошибка на шаге {step_num}: {e}")
                    state.context["error"] = str(e)
                
                return state
            
            # Добавляем узел в граф
            workflow.add_node(f"step_{step_num}", process_step)
        
        # Настраиваем переходы между шагами
        for i, step in enumerate(workflow_config["flow"]):
            step_num = step["step"]
            current_node = f"step_{step_num}"
            
            if i < len(workflow_config["flow"]) - 1:
                # Переход к следующему шагу
                next_step = workflow_config["flow"][i + 1]["step"]
                next_node = f"step_{next_step}"
                workflow.add_edge(current_node, next_node)
            else:
                # Последний шаг - переход к концу
                workflow.add_edge(current_node, END)
        
        # Компилируем граф
        return workflow.compile(checkpointer=MemorySaver())
    
    def _prepare_input_data(self, state: WorkflowState, step: Dict[str, Any]) -> Any:
        """Подготовка входных данных для шага"""
        input_key = step["input"]
        
        if isinstance(input_key, list):
            # Если несколько входных данных
            return [state.context.get(key, "") for key in input_key]
        else:
            # Одно входное значение
            return state.context.get(input_key, "")
    
    async def run_workflow(self, workflow_name: str, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Запуск рабочего процесса"""
        
        if workflow_name not in self.workflows:
            raise ValueError(f"Рабочий процесс '{workflow_name}' не найден")
        
        # Создаем начальное состояние
        workflow_config = self.interactions_config["workflows"][workflow_name]
        initial_state = WorkflowState(
            context=initial_data,
            max_iterations=workflow_config.get("max_iterations", 5),
            workflow_name=workflow_name
        )
        
        logger.info(f"Запуск рабочего процесса: {workflow_name}")
        
        try:
            # Запускаем рабочий процесс
            workflow = self.workflows[workflow_name]
            result = await workflow.ainvoke(initial_state)
            
            logger.info(f"Рабочий процесс '{workflow_name}' завершен успешно")
            
            return {
                "workflow_name": workflow_name,
                "messages": result.messages,
                "context": result.context,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Ошибка при выполнении рабочего процесса '{workflow_name}': {e}")
            return {
                "workflow_name": workflow_name,
                "error": str(e),
                "success": False
            }
    
    def get_available_workflows(self) -> List[str]:
        """Получить список доступных рабочих процессов"""
        return list(self.workflows.keys())
    
    def get_workflow_info(self, workflow_name: str) -> Dict[str, Any]:
        """Получить информацию о рабочем процессе"""
        if workflow_name not in self.interactions_config["workflows"]:
            raise ValueError(f"Рабочий процесс '{workflow_name}' не найден")
        
        return self.interactions_config["workflows"][workflow_name]
    
    def get_agents_info(self) -> Dict[str, Any]:
        """Получить информацию об агентах"""
        return {
            agent_id: agent.get_info() 
            for agent_id, agent in self.agents.items()
        } 
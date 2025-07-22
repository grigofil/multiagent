"""
Интеграция с LangGraph для сложных рабочих процессов
"""
import asyncio
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
from loguru import logger

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from .agent_router import Message, MessageType, AgentRouter
from .interaction_logger import InteractionLogger


@dataclass
class WorkflowState:
    """Состояние рабочего процесса"""
    messages: List[Message] = field(default_factory=list)
    current_step: str = ""
    step_results: Dict[str, Any] = field(default_factory=dict)
    workflow_data: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class LangGraphWorkflowManager:
    """Менеджер рабочих процессов с использованием LangGraph"""
    
    def __init__(self, agent_router: AgentRouter, interaction_logger: InteractionLogger):
        self.agent_router = agent_router
        self.interaction_logger = interaction_logger
        self.workflows: Dict[str, StateGraph] = {}
        self.checkpoint_saver = MemorySaver()
        
        logger.info("Инициализирован менеджер рабочих процессов LangGraph")
    
    def create_data_analysis_workflow(self) -> StateGraph:
        """Создать рабочий процесс анализа данных"""
        
        def create_initial_state() -> WorkflowState:
            return WorkflowState(
                current_step="start",
                metadata={"workflow_type": "data_analysis"}
            )
        
        # Создаем граф состояний
        workflow = StateGraph(WorkflowState)
        
        # Определяем узлы (шаги)
        workflow.add_node("start", self._start_node)
        workflow.add_node("analyze_data", self._analyze_data_node)
        workflow.add_node("generate_insights", self._generate_insights_node)
        workflow.add_node("create_visualization", self._create_visualization_node)
        workflow.add_node("finalize_report", self._finalize_report_node)
        
        # Определяем переходы
        workflow.set_entry_point("start")
        workflow.add_edge("start", "analyze_data")
        workflow.add_edge("analyze_data", "generate_insights")
        workflow.add_edge("generate_insights", "create_visualization")
        workflow.add_edge("create_visualization", "finalize_report")
        workflow.add_edge("finalize_report", END)
        
        # Добавляем условные переходы для обработки ошибок
        workflow.add_conditional_edges(
            "analyze_data",
            self._should_continue,
            {
                "continue": "generate_insights",
                "error": "finalize_report"
            }
        )
        
        return workflow.compile(checkpointer=self.checkpoint_saver)
    
    def create_code_development_workflow(self) -> StateGraph:
        """Создать рабочий процесс разработки кода"""
        
        # Создаем граф состояний
        workflow = StateGraph(WorkflowState)
        
        # Определяем узлы
        workflow.add_node("start", self._start_node)
        workflow.add_node("plan_architecture", self._plan_architecture_node)
        workflow.add_node("generate_code", self._generate_code_node)
        workflow.add_node("review_code", self._review_code_node)
        workflow.add_node("refactor_code", self._refactor_code_node)
        workflow.add_node("test_code", self._test_code_node)
        workflow.add_node("finalize_code", self._finalize_code_node)
        
        # Определяем переходы
        workflow.set_entry_point("start")
        workflow.add_edge("start", "plan_architecture")
        workflow.add_edge("plan_architecture", "generate_code")
        
        # Условные переходы для ревью
        workflow.add_conditional_edges(
            "generate_code",
            self._code_review_decision,
            {
                "approve": "test_code",
                "refactor": "refactor_code"
            }
        )
        
        workflow.add_edge("refactor_code", "review_code")
        workflow.add_edge("review_code", "test_code")
        workflow.add_edge("test_code", "finalize_code")
        workflow.add_edge("finalize_code", END)
        
        return workflow.compile(checkpointer=self.checkpoint_saver)
    
    def create_project_management_workflow(self) -> StateGraph:
        """Создать рабочий процесс управления проектами"""
        
        # Создаем граф состояний
        workflow = StateGraph(WorkflowState)
        
        # Определяем узлы
        workflow.add_node("start", self._start_node)
        workflow.add_node("analyze_requirements", self._analyze_requirements_node)
        workflow.add_node("create_project_plan", self._create_project_plan_node)
        workflow.add_node("define_tasks", self._define_tasks_node)
        workflow.add_node("estimate_resources", self._estimate_resources_node)
        workflow.add_node("create_timeline", self._create_timeline_node)
        workflow.add_node("finalize_project", self._finalize_project_node)
        
        # Определяем переходы
        workflow.set_entry_point("start")
        workflow.add_edge("start", "analyze_requirements")
        workflow.add_edge("analyze_requirements", "create_project_plan")
        workflow.add_edge("create_project_plan", "define_tasks")
        workflow.add_edge("define_tasks", "estimate_resources")
        workflow.add_edge("estimate_resources", "create_timeline")
        workflow.add_edge("create_timeline", "finalize_project")
        workflow.add_edge("finalize_project", END)
        
        return workflow.compile(checkpointer=self.checkpoint_saver)
    
    # Узлы для рабочих процессов
    
    async def _start_node(self, state: WorkflowState) -> WorkflowState:
        """Начальный узел"""
        state.current_step = "start"
        state.metadata["start_time"] = datetime.now().isoformat()
        logger.info("Начало рабочего процесса")
        return state
    
    async def _analyze_data_node(self, state: WorkflowState) -> WorkflowState:
        """Узел анализа данных"""
        try:
            state.current_step = "analyze_data"
            
            # Создаем сообщение для анализатора данных
            message = Message(
                id=f"analysis_{datetime.now().timestamp()}",
                sender="system",
                recipients=["analyst"],
                message_type=MessageType.TASK,
                content=state.workflow_data.get("data", "Нет данных для анализа"),
                metadata={"step": "analyze_data", "workflow": "data_analysis"}
            )
            
            # Отправляем сообщение через роутер
            await self.agent_router.send_message(message)
            
            # Ждем ответа (в реальной системе здесь была бы более сложная логика)
            await asyncio.sleep(1)
            
            # Симулируем результат
            result = "Анализ данных завершен успешно"
            state.step_results["analyze_data"] = result
            state.workflow_data["analysis_result"] = result
            
            logger.info("Анализ данных завершен")
            return state
            
        except Exception as e:
            state.errors.append(f"Ошибка анализа данных: {str(e)}")
            logger.error(f"Ошибка в узле анализа данных: {e}")
            return state
    
    async def _generate_insights_node(self, state: WorkflowState) -> WorkflowState:
        """Узел генерации инсайтов"""
        try:
            state.current_step = "generate_insights"
            
            # Используем результат анализа для генерации инсайтов
            analysis_result = state.step_results.get("analyze_data", "")
            
            message = Message(
                id=f"insights_{datetime.now().timestamp()}",
                sender="system",
                recipients=["analyst"],
                message_type=MessageType.TASK,
                content=f"Сгенерируй инсайты на основе анализа: {analysis_result}",
                metadata={"step": "generate_insights", "workflow": "data_analysis"}
            )
            
            await self.agent_router.send_message(message)
            await asyncio.sleep(1)
            
            result = "Инсайты сгенерированы"
            state.step_results["generate_insights"] = result
            state.workflow_data["insights"] = result
            
            logger.info("Инсайты сгенерированы")
            return state
            
        except Exception as e:
            state.errors.append(f"Ошибка генерации инсайтов: {str(e)}")
            logger.error(f"Ошибка в узле генерации инсайтов: {e}")
            return state
    
    async def _create_visualization_node(self, state: WorkflowState) -> WorkflowState:
        """Узел создания визуализации"""
        try:
            state.current_step = "create_visualization"
            
            message = Message(
                id=f"viz_{datetime.now().timestamp()}",
                sender="system",
                recipients=["analyst"],
                message_type=MessageType.TASK,
                content="Создай рекомендации по визуализации данных",
                metadata={"step": "create_visualization", "workflow": "data_analysis"}
            )
            
            await self.agent_router.send_message(message)
            await asyncio.sleep(1)
            
            result = "Рекомендации по визуализации созданы"
            state.step_results["create_visualization"] = result
            state.workflow_data["visualization"] = result
            
            logger.info("Визуализация создана")
            return state
            
        except Exception as e:
            state.errors.append(f"Ошибка создания визуализации: {str(e)}")
            logger.error(f"Ошибка в узле создания визуализации: {e}")
            return state
    
    async def _finalize_report_node(self, state: WorkflowState) -> WorkflowState:
        """Узел финализации отчета"""
        try:
            state.current_step = "finalize_report"
            
            # Собираем все результаты
            report_data = {
                "analysis": state.step_results.get("analyze_data"),
                "insights": state.step_results.get("generate_insights"),
                "visualization": state.step_results.get("create_visualization"),
                "errors": state.errors
            }
            
            message = Message(
                id=f"report_{datetime.now().timestamp()}",
                sender="system",
                recipients=["analyst"],
                message_type=MessageType.TASK,
                content=f"Создай финальный отчет на основе: {report_data}",
                metadata={"step": "finalize_report", "workflow": "data_analysis"}
            )
            
            await self.agent_router.send_message(message)
            await asyncio.sleep(1)
            
            result = "Финальный отчет создан"
            state.step_results["finalize_report"] = result
            state.workflow_data["final_report"] = result
            
            logger.info("Отчет финализирован")
            return state
            
        except Exception as e:
            state.errors.append(f"Ошибка финализации отчета: {str(e)}")
            logger.error(f"Ошибка в узле финализации отчета: {e}")
            return state
    
    # Узлы для разработки кода
    
    async def _plan_architecture_node(self, state: WorkflowState) -> WorkflowState:
        """Узел планирования архитектуры"""
        state.current_step = "plan_architecture"
        state.step_results["plan_architecture"] = "Архитектура спланирована"
        logger.info("Архитектура спланирована")
        return state
    
    async def _generate_code_node(self, state: WorkflowState) -> WorkflowState:
        """Узел генерации кода"""
        try:
            state.current_step = "generate_code"
            
            message = Message(
                id=f"code_{datetime.now().timestamp()}",
                sender="system",
                recipients=["coder"],
                message_type=MessageType.TASK,
                content=state.workflow_data.get("requirements", "Создай код"),
                metadata={"step": "generate_code", "workflow": "code_development"}
            )
            
            await self.agent_router.send_message(message)
            await asyncio.sleep(1)
            
            result = "Код сгенерирован"
            state.step_results["generate_code"] = result
            state.workflow_data["generated_code"] = result
            
            logger.info("Код сгенерирован")
            return state
            
        except Exception as e:
            state.errors.append(f"Ошибка генерации кода: {str(e)}")
            logger.error(f"Ошибка в узле генерации кода: {e}")
            return state
    
    async def _review_code_node(self, state: WorkflowState) -> WorkflowState:
        """Узел ревью кода"""
        try:
            state.current_step = "review_code"
            
            code_to_review = state.step_results.get("generate_code", "")
            
            message = Message(
                id=f"review_{datetime.now().timestamp()}",
                sender="system",
                recipients=["reviewer"],
                message_type=MessageType.TASK,
                content=f"Проведи ревью кода: {code_to_review}",
                metadata={"step": "review_code", "workflow": "code_development"}
            )
            
            await self.agent_router.send_message(message)
            await asyncio.sleep(1)
            
            result = "Ревью кода завершено"
            state.step_results["review_code"] = result
            state.workflow_data["review_result"] = result
            
            logger.info("Ревью кода завершено")
            return state
            
        except Exception as e:
            state.errors.append(f"Ошибка ревью кода: {str(e)}")
            logger.error(f"Ошибка в узле ревью кода: {e}")
            return state
    
    async def _refactor_code_node(self, state: WorkflowState) -> WorkflowState:
        """Узел рефакторинга кода"""
        state.current_step = "refactor_code"
        state.step_results["refactor_code"] = "Код отрефакторен"
        logger.info("Код отрефакторен")
        return state
    
    async def _test_code_node(self, state: WorkflowState) -> WorkflowState:
        """Узел тестирования кода"""
        state.current_step = "test_code"
        state.step_results["test_code"] = "Код протестирован"
        logger.info("Код протестирован")
        return state
    
    async def _finalize_code_node(self, state: WorkflowState) -> WorkflowState:
        """Узел финализации кода"""
        state.current_step = "finalize_code"
        state.step_results["finalize_code"] = "Код финализирован"
        logger.info("Код финализирован")
        return state
    
    # Узлы для управления проектами
    
    async def _analyze_requirements_node(self, state: WorkflowState) -> WorkflowState:
        """Узел анализа требований"""
        state.current_step = "analyze_requirements"
        state.step_results["analyze_requirements"] = "Требования проанализированы"
        logger.info("Требования проанализированы")
        return state
    
    async def _create_project_plan_node(self, state: WorkflowState) -> WorkflowState:
        """Узел создания плана проекта"""
        state.current_step = "create_project_plan"
        state.step_results["create_project_plan"] = "План проекта создан"
        logger.info("План проекта создан")
        return state
    
    async def _define_tasks_node(self, state: WorkflowState) -> WorkflowState:
        """Узел определения задач"""
        state.current_step = "define_tasks"
        state.step_results["define_tasks"] = "Задачи определены"
        logger.info("Задачи определены")
        return state
    
    async def _estimate_resources_node(self, state: WorkflowState) -> WorkflowState:
        """Узел оценки ресурсов"""
        state.current_step = "estimate_resources"
        state.step_results["estimate_resources"] = "Ресурсы оценены"
        logger.info("Ресурсы оценены")
        return state
    
    async def _create_timeline_node(self, state: WorkflowState) -> WorkflowState:
        """Узел создания временной шкалы"""
        state.current_step = "create_timeline"
        state.step_results["create_timeline"] = "Временная шкала создана"
        logger.info("Временная шкала создана")
        return state
    
    async def _finalize_project_node(self, state: WorkflowState) -> WorkflowState:
        """Узел финализации проекта"""
        state.current_step = "finalize_project"
        state.step_results["finalize_project"] = "Проект финализирован"
        logger.info("Проект финализирован")
        return state
    
    # Функции принятия решений
    
    def _should_continue(self, state: WorkflowState) -> str:
        """Решение о продолжении рабочего процесса"""
        if state.errors:
            return "error"
        return "continue"
    
    def _code_review_decision(self, state: WorkflowState) -> str:
        """Решение о ревью кода"""
        # Симулируем решение на основе качества кода
        code_quality = state.step_results.get("generate_code", "")
        if "хороший" in code_quality.lower() or "качественный" in code_quality.lower():
            return "approve"
        return "refactor"
    
    # Методы управления рабочими процессами
    
    def register_workflow(self, name: str, workflow: StateGraph) -> None:
        """Зарегистрировать рабочий процесс"""
        self.workflows[name] = workflow
        logger.info(f"Зарегистрирован рабочий процесс: {name}")
    
    async def run_workflow(self, workflow_name: str, initial_data: Dict[str, Any] = None) -> WorkflowState:
        """Запустить рабочий процесс"""
        if workflow_name not in self.workflows:
            raise ValueError(f"Рабочий процесс '{workflow_name}' не найден")
        
        workflow = self.workflows[workflow_name]
        
        # Создаем начальное состояние
        initial_state = WorkflowState(
            workflow_data=initial_data or {},
            metadata={"workflow_name": workflow_name}
        )
        
        try:
            # Конфигурация для checkpointer
            config = {
                "configurable": {
                    "thread_id": f"thread_{workflow_name}_{datetime.now().timestamp()}",
                    "checkpoint_id": f"checkpoint_{workflow_name}_{datetime.now().timestamp()}"
                }
            }
            
            # Запускаем рабочий процесс
            result = await workflow.ainvoke(initial_state, config)
            logger.info(f"Рабочий процесс '{workflow_name}' завершен успешно")
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при выполнении рабочего процесса '{workflow_name}': {e}")
            initial_state.errors.append(str(e))
            return initial_state
    
    def get_available_workflows(self) -> List[str]:
        """Получить список доступных рабочих процессов"""
        return list(self.workflows.keys())
    
    def get_workflow_info(self, workflow_name: str) -> Dict[str, Any]:
        """Получить информацию о рабочем процессе"""
        if workflow_name not in self.workflows:
            return {}
        
        workflow = self.workflows[workflow_name]
        
        # Безопасно получаем информацию о workflow
        info = {
            "name": workflow_name,
            "nodes": list(workflow.nodes.keys()) if hasattr(workflow, 'nodes') else [],
        }
        
        # Проверяем наличие атрибутов перед обращением к ним
        if hasattr(workflow, 'edges'):
            info["edges"] = list(workflow.edges.keys())
        else:
            info["edges"] = []
            
        if hasattr(workflow, 'conditional_edges'):
            info["has_conditional_edges"] = bool(workflow.conditional_edges)
        else:
            info["has_conditional_edges"] = False
            
        return info 
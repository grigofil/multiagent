"""
Демонстрация возможностей Итерации №3: Механизм взаимодействия агентов
Работает без необходимости API ключа
"""
import asyncio
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.workflow import AgentRouter, InteractionLogger, LangGraphWorkflowManager, Message, MessageType, RoutingRule, RoutingStrategy
from src.utils.advanced_config_loader import AdvancedConfigLoader

# Настройка логирования
console = Console()


async def main():
    """Основная функция демонстрации"""
    console.print(Panel.fit("🔄 Демонстрация Итерации №3: Механизм взаимодействия агентов", style="bold blue"))
    
    try:
        # Инициализация компонентов
        config_loader = AdvancedConfigLoader()
        agent_router = AgentRouter(config_loader)
        interaction_logger = InteractionLogger("demo_logs")
        langgraph_workflow_manager = LangGraphWorkflowManager(agent_router, interaction_logger)
        
        # Создаем директорию для логов
        os.makedirs("demo_logs", exist_ok=True)
        
        # Показываем информацию о системе
        await show_system_info(agent_router, langgraph_workflow_manager)
        
        # Демонстрируем возможности
        await demonstrate_routing(agent_router, interaction_logger)
        await demonstrate_workflows(langgraph_workflow_manager, interaction_logger)
        await demonstrate_logging(interaction_logger)
        
    except Exception as e:
        console.print(f"[red]❌ Ошибка: {e}[/red]")


async def show_system_info(agent_router: AgentRouter, langgraph_workflow_manager: LangGraphWorkflowManager):
    """Показать информацию о системе"""
    console.print("\n[bold green]📊 Информация о системе:[/bold green]")
    
    # Информация о маршрутизаторе
    router_stats = agent_router.get_stats()
    router_table = Table(title="📡 Маршрутизатор агентов")
    router_table.add_column("Метрика", style="cyan")
    router_table.add_column("Значение", style="green")
    
    router_table.add_row("Сообщений обработано", str(router_stats["messages_processed"]))
    router_table.add_row("Сообщений маршрутизировано", str(router_stats["messages_routed"]))
    router_table.add_row("Ошибок", str(router_stats["errors"]))
    router_table.add_row("Среднее время обработки", f"{router_stats['avg_processing_time']:.2f}с")
    router_table.add_row("Правил маршрутизации", str(len(agent_router.routing_rules)))
    
    console.print(router_table)
    
    # Информация о LangGraph рабочих процессах
    langgraph_workflows = langgraph_workflow_manager.get_available_workflows()
    langgraph_table = Table(title="🔄 LangGraph рабочие процессы")
    langgraph_table.add_column("Название", style="cyan")
    langgraph_table.add_column("Узлы", style="green")
    langgraph_table.add_column("Условные переходы", style="yellow")
    
    for workflow_name in langgraph_workflows:
        info = langgraph_workflow_manager.get_workflow_info(workflow_name)
        langgraph_table.add_row(
            workflow_name,
            str(len(info.get("nodes", []))),
            "Да" if info.get("has_conditional_edges", False) else "Нет"
        )
    
    console.print(langgraph_table)


async def demonstrate_routing(agent_router: AgentRouter, interaction_logger: InteractionLogger):
    """Демонстрация маршрутизации сообщений"""
    console.print("\n[bold blue]📡 Демонстрация маршрутизации сообщений:[/bold blue]")
    
    # Создаем мок-агентов для демонстрации
    class MockAgent:
        def __init__(self, name):
            self.name = name
            self.processed_messages = []
        
        async def process(self, message):
            self.processed_messages.append(message)
            return f"Обработано агентом {self.name}"
    
    agent_router.agents = {
        "analyst": MockAgent("analyst"),
        "coder": MockAgent("coder"),
        "reviewer": MockAgent("reviewer"),
        "manager": MockAgent("manager"),
        "ideator": MockAgent("ideator"),
        "assessor": MockAgent("assessor")
    }
    
    # Добавляем правила маршрутизации
    agent_router.add_default_routing_rules()
    
    # Создаем тестовые сообщения
    messages = [
        Message(
            id="msg_001",
            sender="system",
            recipients=[],
            message_type=MessageType.TASK,
            content="Проанализируй данные продаж за последний квартал и выяви тренды"
        ),
        Message(
            id="msg_002",
            sender="system",
            recipients=[],
            message_type=MessageType.TASK,
            content="Создай функцию для вычисления факториала с обработкой ошибок"
        ),
        Message(
            id="msg_003",
            sender="system",
            recipients=[],
            message_type=MessageType.TASK,
            content="Проведи ревью кода на предмет безопасности и производительности"
        ),
        Message(
            id="msg_004",
            sender="system",
            recipients=[],
            message_type=MessageType.TASK,
            content="Создай план проекта для разработки веб-приложения"
        ),
        Message(
            id="msg_005",
            sender="system",
            recipients=[],
            message_type=MessageType.TASK,
            content="Генерируй инновационные идеи для улучшения пользовательского опыта"
        ),
        Message(
            id="msg_006",
            sender="system",
            recipients=[],
            message_type=MessageType.TASK,
            content="Оцени качество и точность предоставленного анализа данных"
        )
    ]
    
    routing_table = Table(title="📨 Маршрутизация сообщений")
    routing_table.add_column("Сообщение", style="cyan")
    routing_table.add_column("Тип", style="green")
    routing_table.add_column("Маршрутизировано к", style="yellow")
    routing_table.add_column("Стратегия", style="magenta")
    
    for message in messages:
        # Логируем отправку сообщения
        interaction_logger.log_interaction(
            message=message,
            response=None,
            processing_time=0.0,
            error=None
        )
        
        # Маршрутизируем сообщение
        routed_messages = await agent_router.route_message(message)
        
        # Определяем стратегию маршрутизации
        strategy = "Последовательная"
        if len(routed_messages) > 1:
            strategy = "Параллельная"
        
        routing_table.add_row(
            message.content[:40] + "...",
            message.message_type.value,
            ", ".join([", ".join(msg.recipients) for msg in routed_messages]),
            strategy
        )
        
        # Логируем результат
        for routed_msg in routed_messages:
            response_message = Message(
                id=f"response_{routed_msg.id}",
                sender=routed_msg.recipients[0] if routed_msg.recipients else "unknown",
                recipients=[routed_msg.sender],
                message_type=MessageType.RESULT,
                content=f"Обработано агентом {routed_msg.recipients[0] if routed_msg.recipients else 'unknown'}"
            )
            interaction_logger.log_interaction(
                message=routed_msg,
                response=response_message,
                processing_time=0.1,
                error=None
            )
    
    console.print(routing_table)


async def demonstrate_workflows(langgraph_workflow_manager: LangGraphWorkflowManager, interaction_logger: InteractionLogger):
    """Демонстрация LangGraph рабочих процессов"""
    console.print("\n[bold blue]🔄 Демонстрация LangGraph рабочих процессов:[/bold blue]")
    
    # Создаем и регистрируем рабочие процессы
    workflows = {
        "data_analysis": langgraph_workflow_manager.create_data_analysis_workflow(),
        "code_development": langgraph_workflow_manager.create_code_development_workflow(),
        "project_management": langgraph_workflow_manager.create_project_management_workflow()
    }
    
    for name, workflow in workflows.items():
        langgraph_workflow_manager.register_workflow(f"demo_{name}", workflow)
    
    # Тестовые данные для разных рабочих процессов
    test_data = {
        "data_analysis": {
            "data": {
                "sales": [120, 180, 220, 190, 280],
                "months": ["Янв", "Фев", "Мар", "Апр", "Май"]
            }
        },
        "code_development": {
            "requirements": "Создай класс для работы с базой данных"
        },
        "project_management": {
            "project_name": "Веб-приложение для управления задачами",
            "requirements": "Система управления проектами с пользователями и задачами"
        }
    }
    
    workflow_table = Table(title="🔄 Выполнение рабочих процессов")
    workflow_table.add_column("Рабочий процесс", style="cyan")
    workflow_table.add_column("Статус", style="green")
    workflow_table.add_column("Шагов выполнено", style="yellow")
    workflow_table.add_column("Время выполнения", style="magenta")
    
    for workflow_name, data in test_data.items():
        start_time = datetime.now()
        
        try:
            result = await langgraph_workflow_manager.run_workflow(f"demo_{workflow_name}", data)
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            if isinstance(result, dict) and 'step_results' in result:
                status = "✅ Успешно"
                steps_count = len(result['step_results'])
            else:
                status = "❌ Ошибка"
                steps_count = 0
            
            workflow_table.add_row(
                workflow_name.replace("_", " ").title(),
                status,
                str(steps_count),
                f"{execution_time:.2f}с"
            )
            
        except Exception as e:
            workflow_table.add_row(
                workflow_name.replace("_", " ").title(),
                "❌ Ошибка",
                "0",
                "N/A"
            )
    
    console.print(workflow_table)


async def demonstrate_logging(interaction_logger: InteractionLogger):
    """Демонстрация системы логирования"""
    console.print("\n[bold blue]📊 Демонстрация системы логирования:[/bold blue]")
    
    # Получаем статистику
    stats = interaction_logger.get_system_health()
    
    stats_table = Table(title="📈 Статистика системы")
    stats_table.add_column("Метрика", style="cyan")
    stats_table.add_column("Значение", style="green")
    
    stats_table.add_row("Всего взаимодействий", str(stats['total_interactions']))
    stats_table.add_row("Процент успешных", f"{stats['success_rate']*100:.1f}%")
    stats_table.add_row("Среднее время ответа", f"{stats['avg_response_time']:.2f}с")
    stats_table.add_row("Активных агентов", str(stats['active_agents']))
    stats_table.add_row("Время работы", f"{stats['uptime']:.1f}с")
    stats_table.add_row("Последняя активность", stats['last_activity'] or "Нет")
    
    console.print(stats_table)
    
    # Показываем последние взаимодействия
    history = interaction_logger.get_interaction_history(limit=5)
    
    if history:
        history_table = Table(title="📝 Последние взаимодействия")
        history_table.add_column("Время", style="cyan")
        history_table.add_column("Отправитель", style="green")
        history_table.add_column("Получатели", style="yellow")
        history_table.add_column("Тип", style="magenta")
        history_table.add_column("Статус", style="blue")
        
        for interaction in history:
            status = "✅ Успешно" if not interaction.get('error') else "❌ Ошибка"
            history_table.add_row(
                interaction['timestamp'][:19],
                interaction['sender'],
                ", ".join(interaction['recipients']),
                interaction['message_type'],
                status
            )
        
        console.print(history_table)
    
    # Генерируем отчет
    try:
        report = interaction_logger.generate_report()
        console.print(f"\n[green]📄 Отчет сгенерирован:[/green] {len(report)} символов")
    except Exception as e:
        console.print(f"\n[red]❌ Ошибка генерации отчета: {e}[/red]")


if __name__ == "__main__":
    asyncio.run(main()) 
"""
Основной файл для запуска мультиагентной системы
"""
import asyncio
import os
from dotenv import load_dotenv
from loguru import logger
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.workflow import MultiAgentWorkflow
from src.workflow import AgentRouter, InteractionLogger, LangGraphWorkflowManager, Message, MessageType, RoutingRule, RoutingStrategy
from src.utils import ConfigLoader, get_api_key
from src.utils.advanced_config_loader import AdvancedConfigLoader
from src.prompts import PromptTemplates

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logger.add("logs/multiagent.log", rotation="1 day", retention="7 days")

console = Console()


async def main():
    """Основная функция"""
    console.print(Panel.fit("🤖 Мультиагентная система", style="bold blue"))
    
    try:
        # Инициализация
        config_loader = ConfigLoader()
        advanced_config_loader = AdvancedConfigLoader()
        api_key = get_api_key()
        
        if not api_key:
            console.print("[red]⚠️  API ключ не найден! Установите переменную OPENAI_API_KEY[/red]")
            return
        
        # Создание мультиагентной системы
        workflow_manager = MultiAgentWorkflow(config_loader, api_key)
        
        # Создание компонентов Итерации №3
        agent_router = AgentRouter(advanced_config_loader, api_key)
        interaction_logger = InteractionLogger("logs")
        langgraph_workflow_manager = LangGraphWorkflowManager(agent_router, interaction_logger)
        
        # Показываем информацию о системе
        await show_system_info(workflow_manager, advanced_config_loader, agent_router, langgraph_workflow_manager)
        
        # Запускаем примеры
        await run_examples(workflow_manager, agent_router, langgraph_workflow_manager, interaction_logger)
        
    except Exception as e:
        logger.error(f"Ошибка в основной функции: {e}")
        console.print(f"[red]❌ Ошибка: {e}[/red]")


async def show_system_info(workflow_manager: MultiAgentWorkflow, advanced_config_loader: AdvancedConfigLoader, agent_router: AgentRouter, langgraph_workflow_manager: LangGraphWorkflowManager):
    """Показать информацию о системе"""
    console.print("\n[bold green]📊 Информация о системе:[/bold green]")
    
    # Информация об агентах
    agents_info = workflow_manager.get_agents_info()
    agents_table = Table(title="🤖 Агенты")
    agents_table.add_column("ID", style="cyan")
    agents_table.add_column("Имя", style="green")
    agents_table.add_column("Роль", style="yellow")
    agents_table.add_column("Модель", style="magenta")
    agents_table.add_column("Шаблон", style="blue")
    
    for agent_id, info in agents_info.items():
        agents_table.add_row(
            agent_id,
            info["name"],
            info["role"],
            info["model"]["model_name"],
            info.get("prompt_template", "Нет")
        )
    
    console.print(agents_table)
    
    # Информация о возможностях агентов
    capabilities_table = Table(title="🔧 Возможности агентов")
    capabilities_table.add_column("Агент", style="cyan")
    capabilities_table.add_column("Возможности", style="green")
    capabilities_table.add_column("Ограничения", style="yellow")
    
    for agent_id in agents_info.keys():
        capabilities = advanced_config_loader.get_agent_capabilities(agent_id)
        limitations = advanced_config_loader.get_agent_limitations(agent_id)
        capabilities_table.add_row(
            agent_id,
            ", ".join(capabilities[:3]) + ("..." if len(capabilities) > 3 else ""),
            ", ".join(limitations[:2]) + ("..." if len(limitations) > 2 else "")
        )
    
    console.print(capabilities_table)
    
    # Информация о провайдерах
    providers = advanced_config_loader.get_supported_providers()
    providers_table = Table(title="🔌 Поддерживаемые провайдера")
    providers_table.add_column("Провайдер", style="cyan")
    providers_table.add_column("Модели", style="green")
    
    for provider in providers:
        models = advanced_config_loader.get_provider_models(provider)
        providers_table.add_row(
            provider,
            ", ".join(models[:3]) + ("..." if len(models) > 3 else "")
        )
    
    console.print(providers_table)
    
    # Информация о шаблонах промптов
    templates = PromptTemplates.list_templates()
    templates_table = Table(title="📝 Доступные шаблоны промптов")
    templates_table.add_column("Шаблон", style="cyan")
    templates_table.add_column("Переменные", style="green")
    
    for template_name in templates:
        template = PromptTemplates.get_template(template_name)
        templates_table.add_row(
            template_name,
            ", ".join(template.variables)
        )
    
    console.print(templates_table)
    
    # Информация о рабочих процессах
    workflows = workflow_manager.get_available_workflows()
    workflows_table = Table(title="🔄 Рабочие процессы")
    workflows_table.add_column("ID", style="cyan")
    workflows_table.add_column("Название", style="green")
    workflows_table.add_column("Описание", style="yellow")
    
    for workflow_id in workflows:
        info = workflow_manager.get_workflow_info(workflow_id)
        workflows_table.add_row(
            workflow_id,
            info["name"],
            info["description"]
        )
    
    console.print(workflows_table)
    
    # Информация о компонентах Итерации №3
    console.print("\n[bold green]🔄 Компоненты Итерации №3:[/bold green]")
    
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


async def run_examples(workflow_manager: MultiAgentWorkflow, agent_router: AgentRouter, langgraph_workflow_manager: LangGraphWorkflowManager, interaction_logger: InteractionLogger):
    """Запуск примеров использования"""
    console.print("\n[bold green]🚀 Запуск примеров:[/bold green]")
    
    # Пример 1: Анализ данных
    console.print("\n[bold blue]📈 Пример 1: Анализ данных[/bold blue]")
    data_analysis_data = {
        "data_input": {
            "sales": [100, 150, 200, 180, 250],
            "months": ["Янв", "Фев", "Мар", "Апр", "Май"],
            "target": 200
        }
    }
    
    result = await workflow_manager.run_workflow("data_analysis_workflow", data_analysis_data)
    
    if result["success"]:
        console.print("[green]✅ Анализ данных завершен успешно[/green]")
        console.print(f"[yellow]Результат:[/yellow] {result['context'].get('analysis_result', 'Нет результата')[:200]}...")
    else:
        console.print(f"[red]❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}[/red]")
    
    # Пример 2: Разработка и ревью кода
    console.print("\n[bold blue]💻 Пример 2: Разработка и ревью кода[/bold blue]")
    code_task_data = {
        "task_description": "Создай функцию для вычисления факториала числа с обработкой ошибок"
    }
    
    result = await workflow_manager.run_workflow("code_review_workflow", code_task_data)
    
    if result["success"]:
        console.print("[green]✅ Разработка и ревью кода завершены успешно[/green]")
        
        # Показываем результаты по шагам
        for message in result["messages"]:
            console.print(f"\n[cyan]Шаг {message['step']} - {message['agent']}:[/cyan]")
            console.print(f"[yellow]Вход:[/yellow] {str(message['input'])[:100]}...")
            console.print(f"[green]Выход:[/green] {str(message['output'])[:200]}...")
    else:
        console.print(f"[red]❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}[/red]")
    
    # Пример 3: Демонстрация маршрутизации сообщений (Итерация №3)
    console.print("\n[bold blue]📡 Пример 3: Маршрутизация сообщений (Итерация №3)[/bold blue]")
    
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
        "reviewer": MockAgent("reviewer")
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
            content="Проанализируй данные продаж за последний квартал"
        ),
        Message(
            id="msg_002",
            sender="system",
            recipients=[],
            message_type=MessageType.TASK,
            content="Создай функцию для вычисления факториала"
        ),
        Message(
            id="msg_003",
            sender="system",
            recipients=[],
            message_type=MessageType.TASK,
            content="Проведи ревью кода на предмет безопасности"
        )
    ]
    
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
        
        console.print(f"\n[cyan]Сообщение:[/cyan] {message.content[:50]}...")
        console.print(f"[green]Маршрутизировано к:[/green] {[msg.recipients for msg in routed_messages]}")
        
        # Логируем результат
        for routed_msg in routed_messages:
            interaction_logger.log_interaction(
                message=routed_msg,
                response=f"Обработано агентом {routed_msg.recipients[0] if routed_msg.recipients else 'unknown'}",
                processing_time=0.1,
                error=None
            )
    
    # Показываем статистику
    stats = interaction_logger.get_system_health()
    console.print(f"\n[green]📊 Статистика взаимодействий:[/green]")
    console.print(f"Всего взаимодействий: {stats['total_interactions']}")
    console.print(f"Среднее время обработки: {stats['avg_processing_time']:.2f}с")
    console.print(f"Ошибок: {stats['error_count']}")
    
    # Пример 4: Демонстрация LangGraph рабочего процесса (Итерация №3)
    console.print("\n[bold blue]🔄 Пример 4: LangGraph рабочий процесс (Итерация №3)[/bold blue]")
    
    # Создаем и регистрируем рабочий процесс анализа данных
    data_analysis_workflow = langgraph_workflow_manager.create_data_analysis_workflow()
    langgraph_workflow_manager.register_workflow("demo_data_analysis", data_analysis_workflow)
    
    # Тестовые данные
    demo_data = {
        "data": {
            "sales": [120, 180, 220, 190, 280],
            "months": ["Янв", "Фев", "Мар", "Апр", "Май"]
        }
    }
    
    # Запускаем рабочий процесс
    result = await langgraph_workflow_manager.run_workflow("demo_data_analysis", demo_data)
    
    if isinstance(result, dict) and 'step_results' in result:
        console.print("[green]✅ LangGraph рабочий процесс завершен успешно[/green]")
        console.print(f"[yellow]Выполнено шагов:[/yellow] {len(result['step_results'])}")
        
        for step, result_text in result['step_results'].items():
            console.print(f"  [cyan]{step}:[/cyan] {result_text}")
    else:
        console.print(f"[red]❌ Ошибка в LangGraph рабочем процессе[/red]")
    
    # Демонстрация Итерации №4
    console.print("\n[bold blue]🎯 ДЕМОНСТРАЦИЯ ИТЕРАЦИИ №4[/bold blue]")
    console.print("="*80)
    
    try:
        from demo_iteration4 import Iteration4Demo
        demo4 = Iteration4Demo()
        demo4.run_demo()
    except ImportError as e:
        console.print(f"[red]❌ Ошибка импорта демо Итерации №4: {e}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Ошибка в демо Итерации №4: {e}[/red]")
    
    # Демонстрация Итерации №5
    console.print("\n[bold blue]🎯 ДЕМОНСТРАЦИЯ ИТЕРАЦИИ №5[/bold blue]")
    console.print("="*80)
    
    try:
        from demo_iteration5 import Iteration5Demo
        demo5 = Iteration5Demo()
        await demo5.run_demo()
    except ImportError as e:
        console.print(f"[red]❌ Ошибка импорта демо Итерации №5: {e}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Ошибка в демо Итерации №5: {e}[/red]")


if __name__ == "__main__":
    # Создаем директорию для логов
    os.makedirs("logs", exist_ok=True)
    
    # Запускаем основную функцию
    asyncio.run(main()) 
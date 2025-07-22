"""
Пример использования мультиагентной системы
"""
import asyncio
import os
from dotenv import load_dotenv
from loguru import logger
from rich.console import Console
from rich.panel import Panel

from src.workflow import MultiAgentWorkflow
from src.utils import ConfigLoader, get_api_key

# Загружаем переменные окружения
load_dotenv()

console = Console()


async def example_data_analysis():
    """Пример анализа данных с помощью мультиагентной системы"""
    console.print(Panel.fit("📊 Пример: Анализ данных", style="bold green"))
    
    try:
        # Инициализация
        config_loader = ConfigLoader()
        api_key = get_api_key()
        
        if not api_key:
            console.print("[red]⚠️  API ключ не найден![/red]")
            return
        
        workflow_manager = MultiAgentWorkflow(config_loader, api_key)
        
        # Данные для анализа
        sample_data = {
            "data_input": {
                "company": "TechCorp",
                "quarterly_revenue": [1200000, 1350000, 1420000, 1580000],
                "quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expenses": [800000, 850000, 900000, 950000],
                "target_growth": 0.15
            }
        }
        
        console.print("[yellow]📈 Анализируем финансовые данные компании...[/yellow]")
        
        # Запускаем анализ
        result = await workflow_manager.run_workflow("data_analysis_workflow", sample_data)
        
        if result["success"]:
            console.print("[green]✅ Анализ завершен успешно![/green]")
            
            analysis_result = result["context"].get("analysis_result", "")
            console.print(f"\n[bold]Результат анализа:[/bold]\n{analysis_result}")
            
        else:
            console.print(f"[red]❌ Ошибка: {result.get('error')}[/red]")
            
    except Exception as e:
        logger.error(f"Ошибка в примере анализа данных: {e}")
        console.print(f"[red]❌ Ошибка: {e}[/red]")


async def example_code_development():
    """Пример разработки кода с ревью"""
    console.print(Panel.fit("💻 Пример: Разработка кода", style="bold blue"))
    
    try:
        # Инициализация
        config_loader = ConfigLoader()
        api_key = get_api_key()
        
        if not api_key:
            console.print("[red]⚠️  API ключ не найден![/red]")
            return
        
        workflow_manager = MultiAgentWorkflow(config_loader, api_key)
        
        # Задача для разработки
        coding_task = {
            "task_description": """
            Создай Python класс для работы с базой данных SQLite, который должен:
            1. Поддерживать подключение к базе данных
            2. Выполнять CRUD операции (Create, Read, Update, Delete)
            3. Обрабатывать ошибки и исключения
            4. Использовать контекстные менеджеры
            5. Включать логирование операций
            """,
            "requirements": "Используй современные практики Python, добавь типизацию и документацию"
        }
        
        console.print("[yellow]🔧 Разрабатываем класс для работы с базой данных...[/yellow]")
        
        # Запускаем процесс разработки и ревью
        result = await workflow_manager.run_workflow("code_review_workflow", coding_task)
        
        if result["success"]:
            console.print("[green]✅ Разработка и ревью завершены успешно![/green]")
            
            # Показываем результаты по шагам
            for i, message in enumerate(result["messages"], 1):
                console.print(f"\n[bold cyan]Шаг {i}: {message['agent']}[/bold cyan]")
                
                if message['agent'] == 'coder':
                    console.print("[green]Сгенерированный код:[/green]")
                    code_output = str(message['output'])
                    # Показываем только начало кода
                    console.print(code_output[:500] + "..." if len(code_output) > 500 else code_output)
                
                elif message['agent'] == 'reviewer':
                    console.print("[yellow]Ревью кода:[/yellow]")
                    review_output = str(message['output'])
                    console.print(review_output[:300] + "..." if len(review_output) > 300 else review_output)
            
            # Финальный результат
            final_code = result["context"].get("improved_code", "")
            if final_code:
                console.print(f"\n[bold green]🎯 Финальный улучшенный код:[/bold green]")
                console.print(final_code[:800] + "..." if len(final_code) > 800 else final_code)
                
        else:
            console.print(f"[red]❌ Ошибка: {result.get('error')}[/red]")
            
    except Exception as e:
        logger.error(f"Ошибка в примере разработки кода: {e}")
        console.print(f"[red]❌ Ошибка: {e}[/red]")


async def example_project_management():
    """Пример управления проектом"""
    console.print(Panel.fit("📋 Пример: Управление проектом", style="bold magenta"))
    
    try:
        # Инициализация
        config_loader = ConfigLoader()
        api_key = get_api_key()
        
        if not api_key:
            console.print("[red]⚠️  API ключ не найден![/red]")
            return
        
        workflow_manager = MultiAgentWorkflow(config_loader, api_key)
        
        # Данные проекта
        project_data = {
            "data_input": {
                "project_name": "E-commerce Platform",
                "description": "Разработка современной платформы электронной коммерции",
                "team_size": 8,
                "deadline": "6 месяцев",
                "budget": "$500,000",
                "technologies": ["React", "Node.js", "PostgreSQL", "Redis"],
                "key_features": [
                    "Пользовательская аутентификация",
                    "Каталог товаров",
                    "Корзина покупок",
                    "Система платежей",
                    "Админ-панель",
                    "API для мобильных приложений"
                ]
            }
        }
        
        console.print("[yellow]📋 Анализируем проект и создаем план управления...[/yellow]")
        
        # Запускаем анализ проекта
        result = await workflow_manager.run_workflow("data_analysis_workflow", project_data)
        
        if result["success"]:
            console.print("[green]✅ Анализ проекта завершен успешно![/green]")
            
            analysis_result = result["context"].get("analysis_result", "")
            console.print(f"\n[bold]Результат анализа проекта:[/bold]\n{analysis_result}")
            
        else:
            console.print(f"[red]❌ Ошибка: {result.get('error')}[/red]")
            
    except Exception as e:
        logger.error(f"Ошибка в примере управления проектом: {e}")
        console.print(f"[red]❌ Ошибка: {e}[/red]")


async def main():
    """Запуск всех примеров"""
    console.print(Panel.fit("🚀 Примеры использования мультиагентной системы", style="bold blue"))
    
    # Создаем директорию для логов
    os.makedirs("logs", exist_ok=True)
    
    # Запускаем примеры
    await example_data_analysis()
    console.print("\n" + "="*80 + "\n")
    
    await example_code_development()
    console.print("\n" + "="*80 + "\n")
    
    await example_project_management()


if __name__ == "__main__":
    asyncio.run(main()) 
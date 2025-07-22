#!/usr/bin/env python3
"""
Пример анализа данных из Confluence/JIRA
Демонстрирует использование ConfluenceJiraAnalystAgent для анализа данных
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Импорты для работы с агентами
from src.agents.task_specific_agents import ConfluenceJiraAnalystAgent, TaskSpecificAgentFactory
from src.agents.base_agent import AgentConfig

console = Console()


class ConfluenceJiraAnalysisExample:
    """Пример анализа данных из Confluence/JIRA"""
    
    def __init__(self):
        self.console = Console()
        self.analyst_agent = None
        self.setup_agent()
    
    def setup_agent(self):
        """Настройка агента-аналитика"""
        config = AgentConfig(
            name="Confluence/JIRA Analyst",
            role="Data Analyst",
            description="Специалист по анализу данных из Confluence и JIRA",
            model={
                "provider": "openai",
                "model_name": "gpt-4",
                "temperature": 0.1,
                "max_tokens": 4000,
                "top_p": 0.9
            },
            system_prompt="""Ты опытный аналитик данных, специализирующийся на анализе данных из Confluence и JIRA.
            Твоя задача - извлекать инсайты, выявлять паттерны и предоставлять рекомендации на основе данных.
            Всегда давай конкретные, actionable рекомендации с метриками.""",
            capabilities=[
                "data_analysis",
                "trend_analysis", 
                "collaboration_analysis",
                "project_health_assessment",
                "team_productivity_analysis"
            ],
            limitations=["cannot_access_real_apis", "works_with_mock_data"]
        )
        
        self.analyst_agent = ConfluenceJiraAnalystAgent(config, "demo-key")
    
    def generate_mock_jira_data(self) -> Dict[str, Any]:
        """Генерация мок-данных JIRA"""
        return {
            "project": "Multi-Agent System",
            "period": "Last 30 days",
            "issues": [
                {
                    "key": "PROJ-101",
                    "summary": "Implement base agent functionality",
                    "status": "Done",
                    "priority": "High",
                    "assignee": "Alice Johnson",
                    "created": "2024-01-15",
                    "resolved": "2024-01-20",
                    "story_points": 8,
                    "labels": ["backend", "core"]
                },
                {
                    "key": "PROJ-102", 
                    "summary": "Add agent communication system",
                    "status": "In Progress",
                    "priority": "High",
                    "assignee": "Bob Smith",
                    "created": "2024-01-18",
                    "resolved": None,
                    "story_points": 13,
                    "labels": ["communication", "core"]
                },
                {
                    "key": "PROJ-103",
                    "summary": "Create user interface",
                    "status": "To Do",
                    "priority": "Medium",
                    "assignee": "Carol Davis",
                    "created": "2024-01-20",
                    "resolved": None,
                    "story_points": 5,
                    "labels": ["frontend", "ui"]
                },
                {
                    "key": "PROJ-104",
                    "summary": "Write documentation",
                    "status": "Done",
                    "priority": "Low",
                    "assignee": "David Wilson",
                    "created": "2024-01-10",
                    "resolved": "2024-01-25",
                    "story_points": 3,
                    "labels": ["documentation"]
                },
                {
                    "key": "PROJ-105",
                    "summary": "Add unit tests",
                    "status": "In Progress",
                    "priority": "Medium",
                    "assignee": "Eve Brown",
                    "created": "2024-01-22",
                    "resolved": None,
                    "story_points": 8,
                    "labels": ["testing", "quality"]
                }
            ],
            "sprints": [
                {
                    "name": "Sprint 1",
                    "start_date": "2024-01-15",
                    "end_date": "2024-01-28",
                    "planned_points": 25,
                    "completed_points": 11
                }
            ]
        }
    
    def generate_mock_confluence_data(self) -> Dict[str, Any]:
        """Генерация мок-данных Confluence"""
        return {
            "space": "Multi-Agent System",
            "period": "Last 30 days",
            "pages": [
                {
                    "title": "System Architecture Overview",
                    "author": "Alice Johnson",
                    "created": "2024-01-15",
                    "updated": "2024-01-20",
                    "views": 45,
                    "likes": 8,
                    "comments": [
                        {"author": "Bob Smith", "content": "Great overview!", "date": "2024-01-16"},
                        {"author": "Carol Davis", "content": "Need more details on UI", "date": "2024-01-17"}
                    ],
                    "tags": ["architecture", "documentation"],
                    "word_count": 1200
                },
                {
                    "title": "API Documentation",
                    "author": "Bob Smith", 
                    "created": "2024-01-18",
                    "updated": "2024-01-22",
                    "views": 32,
                    "likes": 5,
                    "comments": [
                        {"author": "David Wilson", "content": "Very helpful!", "date": "2024-01-19"}
                    ],
                    "tags": ["api", "documentation"],
                    "word_count": 800
                },
                {
                    "title": "Development Guidelines",
                    "author": "Carol Davis",
                    "created": "2024-01-20",
                    "updated": "2024-01-25",
                    "views": 28,
                    "likes": 6,
                    "comments": [
                        {"author": "Eve Brown", "content": "Should add testing guidelines", "date": "2024-01-21"},
                        {"author": "Alice Johnson", "content": "Agreed, will update", "date": "2024-01-22"}
                    ],
                    "tags": ["guidelines", "development"],
                    "word_count": 600
                },
                {
                    "title": "Project Status Report",
                    "author": "David Wilson",
                    "created": "2024-01-25",
                    "updated": "2024-01-25",
                    "views": 15,
                    "likes": 3,
                    "comments": [],
                    "tags": ["status", "report"],
                    "word_count": 400
                }
            ]
        }
    
    def show_jira_analysis(self, jira_data: Dict[str, Any]):
        """Показать анализ данных JIRA"""
        self.console.print("\n" + "="*80)
        self.console.print("📊 АНАЛИЗ ДАННЫХ JIRA", style="bold blue")
        self.console.print("="*80)
        
        # Извлекаем метрики
        metrics = self.analyst_agent.extract_jira_metrics(jira_data)
        
        # Создаем таблицу с метриками
        metrics_table = Table(title="Метрики JIRA")
        metrics_table.add_column("Метрика", style="cyan")
        metrics_table.add_column("Значение", style="green")
        metrics_table.add_column("Описание", style="yellow")
        
        metrics_table.add_row(
            "Всего задач",
            str(metrics["total_issues"]),
            "Общее количество задач в проекте"
        )
        
        # Статусы задач
        status_summary = ", ".join([f"{status}: {count}" for status, count in metrics["by_status"].items()])
        metrics_table.add_row(
            "Распределение по статусам",
            status_summary,
            "Текущее состояние задач"
        )
        
        # Приоритеты
        priority_summary = ", ".join([f"{priority}: {count}" for priority, count in metrics["by_priority"].items()])
        metrics_table.add_row(
            "Распределение по приоритетам",
            priority_summary,
            "Важность задач"
        )
        
        # Исполнители
        assignee_summary = ", ".join([f"{assignee}: {count}" for assignee, count in metrics["by_assignee"].items()])
        metrics_table.add_row(
            "Распределение по исполнителям",
            assignee_summary,
            "Нагрузка на команду"
        )
        
        self.console.print(metrics_table)
        
        # Анализ спринтов
        if jira_data.get("sprints"):
            self.console.print("\n🏃 Анализ спринтов:")
            sprint_table = Table()
            sprint_table.add_column("Спринт", style="cyan")
            sprint_table.add_column("Запланировано", style="green")
            sprint_table.add_column("Выполнено", style="yellow")
            sprint_table.add_column("Прогресс", style="magenta")
            
            for sprint in jira_data["sprints"]:
                planned = sprint["planned_points"]
                completed = sprint["completed_points"]
                progress = (completed / planned * 100) if planned > 0 else 0
                
                sprint_table.add_row(
                    sprint["name"],
                    str(planned),
                    str(completed),
                    f"{progress:.1f}%"
                )
            
            self.console.print(sprint_table)
        
        # Рекомендации
        self.console.print("\n💡 Рекомендации:")
        recommendations = [
            "📈 Увеличить количество завершенных задач в текущем спринте",
            "⚖️ Сбалансировать нагрузку между исполнителями",
            "🎯 Приоритизировать задачи с высоким приоритетом",
            "📊 Регулярно отслеживать прогресс спринтов"
        ]
        
        for rec in recommendations:
            self.console.print(f"   {rec}")
    
    def show_confluence_analysis(self, confluence_data: Dict[str, Any]):
        """Показать анализ данных Confluence"""
        self.console.print("\n" + "="*80)
        self.console.print("📚 АНАЛИЗ ДАННЫХ CONFLUENCE", style="bold blue")
        self.console.print("="*80)
        
        # Извлекаем инсайты
        insights = self.analyst_agent.extract_confluence_insights(confluence_data)
        
        # Создаем таблицу с инсайтами
        insights_table = Table(title="Инсайты Confluence")
        insights_table.add_column("Метрика", style="cyan")
        insights_table.add_column("Значение", style="green")
        insights_table.add_column("Описание", style="yellow")
        
        insights_table.add_row(
            "Всего страниц",
            str(insights["total_pages"]),
            "Количество созданных страниц"
        )
        
        insights_table.add_row(
            "Всего комментариев",
            str(insights["total_comments"]),
            "Активность обсуждений"
        )
        
        # Самые активные авторы
        top_authors = sorted(insights["most_active_authors"].items(), key=lambda x: x[1], reverse=True)[:3]
        authors_summary = ", ".join([f"{author}: {count}" for author, count in top_authors])
        insights_table.add_row(
            "Топ авторы",
            authors_summary,
            "Наиболее активные участники"
        )
        
        # Популярные темы
        top_topics = sorted(insights["popular_topics"].items(), key=lambda x: x[1], reverse=True)[:3]
        topics_summary = ", ".join([f"{topic}: {count}" for topic, count in top_topics])
        insights_table.add_row(
            "Популярные темы",
            topics_summary,
            "Часто используемые теги"
        )
        
        self.console.print(insights_table)
        
        # Анализ страниц
        self.console.print("\n📄 Анализ страниц:")
        pages_table = Table()
        pages_table.add_column("Страница", style="cyan")
        pages_table.add_column("Автор", style="green")
        pages_table.add_column("Просмотры", style="yellow")
        pages_table.add_column("Лайки", style="magenta")
        pages_table.add_column("Комментарии", style="blue")
        
        for page in confluence_data["pages"]:
            pages_table.add_row(
                page["title"][:30] + "..." if len(page["title"]) > 30 else page["title"],
                page["author"],
                str(page["views"]),
                str(page["likes"]),
                str(len(page["comments"]))
            )
        
        self.console.print(pages_table)
        
        # Рекомендации
        self.console.print("\n💡 Рекомендации:")
        recommendations = [
            "📝 Поощрять создание документации всеми участниками команды",
            "💬 Активизировать обсуждения в комментариях",
            "🏷️ Использовать теги для лучшей организации контента",
            "📊 Регулярно обновлять популярные страницы"
        ]
        
        for rec in recommendations:
            self.console.print(f"   {rec}")
    
    async def run_comprehensive_analysis(self):
        """Запуск комплексного анализа"""
        self.console.print(Panel(
            "🔍 Комплексный анализ данных Confluence/JIRA\n\n"
            "Этот пример демонстрирует:\n"
            "• Извлечение метрик из данных JIRA\n"
            "• Анализ активности в Confluence\n"
            "• Генерацию рекомендаций\n"
            "• Визуализацию результатов",
            title="📊 Пример анализа данных Confluence/JIRA",
            border_style="blue"
        ))
        
        # Генерируем мок-данные
        with self.console.status("[bold green]Генерация тестовых данных..."):
            jira_data = self.generate_mock_jira_data()
            confluence_data = self.generate_mock_confluence_data()
        
        # Анализируем данные JIRA
        self.show_jira_analysis(jira_data)
        
        # Анализируем данные Confluence
        self.show_confluence_analysis(confluence_data)
        
        # Комплексный анализ через агента
        self.console.print("\n" + "="*80)
        self.console.print("🤖 АНАЛИЗ ЧЕРЕЗ ИИ АГЕНТА", style="bold blue")
        self.console.print("="*80)
        
        # Подготавливаем данные для агента
        analysis_request = {
            "data_source": "jira_confluence",
            "jira_data": jira_data,
            "confluence_data": confluence_data,
            "analysis_type": "comprehensive",
            "metrics": ["productivity", "collaboration", "documentation_quality"],
            "context": "Анализ эффективности команды разработки"
        }
        
        with self.console.status("[bold green]Анализ через ИИ агента..."):
            try:
                # Мокаем ответ агента для демонстрации
                ai_analysis = """## Комплексный анализ команды разработки

### 📈 Ключевые метрики:
- **Продуктивность команды**: 44% от запланированного в спринте
- **Активность документации**: 4 страницы за 30 дней
- **Вовлеченность**: 8 лайков и 5 комментариев

### 🎯 Основные выводы:
1. **Прогресс спринта**: Команда отстает от графика на 56%
2. **Документация**: Хорошая активность, но можно улучшить
3. **Коммуникация**: Умеренная активность в комментариях

### 💡 Рекомендации:
1. **Приоритизация**: Сфокусироваться на завершении текущих задач
2. **Коммуникация**: Увеличить активность в обсуждениях
3. **Документация**: Продолжить создание качественной документации
4. **Мониторинг**: Регулярно отслеживать прогресс спринтов

### 🚀 Следующие шаги:
- Провести ретроспективу спринта
- Пересмотреть оценки задач
- Улучшить процессы коммуникации"""
                
                self.console.print(Panel(ai_analysis, title="🤖 Анализ ИИ агента", border_style="green"))
                
            except Exception as e:
                self.console.print(f"❌ Ошибка анализа: {e}", style="red")
        
        # Итоговая сводка
        self.console.print("\n" + "="*80)
        self.console.print("📋 ИТОГОВАЯ СВОДКА", style="bold blue")
        self.console.print("="*80)
        
        summary_table = Table()
        summary_table.add_column("Аспект", style="cyan")
        summary_table.add_column("Статус", style="green")
        summary_table.add_column("Рекомендация", style="yellow")
        
        summary_table.add_row(
            "Продуктивность",
            "⚠️ Требует внимания",
            "Улучшить планирование спринтов"
        )
        summary_table.add_row(
            "Документация",
            "✅ Хорошо",
            "Продолжить текущую активность"
        )
        summary_table.add_row(
            "Коммуникация",
            "🟡 Удовлетворительно",
            "Увеличить активность в обсуждениях"
        )
        summary_table.add_row(
            "Качество",
            "✅ Хорошо",
            "Поддерживать текущие стандарты"
        )
        
        self.console.print(summary_table)
        
        self.console.print("\n🎯 Этот пример демонстрирует возможности анализа данных из Confluence/JIRA!")
        self.console.print("   Используйте ConfluenceJiraAnalystAgent для автоматизации анализа ваших проектов.")


def main():
    """Главная функция"""
    console.print("🚀 Запуск примера анализа Confluence/JIRA...")
    
    # Создаем и запускаем пример
    example = ConfluenceJiraAnalysisExample()
    asyncio.run(example.run_comprehensive_analysis())


if __name__ == "__main__":
    main() 
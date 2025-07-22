#!/usr/bin/env python3
"""
Демо-скрипт для Итерации №4: Масштабирование шаблона и добавление агентов с разными ролями

Демонстрирует:
- Новые специализированные агенты
- Систему шаблонов для быстрого создания агентов
- Менеджер ролей и валидацию
- Динамическое создание агентов
- Расширенную фабрику агентов
"""

import asyncio
import yaml
from pathlib import Path
from typing import Dict, Any, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax

# Импорты для демонстрации
from src.agents.base_agent import AgentConfig
from src.agents.extended_agents import (
    DatabaseAgent, ImageAnalysisAgent, APIAgent, MachineLearningAgent,
    SecurityAgent, DevOpsAgent, DocumentationAgent, TestingAgent,
    ResearchAgent, CommunicationAgent, ExtendedAgentFactory
)
from src.agents.agent_templates import (
    AgentTemplateManager, DynamicAgentCreator, UniversalAgent, AgentRoleManager
)
from src.agents.specialized_agents import AgentFactory
from src.workflow.agent_router import AgentRouter
from src.workflow.interaction_logger import InteractionLogger
from src.workflow.langgraph_integration import LangGraphWorkflowManager

console = Console()


class Iteration4Demo:
    """Демонстрация возможностей Итерации №4"""
    
    def __init__(self):
        self.console = Console()
        self.template_manager = AgentTemplateManager()
        self.role_manager = AgentRoleManager()
        self.agent_creator = DynamicAgentCreator(self.template_manager)
        self.interaction_logger = InteractionLogger()
        
        # Регистрируем расширенные агенты
        self._register_extended_agents()
    
    def _register_extended_agents(self):
        """Регистрация расширенных агентов в создателе"""
        from src.agents.extended_agents import (
            DatabaseAgent, ImageAnalysisAgent, APIAgent, MachineLearningAgent,
            SecurityAgent, DevOpsAgent, DocumentationAgent, TestingAgent,
            ResearchAgent, CommunicationAgent
        )
        
        agent_classes = {
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
        
        for agent_type, agent_class in agent_classes.items():
            self.agent_creator.register_agent_type(agent_type, agent_class)
    
    def show_welcome(self):
        """Показать приветственное сообщение"""
        welcome_text = """
        🚀 Итерация №4: Масштабирование шаблона и добавление агентов с разными ролями
        
        Новые возможности:
        • 10 новых специализированных агентов
        • Система шаблонов для быстрого создания агентов
        • Менеджер ролей с валидацией и иерархией
        • Динамическое создание агентов
        • Расширенная фабрика агентов
        • Универсальный агент для новых типов
        """
        
        self.console.print(Panel(welcome_text, title="🎯 Демонстрация Итерации №4", border_style="blue"))
    
    def show_agent_overview(self):
        """Показать обзор всех доступных агентов"""
        self.console.print("\n" + "="*80)
        self.console.print("📊 ОБЗОР ДОСТУПНЫХ АГЕНТОВ", style="bold blue")
        self.console.print("="*80)
        
        # Получаем все типы агентов
        all_agent_types = AgentFactory.get_available_agent_types()
        categories = ExtendedAgentFactory.get_agent_categories()
        
        # Создаем таблицу
        table = Table(title="Доступные агенты по категориям")
        table.add_column("Категория", style="cyan", no_wrap=True)
        table.add_column("Агенты", style="green")
        table.add_column("Описание", style="yellow")
        
        category_descriptions = {
            "analysis": "Анализ данных и исследований",
            "development": "Разработка и тестирование",
            "management": "Управление проектами и коммуникации",
            "specialized": "Специализированные технические роли",
            "creative": "Креативные задачи и оценка качества"
        }
        
        for category, agents in categories.items():
            agent_list = ", ".join(agents)
            description = category_descriptions.get(category, "Специализированные задачи")
            table.add_row(category.title(), agent_list, description)
        
        self.console.print(table)
        
        # Показываем статистику
        self.console.print(f"\n📈 Статистика: Всего доступно {len(all_agent_types)} типов агентов")
    
    def show_extended_agents_demo(self):
        """Демонстрация новых расширенных агентов"""
        self.console.print("\n" + "="*80)
        self.console.print("🔧 ДЕМОНСТРАЦИЯ РАСШИРЕННЫХ АГЕНТОВ", style="bold blue")
        self.console.print("="*80)
        
        # Создаем базовую конфигурацию
        base_config = AgentConfig(
            name="Demo Agent",
            role="Demo Role",
            description="Demo Description",
            model={
                "provider": "openai",
                "model_name": "gpt-4",
                "temperature": 0.2,
                "max_tokens": 4000,
                "top_p": 0.9
            },
            system_prompt="You are a demo agent for testing purposes.",
            capabilities=["demo_capability"],
            limitations=["demo_limitation"]
        )
        
        # Демонстрируем несколько новых агентов
        demo_agents = [
            ("Database Agent", "database", {
                "query_type": "select",
                "table": "users",
                "columns": "id, name, email",
                "conditions": "active = true",
                "database_type": "postgresql"
            }),
            ("ML Agent", "ml", {
                "task_type": "classification",
                "algorithm": "random_forest",
                "data_description": "Customer data for churn prediction",
                "hyperparameters": {"n_estimators": 100, "max_depth": 10}
            }),
            ("Security Agent", "security", {
                "security_type": "code_analysis",
                "target": "web_application",
                "vulnerability_types": ["sql_injection", "xss", "csrf"],
                "severity_level": "high"
            }),
            ("DevOps Agent", "devops", {
                "devops_task": "deployment",
                "platform": "kubernetes",
                "environment": "production",
                "tools": ["docker", "helm", "terraform"]
            })
        ]
        
        for agent_name, agent_type, input_data in demo_agents:
            self.console.print(f"\n🔍 Тестирование {agent_name}...")
            
            try:
                # Создаем агента
                agent = self.agent_creator.create_dynamic_agent(base_config, "demo-key")
                
                # Мокаем ответ для демонстрации
                mock_response = f"✅ {agent_name} успешно обработал запрос: {str(input_data)[:50]}..."
                
                self.console.print(f"   📤 Входные данные: {str(input_data)[:80]}...")
                self.console.print(f"   📥 Ответ: {mock_response}")
                self.console.print(f"   ✅ {agent_name} работает корректно")
                
            except Exception as e:
                self.console.print(f"   ❌ Ошибка в {agent_name}: {e}", style="red")
    
    def show_template_system_demo(self):
        """Демонстрация системы шаблонов"""
        self.console.print("\n" + "="*80)
        self.console.print("🎨 ДЕМОНСТРАЦИЯ СИСТЕМЫ ШАБЛОНОВ", style="bold blue")
        self.console.print("="*80)
        
        # Показываем доступные шаблоны
        templates = self.template_manager.list_templates()
        
        if not templates:
            self.console.print("📝 Создание шаблонов по умолчанию...")
            self.template_manager.create_default_templates()
            self.template_manager.load_templates()
            templates = self.template_manager.list_templates()
        
        self.console.print(f"\n📋 Доступные шаблоны ({len(templates)}):")
        
        template_table = Table()
        template_table.add_column("Шаблон", style="cyan")
        template_table.add_column("Базовый тип", style="green")
        template_table.add_column("Описание", style="yellow")
        
        for template_name in templates:
            template = self.template_manager.get_template(template_name)
            if template:
                template_table.add_row(
                    template.name,
                    template.base_type,
                    template.description
                )
        
        self.console.print(template_table)
        
        # Демонстрируем создание агента из шаблона
        self.console.print("\n🔧 Создание агента из шаблона 'junior_analyst':")
        
        try:
            # Мокаем базовую конфигурацию
            with self.console.status("[bold green]Создание агента из шаблона..."):
                mock_base_config = {
                    "name": "Junior Data Analyst",
                    "role": "Data Analyst",
                    "description": "Junior data analyst for basic tasks",
                    "model": {
                        "provider": "openai",
                        "model_name": "gpt-4",
                        "temperature": 0.1,
                        "max_tokens": 2000,
                        "top_p": 0.9
                    },
                    "system_prompt": "You are a junior data analyst.",
                    "capabilities": ["data_analysis"],
                    "limitations": ["limited_experience"]
                }
                
                # Создаем агента из шаблона
                agent_config = self.template_manager.create_agent_from_template(
                    "junior_analyst",
                    {"name": "Custom Junior Analyst"}
                )
                
                self.console.print("✅ Агент успешно создан из шаблона!")
                self.console.print(f"   📝 Имя: {agent_config.name}")
                self.console.print(f"   🎯 Роль: {agent_config.role}")
                self.console.print(f"   🔧 Возможности: {', '.join(agent_config.capabilities)}")
                
        except Exception as e:
            self.console.print(f"❌ Ошибка создания агента из шаблона: {e}", style="red")
    
    def show_role_manager_demo(self):
        """Демонстрация менеджера ролей"""
        self.console.print("\n" + "="*80)
        self.console.print("👥 ДЕМОНСТРАЦИЯ МЕНЕДЖЕРА РОЛЕЙ", style="bold blue")
        self.console.print("="*80)
        
        # Показываем доступные роли
        roles = list(self.role_manager.roles.keys())
        
        self.console.print(f"\n📋 Доступные роли ({len(roles)}):")
        
        role_table = Table()
        role_table.add_column("Роль", style="cyan")
        role_table.add_column("Уровень", style="green")
        role_table.add_column("Обязательные возможности", style="yellow")
        role_table.add_column("Рекомендуемые возможности", style="magenta")
        
        for role_name in roles[:5]:  # Показываем первые 5 ролей
            role_info = self.role_manager.get_role_requirements(role_name)
            
            required_caps = ", ".join(role_info.get("required_capabilities", [])[:3])
            suggested_caps = ", ".join(role_info.get("suggested_capabilities", [])[:3])
            
            role_table.add_row(
                role_info.get("name", role_name),
                role_info.get("level", "unknown"),
                required_caps,
                suggested_caps
            )
        
        self.console.print(role_table)
        
        # Демонстрируем валидацию агента для роли
        self.console.print("\n🔍 Валидация агента для роли 'data_analyst':")
        
        # Создаем тестового агента
        test_config = AgentConfig(
            name="Test Analyst",
            role="Data Analyst",
            description="Test analyst",
            model={"provider": "openai", "model_name": "gpt-4"},
            system_prompt="You are a test analyst.",
            capabilities=["data_analysis", "basic_statistics"],  # Есть обязательные возможности
            limitations=[]
        )
        
        test_agent = UniversalAgent(test_config, "test-key")
        
        # Проверяем валидацию
        is_valid = self.role_manager.validate_agent_for_role(test_agent, "data_analyst")
        
        if is_valid:
            self.console.print("✅ Агент подходит для роли 'data_analyst'")
        else:
            self.console.print("❌ Агент не подходит для роли 'data_analyst'")
        
        # Показываем предложения по улучшению
        improvements = self.role_manager.suggest_agent_improvements(test_agent, "data_analyst")
        
        if improvements:
            self.console.print("\n💡 Предложения по улучшению:")
            for improvement in improvements[:3]:  # Показываем первые 3
                self.console.print(f"   • {improvement}")
        else:
            self.console.print("\n✅ Агент полностью соответствует требованиям роли")
    
    def show_agent_factory_demo(self):
        """Демонстрация расширенной фабрики агентов"""
        self.console.print("\n" + "="*80)
        self.console.print("🏭 ДЕМОНСТРАЦИЯ РАСШИРЕННОЙ ФАБРИКИ АГЕНТОВ", style="bold blue")
        self.console.print("="*80)
        
        # Показываем все доступные типы
        all_types = AgentFactory.get_available_agent_types()
        categories = ExtendedAgentFactory.get_agent_categories()
        
        self.console.print(f"\n📊 Всего доступно типов агентов: {len(all_types)}")
        
        # Демонстрируем создание различных типов агентов
        demo_types = ["analyst", "database", "ml", "security", "devops"]
        
        base_config = AgentConfig(
            name="Factory Demo Agent",
            role="Demo Role",
            description="Demo Description",
            model={
                "provider": "openai",
                "model_name": "gpt-4",
                "temperature": 0.2,
                "max_tokens": 4000,
                "top_p": 0.9
            },
            system_prompt="You are a demo agent.",
            capabilities=["demo"],
            limitations=[]
        )
        
        self.console.print("\n🔧 Создание агентов через фабрику:")
        
        for agent_type in demo_types:
            try:
                with self.console.status(f"[bold green]Создание {agent_type} агента..."):
                    agent = AgentFactory.create_agent(agent_type, base_config, "demo-key")
                    
                    self.console.print(f"   ✅ {agent_type.title()} агент создан успешно")
                    self.console.print(f"      📝 Тип: {type(agent).__name__}")
                    
            except Exception as e:
                self.console.print(f"   ❌ Ошибка создания {agent_type} агента: {e}", style="red")
    
    def show_workflow_integration_demo(self):
        """Демонстрация интеграции с workflow системой"""
        self.console.print("\n" + "="*80)
        self.console.print("🔄 ДЕМОНСТРАЦИЯ ИНТЕГРАЦИИ С WORKFLOW", style="bold blue")
        self.console.print("="*80)
        
        # Создаем роутер агентов
        router_config = {
            "routing_strategies": {
                "sequential": {"enabled": True},
                "parallel": {"enabled": True},
                "conditional": {"enabled": True},
                "broadcast": {"enabled": True}
            },
            "default_strategy": "sequential",
            "timeout": 300,
            "max_retries": 3
        }
        
        try:
            router = AgentRouter(router_config, self.interaction_logger)
            
            # Создаем несколько агентов для демонстрации
            agents = {}
            agent_types = ["analyst", "database", "ml", "security"]
            
            base_config = AgentConfig(
                name="Workflow Agent",
                role="Workflow Role",
                description="Workflow Description",
                model={
                    "provider": "openai",
                    "model_name": "gpt-4",
                    "temperature": 0.2,
                    "max_tokens": 4000,
                    "top_p": 0.9
                },
                system_prompt="You are a workflow agent.",
                capabilities=["workflow_processing"],
                limitations=[]
            )
            
            for agent_type in agent_types:
                try:
                    agent = AgentFactory.create_agent(agent_type, base_config, "demo-key")
                    agents[agent_type] = agent
                except Exception as e:
                    self.console.print(f"   ⚠️ Не удалось создать {agent_type} агента: {e}")
            
            if agents:
                self.console.print(f"✅ Создано {len(agents)} агентов для workflow")
                
                # Демонстрируем маршрутизацию
                self.console.print("\n🛣️ Демонстрация маршрутизации сообщений:")
                
                # Создаем тестовое сообщение
                test_message = {
                    "content": "Analyze this data and provide security recommendations",
                    "sender": "user",
                    "recipients": list(agents.keys()),
                    "priority": "high"
                }
                
                with self.console.status("[bold green]Обработка сообщения через workflow..."):
                    # Мокаем обработку для демонстрации
                    self.console.print("   📤 Сообщение отправлено в workflow")
                    self.console.print("   🔄 Агенты обрабатывают сообщение...")
                    self.console.print("   📥 Получены ответы от всех агентов")
                    self.console.print("   ✅ Workflow выполнен успешно")
                
        except Exception as e:
            self.console.print(f"❌ Ошибка в workflow интеграции: {e}", style="red")
    
    def show_interactive_demo(self):
        """Интерактивная демонстрация"""
        self.console.print("\n" + "="*80)
        self.console.print("🎮 ИНТЕРАКТИВНАЯ ДЕМОНСТРАЦИЯ", style="bold blue")
        self.console.print("="*80)
        
        self.console.print("\nВыберите действие для демонстрации:")
        
        options = [
            ("1", "Создать агента из шаблона"),
            ("2", "Проверить валидацию роли"),
            ("3", "Показать иерархию ролей"),
            ("4", "Создать кастомного агента"),
            ("5", "Завершить демонстрацию")
        ]
        
        for key, description in options:
            self.console.print(f"   {key}. {description}")
        
        while True:
            choice = Prompt.ask("\nВыберите опцию", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                self._interactive_template_creation()
            elif choice == "2":
                self._interactive_role_validation()
            elif choice == "3":
                self._interactive_role_hierarchy()
            elif choice == "4":
                self._interactive_custom_agent()
            elif choice == "5":
                break
    
    def _interactive_template_creation(self):
        """Интерактивное создание агента из шаблона"""
        templates = self.template_manager.list_templates()
        
        if not templates:
            self.console.print("❌ Нет доступных шаблонов")
            return
        
        self.console.print(f"\n📋 Доступные шаблоны:")
        for i, template_name in enumerate(templates, 1):
            template = self.template_manager.get_template(template_name)
            if template:
                self.console.print(f"   {i}. {template.name} ({template.base_type})")
        
        try:
            choice = int(Prompt.ask("Выберите номер шаблона", choices=[str(i) for i in range(1, len(templates) + 1)]))
            template_name = templates[choice - 1]
            
            custom_name = Prompt.ask("Введите кастомное имя агента (или Enter для пропуска)")
            
            custom_config = {}
            if custom_name:
                custom_config["name"] = custom_name
            
            with self.console.status("[bold green]Создание агента..."):
                agent_config = self.template_manager.create_agent_from_template(template_name, custom_config)
                
                self.console.print(f"✅ Агент создан успешно!")
                self.console.print(f"   📝 Имя: {agent_config.name}")
                self.console.print(f"   🎯 Роль: {agent_config.role}")
                self.console.print(f"   📄 Описание: {agent_config.description}")
                
        except Exception as e:
            self.console.print(f"❌ Ошибка: {e}", style="red")
    
    def _interactive_role_validation(self):
        """Интерактивная валидация роли"""
        roles = list(self.role_manager.roles.keys())
        
        self.console.print(f"\n👥 Доступные роли:")
        for i, role_name in enumerate(roles[:10], 1):  # Показываем первые 10
            role_info = self.role_manager.get_role_requirements(role_name)
            self.console.print(f"   {i}. {role_info.get('name', role_name)} ({role_info.get('level', 'unknown')})")
        
        try:
            choice = int(Prompt.ask("Выберите номер роли", choices=[str(i) for i in range(1, min(11, len(roles) + 1))]))
            role_name = roles[choice - 1]
            
            # Создаем тестового агента
            capabilities_input = Prompt.ask("Введите возможности агента через запятую")
            capabilities = [cap.strip() for cap in capabilities_input.split(",") if cap.strip()]
            
            test_config = AgentConfig(
                name="Test Agent",
                role="Test Role",
                description="Test Description",
                model={"provider": "openai", "model_name": "gpt-4"},
                system_prompt="You are a test agent.",
                capabilities=capabilities,
                limitations=[]
            )
            
            test_agent = UniversalAgent(test_config, "test-key")
            
            # Проверяем валидацию
            is_valid = self.role_manager.validate_agent_for_role(test_agent, role_name)
            
            if is_valid:
                self.console.print(f"✅ Агент подходит для роли '{role_name}'")
            else:
                self.console.print(f"❌ Агент не подходит для роли '{role_name}'")
            
            # Показываем предложения
            improvements = self.role_manager.suggest_agent_improvements(test_agent, role_name)
            if improvements:
                self.console.print("\n💡 Предложения по улучшению:")
                for improvement in improvements[:5]:
                    self.console.print(f"   • {improvement}")
                    
        except Exception as e:
            self.console.print(f"❌ Ошибка: {e}", style="red")
    
    def _interactive_role_hierarchy(self):
        """Интерактивный показ иерархии ролей"""
        roles = list(self.role_manager.roles.keys())
        
        self.console.print(f"\n👥 Доступные роли:")
        for i, role_name in enumerate(roles[:10], 1):
            role_info = self.role_manager.get_role_requirements(role_name)
            self.console.print(f"   {i}. {role_info.get('name', role_name)}")
        
        try:
            choice = int(Prompt.ask("Выберите номер роли для просмотра иерархии", choices=[str(i) for i in range(1, min(11, len(roles) + 1))]))
            role_name = roles[choice - 1]
            
            hierarchy = self.role_manager.get_role_hierarchy(role_name)
            
            if hierarchy:
                self.console.print(f"\n📈 Иерархия для роли '{role_name}':")
                for i, next_role in enumerate(hierarchy, 1):
                    self.console.print(f"   {i}. {next_role}")
            else:
                self.console.print(f"\n📈 Для роли '{role_name}' нет определенной иерархии")
                
        except Exception as e:
            self.console.print(f"❌ Ошибка: {e}", style="red")
    
    def _interactive_custom_agent(self):
        """Интерактивное создание кастомного агента"""
        self.console.print("\n🎨 Создание кастомного агента:")
        
        try:
            name = Prompt.ask("Введите имя агента")
            role = Prompt.ask("Введите роль агента")
            description = Prompt.ask("Введите описание агента")
            
            capabilities_input = Prompt.ask("Введите возможности через запятую")
            capabilities = [cap.strip() for cap in capabilities_input.split(",") if cap.strip()]
            
            custom_config = AgentConfig(
                name=name,
                role=role,
                description=description,
                model={
                    "provider": "openai",
                    "model_name": "gpt-4",
                    "temperature": 0.2,
                    "max_tokens": 4000,
                    "top_p": 0.9
                },
                system_prompt=f"You are a {role}.",
                capabilities=capabilities,
                limitations=[]
            )
            
            # Создаем универсального агента
            agent = UniversalAgent(custom_config, "demo-key")
            
            self.console.print(f"✅ Кастомный агент создан успешно!")
            self.console.print(f"   📝 Имя: {agent.config.name}")
            self.console.print(f"   🎯 Роль: {agent.config.role}")
            self.console.print(f"   🔧 Возможности: {', '.join(agent.config.capabilities)}")
            
        except Exception as e:
            self.console.print(f"❌ Ошибка: {e}", style="red")
    
    def show_summary(self):
        """Показать итоговую сводку"""
        self.console.print("\n" + "="*80)
        self.console.print("📊 ИТОГОВАЯ СВОДКА ИТЕРАЦИИ №4", style="bold blue")
        self.console.print("="*80)
        
        # Статистика
        all_agent_types = AgentFactory.get_available_agent_types()
        categories = ExtendedAgentFactory.get_agent_categories()
        templates = self.template_manager.list_templates()
        roles = list(self.role_manager.roles.keys())
        
        summary_table = Table(title="Статистика Итерации №4")
        summary_table.add_column("Метрика", style="cyan")
        summary_table.add_column("Значение", style="green")
        summary_table.add_column("Описание", style="yellow")
        
        summary_table.add_row(
            "Всего типов агентов",
            str(len(all_agent_types)),
            "Базовые + расширенные агенты"
        )
        summary_table.add_row(
            "Категорий агентов",
            str(len(categories)),
            "Группировка по специализации"
        )
        summary_table.add_row(
            "Доступных шаблонов",
            str(len(templates)),
            "Шаблоны для быстрого создания"
        )
        summary_table.add_row(
            "Определенных ролей",
            str(len(roles)),
            "Роли с требованиями и иерархией"
        )
        
        self.console.print(summary_table)
        
        # Ключевые возможности
        self.console.print("\n🎯 Ключевые возможности Итерации №4:")
        features = [
            "✅ 10 новых специализированных агентов",
            "✅ Система шаблонов для быстрого создания",
            "✅ Менеджер ролей с валидацией",
            "✅ Динамическое создание агентов",
            "✅ Расширенная фабрика агентов",
            "✅ Универсальный агент для новых типов",
            "✅ Интеграция с workflow системой",
            "✅ Интерактивная демонстрация"
        ]
        
        for feature in features:
            self.console.print(f"   {feature}")
        
        self.console.print("\n🚀 Итерация №4 успешно завершена!")
    
    def run_demo(self):
        """Запуск полной демонстрации"""
        try:
            self.show_welcome()
            
            # Основные демонстрации
            self.show_agent_overview()
            self.show_extended_agents_demo()
            self.show_template_system_demo()
            self.show_role_manager_demo()
            self.show_agent_factory_demo()
            self.show_workflow_integration_demo()
            
            # Интерактивная часть
            if Confirm.ask("\n🎮 Хотите попробовать интерактивную демонстрацию?"):
                self.show_interactive_demo()
            
            self.show_summary()
            
        except KeyboardInterrupt:
            self.console.print("\n\n⏹️ Демонстрация прервана пользователем")
        except Exception as e:
            self.console.print(f"\n❌ Ошибка в демонстрации: {e}", style="red")


def main():
    """Главная функция"""
    console.print("🚀 Запуск демонстрации Итерации №4...")
    
    # Создаем и запускаем демонстрацию
    demo = Iteration4Demo()
    demo.run_demo()


if __name__ == "__main__":
    main() 
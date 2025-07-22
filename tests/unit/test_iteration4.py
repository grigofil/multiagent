"""
Тесты для Итерации №4: Масштабирование шаблона и добавление агентов с разными ролями
"""
import pytest
import asyncio
import yaml
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

# Импорты для тестирования
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


@pytest.fixture
def mock_config():
    """Мок конфигурации агента"""
    return AgentConfig(
        name="Test Agent",
        role="Test Role",
        description="Test Description",
        model={
            "provider": "openai",
            "model_name": "gpt-4",
            "temperature": 0.2,
            "max_tokens": 4000,
            "top_p": 0.9
        },
        system_prompt="You are a test agent.",
        capabilities=["test_capability"],
        limitations=["test_limitation"]
    )

@pytest.fixture
def mock_api_key():
    """Мок API ключа"""
    return "test-api-key"


class TestExtendedAgents:
    """Тесты для расширенных агентов"""
    
    @pytest.mark.asyncio
    async def test_database_agent(self, mock_config, mock_api_key):
        """Тест агента базы данных"""
        agent = DatabaseAgent(mock_config, mock_api_key)
        
        # Тест с dict входными данными
        input_data = {
            "query_type": "select",
            "table": "users",
            "columns": "id, name, email",
            "conditions": "active = true",
            "database_type": "postgresql"
        }
        
        with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "SELECT id, name, email FROM users WHERE active = true;"
            
            result = await agent.process(input_data)
            
            assert result == "SELECT id, name, email FROM users WHERE active = true;"
            mock_generate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_image_analysis_agent(self, mock_config, mock_api_key):
        """Тест агента анализа изображений"""
        agent = ImageAnalysisAgent(mock_config, mock_api_key)
        
        input_data = {
            "image_url": "https://example.com/image.jpg",
            "analysis_type": "object_detection",
            "features": ["objects", "faces", "text"]
        }
        
        with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "Обнаружены объекты: человек, машина, здание"
            
            result = await agent.process(input_data)
            
            assert "человек" in result
            mock_generate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_api_agent(self, mock_config, mock_api_key):
        """Тест API агента"""
        agent = APIAgent(mock_config, mock_api_key)
        
        input_data = {
            "api_endpoint": "https://api.example.com/users",
            "method": "GET",
            "parameters": {"limit": 10},
            "headers": {"Authorization": "Bearer token"}
        }
        
        with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "API запрос выполнен успешно"
            
            result = await agent.process(input_data)
            
            assert "API запрос" in result
            mock_generate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_ml_agent(self, mock_config, mock_api_key):
        """Тест ML агента"""
        agent = MachineLearningAgent(mock_config, mock_api_key)
        
        input_data = {
            "task_type": "classification",
            "algorithm": "random_forest",
            "data_description": "Данные о клиентах",
            "hyperparameters": {"n_estimators": 100}
        }
        
        with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "ML модель обучена с точностью 85%"
            
            result = await agent.process(input_data)
            
            assert "ML модель" in result
            mock_generate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_security_agent(self, mock_config, mock_api_key):
        """Тест агента безопасности"""
        agent = SecurityAgent(mock_config, mock_api_key)
        
        input_data = {
            "security_type": "code_analysis",
            "target": "web_application",
            "vulnerability_types": ["sql_injection", "xss"],
            "severity_level": "high"
        }
        
        with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "Обнаружены уязвимости: SQL injection, XSS"
            
            result = await agent.process(input_data)
            
            assert "уязвимости" in result
            mock_generate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_devops_agent(self, mock_config, mock_api_key):
        """Тест DevOps агента"""
        agent = DevOpsAgent(mock_config, mock_api_key)
        
        input_data = {
            "devops_task": "deployment",
            "platform": "kubernetes",
            "environment": "production",
            "tools": ["docker", "helm"]
        }
        
        with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "Deployment pipeline настроен"
            
            result = await agent.process(input_data)
            
            assert "Deployment" in result
            mock_generate.assert_called_once()


class TestAgentTemplates:
    """Тесты для системы шаблонов агентов"""
    
    @pytest.fixture
    def template_manager(self, tmp_path):
        """Создать менеджер шаблонов с временной директорией"""
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        return AgentTemplateManager(str(templates_dir))
    
    def test_template_manager_creation(self, template_manager):
        """Тест создания менеджера шаблонов"""
        assert template_manager.templates_dir.exists()
        assert isinstance(template_manager.templates, dict)
    
    def test_create_default_templates(self, template_manager):
        """Тест создания шаблонов по умолчанию"""
        template_manager.create_default_templates()
        
        # Проверяем, что созданы файлы шаблонов
        template_files = list(template_manager.templates_dir.glob("*.yaml"))
        assert len(template_files) >= 3  # junior_analyst, senior_developer, security_expert
        
        # Проверяем загрузку шаблонов
        template_manager.load_templates()
        assert "junior_analyst" in template_manager.templates
        assert "senior_developer" in template_manager.templates
        assert "security_expert" in template_manager.templates
    
    def test_get_template(self, template_manager):
        """Тест получения шаблона"""
        template_manager.create_default_templates()
        template_manager.load_templates()
        
        template = template_manager.get_template("junior_analyst")
        assert template is not None
        assert template.name == "Junior Data Analyst"
        assert template.base_type == "analyst"
    
    def test_list_templates(self, template_manager):
        """Тест списка шаблонов"""
        template_manager.create_default_templates()
        template_manager.load_templates()
        
        templates = template_manager.list_templates()
        assert "junior_analyst" in templates
        assert "senior_developer" in templates
        assert "security_expert" in templates
    
    def test_create_agent_from_template(self, template_manager):
        """Тест создания агента из шаблона"""
        template_manager.create_default_templates()
        template_manager.load_templates()
        
        # Мокаем загрузку базовой конфигурации
        with patch.object(template_manager, '_get_base_config') as mock_get_config:
            mock_get_config.return_value = {
                "name": "Test Agent",
                "role": "Test Role",
                "description": "Test Description",
                "model": {
                    "provider": "openai",
                    "model_name": "gpt-4",
                    "temperature": 0.2,
                    "max_tokens": 4000,
                    "top_p": 0.9
                },
                "system_prompt": "You are a test agent.",
                "capabilities": [],
                "limitations": []
            }
            
            agent_config = template_manager.create_agent_from_template("junior_analyst")
            
            assert isinstance(agent_config, AgentConfig)
            assert agent_config.name == "Test Agent"
    
    def test_apply_template_customizations(self, template_manager):
        """Тест применения кастомизаций шаблона"""
        base_config = {
            "name": "Base Agent",
            "model": {"temperature": 0.2, "max_tokens": 4000},
            "capabilities": ["basic"]
        }
        
        customizations = {
            "model": {"temperature": 0.1},
            "capabilities": ["advanced"],
            "description": "Custom description"
        }
        
        result = template_manager._apply_template_customizations(base_config, customizations)
        
        assert result["model"]["temperature"] == 0.1
        assert result["model"]["max_tokens"] == 4000  # Сохранено из базовой конфигурации
        assert result["capabilities"] == ["advanced"]
        assert result["description"] == "Custom description"


class TestDynamicAgentCreator:
    """Тесты для создателя динамических агентов"""
    
    @pytest.fixture
    def template_manager(self, tmp_path):
        """Создать менеджер шаблонов"""
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        return AgentTemplateManager(str(templates_dir))
    
    @pytest.fixture
    def agent_creator(self, template_manager):
        """Создать создателя агентов"""
        return DynamicAgentCreator(template_manager)
    
    def test_register_agent_type(self, agent_creator):
        """Тест регистрации типа агента"""
        class CustomAgent:
            pass
        
        agent_creator.register_agent_type("custom", CustomAgent)
        assert "custom" in agent_creator.agent_registry
        assert agent_creator.agent_registry["custom"] == CustomAgent
    
    def test_create_dynamic_agent(self, agent_creator, mock_config, mock_api_key):
        """Тест создания динамического агента"""
        # Регистрируем кастомный тип
        class CustomAgent:
            def __init__(self, config, api_key):
                self.config = config
                self.api_key = api_key
        
        agent_creator.register_agent_type("test_role", CustomAgent)
        
        # Создаем агента
        agent = agent_creator.create_dynamic_agent(mock_config, mock_api_key)
        
        assert isinstance(agent, CustomAgent)
        assert agent.config == mock_config
        assert agent.api_key == mock_api_key
    
    def test_create_universal_agent(self, agent_creator, mock_config, mock_api_key):
        """Тест создания универсального агента для неизвестного типа"""
        # Создаем агента с неизвестным типом
        agent = agent_creator.create_dynamic_agent(mock_config, mock_api_key)
        
        assert isinstance(agent, UniversalAgent)
        assert agent.config == mock_config
        assert agent.api_key == mock_api_key


class TestUniversalAgent:
    """Тесты для универсального агента"""
    
    @pytest.fixture
    def mock_config(self):
        """Мок конфигурации"""
        return AgentConfig(
            name="Universal Agent",
            role="Universal Role",
            description="Universal Description",
            model={
                "provider": "openai",
                "model_name": "gpt-4",
                "temperature": 0.2,
                "max_tokens": 4000,
                "top_p": 0.9
            },
            system_prompt="You are a universal agent.",
            capabilities=["universal_processing"],
            limitations=["no_specialization"]
        )
    
    @pytest.mark.asyncio
    async def test_universal_agent_dict_input(self, mock_config, mock_api_key):
        """Тест универсального агента с dict входными данными"""
        agent = UniversalAgent(mock_config, mock_api_key)
        
        input_data = {
            "context": "Test context",
            "requirements": "Test requirements",
            "data": {"key": "value"}
        }
        
        with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "Универсальная обработка выполнена"
            
            result = await agent.process(input_data)
            
            assert "Универсальная обработка" in result
            mock_generate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_universal_agent_string_input(self, mock_config, mock_api_key):
        """Тест универсального агента со строковыми входными данными"""
        agent = UniversalAgent(mock_config, mock_api_key)
        
        input_data = "Простая строка для обработки"
        
        with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "Строка обработана"
            
            result = await agent.process(input_data)
            
            assert "Строка обработана" in result
            mock_generate.assert_called_once()


class TestAgentRoleManager:
    """Тесты для менеджера ролей агентов"""
    
    @pytest.fixture
    def role_manager(self, tmp_path):
        """Создать менеджер ролей с временным файлом"""
        role_file = tmp_path / "agent_roles.yaml"
        
        # Создаем тестовую конфигурацию ролей
        role_data = {
            "roles": {
                "data_analyst": {
                    "name": "Data Analyst",
                    "level": "junior",
                    "required_capabilities": ["data_analysis", "basic_statistics"],
                    "suggested_capabilities": ["data_visualization"]
                },
                "senior_developer": {
                    "name": "Senior Developer",
                    "level": "senior",
                    "required_capabilities": ["code_generation", "architecture_design"],
                    "suggested_capabilities": ["mentoring"]
                }
            },
            "hierarchy": {
                "data_analyst": ["senior_data_analyst"],
                "senior_developer": ["tech_lead", "architect"]
            }
        }
        
        with open(role_file, 'w', encoding='utf-8') as f:
            yaml.dump(role_data, f, default_flow_style=False, allow_unicode=True)
        
        # Создаем менеджер с временным файлом
        manager = AgentRoleManager()
        manager.roles = role_data["roles"]
        manager.role_hierarchy = role_data["hierarchy"]
        
        return manager
    
    def test_get_role_requirements(self, role_manager):
        """Тест получения требований роли"""
        requirements = role_manager.get_role_requirements("data_analyst")
        
        assert requirements["name"] == "Data Analyst"
        assert requirements["level"] == "junior"
        assert "data_analysis" in requirements["required_capabilities"]
        assert "data_visualization" in requirements["suggested_capabilities"]
    
    def test_get_role_hierarchy(self, role_manager):
        """Тест получения иерархии ролей"""
        hierarchy = role_manager.get_role_hierarchy("data_analyst")
        
        assert "senior_data_analyst" in hierarchy
    
    def test_validate_agent_for_role(self, role_manager, mock_config):
        """Тест валидации агента для роли"""
        # Агент с подходящими возможностями
        mock_config.capabilities = ["data_analysis", "basic_statistics"]
        agent = UniversalAgent(mock_config, "test-key")
        
        assert role_manager.validate_agent_for_role(agent, "data_analyst") == True
        
        # Агент с недостающими возможностями
        mock_config.capabilities = ["data_analysis"]  # Отсутствует basic_statistics
        agent = UniversalAgent(mock_config, "test-key")
        
        assert role_manager.validate_agent_for_role(agent, "data_analyst") == False
    
    def test_suggest_agent_improvements(self, role_manager, mock_config):
        """Тест предложения улучшений для агента"""
        # Агент с недостающими возможностями
        mock_config.capabilities = ["data_analysis"]  # Отсутствует basic_statistics
        agent = UniversalAgent(mock_config, "test-key")
        
        improvements = role_manager.suggest_agent_improvements(agent, "data_analyst")
        
        assert len(improvements) >= 1
        assert any("basic_statistics" in improvement for improvement in improvements)
        assert any("data_visualization" in improvement for improvement in improvements)


class TestExtendedAgentFactory:
    """Тесты для расширенной фабрики агентов"""
    
    def test_get_available_agent_types(self):
        """Тест получения доступных типов агентов"""
        types = ExtendedAgentFactory.get_available_agent_types()
        
        # Проверяем базовые типы
        assert "analyst" in types
        assert "coder" in types
        assert "reviewer" in types
        
        # Проверяем расширенные типы
        assert "database" in types
        assert "image_analysis" in types
        assert "api" in types
        assert "ml" in types
        assert "security" in types
        assert "devops" in types
        assert "documentation" in types
        assert "testing" in types
        assert "research" in types
        assert "communication" in types
    
    def test_get_agent_categories(self):
        """Тест получения категорий агентов"""
        categories = ExtendedAgentFactory.get_agent_categories()
        
        assert "analysis" in categories
        assert "development" in categories
        assert "management" in categories
        assert "specialized" in categories
        assert "creative" in categories
        
        # Проверяем содержимое категорий
        assert "analyst" in categories["analysis"]
        assert "coder" in categories["development"]
        assert "database" in categories["specialized"]


class TestAgentFactoryIntegration:
    """Интеграционные тесты фабрики агентов"""
    
    def test_agent_factory_with_extended_agents(self, mock_config, mock_api_key):
        """Тест фабрики агентов с расширенными типами"""
        # Тестируем создание базовых агентов
        analyst = AgentFactory.create_agent("analyst", mock_config, mock_api_key)
        assert analyst is not None
        
        # Тестируем создание расширенных агентов
        database_agent = AgentFactory.create_agent("database", mock_config, mock_api_key)
        assert database_agent is not None
        assert isinstance(database_agent, DatabaseAgent)
        
        ml_agent = AgentFactory.create_agent("ml", mock_config, mock_api_key)
        assert ml_agent is not None
        assert isinstance(ml_agent, MachineLearningAgent)
    
    def test_agent_factory_unknown_type(self, mock_config, mock_api_key):
        """Тест фабрики агентов с неизвестным типом"""
        with pytest.raises(ValueError, match="Неизвестный тип агента"):
            AgentFactory.create_agent("unknown_type", mock_config, mock_api_key)
    
    def test_get_available_agent_types_integration(self):
        """Тест получения всех доступных типов агентов"""
        types = AgentFactory.get_available_agent_types()
        
        # Проверяем, что включены как базовые, так и расширенные типы
        base_types = ["analyst", "coder", "reviewer", "manager", "ideator", "assessor"]
        extended_types = ["database", "image_analysis", "api", "ml", "security", "devops"]
        
        for base_type in base_types:
            assert base_type in types
        
        for extended_type in extended_types:
            assert extended_type in types


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v"]) 
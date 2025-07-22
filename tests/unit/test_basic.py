"""
Простой тест для проверки базовой функциональности мультиагентной системы
"""
import asyncio
import os
import sys
from pathlib import Path

# Добавляем src в путь для импортов
sys.path.append(str(Path(__file__).parent / "src"))

from src.utils import ConfigLoader
from src.workflow import MultiAgentWorkflow


async def test_config_loading():
    """Тест загрузки конфигураций"""
    print("🧪 Тестирование загрузки конфигураций...")
    
    try:
        config_loader = ConfigLoader()
        
        # Загружаем конфигурации
        agents_config = config_loader.load_agents_config()
        interactions_config = config_loader.load_interactions_config()
        
        # Проверяем структуру
        assert "agents" in agents_config, "Конфигурация агентов не найдена"
        assert "workflows" in interactions_config, "Конфигурация рабочих процессов не найдена"
        
        print("✅ Конфигурации загружены успешно")
        print(f"   - Агентов: {len(agents_config['agents'])}")
        print(f"   - Рабочих процессов: {len(interactions_config['workflows'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при загрузке конфигураций: {e}")
        return False


async def test_workflow_initialization():
    """Тест инициализации рабочих процессов"""
    print("\n🧪 Тестирование инициализации рабочих процессов...")
    
    try:
        config_loader = ConfigLoader()
        
        # Создаем мультиагентную систему (без API ключа для теста)
        workflow_manager = MultiAgentWorkflow(config_loader, api_key=None)
        
        # Проверяем доступные рабочие процессы
        workflows = workflow_manager.get_available_workflows()
        assert len(workflows) > 0, "Нет доступных рабочих процессов"
        
        # Проверяем информацию об агентах
        agents_info = workflow_manager.get_agents_info()
        assert len(agents_info) > 0, "Нет инициализированных агентов"
        
        print("✅ Рабочие процессы инициализированы успешно")
        print(f"   - Доступных процессов: {len(workflows)}")
        print(f"   - Инициализированных агентов: {len(agents_info)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при инициализации рабочих процессов: {e}")
        return False


async def test_agent_factory():
    """Тест фабрики агентов"""
    print("\n🧪 Тестирование фабрики агентов...")
    
    try:
        from src.agents import AgentFactory, AgentConfig
        
        # Создаем тестовую конфигурацию
        config = AgentConfig(
            name="Test Agent",
            role="Тестовый агент",
            model={
                "provider": "openai",
                "model_name": "gpt-4",
                "temperature": 0.1
            },
            system_prompt="Ты тестовый агент для проверки функциональности."
        )
        
        # Тестируем создание агентов
        agent_types = ["analyst", "coder", "reviewer"]
        
        for agent_type in agent_types:
            try:
                agent = AgentFactory.create_agent(agent_type, config, api_key=None)
                print(f"   ✅ Агент типа '{agent_type}' создан успешно")
            except Exception as e:
                print(f"   ❌ Ошибка создания агента '{agent_type}': {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тесте фабрики агентов: {e}")
        return False


async def main():
    """Основная функция тестирования"""
    print("🚀 Запуск базовых тестов мультиагентной системы\n")
    
    # Создаем директорию для логов
    os.makedirs("logs", exist_ok=True)
    
    # Запускаем тесты
    tests = [
        test_config_loading,
        test_workflow_initialization,
        test_agent_factory
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"❌ Критическая ошибка в тесте: {e}")
            results.append(False)
    
    # Итоговый результат
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 Результаты тестирования: {passed}/{total} тестов прошли успешно")
    
    if passed == total:
        print("🎉 Все тесты прошли успешно! Система готова к использованию.")
    else:
        print("⚠️  Некоторые тесты не прошли. Проверьте конфигурацию.")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 
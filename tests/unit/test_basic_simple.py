"""
Упрощенный тест для проверки базовой структуры мультиагентной системы
"""
import os
import sys
from pathlib import Path

# Добавляем src в путь для импортов
sys.path.append(str(Path(__file__).parent / "src"))

from src.utils import ConfigLoader


def test_config_loading():
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
        
        # Показываем детали
        print("\n📋 Агенты:")
        for agent_id, agent_config in agents_config["agents"].items():
            print(f"   - {agent_id}: {agent_config['name']} ({agent_config['role']})")
        
        print("\n🔄 Рабочие процессы:")
        for workflow_id, workflow_config in interactions_config["workflows"].items():
            print(f"   - {workflow_id}: {workflow_config['name']}")
            print(f"     Описание: {workflow_config['description']}")
            print(f"     Агенты: {', '.join(workflow_config['agents'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при загрузке конфигураций: {e}")
        return False


def test_file_structure():
    """Тест структуры файлов"""
    print("\n🧪 Тестирование структуры файлов...")
    
    required_files = [
        "config/agents_config.yaml",
        "config/interactions.yaml",
        "src/agents/__init__.py",
        "src/agents/base_agent.py",
        "src/agents/specialized_agents.py",
        "src/workflow/__init__.py",
        "src/workflow/multi_agent_workflow.py",
        "src/utils/__init__.py",
        "src/utils/config_loader.py",
        "main.py",
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Отсутствуют файлы: {missing_files}")
        return False
    else:
        print("✅ Все необходимые файлы присутствуют")
        return True


def test_imports():
    """Тест импортов основных модулей"""
    print("\n🧪 Тестирование импортов...")
    
    try:
        # Тестируем импорт утилит
        from src.utils import ConfigLoader, get_api_key
        print("✅ Модуль utils импортирован успешно")
        
        # Тестируем импорт агентов (без LangChain)
        from src.agents.base_agent import AgentConfig, AgentState
        print("✅ Базовые классы агентов импортированы успешно")
        
        # Тестируем импорт фабрики агентов
        from src.agents.specialized_agents import AgentFactory
        print("✅ Фабрика агентов импортирована успешно")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при импорте модулей: {e}")
        return False


def test_config_validation():
    """Тест валидации конфигураций"""
    print("\n🧪 Тестирование валидации конфигураций...")
    
    try:
        config_loader = ConfigLoader()
        agents_config = config_loader.load_agents_config()
        
        # Проверяем структуру конфигурации агентов
        for agent_id, agent_config in agents_config["agents"].items():
            required_fields = ["name", "role", "model", "system_prompt"]
            for field in required_fields:
                assert field in agent_config, f"Поле '{field}' отсутствует в конфигурации агента {agent_id}"
            
            # Проверяем структуру модели
            model_config = agent_config["model"]
            model_fields = ["provider", "model_name", "temperature"]
            for field in model_fields:
                assert field in model_config, f"Поле '{field}' отсутствует в конфигурации модели агента {agent_id}"
        
        print("✅ Конфигурации агентов валидны")
        
        # Проверяем конфигурацию рабочих процессов
        interactions_config = config_loader.load_interactions_config()
        
        for workflow_id, workflow_config in interactions_config["workflows"].items():
            required_fields = ["name", "description", "agents", "flow"]
            for field in required_fields:
                assert field in workflow_config, f"Поле '{field}' отсутствует в конфигурации процесса {workflow_id}"
        
        print("✅ Конфигурации рабочих процессов валидны")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка валидации конфигураций: {e}")
        return False


def main():
    """Основная функция тестирования"""
    print("🚀 Запуск базовых тестов мультиагентной системы\n")
    
    # Создаем директорию для логов
    os.makedirs("logs", exist_ok=True)
    
    # Запускаем тесты
    tests = [
        test_file_structure,
        test_config_loading,
        test_imports,
        test_config_validation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Критическая ошибка в тесте: {e}")
            results.append(False)
    
    # Итоговый результат
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 Результаты тестирования: {passed}/{total} тестов прошли успешно")
    
    if passed == total:
        print("🎉 Все тесты прошли успешно! Базовая структура системы готова.")
        print("\n📝 Следующие шаги:")
        print("1. Установите полные зависимости: pip install -r requirements.txt")
        print("2. Настройте API ключ в файле .env")
        print("3. Запустите систему: python main.py")
    else:
        print("⚠️  Некоторые тесты не прошли. Проверьте структуру проекта.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
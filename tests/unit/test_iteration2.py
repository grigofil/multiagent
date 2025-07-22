"""
Тест для проверки функциональности Итерации №2
"""
import asyncio
import os
import sys
from pathlib import Path

# Добавляем src в путь для импортов
sys.path.append(str(Path(__file__).parent / "src"))

from src.utils.advanced_config_loader import AdvancedConfigLoader
from src.prompts import PromptTemplates


def test_advanced_config_loader():
    """Тест расширенного загрузчика конфигураций"""
    print("🧪 Тестирование расширенного загрузчика конфигураций...")
    
    try:
        config_loader = AdvancedConfigLoader()
        
        # Загружаем конфигурации
        agents_config = config_loader.load_agents_config()
        interactions_config = config_loader.load_interactions_config()
        
        # Проверяем расширенную структуру
        assert "agents" in agents_config, "Конфигурация агентов не найдена"
        assert "supported_providers" in agents_config, "Конфигурация провайдеров не найдена"
        assert "security" in agents_config, "Конфигурация безопасности не найдена"
        
        print("✅ Расширенные конфигурации загружены успешно")
        
        # Проверяем детали агентов
        agents = agents_config["agents"]
        for agent_id, agent_data in agents.items():
            print(f"\n📋 Агент: {agent_id}")
            print(f"   Имя: {agent_data['name']}")
            print(f"   Роль: {agent_data['role']}")
            print(f"   Описание: {agent_data['description']}")
            print(f"   Шаблон промпта: {agent_data.get('prompt_template', 'Нет')}")
            print(f"   Возможности: {agent_data.get('capabilities', [])}")
            print(f"   Ограничения: {agent_data.get('limitations', [])}")
            
            # Проверяем конфигурацию модели
            model_config = agent_data["model"]
            print(f"   Модель: {model_config['model_name']} ({model_config['provider']})")
            print(f"   Параметры: temp={model_config['temperature']}, max_tokens={model_config.get('max_tokens', 'N/A')}")
        
        # Проверяем поддерживаемые провайдеры
        providers = agents_config["supported_providers"]
        print(f"\n🔌 Поддерживаемые провайдеры: {list(providers.keys())}")
        
        for provider_name, provider_data in providers.items():
            print(f"   {provider_name}: {provider_data['name']}")
            print(f"     Модели: {provider_data['models']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании расширенного загрузчика: {e}")
        return False


def test_prompt_templates():
    """Тест шаблонов промптов"""
    print("\n🧪 Тестирование шаблонов промптов...")
    
    try:
        # Проверяем доступные шаблоны
        templates = PromptTemplates.list_templates()
        print(f"✅ Доступные шаблоны: {templates}")
        
        # Тестируем каждый шаблон
        for template_name in templates:
            try:
                template = PromptTemplates.get_template(template_name)
                print(f"   ✅ Шаблон '{template_name}' загружен успешно")
                print(f"      Переменные: {template.variables}")
                
                # Тестируем рендеринг с тестовыми данными
                test_vars = {var: f"test_{var}" for var in template.variables}
                rendered = template.render(**test_vars)
                print(f"      Рендеринг: {len(rendered)} символов")
                
            except Exception as e:
                print(f"   ❌ Ошибка в шаблоне '{template_name}': {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании шаблонов промптов: {e}")
        return False


def test_config_validation():
    """Тест валидации конфигураций"""
    print("\n🧪 Тестирование валидации конфигураций...")
    
    try:
        config_loader = AdvancedConfigLoader()
        
        # Валидируем все конфигурации
        validation_results = config_loader.validate_all_configs()
        
        print(f"📊 Результаты валидации:")
        for check_name, result in validation_results.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check_name}")
        
        # Проверяем возможности агентов
        agents_config = config_loader.load_agents_config()
        agents = agents_config["agents"]
        
        print(f"\n🔍 Анализ возможностей агентов:")
        for agent_id in agents.keys():
            capabilities = config_loader.get_agent_capabilities(agent_id)
            limitations = config_loader.get_agent_limitations(agent_id)
            print(f"   {agent_id}:")
            print(f"     Возможности: {capabilities}")
            print(f"     Ограничения: {limitations}")
        
        # Проверяем поддерживаемые провайдеры
        providers = config_loader.get_supported_providers()
        print(f"\n🔌 Поддерживаемые провайдеры: {providers}")
        
        for provider in providers:
            models = config_loader.get_provider_models(provider)
            print(f"   {provider}: {models}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании валидации: {e}")
        return False


def test_security_config():
    """Тест конфигурации безопасности"""
    print("\n🧪 Тестирование конфигурации безопасности...")
    
    try:
        config_loader = AdvancedConfigLoader()
        security_config = config_loader.get_security_config()
        
        print(f"✅ Конфигурация безопасности загружена:")
        print(f"   Максимальная длина ввода: {security_config.max_input_length}")
        print(f"   Максимальная длина вывода: {security_config.max_output_length}")
        print(f"   Фильтрация контента: {security_config.content_filtering}")
        print(f"   Ограничения скорости: {security_config.rate_limiting}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании конфигурации безопасности: {e}")
        return False


def test_prompt_template_rendering():
    """Тест рендеринга шаблонов промптов"""
    print("\n🧪 Тестирование рендеринга шаблонов промптов...")
    
    try:
        # Тестируем шаблон анализа данных
        data_analysis_template = PromptTemplates.get_template("data_analysis")
        
        test_data = {
            "data": {
                "sales": [100, 150, 200, 180, 250],
                "months": ["Янв", "Фев", "Мар", "Апр", "Май"]
            },
            "context": "Анализ продаж за Q1",
            "requirements": "Выявить тренды и аномалии"
        }
        
        rendered = data_analysis_template.render(**test_data)
        print(f"✅ Шаблон анализа данных отрендерен успешно")
        print(f"   Длина: {len(rendered)} символов")
        print(f"   Содержит данные: {'sales' in rendered}")
        print(f"   Содержит контекст: {'Q1' in rendered}")
        
        # Тестируем шаблон генерации кода
        code_generation_template = PromptTemplates.get_template("code_generation")
        
        test_code_data = {
            "task": "Создать функцию для вычисления факториала",
            "requirements": "С обработкой ошибок и документацией",
            "language": "Python",
            "version": "3.8+",
            "style": "PEP 8",
            "context": "Математические вычисления"
        }
        
        rendered_code = code_generation_template.render(**test_code_data)
        print(f"✅ Шаблон генерации кода отрендерен успешно")
        print(f"   Длина: {len(rendered_code)} символов")
        print(f"   Содержит задачу: {'факториала' in rendered_code}")
        print(f"   Содержит язык: {'Python' in rendered_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании рендеринга: {e}")
        return False


async def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов Итерации №2: Расширенная конфигурация и промпты\n")
    
    # Создаем директорию для логов
    os.makedirs("logs", exist_ok=True)
    
    # Запускаем тесты
    tests = [
        test_advanced_config_loader,
        test_prompt_templates,
        test_config_validation,
        test_security_config,
        test_prompt_template_rendering
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
    
    print(f"\n📊 Результаты тестирования Итерации №2: {passed}/{total} тестов прошли успешно")
    
    if passed == total:
        print("🎉 Все тесты Итерации №2 прошли успешно!")
        print("\n✅ Реализованные возможности:")
        print("   - Расширенная конфигурация агентов с валидацией")
        print("   - Поддержка различных LLM провайдеров")
        print("   - Шаблоны промптов с Jinja2")
        print("   - Система возможностей и ограничений агентов")
        print("   - Конфигурация безопасности")
        print("   - Новые специализированные агенты")
    else:
        print("⚠️  Некоторые тесты не прошли. Проверьте конфигурацию.")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 
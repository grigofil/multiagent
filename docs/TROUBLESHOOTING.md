# Устранение неполадок

## Общие проблемы

### 1. Проблемы с API ключами

#### Симптомы
- Ошибка `401 Unauthorized`
- Сообщение `Invalid API key`
- Агенты не могут подключиться к LLM

#### Решения
```bash
# Проверка переменных окружения
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY

# Обновление API ключей
export OPENAI_API_KEY="sk-your-new-api-key"
export ANTHROPIC_API_KEY="sk-ant-your-new-api-key"

# Проверка в Python
import os
print(os.getenv('OPENAI_API_KEY'))
```

#### Профилактика
- Регулярно проверяйте баланс API ключей
- Используйте разные ключи для разных сред
- Настройте мониторинг использования API

### 2. Проблемы с памятью

#### Симптомы
- Ошибка `MemoryError`
- Медленная работа системы
- Агенты не отвечают

#### Решения
```python
# Мониторинг использования памяти
import psutil
import gc

def check_memory_usage():
    """Проверка использования памяти"""
    memory = psutil.virtual_memory()
    print(f"Memory usage: {memory.percent}%")
    print(f"Available: {memory.available / 1024 / 1024:.2f} MB")
    
    if memory.percent > 80:
        print("Warning: High memory usage!")
        gc.collect()  # Принудительная очистка памяти

# Ограничение размера кэша
import functools
from typing import Dict, Any

class LimitedCache:
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: Dict[str, Any] = {}
    
    def get(self, key: str):
        return self.cache.get(key)
    
    def set(self, key: str, value: Any):
        if len(self.cache) >= self.max_size:
            # Удаление самого старого элемента
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        self.cache[key] = value
```

#### Профилактика
- Мониторинг использования памяти
- Ограничение размера кэша
- Регулярная очистка памяти

### 3. Проблемы с сетью

#### Симптомы
- Таймауты при запросах
- Ошибки подключения
- Медленные ответы

#### Решения
```python
# Настройка таймаутов
import aiohttp
import asyncio

async def make_request_with_timeout(url: str, timeout: int = 30):
    """Запрос с настройкой таймаута"""
    timeout_config = aiohttp.ClientTimeout(total=timeout)
    
    async with aiohttp.ClientSession(timeout=timeout_config) as session:
        try:
            async with session.get(url) as response:
                return await response.text()
        except asyncio.TimeoutError:
            print(f"Request to {url} timed out")
            return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None

# Retry механизм
import tenacity

@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    retry=tenacity.retry_if_exception_type((ConnectionError, TimeoutError))
)
async def robust_request(url: str):
    """Устойчивый запрос с повторными попытками"""
    return await make_request_with_timeout(url)
```

## Проблемы с агентами

### 1. Агент не отвечает

#### Диагностика
```python
# Проверка состояния агента
def diagnose_agent(agent):
    """Диагностика состояния агента"""
    issues = []
    
    # Проверка конфигурации
    if not agent.config:
        issues.append("Missing configuration")
    
    # Проверка API ключа
    if not agent.api_key:
        issues.append("Missing API key")
    
    # Проверка модели
    if not agent.config.model:
        issues.append("Missing model configuration")
    
    # Проверка системного промпта
    if not agent.config.system_prompt:
        issues.append("Missing system prompt")
    
    return issues

# Тестовый запрос
async def test_agent_response(agent):
    """Тестирование ответа агента"""
    try:
        result = await agent.process({"test": "data"})
        print(f"Agent responded successfully: {result[:100]}...")
        return True
    except Exception as e:
        print(f"Agent failed to respond: {e}")
        return False
```

#### Решения
```python
# Сброс состояния агента
def reset_agent(agent):
    """Сброс состояния агента"""
    agent.reset_state()
    print("Agent state reset successfully")

# Пересоздание агента
def recreate_agent(agent_type: str, config: AgentConfig, api_key: str):
    """Пересоздание агента"""
    factory = TaskSpecificAgentFactory()
    return factory.create_agent(agent_type, config, api_key)
```

### 2. Неправильные ответы агента

#### Диагностика
```python
# Анализ ответов агента
def analyze_agent_responses(agent, test_cases: list):
    """Анализ ответов агента на тестовых случаях"""
    results = []
    
    for test_case in test_cases:
        try:
            response = await agent.process(test_case["input"])
            
            # Проверка качества ответа
            quality_score = evaluate_response_quality(
                response, 
                test_case["expected"]
            )
            
            results.append({
                "test_case": test_case["name"],
                "response": response,
                "quality_score": quality_score,
                "passed": quality_score > 0.7
            })
            
        except Exception as e:
            results.append({
                "test_case": test_case["name"],
                "error": str(e),
                "passed": False
            })
    
    return results

def evaluate_response_quality(actual: str, expected: str) -> float:
    """Оценка качества ответа"""
    # Простая оценка на основе совпадения ключевых слов
    actual_words = set(actual.lower().split())
    expected_words = set(expected.lower().split())
    
    if not expected_words:
        return 1.0
    
    intersection = actual_words.intersection(expected_words)
    return len(intersection) / len(expected_words)
```

#### Решения
```python
# Улучшение промпта
def improve_system_prompt(agent, issues: list):
    """Улучшение системного промпта на основе проблем"""
    current_prompt = agent.config.system_prompt
    
    improvements = []
    
    if "неполные ответы" in issues:
        improvements.append("Всегда давайте полные и детальные ответы.")
    
    if "неправильный формат" in issues:
        improvements.append("Строго следуйте указанному формату ответа.")
    
    if "нерелевантные ответы" in issues:
        improvements.append("Отвечайте только на заданный вопрос.")
    
    improved_prompt = current_prompt + "\n\n" + "\n".join(improvements)
    
    # Обновление конфигурации
    agent.config.system_prompt = improved_prompt
    return agent
```

## Проблемы с производительностью

### 1. Медленные ответы

#### Диагностика
```python
# Профилирование производительности
import time
import cProfile
import pstats

def profile_agent_performance(agent, test_input: dict):
    """Профилирование производительности агента"""
    profiler = cProfile.Profile()
    profiler.enable()
    
    start_time = time.time()
    result = await agent.process(test_input)
    end_time = time.time()
    
    profiler.disable()
    
    # Анализ результатов
    execution_time = end_time - start_time
    stats = pstats.Stats(profiler)
    
    print(f"Execution time: {execution_time:.2f} seconds")
    print("Top 10 function calls:")
    stats.sort_stats('cumulative').print_stats(10)
    
    return {
        "execution_time": execution_time,
        "result_length": len(result),
        "stats": stats
    }
```

#### Решения
```python
# Оптимизация кэширования
class OptimizedCache:
    def __init__(self):
        self.cache = {}
        self.access_count = {}
    
    def get(self, key: str):
        if key in self.cache:
            self.access_count[key] += 1
            return self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        self.cache[key] = value
        self.access_count[key] = 1
    
    def cleanup_least_used(self, max_size: int = 1000):
        """Удаление наименее используемых элементов"""
        if len(self.cache) > max_size:
            # Сортировка по количеству обращений
            sorted_items = sorted(
                self.access_count.items(), 
                key=lambda x: x[1]
            )
            
            # Удаление 20% наименее используемых
            items_to_remove = len(self.cache) - max_size
            for key, _ in sorted_items[:items_to_remove]:
                del self.cache[key]
                del self.access_count[key]

# Асинхронная обработка
async def process_batch(agent, inputs: list):
    """Пакетная обработка запросов"""
    tasks = []
    for input_data in inputs:
        task = agent.process(input_data)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

### 2. Высокое потребление ресурсов

#### Мониторинг
```python
# Мониторинг ресурсов
import psutil
import threading
import time

class ResourceMonitor:
    def __init__(self):
        self.monitoring = False
        self.metrics = []
    
    def start_monitoring(self):
        """Запуск мониторинга ресурсов"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Остановка мониторинга"""
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join()
    
    def _monitor_loop(self):
        """Цикл мониторинга"""
        while self.monitoring:
            metrics = {
                'timestamp': time.time(),
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent
            }
            
            self.metrics.append(metrics)
            
            # Предупреждения
            if metrics['cpu_percent'] > 80:
                print(f"Warning: High CPU usage: {metrics['cpu_percent']}%")
            
            if metrics['memory_percent'] > 80:
                print(f"Warning: High memory usage: {metrics['memory_percent']}%")
            
            time.sleep(5)  # Проверка каждые 5 секунд
    
    def get_metrics_summary(self):
        """Получение сводки метрик"""
        if not self.metrics:
            return {}
        
        cpu_values = [m['cpu_percent'] for m in self.metrics]
        memory_values = [m['memory_percent'] for m in self.metrics]
        
        return {
            'avg_cpu': sum(cpu_values) / len(cpu_values),
            'max_cpu': max(cpu_values),
            'avg_memory': sum(memory_values) / len(memory_values),
            'max_memory': max(memory_values),
            'total_measurements': len(self.metrics)
        }
```

## Проблемы с конфигурацией

### 1. Неправильная конфигурация

#### Валидация конфигурации
```python
# Валидатор конфигурации
from typing import Dict, Any, List

class ConfigValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_agent_config(self, config: Dict[str, Any]) -> bool:
        """Валидация конфигурации агента"""
        self.errors = []
        self.warnings = []
        
        # Проверка обязательных полей
        required_fields = ['name', 'role', 'description', 'model', 'system_prompt']
        for field in required_fields:
            if field not in config:
                self.errors.append(f"Missing required field: {field}")
        
        # Проверка модели
        if 'model' in config:
            self._validate_model_config(config['model'])
        
        # Проверка промпта
        if 'system_prompt' in config:
            self._validate_prompt(config['system_prompt'])
        
        return len(self.errors) == 0
    
    def _validate_model_config(self, model_config: Dict[str, Any]):
        """Валидация конфигурации модели"""
        required_model_fields = ['provider', 'model_name']
        for field in required_model_fields:
            if field not in model_config:
                self.errors.append(f"Missing model field: {field}")
        
        # Проверка температуры
        if 'temperature' in model_config:
            temp = model_config['temperature']
            if not (0 <= temp <= 2):
                self.warnings.append(f"Temperature {temp} is outside recommended range [0, 2]")
    
    def _validate_prompt(self, prompt: str):
        """Валидация промпта"""
        if len(prompt) < 10:
            self.warnings.append("System prompt is very short")
        
        if len(prompt) > 10000:
            self.warnings.append("System prompt is very long")
    
    def get_validation_report(self) -> Dict[str, List[str]]:
        """Получение отчета о валидации"""
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'is_valid': len(self.errors) == 0
        }
```

### 2. Проблемы с загрузкой конфигурации

#### Решения
```python
# Безопасная загрузка конфигурации
import yaml
import os
from typing import Dict, Any

def safe_load_config(config_path: str) -> Dict[str, Any]:
    """Безопасная загрузка конфигурации"""
    try:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Валидация конфигурации
        validator = ConfigValidator()
        if not validator.validate_agent_config(config):
            print("Configuration validation failed:")
            for error in validator.errors:
                print(f"  Error: {error}")
            for warning in validator.warnings:
                print(f"  Warning: {warning}")
        
        return config
        
    except yaml.YAMLError as e:
        print(f"YAML parsing error: {e}")
        return {}
    except Exception as e:
        print(f"Config loading error: {e}")
        return {}

# Резервная конфигурация
def get_fallback_config() -> Dict[str, Any]:
    """Получение резервной конфигурации"""
    return {
        'name': 'Default Agent',
        'role': 'General Purpose',
        'description': 'Default agent configuration',
        'model': {
            'provider': 'openai',
            'model_name': 'gpt-3.5-turbo',
            'temperature': 0.7
        },
        'system_prompt': 'You are a helpful AI assistant.',
        'capabilities': ['general_assistance'],
        'limitations': ['Limited to general tasks']
    }
```

## Логирование и отладка

### 1. Настройка детального логирования

```python
# Расширенное логирование
import logging
import json
from datetime import datetime

class DetailedLogger:
    def __init__(self, name: str, log_file: str = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Форматтер с детальной информацией
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - '
            '%(filename)s:%(lineno)d - %(funcName)s - %(message)s'
        )
        
        # Консольный обработчик
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Файловый обработчик
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def log_agent_interaction(self, agent_name: str, input_data: dict, 
                            output: str, execution_time: float):
        """Логирование взаимодействия с агентом"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'agent_name': agent_name,
            'input_data': input_data,
            'output': output,
            'execution_time': execution_time,
            'input_size': len(str(input_data)),
            'output_size': len(output)
        }
        
        self.logger.info(f"Agent interaction: {json.dumps(log_entry)}")
    
    def log_error(self, error: Exception, context: dict = None):
        """Логирование ошибок"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context or {}
        }
        
        self.logger.error(f"Error occurred: {json.dumps(error_entry)}")
```

### 2. Отладочные инструменты

```python
# Отладочные декораторы
import functools
import time
import traceback

def debug_function(func):
    """Декоратор для отладки функций"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger = logging.getLogger('debug')
        
        logger.debug(f"Entering {func.__name__} with args={args}, kwargs={kwargs}")
        
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            logger.debug(f"Exiting {func.__name__} with result={result} "
                        f"(execution_time={execution_time:.2f}s)")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Error in {func.__name__}: {e} "
                        f"(execution_time={execution_time:.2f}s)")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    return wrapper

# Мониторинг производительности
class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
    
    def monitor(self, func_name: str):
        """Декоратор для мониторинга производительности"""
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                
                try:
                    result = await func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    
                    # Обновление метрик
                    if func_name not in self.metrics:
                        self.metrics[func_name] = {
                            'calls': 0,
                            'total_time': 0,
                            'avg_time': 0,
                            'errors': 0
                        }
                    
                    self.metrics[func_name]['calls'] += 1
                    self.metrics[func_name]['total_time'] += execution_time
                    self.metrics[func_name]['avg_time'] = (
                        self.metrics[func_name]['total_time'] / 
                        self.metrics[func_name]['calls']
                    )
                    
                    return result
                    
                except Exception as e:
                    execution_time = time.time() - start_time
                    self.metrics[func_name]['errors'] += 1
                    raise
            
            return wrapper
        return decorator
    
    def get_metrics(self) -> dict:
        """Получение метрик производительности"""
        return self.metrics
```

## Часто задаваемые вопросы (FAQ)

### Q: Агент не отвечает на запросы
**A:** Проверьте:
1. Правильность API ключей
2. Доступность интернета
3. Состояние агента (`agent.reset_state()`)
4. Логи на наличие ошибок

### Q: Медленные ответы от агентов
**A:** Попробуйте:
1. Уменьшить размер входных данных
2. Использовать кэширование
3. Оптимизировать промпты
4. Проверить нагрузку на систему

### Q: Ошибки памяти
**A:** Решения:
1. Ограничить размер кэша
2. Использовать потоковую обработку
3. Регулярно очищать память
4. Увеличить доступную память

### Q: Проблемы с конфигурацией
**A:** Используйте:
1. Валидатор конфигурации
2. Проверьте синтаксис YAML
3. Убедитесь в наличии всех обязательных полей
4. Проверьте права доступа к файлам

### Q: Как отладить проблемы с агентами?
**A:** Включите:
1. Детальное логирование
2. Мониторинг производительности
3. Отладочные декораторы
4. Проверку метрик системы

Этот документ предоставляет comprehensive руководство по устранению неполадок в мультиагентной системе, включая диагностику, решения и профилактические меры. 
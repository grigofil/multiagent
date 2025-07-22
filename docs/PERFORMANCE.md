# Производительность и оптимизация

## Метрики производительности

### 1. Основные метрики

```python
# src/utils/performance_metrics.py
import time
import psutil
import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PerformanceMetrics:
    """Метрики производительности"""
    execution_time: float
    memory_usage: float
    cpu_usage: float
    input_size: int
    output_size: int
    success: bool
    error_message: str = None

class PerformanceMonitor:
    """Монитор производительности"""
    
    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
        self.start_time = None
    
    def start_monitoring(self):
        """Начало мониторинга"""
        self.start_time = time.time()
    
    def end_monitoring(self, input_data: Any, output: Any, 
                      success: bool = True, error: str = None) -> PerformanceMetrics:
        """Завершение мониторинга"""
        if self.start_time is None:
            raise ValueError("Monitoring not started")
        
        execution_time = time.time() - self.start_time
        memory_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent()
        
        metrics = PerformanceMetrics(
            execution_time=execution_time,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            input_size=len(str(input_data)),
            output_size=len(str(output)),
            success=success,
            error_message=error
        )
        
        self.metrics_history.append(metrics)
        return metrics
    
    def get_average_metrics(self) -> Dict[str, float]:
        """Получение средних метрик"""
        if not self.metrics_history:
            return {}
        
        total_metrics = len(self.metrics_history)
        successful_metrics = [m for m in self.metrics_history if m.success]
        
        return {
            'avg_execution_time': sum(m.execution_time for m in self.metrics_history) / total_metrics,
            'avg_memory_usage': sum(m.memory_usage for m in self.metrics_history) / total_metrics,
            'avg_cpu_usage': sum(m.cpu_usage for m in self.metrics_history) / total_metrics,
            'success_rate': len(successful_metrics) / total_metrics,
            'total_requests': total_metrics
        }
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Получение отчета о производительности"""
        avg_metrics = self.get_average_metrics()
        
        if not self.metrics_history:
            return avg_metrics
        
        # Анализ трендов
        recent_metrics = self.metrics_history[-10:]  # Последние 10 запросов
        recent_avg_time = sum(m.execution_time for m in recent_metrics) / len(recent_metrics)
        
        # Определение тренда
        if len(self.metrics_history) >= 20:
            older_metrics = self.metrics_history[-20:-10]
            older_avg_time = sum(m.execution_time for m in older_metrics) / len(older_metrics)
            trend = "improving" if recent_avg_time < older_avg_time else "degrading"
        else:
            trend = "insufficient_data"
        
        return {
            **avg_metrics,
            'trend': trend,
            'recent_avg_execution_time': recent_avg_time,
            'max_execution_time': max(m.execution_time for m in self.metrics_history),
            'min_execution_time': min(m.execution_time for m in self.metrics_history)
        }
```

### 2. Мониторинг в реальном времени

```python
# src/utils/realtime_monitor.py
import asyncio
import threading
import time
from typing import Dict, Any, Callable
import logging

class RealtimeMonitor:
    """Монитор в реальном времени"""
    
    def __init__(self, update_interval: float = 1.0):
        self.update_interval = update_interval
        self.monitoring = False
        self.callbacks: List[Callable[[Dict[str, Any]], None]] = []
        self.logger = logging.getLogger(__name__)
    
    def add_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Добавление callback для обновлений"""
        self.callbacks.append(callback)
    
    def start_monitoring(self):
        """Запуск мониторинга"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        self.logger.info("Real-time monitoring started")
    
    def stop_monitoring(self):
        """Остановка мониторинга"""
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join()
        self.logger.info("Real-time monitoring stopped")
    
    def _monitor_loop(self):
        """Цикл мониторинга"""
        while self.monitoring:
            try:
                metrics = self._collect_metrics()
                
                # Вызов всех callbacks
                for callback in self.callbacks:
                    try:
                        callback(metrics)
                    except Exception as e:
                        self.logger.error(f"Callback error: {e}")
                
                time.sleep(self.update_interval)
                
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                time.sleep(self.update_interval)
    
    def _collect_metrics(self) -> Dict[str, Any]:
        """Сбор метрик"""
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent()
        disk = psutil.disk_usage('/')
        
        return {
            'timestamp': time.time(),
            'memory_percent': memory.percent,
            'memory_available': memory.available / 1024 / 1024,  # MB
            'cpu_percent': cpu,
            'disk_percent': disk.percent,
            'disk_free': disk.free / 1024 / 1024 / 1024,  # GB
            'load_average': psutil.getloadavg()
        }

# Пример использования
def print_metrics(metrics: Dict[str, Any]):
    """Callback для вывода метрик"""
    print(f"CPU: {metrics['cpu_percent']}%, "
          f"Memory: {metrics['memory_percent']}%, "
          f"Disk: {metrics['disk_percent']}%")

monitor = RealtimeMonitor(update_interval=2.0)
monitor.add_callback(print_metrics)
monitor.start_monitoring()
```

## Оптимизация производительности

### 1. Кэширование

```python
# src/utils/advanced_cache.py
import asyncio
import hashlib
import json
import time
from typing import Any, Dict, Optional
from functools import wraps
import redis

class AdvancedCache:
    """Продвинутый кэш с различными стратегиями"""
    
    def __init__(self, redis_url: str = None, max_memory_mb: int = 100):
        self.redis_url = redis_url
        self.max_memory = max_memory_mb * 1024 * 1024  # Convert to bytes
        self.memory_cache = {}
        self.access_times = {}
        self.cache_hits = 0
        self.cache_misses = 0
        
        if redis_url:
            self.redis = redis.from_url(redis_url)
        else:
            self.redis = None
    
    def _generate_key(self, data: Any) -> str:
        """Генерация ключа кэша"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    async def get(self, key: str) -> Optional[Any]:
        """Получение данных из кэша"""
        # Попытка получить из Redis
        if self.redis:
            try:
                cached_data = self.redis.get(key)
                if cached_data:
                    self.cache_hits += 1
                    return json.loads(cached_data)
            except Exception:
                pass
        
        # Попытка получить из памяти
        if key in self.memory_cache:
            self.cache_hits += 1
            self.access_times[key] = time.time()
            return self.memory_cache[key]
        
        self.cache_misses += 1
        return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        """Сохранение данных в кэш"""
        # Сохранение в Redis
        if self.redis:
            try:
                self.redis.setex(key, ttl, json.dumps(value))
            except Exception:
                pass
        
        # Сохранение в память
        self.memory_cache[key] = value
        self.access_times[key] = time.time()
        
        # Проверка размера памяти
        self._cleanup_if_needed()
    
    def _cleanup_if_needed(self):
        """Очистка кэша при превышении лимита"""
        if len(self.memory_cache) == 0:
            return
        
        # Оценка размера кэша
        cache_size = sum(len(str(v)) for v in self.memory_cache.values())
        
        if cache_size > self.max_memory:
            # Удаление наименее используемых элементов
            sorted_items = sorted(
                self.access_times.items(),
                key=lambda x: x[1]
            )
            
            # Удаляем 20% наименее используемых
            items_to_remove = len(sorted_items) // 5
            for key, _ in sorted_items[:items_to_remove]:
                del self.memory_cache[key]
                del self.access_times[key]
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Получение статистики кэша"""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = self.cache_hits / total_requests if total_requests > 0 else 0
        
        return {
            'hits': self.cache_hits,
            'misses': self.cache_misses,
            'hit_rate': hit_rate,
            'memory_cache_size': len(self.memory_cache),
            'redis_available': self.redis is not None
        }

# Декоратор для кэширования
def cache_result(prefix: str = "", ttl: int = 3600):
    """Декоратор для кэширования результатов функций"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = AdvancedCache()
            
            # Генерация ключа кэша
            cache_key = f"{prefix}:{hash(str(args) + str(kwargs))}"
            
            # Попытка получить из кэша
            cached_result = await cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Выполнение функции
            result = await func(*args, **kwargs)
            
            # Сохранение в кэш
            await cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator
```

### 2. Асинхронная обработка

```python
# src/utils/async_processor.py
import asyncio
from typing import List, Any, Callable, TypeVar
from concurrent.futures import ThreadPoolExecutor
import time

T = TypeVar('T')
R = TypeVar('R')

class AsyncProcessor:
    """Асинхронный процессор для обработки данных"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_batch(self, items: List[T], 
                          processor: Callable[[T], R],
                          batch_size: int = 10) -> List[R]:
        """Пакетная обработка элементов"""
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            # Создание задач для батча
            tasks = []
            for item in batch:
                task = asyncio.create_task(
                    self._process_item(item, processor)
                )
                tasks.append(task)
            
            # Ожидание завершения батча
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Фильтрация успешных результатов
            for result in batch_results:
                if not isinstance(result, Exception):
                    results.append(result)
        
        return results
    
    async def _process_item(self, item: T, processor: Callable[[T], R]) -> R:
        """Обработка одного элемента"""
        loop = asyncio.get_event_loop()
        
        # Выполнение в отдельном потоке
        return await loop.run_in_executor(self.executor, processor, item)
    
    async def process_with_timeout(self, items: List[T],
                                 processor: Callable[[T], R],
                                 timeout: float = 30.0) -> List[R]:
        """Обработка с таймаутом"""
        tasks = []
        for item in items:
            task = asyncio.create_task(self._process_item(item, processor))
            tasks.append(task)
        
        # Ожидание с таймаутом
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            # Отмена незавершенных задач
            for task in tasks:
                if not task.done():
                    task.cancel()
            raise
        
        return [r for r in results if not isinstance(r, Exception)]
    
    def __del__(self):
        """Очистка ресурсов"""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)

# Пример использования
async def process_large_dataset():
    """Пример обработки большого набора данных"""
    processor = AsyncProcessor(max_workers=8)
    
    # Большой набор данных
    data_items = [f"item_{i}" for i in range(1000)]
    
    def process_item(item: str) -> str:
        # Имитация обработки
        time.sleep(0.1)
        return f"processed_{item}"
    
    # Пакетная обработка
    results = await processor.process_batch(
        data_items, 
        process_item, 
        batch_size=50
    )
    
    return results
```

### 3. Оптимизация памяти

```python
# src/utils/memory_optimizer.py
import gc
import psutil
import weakref
from typing import Dict, Any, List
import logging

class MemoryOptimizer:
    """Оптимизатор памяти"""
    
    def __init__(self, memory_threshold: float = 80.0):
        self.memory_threshold = memory_threshold
        self.logger = logging.getLogger(__name__)
        self.optimization_history = []
    
    def check_memory_usage(self) -> Dict[str, float]:
        """Проверка использования памяти"""
        memory = psutil.virtual_memory()
        
        return {
            'percent': memory.percent,
            'available_mb': memory.available / 1024 / 1024,
            'used_mb': memory.used / 1024 / 1024,
            'total_mb': memory.total / 1024 / 1024
        }
    
    def optimize_if_needed(self) -> bool:
        """Оптимизация памяти при необходимости"""
        memory_usage = self.check_memory_usage()
        
        if memory_usage['percent'] > self.memory_threshold:
            self.logger.warning(f"High memory usage: {memory_usage['percent']}%")
            
            # Принудительная очистка памяти
            gc.collect()
            
            # Очистка слабых ссылок
            gc.collect(2)
            
            # Запись оптимизации
            self.optimization_history.append({
                'timestamp': time.time(),
                'memory_before': memory_usage,
                'memory_after': self.check_memory_usage()
            })
            
            return True
        
        return False
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Получение статистики оптимизации"""
        return {
            'total_optimizations': len(self.optimization_history),
            'last_optimization': self.optimization_history[-1] if self.optimization_history else None,
            'current_memory': self.check_memory_usage()
        }

class MemoryEfficientCache:
    """Кэш с эффективным использованием памяти"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache = {}
        self.access_order = []
        self.memory_optimizer = MemoryOptimizer()
    
    def get(self, key: str) -> Any:
        """Получение значения из кэша"""
        if key in self.cache:
            # Обновление порядка доступа
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """Установка значения в кэш"""
        # Проверка необходимости оптимизации
        self.memory_optimizer.optimize_if_needed()
        
        # Удаление старых элементов при превышении лимита
        if len(self.cache) >= self.max_size:
            oldest_key = self.access_order[0]
            del self.cache[oldest_key]
            self.access_order.pop(0)
        
        # Добавление нового элемента
        self.cache[key] = value
        self.access_order.append(key)
    
    def clear(self):
        """Очистка кэша"""
        self.cache.clear()
        self.access_order.clear()
        gc.collect()
```

## Профилирование и анализ

### 1. Профилирование кода

```python
# src/utils/profiler.py
import cProfile
import pstats
import io
import time
from functools import wraps
from typing import Callable, Any

class CodeProfiler:
    """Профилировщик кода"""
    
    def __init__(self):
        self.profiler = cProfile.Profile()
        self.stats = None
    
    def start_profiling(self):
        """Начало профилирования"""
        self.profiler.enable()
    
    def stop_profiling(self) -> pstats.Stats:
        """Остановка профилирования"""
        self.profiler.disable()
        self.stats = pstats.Stats(self.profiler)
        return self.stats
    
    def get_profile_report(self, sort_by: str = 'cumulative', 
                          limit: int = 20) -> str:
        """Получение отчета профилирования"""
        if not self.stats:
            return "No profiling data available"
        
        # Захват вывода
        output = io.StringIO()
        self.stats.sort_stats(sort_by).print_stats(limit, stream=output)
        return output.getvalue()
    
    def save_profile_data(self, filename: str):
        """Сохранение данных профилирования"""
        if self.stats:
            self.stats.dump_stats(filename)

def profile_function(func: Callable) -> Callable:
    """Декоратор для профилирования функций"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        profiler = CodeProfiler()
        profiler.start_profiling()
        
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            stats = profiler.stop_profiling()
            print(f"Profile for {func.__name__}:")
            print(profiler.get_profile_report())
    
    return wrapper

# Пример использования
@profile_function
async def expensive_operation():
    """Дорогая операция для профилирования"""
    # Имитация дорогой операции
    await asyncio.sleep(1)
    return "result"
```

### 2. Анализ производительности

```python
# src/utils/performance_analyzer.py
import time
import statistics
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import numpy as np

class PerformanceAnalyzer:
    """Анализатор производительности"""
    
    def __init__(self):
        self.measurements = []
    
    def measure_execution_time(self, func: Callable) -> Callable:
        """Декоратор для измерения времени выполнения"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                self.measurements.append({
                    'function': func.__name__,
                    'execution_time': execution_time,
                    'timestamp': time.time(),
                    'success': True
                })
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                self.measurements.append({
                    'function': func.__name__,
                    'execution_time': execution_time,
                    'timestamp': time.time(),
                    'success': False,
                    'error': str(e)
                })
                
                raise
        
        return wrapper
    
    def get_statistics(self, function_name: str = None) -> Dict[str, float]:
        """Получение статистики производительности"""
        if function_name:
            measurements = [m for m in self.measurements if m['function'] == function_name]
        else:
            measurements = self.measurements
        
        if not measurements:
            return {}
        
        execution_times = [m['execution_time'] for m in measurements]
        success_rate = sum(1 for m in measurements if m['success']) / len(measurements)
        
        return {
            'count': len(measurements),
            'mean_time': statistics.mean(execution_times),
            'median_time': statistics.median(execution_times),
            'min_time': min(execution_times),
            'max_time': max(execution_times),
            'std_dev': statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
            'success_rate': success_rate
        }
    
    def plot_performance_trend(self, function_name: str = None):
        """Построение графика тренда производительности"""
        if function_name:
            measurements = [m for m in self.measurements if m['function'] == function_name]
        else:
            measurements = self.measurements
        
        if not measurements:
            print("No data to plot")
            return
        
        # Подготовка данных
        timestamps = [m['timestamp'] for m in measurements]
        execution_times = [m['execution_time'] for m in measurements]
        
        # Нормализация временных меток
        start_time = min(timestamps)
        normalized_timestamps = [t - start_time for t in timestamps]
        
        # Построение графика
        plt.figure(figsize=(12, 6))
        plt.plot(normalized_timestamps, execution_times, 'b-', alpha=0.7)
        plt.scatter(normalized_timestamps, execution_times, c='red', s=20)
        
        # Линия тренда
        if len(execution_times) > 1:
            z = np.polyfit(normalized_timestamps, execution_times, 1)
            p = np.poly1d(z)
            plt.plot(normalized_timestamps, p(normalized_timestamps), "r--", alpha=0.8)
        
        plt.xlabel('Time (seconds)')
        plt.ylabel('Execution Time (seconds)')
        plt.title(f'Performance Trend for {function_name or "All Functions"}')
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def generate_performance_report(self) -> str:
        """Генерация отчета о производительности"""
        if not self.measurements:
            return "No performance data available"
        
        report = []
        report.append("=== Performance Report ===\n")
        
        # Общая статистика
        all_stats = self.get_statistics()
        report.append("Overall Statistics:")
        for key, value in all_stats.items():
            report.append(f"  {key}: {value:.4f}")
        
        report.append("\nFunction-specific Statistics:")
        
        # Статистика по функциям
        functions = set(m['function'] for m in self.measurements)
        for func in functions:
            stats = self.get_statistics(func)
            report.append(f"\n{func}:")
            for key, value in stats.items():
                report.append(f"  {key}: {value:.4f}")
        
        return "\n".join(report)
```

## Рекомендации по оптимизации

### 1. Оптимизация агентов

```python
# Рекомендации для оптимизации агентов

class OptimizedAgent(BaseAgent):
    """Оптимизированный базовый агент"""
    
    def __init__(self, config: AgentConfig, api_key: str = None):
        super().__init__(config, api_key)
        self.cache = AdvancedCache()
        self.performance_monitor = PerformanceMonitor()
    
    async def process(self, input_data: Any) -> str:
        """Оптимизированная обработка данных"""
        # Проверка кэша
        cache_key = self._generate_cache_key(input_data)
        cached_result = await self.cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Мониторинг производительности
        self.performance_monitor.start_monitoring()
        
        try:
            # Обработка данных
            result = await self._process_optimized(input_data)
            
            # Сохранение в кэш
            await self.cache.set(cache_key, result, ttl=3600)
            
            # Завершение мониторинга
            self.performance_monitor.end_monitoring(input_data, result)
            
            return result
            
        except Exception as e:
            self.performance_monitor.end_monitoring(input_data, "", success=False, error=str(e))
            raise
    
    async def _process_optimized(self, input_data: Any) -> str:
        """Оптимизированная обработка"""
        # Предобработка
        processed_input = self._preprocess_efficiently(input_data)
        
        # Генерация ответа с оптимизированными параметрами
        response = await self._generate_response_optimized(processed_input)
        
        # Постобработка
        return self._postprocess_efficiently(response)
    
    def _preprocess_efficiently(self, data: Any) -> str:
        """Эффективная предобработка"""
        if isinstance(data, dict):
            # Использование только необходимых полей
            essential_fields = ['content', 'type', 'priority']
            filtered_data = {k: v for k, v in data.items() if k in essential_fields}
            return str(filtered_data)
        return str(data)
    
    async def _generate_response_optimized(self, input_text: str) -> str:
        """Оптимизированная генерация ответа"""
        # Ограничение размера входных данных
        if len(input_text) > 4000:
            input_text = input_text[:4000] + "..."
        
        # Оптимизированные параметры модели
        optimized_params = {
            "temperature": 0.5,  # Более стабильные ответы
            "max_tokens": 1000,  # Ограничение размера ответа
            "top_p": 0.9
        }
        
        return await self._generate_response(input_text, optimized_params)
    
    def _postprocess_efficiently(self, response: str) -> str:
        """Эффективная постобработка"""
        # Ограничение размера ответа
        if len(response) > 2000:
            response = response[:2000] + "..."
        
        return response
```

### 2. Оптимизация рабочих процессов

```python
# Оптимизированный рабочий процесс

class OptimizedWorkflow:
    """Оптимизированный рабочий процесс"""
    
    def __init__(self, agents: Dict[str, BaseAgent]):
        self.agents = agents
        self.cache = AdvancedCache()
        self.processor = AsyncProcessor(max_workers=4)
        self.memory_optimizer = MemoryOptimizer()
    
    async def execute_optimized(self, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Оптимизированное выполнение рабочего процесса"""
        # Проверка кэша для всего рабочего процесса
        workflow_key = self._generate_workflow_key(initial_data)
        cached_result = await self.cache.get(workflow_key)
        if cached_result:
            return cached_result
        
        # Параллельная обработка независимых шагов
        current_data = initial_data.copy()
        
        # Группировка независимых шагов
        independent_steps = self._group_independent_steps()
        
        for step_group in independent_steps:
            # Параллельное выполнение группы шагов
            tasks = []
            for step in step_group:
                task = self._execute_step_optimized(step, current_data)
                tasks.append(task)
            
            # Ожидание завершения группы
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Обновление данных
            for step, result in zip(step_group, results):
                if not isinstance(result, Exception):
                    current_data[step['output_key']] = result
            
            # Оптимизация памяти после каждой группы
            self.memory_optimizer.optimize_if_needed()
        
        # Сохранение результата в кэш
        await self.cache.set(workflow_key, current_data, ttl=1800)
        
        return current_data
    
    async def _execute_step_optimized(self, step: Dict[str, Any], 
                                    data: Dict[str, Any]) -> Any:
        """Оптимизированное выполнение шага"""
        agent = self.agents[step['agent']]
        
        # Подготовка входных данных
        agent_input = self._prepare_agent_input(data, step['input_mapping'])
        
        # Проверка кэша для шага
        step_key = f"{step['name']}:{hash(str(agent_input))}"
        cached_step_result = await self.cache.get(step_key)
        if cached_step_result:
            return cached_step_result
        
        # Выполнение шага
        result = await agent.process(agent_input)
        
        # Сохранение результата шага в кэш
        await self.cache.set(step_key, result, ttl=900)
        
        return result
    
    def _group_independent_steps(self) -> List[List[Dict[str, Any]]]:
        """Группировка независимых шагов для параллельного выполнения"""
        # Простая группировка - каждый шаг в отдельной группе
        # В реальной реализации здесь была бы логика определения зависимостей
        return [[step] for step in self.workflow_steps]
```

### 3. Мониторинг и алерты

```python
# Система мониторинга и алертов

class PerformanceAlertSystem:
    """Система алертов производительности"""
    
    def __init__(self):
        self.thresholds = {
            'execution_time': 30.0,  # секунды
            'memory_usage': 85.0,    # проценты
            'cpu_usage': 90.0,       # проценты
            'error_rate': 0.1        # 10%
        }
        self.alerts = []
    
    def check_performance(self, metrics: PerformanceMetrics) -> List[str]:
        """Проверка производительности и генерация алертов"""
        alerts = []
        
        # Проверка времени выполнения
        if metrics.execution_time > self.thresholds['execution_time']:
            alerts.append(f"High execution time: {metrics.execution_time:.2f}s")
        
        # Проверка использования памяти
        if metrics.memory_usage > self.thresholds['memory_usage']:
            alerts.append(f"High memory usage: {metrics.memory_usage:.1f}%")
        
        # Проверка использования CPU
        if metrics.cpu_usage > self.thresholds['cpu_usage']:
            alerts.append(f"High CPU usage: {metrics.cpu_usage:.1f}%")
        
        # Сохранение алертов
        for alert in alerts:
            self.alerts.append({
                'timestamp': time.time(),
                'alert': alert,
                'metrics': metrics
            })
        
        return alerts
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Получение сводки алертов"""
        if not self.alerts:
            return {"total_alerts": 0}
        
        recent_alerts = [a for a in self.alerts 
                        if time.time() - a['timestamp'] < 3600]  # Последний час
        
        return {
            'total_alerts': len(self.alerts),
            'recent_alerts': len(recent_alerts),
            'alert_types': list(set(a['alert'].split(':')[0] for a in self.alerts))
        }
```

Этот документ предоставляет comprehensive руководство по оптимизации производительности мультиагентной системы, включая мониторинг, кэширование, асинхронную обработку и профилирование. 
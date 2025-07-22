# Развертывание

## Требования к системе

### Минимальные требования
- Python 3.8+
- 4GB RAM
- 10GB свободного места на диске
- Интернет-соединение для доступа к API

### Рекомендуемые требования
- Python 3.9+
- 8GB RAM
- 20GB свободного места на диске
- SSD для быстрого доступа к данным

## Установка

### 1. Подготовка окружения

```bash
# Создание виртуального окружения
python -m venv agents_env

# Активация окружения
# Windows
agents_env\Scripts\activate
# Linux/Mac
source agents_env/bin/activate
```

### 2. Установка зависимостей

```bash
# Обновление pip
pip install --upgrade pip

# Установка зависимостей
pip install -r requirements.txt

# Установка дополнительных пакетов для разработки
pip install pytest pytest-asyncio pytest-cov pytest-xdist
pip install black flake8 mypy
```

### 3. Настройка конфигурации

```bash
# Копирование файла окружения
cp env.example .env

# Редактирование .env файла
# Добавьте ваши API ключи и настройки
```

## Конфигурация окружения

### Переменные окружения

```bash
# .env
# API Keys
OPENAI_API_KEY=sk-your-openai-api-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key
GOOGLE_API_KEY=your-google-api-key

# System Configuration
AGENT_SYSTEM_ENV=production
LOG_LEVEL=INFO
DEBUG_MODE=false

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/agents_db
REDIS_URL=redis://localhost:6379

# Monitoring
MONITORING_ENABLED=true
METRICS_ENDPOINT=http://localhost:9090
CACHE_TTL=3600

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Конфигурация логов

```python
# logging_config.py
import logging
import logging.handlers
import os

def setup_logging():
    """Настройка системы логирования"""
    
    # Создание директории для логов
    os.makedirs('logs', exist_ok=True)
    
    # Конфигурация корневого логгера
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.handlers.RotatingFileHandler(
                'logs/multiagent.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            ),
            logging.handlers.RotatingFileHandler(
                'logs/errors.log',
                maxBytes=5*1024*1024,   # 5MB
                backupCount=3
            ),
            logging.StreamHandler()
        ]
    )
    
    # Настройка логгера для агентов
    agent_logger = logging.getLogger('agents')
    agent_logger.setLevel(logging.INFO)
    
    # Настройка логгера для взаимодействий
    interaction_logger = logging.getLogger('interactions')
    interaction_logger.setLevel(logging.DEBUG)
```

## Развертывание в продакшене

### 1. Docker развертывание

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание пользователя для безопасности
RUN useradd -m -u 1000 agentuser && chown -R agentuser:agentuser /app
USER agentuser

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["python", "main.py"]
```

### 2. Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  agents:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - AGENT_SYSTEM_ENV=production
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=agents_db
      - POSTGRES_USER=agentuser
      - POSTGRES_PASSWORD=agentpass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - agents

volumes:
  redis_data:
  postgres_data:
```

### 3. Kubernetes развертывание

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agents-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agents
  template:
    metadata:
      labels:
        app: agents
    spec:
      containers:
      - name: agents
        image: agents:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: agents-secrets
              key: openai-api-key
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: agents-secrets
              key: anthropic-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Мониторинг и логирование

### 1. Настройка мониторинга

```python
# monitoring.py
import time
import psutil
import logging
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Метрики
AGENT_REQUESTS = Counter('agent_requests_total', 'Total agent requests', ['agent_type'])
AGENT_RESPONSE_TIME = Histogram('agent_response_time_seconds', 'Agent response time', ['agent_type'])
AGENT_ERRORS = Counter('agent_errors_total', 'Total agent errors', ['agent_type'])
SYSTEM_MEMORY = Gauge('system_memory_bytes', 'System memory usage')
SYSTEM_CPU = Gauge('system_cpu_percent', 'System CPU usage')

class MonitoringService:
    def __init__(self, port=9090):
        self.port = port
        self.logger = logging.getLogger(__name__)
        
    def start(self):
        """Запуск сервера метрик"""
        start_http_server(self.port)
        self.logger.info(f"Monitoring server started on port {self.port}")
        
    def update_system_metrics(self):
        """Обновление системных метрик"""
        SYSTEM_MEMORY.set(psutil.virtual_memory().used)
        SYSTEM_CPU.set(psutil.cpu_percent())
        
    def record_request(self, agent_type: str, response_time: float, success: bool):
        """Запись метрик запроса"""
        AGENT_REQUESTS.labels(agent_type=agent_type).inc()
        AGENT_RESPONSE_TIME.labels(agent_type=agent_type).observe(response_time)
        
        if not success:
            AGENT_ERRORS.labels(agent_type=agent_type).inc()
```

### 2. Настройка логирования

```python
# logging_setup.py
import logging
import json
from datetime import datetime
from typing import Dict, Any

class JSONFormatter(logging.Formatter):
    """Форматтер для JSON логов"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Добавление дополнительных полей
        if hasattr(record, 'agent_type'):
            log_entry['agent_type'] = record.agent_type
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
            
        return json.dumps(log_entry)

def setup_production_logging():
    """Настройка логирования для продакшена"""
    
    # Создание директории для логов
    os.makedirs('logs', exist_ok=True)
    
    # Настройка корневого логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Очистка существующих обработчиков
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Файловый обработчик для всех логов
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/application.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(file_handler)
    
    # Файловый обработчик для ошибок
    error_handler = logging.handlers.RotatingFileHandler(
        'logs/errors.log',
        maxBytes=5*1024*1024,   # 5MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(error_handler)
    
    # Консольный обработчик для разработки
    if os.getenv('DEBUG_MODE', 'false').lower() == 'true':
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(JSONFormatter())
        root_logger.addHandler(console_handler)
```

## Безопасность

### 1. Управление секретами

```python
# security.py
import os
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode

class SecretManager:
    def __init__(self, key_file: str = '.secret_key'):
        self.key_file = key_file
        self.cipher = self._get_cipher()
        
    def _get_cipher(self) -> Fernet:
        """Получение или создание ключа шифрования"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        
        return Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Шифрование данных"""
        return b64encode(self.cipher.encrypt(data.encode())).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Расшифровка данных"""
        return self.cipher.decrypt(b64decode(encrypted_data)).decode()

# Использование
secret_manager = SecretManager()
encrypted_api_key = secret_manager.encrypt("your-api-key")
decrypted_api_key = secret_manager.decrypt(encrypted_api_key)
```

### 2. Аутентификация и авторизация

```python
# auth.py
import jwt
import hashlib
import time
from typing import Optional, Dict, Any
from functools import wraps

class AuthManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        
    def create_token(self, user_id: str, permissions: list) -> str:
        """Создание JWT токена"""
        payload = {
            'user_id': user_id,
            'permissions': permissions,
            'exp': time.time() + 3600,  # 1 час
            'iat': time.time()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Проверка JWT токена"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def hash_password(self, password: str) -> str:
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()

def require_auth(permissions: list = None):
    """Декоратор для проверки аутентификации"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Проверка токена из заголовков
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not token:
                raise UnauthorizedError("Token required")
            
            payload = auth_manager.verify_token(token)
            if not payload:
                raise UnauthorizedError("Invalid token")
            
            # Проверка разрешений
            if permissions:
                user_permissions = payload.get('permissions', [])
                if not any(perm in user_permissions for perm in permissions):
                    raise ForbiddenError("Insufficient permissions")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## Масштабирование

### 1. Горизонтальное масштабирование

```python
# load_balancer.py
import asyncio
import aiohttp
from typing import List, Dict
import random

class LoadBalancer:
    def __init__(self, agent_instances: List[str]):
        self.instances = agent_instances
        self.current_index = 0
        
    def get_next_instance(self) -> str:
        """Получение следующего экземпляра (round-robin)"""
        instance = self.instances[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.instances)
        return instance
    
    def get_random_instance(self) -> str:
        """Получение случайного экземпляра"""
        return random.choice(self.instances)
    
    async def health_check(self) -> Dict[str, bool]:
        """Проверка здоровья экземпляров"""
        health_status = {}
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for instance in self.instances:
                task = self._check_instance_health(session, instance)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for instance, result in zip(self.instances, results):
                health_status[instance] = isinstance(result, bool) and result
        
        return health_status
    
    async def _check_instance_health(self, session: aiohttp.ClientSession, instance: str) -> bool:
        """Проверка здоровья конкретного экземпляра"""
        try:
            async with session.get(f"{instance}/health", timeout=5) as response:
                return response.status == 200
        except:
            return False
```

### 2. Кэширование

```python
# cache.py
import redis
import json
import hashlib
from typing import Any, Optional
from functools import wraps

class CacheManager:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        
    def _generate_key(self, prefix: str, data: Any) -> str:
        """Генерация ключа кэша"""
        data_str = json.dumps(data, sort_keys=True)
        hash_value = hashlib.md5(data_str.encode()).hexdigest()
        return f"{prefix}:{hash_value}"
    
    def get(self, key: str) -> Optional[Any]:
        """Получение данных из кэша"""
        try:
            data = self.redis.get(key)
            return json.loads(data) if data else None
        except:
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Сохранение данных в кэш"""
        try:
            return self.redis.setex(key, ttl, json.dumps(value))
        except:
            return False
    
    def delete(self, key: str) -> bool:
        """Удаление данных из кэша"""
        try:
            return bool(self.redis.delete(key))
        except:
            return False

def cache_result(prefix: str, ttl: int = 3600):
    """Декоратор для кэширования результатов"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_manager = CacheManager(os.getenv('REDIS_URL'))
            
            # Генерация ключа кэша
            cache_key = cache_manager._generate_key(prefix, {
                'args': args,
                'kwargs': kwargs
            })
            
            # Попытка получить из кэша
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Выполнение функции
            result = await func(*args, **kwargs)
            
            # Сохранение в кэш
            cache_manager.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator
```

## Резервное копирование

### 1. Автоматическое резервное копирование

```python
# backup.py
import shutil
import os
import tarfile
from datetime import datetime
import schedule
import time

class BackupManager:
    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
        
    def create_backup(self) -> str:
        """Создание резервной копии"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"agents_backup_{timestamp}.tar.gz"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        with tarfile.open(backup_path, "w:gz") as tar:
            # Резервное копирование конфигурации
            if os.path.exists("config"):
                tar.add("config", arcname="config")
            
            # Резервное копирование логов
            if os.path.exists("logs"):
                tar.add("logs", arcname="logs")
            
            # Резервное копирование базы данных (если используется)
            if os.path.exists("data"):
                tar.add("data", arcname="data")
        
        return backup_path
    
    def cleanup_old_backups(self, keep_days: int = 7):
        """Очистка старых резервных копий"""
        current_time = time.time()
        
        for filename in os.listdir(self.backup_dir):
            file_path = os.path.join(self.backup_dir, filename)
            file_age = current_time - os.path.getmtime(file_path)
            
            if file_age > (keep_days * 24 * 3600):
                os.remove(file_path)
                print(f"Removed old backup: {filename}")

# Настройка расписания резервного копирования
def setup_backup_schedule():
    backup_manager = BackupManager()
    
    # Ежедневное резервное копирование в 2:00
    schedule.every().day.at("02:00").do(backup_manager.create_backup)
    
    # Еженедельная очистка старых резервных копий
    schedule.every().sunday.at("03:00").do(backup_manager.cleanup_old_backups)
    
    while True:
        schedule.run_pending()
        time.sleep(60)
```

## Обновление системы

### 1. Zero-downtime обновление

```python
# deployment_manager.py
import subprocess
import time
import requests
from typing import List

class DeploymentManager:
    def __init__(self, health_check_url: str):
        self.health_check_url = health_check_url
        
    def deploy_new_version(self, image_tag: str) -> bool:
        """Развертывание новой версии"""
        try:
            # Обновление Docker образа
            subprocess.run([
                "docker", "pull", f"agents:{image_tag}"
            ], check=True)
            
            # Постепенное обновление экземпляров
            instances = self._get_running_instances()
            
            for instance in instances:
                # Обновление одного экземпляра
                self._update_instance(instance, image_tag)
                
                # Проверка здоровья
                if not self._wait_for_health_check(instance):
                    self._rollback_instance(instance)
                    return False
                
                time.sleep(30)  # Пауза между обновлениями
            
            return True
            
        except Exception as e:
            print(f"Deployment failed: {e}")
            return False
    
    def _get_running_instances(self) -> List[str]:
        """Получение списка запущенных экземпляров"""
        # Реализация получения списка экземпляров
        return ["instance1", "instance2", "instance3"]
    
    def _update_instance(self, instance: str, image_tag: str):
        """Обновление конкретного экземпляра"""
        subprocess.run([
            "docker", "service", "update",
            "--image", f"agents:{image_tag}",
            instance
        ], check=True)
    
    def _wait_for_health_check(self, instance: str, timeout: int = 300) -> bool:
        """Ожидание успешной проверки здоровья"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{instance}/health", timeout=5)
                if response.status_code == 200:
                    return True
            except:
                pass
            
            time.sleep(5)
        
        return False
    
    def _rollback_instance(self, instance: str):
        """Откат экземпляра к предыдущей версии"""
        subprocess.run([
            "docker", "service", "rollback", instance
        ])
```

Этот документ предоставляет полное руководство по развертыванию мультиагентной системы в различных средах, включая настройку мониторинга, безопасности, масштабирования и резервного копирования. 
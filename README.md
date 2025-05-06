
# DeFi Analyzer

**DeFi Analyzer** — это приложение для анализа смарт-контрактов в сети TRON. Оно позволяет запрашивать информацию о смарт-контрактах (адрес, тип, байткод) через REST API, используя TronGrid API, и сохранять данные в базу PostgreSQL. Проект включает бэкенд на FastAPI и фронтенд на React для удобного взаимодействия с API.

## Основные возможности

- **Бэкенд**:
  - Получение данных о смарт-контрактах TRON через endpoint `/wallet/getcontract` TronGrid API.
  - Классификация контрактов на типы: AMM, MULTISIG, OTHER.
  - Кэширование данных в PostgreSQL для ускорения повторных запросов.
  - Логирование запросов и ошибок для отладки.
  - REST API для получения информации по адресу контракта.

- **Фронтенд**:
  - Веб-интерфейс для ввода адреса контракта и отображения данных (адрес, тип, байткод, дата создания).
  - Обработка ошибок и индикация статуса загрузки.

- **Смарт-контракты**:
  - Обрабатывает любые контракты сети TRON с валидным Base58-адресом (например, `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`).
  - Классификация:
    - `AMM`: Контракты с `swap` в байткоде (например, пулы JustSwap).
    - `MULTISIG`: Контракты с `multisig` в байткоде.
    - `OTHER`: Остальные, включая токены TRC-20 (например, USDT), пользовательские контракты.

## Требования

| Компонент           | Версия/Описание                              |
|---------------------|----------------------------------------------|
| **Операционная система** | Linux (Ubuntu/Debian) или WSL2 на Windows |
| **Python**          | 3.8 или выше                                 |
| **PostgreSQL**      | 12 или выше                                  |
| **Браузер**         | Chrome, Firefox или другой современный       |
| **TronGrid API Key**| Ключ от [TronGrid](https://www.trongrid.io/) |

## Установка

### 1. Клонирование репозитория
Склонируйте проект и перейдите в директорию:

```bash
git clone <repository-url>
cd defi-analyzer
```

### 2. Установка PostgreSQL
Установите PostgreSQL, если он ещё не установлен:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

Создайте базу данных и пользователя:

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE defi_analyzer;
CREATE USER defi_user WITH PASSWORD 'password';
ALTER ROLE defi_user SET client_encoding TO 'utf8';
ALTER ROLE defi_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE defi_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE defi_analyzer TO defi_user;
\q
```

### 3. Установка Python-зависимостей
Создайте и активируйте виртуальное окружение, затем установите зависимости:

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests fastapi uvicorn sqlalchemy asyncpg
```

### 4. Настройка окружения
Создайте файл `.env` в папке `backend`:

```bash
cd backend
nano .env
```

Добавьте следующее содержимое, заменив `your_trongrid_api_key` на ваш ключ от TronGrid:

```
DATABASE_URL=postgresql+asyncpg://defi_user:password@localhost:5432/defi_analyzer
TRONGRID_API_KEY=your_trongrid_api_key
```

### 5. Проверка структуры проекта
Убедитесь, что структура проекта соответствует:

```
defi-analyzer/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   └── contracts.py
│   │   ├── blockchain/
│   │   │   └── tron_client.py
│   │   ├── models/
│   │   │   └── contract_models.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── .env
│   └── test_db.py
├── frontend/
│   └── index.html
├── .gitignore
└── README.md
```

## Запуск приложения

### 1. Запуск бэкенда
1. Перейдите в папку `backend`:

   ```bash
   cd backend
   ```

2. Запустите FastAPI-сервер:

   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

   Сервер будет доступен по адресу `http://localhost:8000`.

3. Проверьте корневой маршрут:

   ```bash
   curl http://localhost:8000
   ```

   Ожидаемый ответ:

   ```json
   {"message": "DeFi Analyzer API is running"}
   ```

### 2. Запуск фронтенда
1. Перейдите в папку `frontend`:

   ```bash
   cd frontend
   ```

2. Запустите HTTP-сервер:

   ```bash
   python3 -m http.server 8080
   ```

3. Откройте браузер и перейдите по адресу `http://localhost:8080`.

## Использование

### Через REST API
1. Запросите данные о смарт-контракте, указав его адрес:

   ```bash
   curl http://localhost:8000/contracts/TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t
   ```

   Пример ответа:

   ```json
   {
     "address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
     "type": "OTHER",
     "source_code": "6080604052...",
     "created_at": "2025-05-06T16:12:01.123456",
     "last_analyzed": null
   }
   ```

2. Проверьте сохранённые данные в PostgreSQL:

   ```bash
   psql -U defi_user -d defi_analyzer -h localhost
   ```

   ```sql
   SELECT * FROM contracts WHERE address = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t';
   ```

### Через фронтенд
1. Откройте `http://localhost:8080` в браузере.
2. Введите адрес контракта (например, `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`) в поле ввода.
3. Нажмите кнопку **Fetch Contract**.
4. Просмотрите данные: адрес, тип, байткод, дату создания.

### Примеры смарт-контрактов
| Адрес                              | Тип       | Описание                     |
|------------------------------------|-----------|------------------------------|
| `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` | OTHER     | USDT (TRC-20 токен)          |
| `<JustSwap pool address>`          | AMM       | Пул ликвидности JustSwap     |
| `<Custom contract address>`        | OTHER     | Пользовательский контракт    |

Найти адреса контрактов можно на [TRONSCAN](https://tronscan.org/).

## Отладка и устранение неисправностей

- **Просмотр
# LogServer
Централизованное хранилище логов.

Принимает логи от `logging.handlers.HTTPHandler` и записывает их во внутренние файлы.
Логи записываются в каждый файл, соответствующий текущему дню, логи за прошедший день хранятся в отдельных файлах. По умолчанию, хранятся логи за неделю.

- [Оф. документация](https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler)
- [Пример конфигурации](https://cppsecrets.com/users/1357411510911410511610510350484964103109971051084699111109/Python-Timed-Rotating-File-Logging-Handlers.php)

С помощью этого решения можно удобно хранить логи от всех приложений в одном месте.

## Пример использования
```python
import logging

ip_address = "127.0.0.1"
port = "5000"
path = "/dev/application"

http_handler = logging.handlers.HTTPHandler(f"{ip_address}:{port}", path, method='POST')
logger = logging.getLogger()
logger.addHandler(http_handler)
```

## Запуск
Перед запуском надо сконфигурировать сервер на ваше усмотрение. Надо скопировать содержимое `.env.template` в `.env`
- Добавить приложения
  Чтобы добавить новый модуль для логов, надо в `.env` в `APPS` перечислить через запятую названия приложений.
  ```
  APPS=app
  APPS=app1,app2
  APPS=app1, app2,app3
  ```
  После старта приложение будет автоматически добавлено в обе среды: `prod` и `dev`
- Конфигурация путей к `openapi.json`
  ```
  DOCS=/docs
  REDOC=/redoc
  ```
- Редактирование тэгов `prod` и/или `dev`
  ```
  TAG_PROD=production
  TAG_DEV=developers
  ```
- Редакирование префикса `/dev` и/или `/prod`
  > `server.ru/PREFIX/your_app`
  ```
  PREFIX_PROD=/api/logs/prod
  PREFIX_DEV=/api/logs/dev
  ```
  > `server.ru/api/logs/dev/your_app`
- Настройка журналирования
  ```
  # Новый файл каждый день
  LOG_WHEN=D
  LOG_INTERVAL=1
  # Количество файлов
  LOG_BACKUP_COUNT=7
  # Время в которое будет создаваться новый файл
  LOG_AT_TIME=midnight
  # Форматирование логов
  LOG_FORMAT=%(asctime)s : %(levelname)s : %(message)s
  ```
  [Подробнее о форматировании...](https://docs.python.org/3/library/logging.html#logrecord-attributes)

## TODO
- [ ] Обработка `exception`
- [ ] Обработка `extra`
- [ ] WebUI. Там надо будет реализовать стриминг файла в браузер.


## Links:
- [Of doc: LogRecord Objects](https://docs.python.org/3/library/logging.html#logrecord-objects)
- [TIMED ROTATING FILE HANDLER](https://cppsecrets.com/users/1357411510911410511610510350484964103109971051084699111109/Python-Timed-Rotating-File-Logging-Handlers.php)
- [python after logging.debug() how to view its logrecord](https://stackoverflow.com/questions/57420008/python-after-logging-debug-how-to-view-its-logrecord)
- [Введение в logging на Python](https://khashtamov.com/ru/python-logging/)
- [logging.handlers — Обработчики логирования](https://digitology.tech/docs/python_3/library/logging.handlers.html)
- [Flask http log server](https://github.com/jalp/httplogger)
- [Remote Logging with Python](https://hartlepublian.wordpress.com/2015/03/06/remote-logging-with-python/)

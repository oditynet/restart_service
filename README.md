# restart_service
У вас есть мастер-сервера и ноды-сервера. На каждой крутятся пачка сервисов,которые нужно перезагрузить по ansible. Рандомизация и легкость отсылки через ансибл команд дало рождению такого малька (пока только ssh напрямую).
Малек генерируется при запуске, по этому серверов может быть сколько угодно.

<img src="https://github.com/oditynet/restart_service/blob/main/gui.png" title="withwords" width="500" />

Синтаксис файла hosts:
```
[Masters]
ipaddr <any>
...
[Nodes]
ipaddr <any>
```

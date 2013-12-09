from core.controller import event_dispatcher

main = event_dispatcher.Dispatcher()
while True:
    main.update()
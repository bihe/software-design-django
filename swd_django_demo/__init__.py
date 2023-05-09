import _thread
import threading

from django.apps import apps
from swd_django_demo import settings


def wait_for_ready_event(ready_event: threading.Event) -> None:
    print('wait_for_event starting')
    event_is_set = ready_event.wait()

    print('event set: %s', event_is_set)
    try:
        from swd_django_demo.containers import Container
        container = Container()  # <-- create the container here
        container.config.from_dict(settings.__dict__)

        container.wire(modules=["orders.views",
                                "products.views",])

    except Exception as e:
        _thread.interrupt_main()


t1 = threading.Thread(name='delayed_app_ready',
                      target=wait_for_ready_event,
                      args=(apps.ready_event,))
t1.start()

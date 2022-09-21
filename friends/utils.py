from friends.models import QueuePlace


class Queue:

    FIFO = 'FIFO'
    LIFO = 'LIFO'
    SUPPORTED_STRATEGIES = [FIFO, LIFO]
    def __init__(self, strategy):
        if strategy not in self.SUPPORTED_STRATEGIES:
            raise ValueError(
                f'Strategy {strategy} is not supported, please use one of {self.SUPPORTED_STRATEGIES}'
            )
        self.strategy = strategy
        self.storage = []

    def add(self, value):
        QueuePlace.objects.create(value=value)

    def pop(self):
        if self.strategy == self.FIFO:
            value = QueuePlace.objects.order_by('id').first()
        elif self.strategy == self.LIFO:
            value = QueuePlace.objects.order_by('id').last()
        if value:
            value.delete()
            return value.value
from typing import List

import aio_pika
from fastapi import WebSocket
from typing_extensions import Literal

from backend import schemas
from backend.config import settings


class Notification:
    _active_connections: List[schemas.ConnectedUser] = []

    _exchanges_queues = {
        "product": {"exchange": "products", "queue": "product_notifications"},
        "payment": {"exchange": "payments", "queue": "payment_notifications"},
    }

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Notification, cls).__new__(cls)
        return cls.instance

    def add_connection(self, connection: schemas.ConnectedUser):
        self._active_connections.append(connection)

    def remove_connection(self, connection: WebSocket):
        self._active_connections = [
            conn
            for conn in self._active_connections
            if conn.connection != connection
        ]

    @property
    def active_connections(self):
        return self._active_connections

    @property
    def queues(self):
        return self._exchanges_queues.keys()

    async def send_notification(
        self, message: str, event_type: Literal["payment", "product"]
    ):
        exchange_name = self._exchanges_queues[event_type]["exchange"]
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange(
                exchange_name, aio_pika.ExchangeType.FANOUT
            )
            await exchange.publish(
                aio_pika.Message(body=message.encode()), routing_key=""
            )

    async def consume_notifications(self, event_type: str):
        queue_name = self._exchanges_queues[event_type]["queue"]
        exchange_name = self._exchanges_queues[event_type]["exchange"]
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(queue_name, auto_delete=True)
            await channel.declare_exchange(
                exchange_name, aio_pika.ExchangeType.FANOUT
            )
            await queue.bind(exchange_name)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        message_body = message.body.decode()
                        if event_type == "product":
                            await self.notify_users(message_body)
                        elif event_type == "payment":
                            await self.notify_admins(message_body)

    async def notify_users(self, message: str):
        connected_clients = [
            conn for conn in self.active_connections if not conn.is_superuser
        ]
        for connected_client in connected_clients:
            await connected_client.connection.send_text(message)

    async def notify_admins(self, message: str):
        connected_admins = [
            conn for conn in self.active_connections if conn.is_superuser
        ]
        for connected_admin in connected_admins:
            await connected_admin.connection.send_text(message)


notification = Notification()

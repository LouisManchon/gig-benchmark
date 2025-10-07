"""
Configuration centralisée pour RabbitMQ
"""
import os
import pika


class RabbitMQConfig:
    """Configuration et gestion des connexions RabbitMQ"""
    
    def __init__(self):
        self.host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
        self.port = int(os.getenv('RABBITMQ_PORT', '5672'))
        self.user = os.getenv('RABBITMQ_USER', 'gig_user')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'gig_password')
        self.vhost = os.getenv('RABBITMQ_VHOST', '/')
        self.heartbeat = int(os.getenv('RABBITMQ_HEARTBEAT', '600'))
        self.blocked_timeout = int(os.getenv('RABBITMQ_BLOCKED_TIMEOUT', '300'))
    
    def get_connection(self):
        """Crée et retourne une connexion RabbitMQ"""
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.vhost,
            credentials=credentials,
            heartbeat=self.heartbeat,
            blocked_connection_timeout=self.blocked_timeout
        )
        return pika.BlockingConnection(parameters)
    
    def close_connection(self, connection):
        """Ferme proprement une connexion"""
        if connection and not connection.is_closed:
            connection.close()


rabbitmq_config = RabbitMQConfig()
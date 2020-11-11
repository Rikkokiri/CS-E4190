from types import SimpleNamespace

import pika
import json
import dateutil.parser
import time
from db_and_event_definitions import customers_database, cost_per_hour, BillingEvent, ParkingEvent
from xprint import xprint


class ParkingWorker:

    def __init__(self, worker_id, queue, weight="1"):
        # Do not edit the init method.
        # Set the variables appropriately in the methods below.
        self.connection = None
        self.channel = None
        self.worker_id = worker_id
        self.queue = queue
        self.weight = weight
        self.parking_state = {}
        self.parking_events = []
        self.billing_event_producer = None
        self.customer_app_event_producer = None

    def initialize_rabbitmq(self):
        # To implement - Initialize the RabbitMQ connection, channel, exchange and queue here
        # Also initialize the channels for the billing_event_producer and customer_app_event_producer
        xprint("ParkingWorker {}: initialize_rabbitmq() called".format(self.worker_id))

    def handle_parking_event(self, ch, method, properties, body):
        # To implement - This is the callback that is passed to "on_message_callback" when a message is received
        xprint("ParkingWorker {}: handle_event() called".format(self.worker_id))
        # Handle the application logic and the publishing of events here

    # Utility function to get the customer_id from a parking event
    def get_customer_id_from_parking_event(self, parking_event):
        customer_id = [customer_id for customer_id, car_number in customers_database.items()
                       if parking_event.car_number == car_number]
        if len(customer_id) is 0:
            xprint("{}: Customer Id for car number {} Not found".format(self.worker_id, parking_event.car_number))
            return None
        return customer_id[0]

    # Utility function to get the time difference in seconds
    def calculate_parking_duration_in_seconds(self, entry_time, exit_time):
        timedelta = (exit_time - entry_time).total_seconds()
        return timedelta

    def start_consuming(self):
        # To implement - Start consuming from Rabbit
        xprint("ParkingWorker {}: start_consuming() called".format(self.worker_id))

    def close(self):
        # Do not edit this method
        try:
            xprint("Closing worker with id = {}".format(self.worker_id))
            self.channel.stop_consuming()
            time.sleep(1)
            self.channel.close()
            self.billing_event_producer.close()
            self.customer_app_event_producer.close()
            time.sleep(1)
            self.connection.close()
        except Exception as e:
            print("Exception {} when closing worker with id = {}".format(e, self.worker_id))


class BillingEventProducer:

    def __init__(self, connection, worker_id):
        # Do not edit the init method.
        self.worker_id = worker_id
        # Reusing connection created in ParkingWorker
        self.channel = connection.channel()

    def initialize_rabbitmq(self):
        # To implement - Initialize the RabbitMq connection, channel, exchange and queue here
        xprint("BillingEventProducer {}: initialize_rabbitmq() called".format(self.worker_id))

    def publish(self, billing_event):
        xprint("BillingEventProducer {}: Publishing billing event {}".format(
            self.worker_id,
            vars(billing_event)))
        # To implement - publish a message to the Rabbitmq here
        # Use json.dumps(vars(billing_event)) to convert the parking_event object to JSON

    def close(self):
        # Do not edit this method
        self.channel.close()


class CustomerEventProducer:

    def __init__(self, connection, worker_id):
        # Do not edit the init method.
        self.worker_id = worker_id
        # Reusing connection created in ParkingWorker
        self.channel = connection.channel()

    def initialize_rabbitmq(self):
        # To implement - Initialize the RabbitMq connection, channel, exchange and queue here
        xprint("CustomerEventProducer {}: initialize_rabbitmq() called".format(self.worker_id))

    def publish_billing_event(self, billing_event):
        xprint("{}: CustomerEventProducer: Publishing billing event {}"
              .format(self.worker_id, vars(billing_event)))
        # To implement - publish a message to the Rabbitmq here
        # Use json.dumps(vars(billing_event)) to convert the parking_event object to JSON

    def publish_parking_event(self, customer_id, parking_event):
        xprint("{}: CustomerEventProducer: Publishing parking event {} {}"
              .format(self.worker_id, customer_id, vars(parking_event)))
        # To implement - publish a message to the Rabbitmq here
        # Use json.dumps(vars(parking_event)) to convert the parking_event object to JSON

    def close(self):
        # Do not edit this method
        self.channel.close()

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
        xprint("ParkingWorker {}: initialize_rabbitmq() called".format(self.worker_id))
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='parking_events_exchange', exchange_type='x-consistent-hash')
        xprint(self.queue)
        self.channel.queue_declare(queue=self.queue)
        self.channel.queue_bind(exchange='parking_events_exchange', queue=self.queue, routing_key=self.weight)
        self.channel.queue_declare(queue='parking_events_dead_letter_queue')

        # Also initialize the channels for the billing_event_producer and customer_app_event_producer
        self.billing_event_producer = BillingEventProducer(self.connection, self.worker_id)
        self.customer_app_event_producer = CustomerEventProducer(self.connection, self.worker_id)
        self.billing_event_producer.initialize_rabbitmq()
        self.customer_app_event_producer.initialize_rabbitmq()

    # # ParkingEventProducer: Publishing parking event {'event_type': 'entry', 'car_number': 'HMWPYN', 'timestamp': '2020-11-12T01:00:00.785985'}
    def handle_parking_event(self, ch, method, properties, body):
        # To implement - This is the callback that is passed to "on_message_callback" when a message is received
        xprint("ParkingWorker {}: handle_event() called".format(self.worker_id))
        # Handle the application logic and the publishing of events here
        message = json.loads(body)
        parking_event = ParkingEvent(**message)

        # Check whether car number exists in customer database
        customer_id = self.get_customer_id_from_parking_event(parking_event)

        if customer_id is None:
            self.channel.basic_publish(
                exchange='',
                routing_key='parking_events_dead_letter_queue',
                body = json.dumps(vars(parking_event)))
            # ParkingWorker must negatively acknowledge such a message
            self.channel.basic_nack(delivery_tag = method.delivery_tag, requeue=False)
            # .basicNack(delivery_tag = method.delivery_tag)
        else:
            self.parking_events.append(parking_event)
            self.customer_app_event_producer.publish_parking_event(customer_id, parking_event)

            # The workers produce parking events for every entry and exit to a customer_app_events exchange.
            if parking_event.event_type == 'entry':
                self.parking_state[parking_event.car_number] = parking_event.timestamp
            else: # exit
                # Additionally, when a car exits a parking lot, the worker handling that particlar customer produces a billing event to a queue
                # called billing_events 
                entry_time = dateutil.parser.isoparse(self.parking_state[parking_event.car_number])
                exit_time = dateutil.parser.isoparse(parking_event.timestamp)
                parking_cost = (self.calculate_parking_duration_in_seconds(entry_time, exit_time) / 3600) * cost_per_hour
                billing_event = BillingEvent(customer_id, parking_event.car_number, self.parking_state[parking_event.car_number], parking_event.timestamp, parking_cost)

                self.parking_state.pop(parking_event.car_number)

                self.billing_event_producer.publish(billing_event)


    # Utility function to get the customer_id from a parking event
    def get_customer_id_from_parking_event(self, parking_event):
        customer_id = [customer_id for customer_id, car_number in customers_database.items()
                       if parking_event.car_number == car_number]
        if len(customer_id) == 0:
            xprint("{}: Customer Id for car number {} Not found".format(self.worker_id, parking_event.car_number))
            return None
        return customer_id[0]

    # Utility function to get the time difference in seconds
    def calculate_parking_duration_in_seconds(self, entry_time, exit_time):
        timedelta = (exit_time - entry_time).total_seconds()
        return timedelta

    def start_consuming(self):
        # Start consuming from Rabbit
        xprint("ParkingWorker {}: start_consuming() called".format(self.worker_id))
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.handle_parking_event)
        self.channel.start_consuming()


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
        self.channel.queue_declare(queue='billing_events', durable=True)

    def publish(self, billing_event):
        xprint("BillingEventProducer {}: Publishing billing event {}".format(
            self.worker_id,
            vars(billing_event)))
        # To implement - publish a message to the Rabbitmq here
        # Use json.dumps(vars(billing_event)) to convert the parking_event object to JSON
        # The BillingEventProducer publishes to the queue billing_events through a default / nameless exchange.
        self.channel.basic_publish(
            exchange='',
            routing_key='billing_events',
            body = json.dumps(vars(billing_event))
            )


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
        self.channel.exchange_declare(exchange='customer_app_events', exchange_type='topic')

    def publish_billing_event(self, billing_event):
        xprint("{}: CustomerEventProducer: Publishing billing event {}".format(self.worker_id, vars(billing_event)))
        # To implement - publish a message to the Rabbitmq here
        # Use json.dumps(vars(billing_event)) to convert the parking_event object to JSON
        self.channel.basic_publish(
            exchange='billing_events',
            body = json.dumps(vars(billing_event)),
            routing_key=billing_event.customer_id
            )

    def publish_parking_event(self, customer_id, parking_event):
        xprint("{}: CustomerEventProducer: Publishing parking event {} {}"
              .format(self.worker_id, customer_id, vars(parking_event)))
        # To implement - publish a message to the Rabbitmq here
        # Use json.dumps(vars(parking_event)) to convert the parking_event object to JSON
        # The CustomerEventProducer publishes BillingEvent(s) to customers, which is then consumed by the CustomerEventConsumer from the customer_app_events exchange
        self.channel.basic_publish(
            exchange='customer_app_events',
            body = json.dumps(vars(parking_event)),
            routing_key=customer_id
            )

    def close(self):
        # Do not edit this method
        self.channel.close()

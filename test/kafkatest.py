from streamsx.topology.topology import Topology
from streamsx.topology.schema import CommonSchema
from streamsx.topology.context import submit
from streamsx.topology.context import ContextTypes
import streamsx.kafka as kafka
import time

def delay (v):
    time.sleep (5.0)
    return True

topo = Topology('KafkaHelloWorld')

to_kafka = topo.source (['Hello', 'World!'])
to_kafka = to_kafka.as_string()
# delay tuple by tuple
to_kafka = to_kafka.filter (delay)

# Publish a stream to Kafka using TEST topic, the Kafka servers
# (bootstrap.servers) are configured in the application configuration 'kafka_props'.
kafka.publish (to_kafka, 'TEST', 'kafka_props')

# Subscribe to same topic as a stream
from_kafka = kafka.subscribe (topo, 'TEST', 'kafka_props', CommonSchema.String)

# You'll find the Hello World! in stdout log file:
from_kafka.print()

submit (ContextTypes.DISTRIBUTED, topo)
# The Streams job is kept running.
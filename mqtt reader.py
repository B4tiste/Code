import paho.mqtt.client as mqtt

# Callback when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("data")

# Callback when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global iteration
    iteration += 1
    # print(f"Message {iteration} received: {msg.payload}")
    print(iteration)

# Callback when a message has been published.
def on_publish(client, userdata, mid):
    print(f"Message with mid {mid} has been published.")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="data_subscriber")
iteration = 0

# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Connect to the broker
client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

from diagnosis import diagnose

network_data = {
    "latency": 200,
    "packet_loss": 8,
    "wifi_signal": "strong",
    "dns_time": 50
}

results = diagnose(network_data)

for result in results:
    print(result)
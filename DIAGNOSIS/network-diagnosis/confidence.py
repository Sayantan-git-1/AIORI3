# confidence.py

def calculate_confidence(metrics, problem):
    """
    Calculate a confidence level for a suspected network problem.

    Returns:
        confidence: numeric confidence score (0-1)
        level: High / Medium / Low
    """

    score = 0.0

    latency = metrics.get("latency")
    packet_loss = metrics.get("packet_loss")
    wifi_signal = metrics.get("wifi_signal")
    dns_time = metrics.get("dns_time")

    # High packet loss
    if problem == "High Packet Loss":
        if packet_loss is not None:
            if packet_loss > 10:
                score = 0.95
            elif packet_loss > 5:
                score = 0.85
            elif packet_loss > 2:
                score = 0.60

    # High latency
    elif problem == "High Latency":
        if latency is not None:
            if latency > 300:
                score = 0.95
            elif latency > 150:
                score = 0.85
            elif latency > 100:
                score = 0.60

    # Weak Wi-Fi
    elif problem == "Weak Wi-Fi Signal":
        if wifi_signal is not None:
            if wifi_signal.lower() == "weak":
                score = 0.90
            elif wifi_signal.lower() == "medium":
                score = 0.50

    # DNS problem
    elif problem == "Possible DNS Issue":
        if dns_time is not None:
            if dns_time > 500:
                score = 0.95
            elif dns_time > 200:
                score = 0.85
            elif dns_time > 100:
                score = 0.60

    # Convert score into a readable level
    if score >= 0.80:
        level = "High"
    elif score >= 0.50:
        level = "Medium"
    else:
        level = "Low"

    return score, level
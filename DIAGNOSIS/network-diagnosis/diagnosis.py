def diagnose(metrics):

    results = []

    packet_loss = metrics.get("packet_loss")
    latency = metrics.get("latency")
    wifi_signal = metrics.get("wifi_signal")
    dns_time = metrics.get("dns_time")

    # High Packet Loss
    if packet_loss is not None and packet_loss > 5:

        results.append({
            "problem": "High Packet Loss",
            "severity": "High",
            "confidence": "High",
            "evidence": f"Packet loss is {packet_loss}%, which exceeds 5%."
        })

    # High Latency
    if latency is not None and latency > 150:

        results.append({
            "problem": "High Latency",
            "severity": "Medium",
            "confidence": "High",
            "evidence": f"Latency is {latency} ms, which exceeds 150 ms."
        })

    # Weak Wi-Fi
    if wifi_signal == "weak":

        results.append({
            "problem": "Weak Wi-Fi Signal",
            "severity": "Medium",
            "confidence": "High",
            "evidence": "The measured Wi-Fi signal is weak."
        })

    # DNS issue
    if dns_time is not None and dns_time > 200:

        results.append({
            "problem": "Possible DNS Issue",
            "severity": "Medium",
            "confidence": "Medium",
            "evidence": f"DNS resolution took {dns_time} ms."
        })

    # Multiple-condition diagnosis
    if (
        packet_loss is not None
        and latency is not None
        and packet_loss > 5
        and latency > 150
    ):

        results.append({
            "problem": "Possible Network Instability",
            "severity": "High",
            "confidence": "Medium",
            "evidence": (
                f"Packet loss is {packet_loss}% "
                f"and latency is {latency} ms."
            )
        })
    missing = []

    if packet_loss is None:
        missing.append("packet_loss")

    if latency is None:
        missing.append("latency")

    if wifi_signal is None:
        missing.append("wifi_signal")

    if dns_time is None:
        missing.append("dns_time")
    if missing:
        results.append({
            "problem": "Incomplete Measurements",
            "severity": "Low",
            "confidence": "High",
            "evidence": f"Missing measurements: {', '.join(missing)}"
        })

    return results
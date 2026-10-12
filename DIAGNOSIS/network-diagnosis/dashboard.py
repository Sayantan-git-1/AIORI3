try:
    import streamlit as st  # type: ignore[import-not-found]
except ModuleNotFoundError:
    raise SystemExit("Missing dependency: streamlit. Install it with `pip install streamlit`.")

try:
    import pandas as pd  # type: ignore[import-not-found]
except ModuleNotFoundError:
    try:
        import streamlit as st  # type: ignore[import-not-found]
    except ModuleNotFoundError:
        pass
    else:
        st.error("Missing dependency: pandas. Install it with `pip install pandas`.")
        st.stop()

from diagnosis import diagnose
from recommendations import RECOMMENDATIONS


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="NetDoctor | Network Diagnosis",
    page_icon="🌐",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 16px;
        color: #64748b;
        margin-top: 5px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 23px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🌐 NetDoctor</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Explainable Home and Last-Mile Internet Connectivity Diagnosis
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "Enter network measurements to identify potential connectivity "
    "problems and understand the evidence behind each finding."
)


# --------------------------------------------------
# SIDEBAR: INPUT MEASUREMENTS
# --------------------------------------------------

st.sidebar.header("Network Measurements")

st.sidebar.caption(
    "Enter actual measurements or enable demo mode to explore "
    "the application using illustrative values."
)

demo_mode = st.sidebar.checkbox(
    "Use illustrative demo values",
    value=True
)

if demo_mode:
    latency = 200.0
    packet_loss = 8.0
    wifi_signal = "strong"
    dns_time = 50.0

else:
    latency = st.sidebar.number_input(
        "Latency (ms)",
        min_value=0.0,
        max_value=60000.0,
        value=50.0
    )

    packet_loss = st.sidebar.number_input(
        "Packet Loss (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0
    )

    wifi_signal = st.sidebar.selectbox(
        "Wi-Fi Signal",
        ["strong", "moderate", "weak", "unknown"]
    )

    dns_time = st.sidebar.number_input(
        "DNS Resolution Time (ms)",
        min_value=0.0,
        max_value=60000.0,
        value=30.0
    )


network_data = {
    "latency": latency,
    "packet_loss": packet_loss,
    "wifi_signal": (
        None if wifi_signal == "unknown"
        else wifi_signal
    ),
    "dns_time": dns_time
}


# --------------------------------------------------
# DIAGNOSIS
# --------------------------------------------------

results = diagnose(network_data)


# --------------------------------------------------
# NETWORK OVERVIEW
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Network Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Latency",
    f"{latency:.1f} ms"
)

col2.metric(
    "Packet Loss",
    f"{packet_loss:.1f}%"
)

col3.metric(
    "DNS Resolution",
    f"{dns_time:.1f} ms"
)

col4.metric(
    "Wi-Fi Signal",
    wifi_signal.title()
)


# --------------------------------------------------
# DIAGNOSIS SUMMARY
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Diagnosis Results</div>',
    unsafe_allow_html=True
)

if not results:

    st.success(
        "No issues were flagged by the current diagnostic rules. "
        "This does not guarantee that the connection is problem-free."
    )

else:

    problem_results = [
        result for result in results
        if result["problem"] != "Incomplete Measurements"
    ]

    if problem_results:

        st.write(
            f"**{len(problem_results)} diagnostic finding(s) detected.**"
        )

        for result in problem_results:

            severity = result["severity"]
            problem = result["problem"]

            with st.container(border=True):

                if severity == "High":
                    st.error(f"🔴 {problem}")

                elif severity == "Medium":
                    st.warning(f"🟠 {problem}")

                else:
                    st.info(f"🔵 {problem}")

                st.write(
                    f"**Severity:** {severity}"
                )

                st.write(
                    f"**Evidence assessment:** {result['confidence']}"
                )

                st.write(
                    f"**Supporting evidence:** {result['evidence']}"
                )

                st.caption(
                    "This finding is based on configured diagnostic "
                    "rules and should not be interpreted as proof "
                    "of the underlying root cause."
                )

                recommendations = RECOMMENDATIONS.get(
                    problem,
                    [
                        "Repeat the measurements.",
                        "Compare results across different destinations.",
                        "Investigate the issue further before assigning a root cause."
                    ]
                )

                st.write("**Recommended next steps:**")

                for recommendation in recommendations:
                    st.write(f"- {recommendation}")

    incomplete = [
        result for result in results
        if result["problem"] == "Incomplete Measurements"
    ]

    for result in incomplete:
        st.warning(
            f"{result['problem']}: {result['evidence']}"
        )


# --------------------------------------------------
# MEASUREMENT TABLE
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Measurement Details</div>',
    unsafe_allow_html=True
)

measurement_table = pd.DataFrame(
    [
        {
            "Measurement": "Latency",
            "Value": f"{latency:.1f} ms"
        },
        {
            "Measurement": "Packet Loss",
            "Value": f"{packet_loss:.1f}%"
        },
        {
            "Measurement": "Wi-Fi Signal",
            "Value": wifi_signal.title()
        },
        {
            "Measurement": "DNS Resolution",
            "Value": f"{dns_time:.1f} ms"
        }
    ]
)

st.dataframe(
    measurement_table,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# EXPLAINABILITY
# --------------------------------------------------

st.markdown(
    '<div class="section-title">How the Diagnosis Works</div>',
    unsafe_allow_html=True
)

st.write(
    """
    NetDoctor evaluates the supplied measurements against configured
    diagnostic rules. Each finding includes the evidence that triggered
    the rule, helping users understand why the system flagged a potential
    problem.
    """
)

st.write(
    """
    Multiple findings can occur together. For example, high latency
    and packet loss can indicate degraded network performance, but
    additional tests may be required to distinguish Wi-Fi interference,
    congestion, routing issues, and other possible causes.
    """
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "NetDoctor | Explainable Network Diagnosis | AIORI3 Project"
)

st.caption(
    "Demo measurements are illustrative. Diagnostic results depend "
    "on the measurements and configured rules."
)
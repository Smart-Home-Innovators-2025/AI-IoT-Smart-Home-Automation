# ai_engine.py
# Now uses Gas (V5) and Energy (V6, V7) for recommendations.

from typing import Dict

def energy_ai(power: float, energy_today: float) -> str:
    """Generates energy status report.
    
    Args:
        power: Current power usage in Watts
        energy_today: Total energy consumed today in Wh
    
    Returns:
        Formatted energy status string with power level and daily total
    """
    status = []
    
    # Current Power Usage
    if power > 150:
        power_status = "🔴 HIGH"
    elif 50 < power <= 150:
        power_status = "🟡 MEDIUM"
    else:
        power_status = "🟢 LOW"
    
    status.append(f"  Power: {power_status} ({power:.1f}W)")

    # Daily Energy Total
    status.append(f"  Energy Today: {energy_today:.2f}Wh")
    
    return "\n".join(status)

def gas_ai(gas: int) -> str:
    """Provides gas level status report.
    
    Args:
        gas: Gas sensor reading (ADC value or ppm equivalent)
    
    Returns:
        Formatted gas status string with danger level and recommendations
    """
    
    if gas > 1200:
        status = "🔴 DANGER"
        message = "Gas leak detected! Ventilate immediately."
    elif 600 < gas <= 1200:
        status = "🟡 WARNING"
        message = "High gas level detected."
    else:
        status = "🟢 SAFE"
        message = "Gas levels normal."
    
    return f"  Status: {status}\n  Level: {gas}\n  {message}"

def ai_master(data: Dict[str, float]) -> str:
    """Master function to generate a formatted system status report.
    
    Args:
        data: Dictionary containing sensor values with keys:
            - 'power': Current power usage (V6) in Watts
            - 'energy_today': Total daily energy (V7) in Wh
            - 'gas': Gas sensor level (V5) in ADC value
    
    Returns:
        Formatted system status report string with all sensor summaries
    """
    
    # Get values from data, providing defaults
    power = data.get('power', 0.0) # From V6
    energy_today = data.get('energy_today', 0.0) # From V7
    gas = data.get('gas', 100) # From V5

    # Call the individual status functions
    energy_str = energy_ai(power, energy_today)
    gas_str = gas_ai(gas)

    # Format the final report string
    final_report = (
        "\n╔════════════════════════════════════╗\n"
        "║   🏠 SMART HOME STATUS REPORT 🏠  ║\n"
        "╚════════════════════════════════════╝\n\n"
        "⚡ ENERGY MONITOR\n"
        f"{energy_str}\n\n"
        "💨 GAS DETECTOR\n"
        f"{gas_str}\n\n"
        "═════════════════════════════════════"
    )
    
    return final_report
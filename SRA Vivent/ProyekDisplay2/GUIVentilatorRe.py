import cv2
import numpy as np
import math
import random
import datetime # For displaying current time and date

# --- Configuration and Colors ---
W, H = 1280, 720 # Standard HD resolution
COLOR_DARK_BLUE = (30, 30, 40) # Background color
COLOR_WHITE = (255, 255, 255)
COLOR_LIGHT_GREY = (180, 180, 180)
COLOR_GREY = (100, 100, 100)
COLOR_BLUE_TEXT = (255, 180, 0) # BGR - Yellow-ish blue for values
COLOR_GREEN_TEXT = (0, 255, 0)
COLOR_RED_TEXT = (0, 0, 255)
COLOR_ORANGE_HIGHLIGHT = (0, 120, 255) # For selected modes/buttons
COLOR_WAVE_PRESSURE = (0, 255, 255) # Yellow-ish for pressure
COLOR_WAVE_FLOW = (255, 150, 50)    # Light blue for flow
COLOR_WAVE_VOLUME = (200, 50, 150)  # Magenta-ish for volume

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SMALL = cv2.FONT_HERSHEY_COMPLEX_SMALL

# --- Helper Functions ---
def put_centered_text(img, text, top_left, bottom_right, font=FONT, font_scale=1, color=COLOR_WHITE, thickness=1):
    (x1, y1) = top_left
    (x2, y2) = bottom_right
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    org_x = center_x - text_w // 2
    org_y = center_y + text_h // 2
    cv2.putText(img, text, (org_x, org_y), font, font_scale, color, thickness, cv2.LINE_AA)

def draw_line_with_label(img, p1, p2, label, label_pos, color=COLOR_GREY, thickness=1, font_scale=0.5):
    cv2.line(img, p1, p2, color, thickness)
    cv2.putText(img, label, label_pos, FONT_SMALL, font_scale, COLOR_GREY, 1, cv2.LINE_AA)

# --- Top Bar ---
def draw_top_bar(img, current_time, date_str):
    # Background for top bar
    cv2.rectangle(img, (0, 0), (W, 40), COLOR_DARK_BLUE, -1)
    cv2.line(img, (0, 40), (W, 40), COLOR_GREY, 1)

    # Left Section: Mindray Logo / Mode
    cv2.putText(img, "Mindray", (10, 28), FONT, 0.8, COLOR_LIGHT_GREY, 2, cv2.LINE_AA)
    cv2.putText(img, "SV800", (W - 100, 28), FONT, 0.6, COLOR_LIGHT_GREY, 1, cv2.LINE_AA)

    # Center Section: Date & Time
    time_str = current_time.strftime("%H:%M:%S")
    cv2.putText(img, date_str, (W // 2 - 100, 18), FONT_SMALL, 0.7, COLOR_WHITE, 1, cv2.LINE_AA)
    cv2.putText(img, time_str, (W // 2 - 100, 32), FONT_SMALL, 0.7, COLOR_WHITE, 1, cv2.LINE_AA)

    # Right Section: Battery / Alarms (Simplified)
    cv2.circle(img, (W - 180, 20), 8, COLOR_GREEN_TEXT, -1) # Battery indicator
    cv2.putText(img, "4 Alarms", (W - 160, 28), FONT_SMALL, 0.6, COLOR_RED_TEXT, 1, cv2.LINE_AA)

# --- Right Side Bar ---
def draw_right_side_bar(img):
    panel_x_start = W - 140
    button_width = 130
    button_height = 50
    margin_y = 10

    # Draw vertical separator
    cv2.line(img, (panel_x_start - 5, 40), (panel_x_start - 5, H - 70), COLOR_GREY, 1)

    buttons = ["O2 Suction", "Nebulizer", "Tools", "P-V Tools", "Insp. Hold", "PEEPI", "Weaning", "Lock", "Menu"]
    for i, label in enumerate(buttons):
        y_start = 50 + i * (button_height + margin_y)
        cv2.rectangle(img, (panel_x_start, y_start), (panel_x_start + button_width, y_start + button_height), COLOR_DARK_BLUE, -1)
        cv2.rectangle(img, (panel_x_start, y_start), (panel_x_start + button_width, y_start + button_height), COLOR_GREY, 1)
        put_centered_text(img, label, (panel_x_start, y_start), (panel_x_start + button_width, y_start + button_height), font_scale=0.6, color=COLOR_WHITE)

    # Standby button (highlighted)
    standby_y_start = y_start + button_height + margin_y + 10 # Extra space
    cv2.rectangle(img, (panel_x_start, standby_y_start), (panel_x_start + button_width, standby_y_start + button_height), COLOR_ORANGE_HIGHLIGHT, -1)
    cv2.rectangle(img, (panel_x_start, standby_y_start), (panel_x_start + button_width, standby_y_start + button_height), COLOR_WHITE, 2)
    put_centered_text(img, "Standby", (panel_x_start, standby_y_start), (panel_x_start + button_width, standby_y_start + button_height), font_scale=0.7, color=COLOR_WHITE, thickness=2)

# --- Bottom Mode Panel ---
def draw_bottom_mode_panel(img):
    panel_y_start = H - 70
    cv2.rectangle(img, (0, panel_y_start), (W - 140, H), COLOR_DARK_BLUE, -1)
    cv2.line(img, (0, panel_y_start), (W - 140, panel_y_start), COLOR_GREY, 1)

    modes = ["V-A/C", "P-A/C", "P-SIMV", "CPAP/PSV", "APRV", "AMV"]
    # Draw header tabs
    tab_width = (W - 140) // len(modes)
    for i, mode in enumerate(modes):
        x1 = i * tab_width
        x2 = (i + 1) * tab_width
        cv2.rectangle(img, (x1, panel_y_start), (x2, panel_y_start + 25), COLOR_GREY, -1)
        cv2.rectangle(img, (x1, panel_y_start), (x2, panel_y_start + 25), COLOR_WHITE, 1)
        put_centered_text(img, mode, (x1, panel_y_start), (x2, panel_y_start + 25), font_scale=0.5, color=COLOR_WHITE)

    # Draw current mode parameters (example for V-A/C)
    current_mode_params = [
        ("CGR", "21", COLOR_GREEN_TEXT),
        ("TV", "520", COLOR_BLUE_TEXT),
        ("TV", "12", COLOR_BLUE_TEXT),
        ("fSIMV", "1.70", COLOR_GREEN_TEXT),
        ("Psupp", "5", COLOR_BLUE_TEXT),
    ]

    param_x_offset = 20
    for i, (label, value, color) in enumerate(current_mode_params):
        x = 10 + i * 150
        cv2.putText(img, label, (x, panel_y_start + 45), FONT_SMALL, 0.6, COLOR_GREY, 1, cv2.LINE_AA)
        cv2.putText(img, value, (x, panel_y_start + 65), FONT, 0.9, color, 2, cv2.LINE_AA)
        cv2.putText(img, "%", (x+50, panel_y_start + 65), FONT_SMALL, 0.6, COLOR_GREY, 1, cv2.LINE_AA) # Placeholder for units

    # Highlighting selected mode
    selected_mode_idx = 0 # V-A/C is selected
    x1_selected = selected_mode_idx * tab_width
    x2_selected = (selected_mode_idx + 1) * tab_width
    cv2.rectangle(img, (x1_selected, panel_y_start), (x2_selected, panel_y_start + 25), COLOR_ORANGE_HIGHLIGHT, -1)
    cv2.rectangle(img, (x1_selected, panel_y_start), (x2_selected, panel_y_start + 25), COLOR_WHITE, 2)
    put_centered_text(img, modes[selected_mode_idx], (x1_selected, panel_y_start), (x2_selected, panel_y_start + 25), font_scale=0.5, color=COLOR_WHITE)

    # Simplified status indicators (bottom left corner)
    cv2.circle(img, (20, H - 35), 8, COLOR_GREEN_TEXT, -1)
    cv2.circle(img, (40, H - 35), 8, COLOR_GREEN_TEXT, -1)
    cv2.circle(img, (60, H - 35), 8, COLOR_GREY, -1)

# --- Numeric Display Panel (Right of Waveforms) ---
def draw_numeric_panel(img, numeric_params):
    panel_x_start = W - 140 - 250 # Adjust based on right panel
    panel_y_start = 40
    panel_width = 250
    panel_height = H - 70 - 40 # Total height minus top bar and bottom mode panel

    cv2.line(img, (panel_x_start, panel_y_start), (panel_x_start, panel_y_start + panel_height), COLOR_GREY, 1)

    # Header for numeric values
    cv2.rectangle(img, (panel_x_start + 5, panel_y_start + 5), (panel_x_start + panel_width - 5, panel_y_start + 30), COLOR_GREY, -1)
    put_centered_text(img, "Big Numeric", (panel_x_start + 5, panel_y_start + 5), (panel_x_start + panel_width - 5, panel_y_start + 30), font_scale=0.6)

    # Draw individual numeric values
    num_sections = 5 # Ppeak, Pmean, PEEP, TVe, MV, RR, FiO2, TVi/IBW
    section_height = (panel_height - 40) // num_sections
    
    # Example Parameters (these would come from simulation data)
    # label, value, unit, color
    params_to_display = [
        ("Ppeak", f"{numeric_params['Ppeak']:.1f}", "cmH2O", COLOR_ORANGE_HIGHLIGHT),
        ("PEEP", f"{numeric_params['PEEP']:.1f}", "cmH2O", COLOR_BLUE_TEXT),
        ("TVe", f"{numeric_params['TVe']:.0f}", "mL", COLOR_BLUE_TEXT),
        ("MV", f"{numeric_params['MV']:.2f}", "L/min", COLOR_GREEN_TEXT),
        ("RR", f"{numeric_params['RR']:.0f}", "bpm", COLOR_BLUE_TEXT),
        ("FiO2", f"{numeric_params['FiO2']:.0f}", "%", COLOR_BLUE_TEXT),
        ("TVi/IBW", f"{numeric_params['TVi_IBW']:.1f}", "mL/kg", COLOR_BLUE_TEXT)
    ]
    
    y_offset_start = panel_y_start + 40
    for i, (label, value, unit, color) in enumerate(params_to_display):
        current_y = y_offset_start + i * (section_height + 5) # Added a small gap
        
        cv2.putText(img, label, (panel_x_start + 10, current_y), FONT_SMALL, 0.6, COLOR_GREY, 1, cv2.LINE_AA)
        cv2.putText(img, value, (panel_x_start + 10, current_y + 30), FONT, 1.2, color, 2, cv2.LINE_AA)
        cv2.putText(img, unit, (panel_x_start + 100, current_y + 30), FONT_SMALL, 0.7, COLOR_GREY, 1, cv2.LINE_AA)

        # Draw associated smaller numeric values like Pmean, Pplateau (example for Ppeak)
        if label == "Ppeak":
            cv2.putText(img, f"Pmean {numeric_params['Pmean']:.1f}", (panel_x_start + 10, current_y + 50), FONT_SMALL, 0.6, COLOR_GREY, 1, cv2.LINE_AA)
            cv2.putText(img, f"Pplat {numeric_params['Pplat']:.1f}", (panel_x_start + 10, current_y + 65), FONT_SMALL, 0.6, COLOR_GREY, 1, cv2.LINE_AA)

        # Draw min/max thresholds (simplified, just text)
        # cv2.putText(img, "min 250", (panel_x_start + panel_width - 80, current_y + 10), FONT_SMALL, 0.5, COLOR_GREY, 1, cv2.LINE_AA)
        # cv2.putText(img, "max 750", (panel_x_start + panel_width - 80, current_y + 25), FONT_SMALL, 0.5, COLOR_GREY, 1, cv2.LINE_AA)

# --- Waveform Panel ---
def draw_waveform_panel(img, waveform_data, time_labels, numeric_params):
    panel_x_start = 0
    panel_y_start = 40
    panel_width = W - 140 - 250 # Width is total - right side bar - numeric panel
    panel_height = H - 70 - 40 # Height is total - top bar - bottom mode panel

    # Draw headers for waveforms
    waveform_tabs = ["Waveforms", "Spirometry", "Values", "Big Numeric"]
    tab_width = (panel_width - 10) // len(waveform_tabs)
    for i, tab in enumerate(waveform_tabs):
        x1 = panel_x_start + 5 + i * tab_width
        x2 = panel_x_start + 5 + (i + 1) * tab_width
        cv2.rectangle(img, (x1, panel_y_start + 5), (x2, panel_y_start + 30), COLOR_GREY, -1)
        cv2.rectangle(img, (x1, panel_y_start + 5), (x2, panel_y_start + 30), COLOR_WHITE, 1)
        put_centered_text(img, tab, (x1, panel_y_start + 5), (x2, panel_y_start + 30), font_scale=0.5, color=COLOR_WHITE)

    # Highlight "Waveforms" tab
    x1_selected = panel_x_start + 5
    x2_selected = panel_x_start + 5 + tab_width
    cv2.rectangle(img, (x1_selected, panel_y_start + 5), (x2_selected, panel_y_start + 30), COLOR_ORANGE_HIGHLIGHT, -1)
    cv2.rectangle(img, (x1_selected, panel_y_start + 5), (x2_selected, panel_y_start + 30), COLOR_WHITE, 2)
    put_centered_text(img, "Waveforms", (x1_selected, panel_y_start + 5), (x2_selected, panel_y_start + 30), font_scale=0.5, color=COLOR_WHITE)


    waveform_area_y_start = panel_y_start + 40
    waveform_area_height = panel_height - 50
    single_waveform_height = (waveform_area_height - 20) // 3 # 3 waveforms, with small gap

    waveform_labels = [("Pao", "cmH2O", 50, -20, COLOR_WAVE_PRESSURE),
                       ("Flow", "L/min", 10, -5, COLOR_WAVE_FLOW),
                       ("Volume", "mL", 500, -200, COLOR_WAVE_VOLUME)] # Max/min values for scaling

    plot_left_x = panel_x_start + 50
    plot_right_x = panel_x_start + panel_width - 10
    plot_width = plot_right_x - plot_left_x

    # Draw time labels at the bottom of the waveform panel
    label_y = waveform_area_y_start + waveform_area_height - 5
    for i, label_text in enumerate(time_labels):
        x = plot_left_x + i * (plot_width // (len(time_labels) -1))
        cv2.putText(img, label_text, (x - 10, label_y), FONT_SMALL, 0.4, COLOR_GREY, 1, cv2.LINE_AA)


    for i, (label, unit, max_val, min_val, wave_color) in enumerate(waveform_labels):
        wave_y_start = waveform_area_y_start + i * (single_waveform_height + 10)
        wave_y_end = wave_y_start + single_waveform_height
        mid_y = (wave_y_start + wave_y_end) // 2

        # Draw waveform specific labels and units
        cv2.putText(img, label, (panel_x_start + 10, wave_y_start + 20), FONT_SMALL, 0.6, COLOR_GREY, 1, cv2.LINE_AA)
        cv2.putText(img, unit, (panel_x_start + 10, wave_y_start + 35), FONT_SMALL, 0.4, COLOR_GREY, 1, cv2.LINE_AA)

        # Draw horizontal grid lines
        num_grid_lines = 4
        for j in range(num_grid_lines):
            y_grid = wave_y_start + j * (single_waveform_height // (num_grid_lines - 1))
            cv2.line(img, (plot_left_x, y_grid), (plot_right_x, y_grid), COLOR_GREY, 1)

        # Draw vertical grid lines (aligned with time labels)
        for j in range(len(time_labels)):
            x_grid = plot_left_x + j * (plot_width // (len(time_labels) -1))
            cv2.line(img, (x_grid, wave_y_start), (x_grid, wave_y_end), COLOR_GREY, 1)


        # Plot the actual waveform
        points = []
        if label == "Pao":
            wave_raw_data = waveform_data['pressure']
        elif label == "Flow":
            wave_raw_data = waveform_data['flow']
        else: # Volume
            wave_raw_data = waveform_data['volume']

        # Scale and convert points
        for j, val in enumerate(wave_raw_data):
            # Normalize value to 0-1 range
            normalized_val = (val - min_val) / (max_val - min_val)
            # Map to screen coordinates (y-axis inverted for display)
            # We want higher values to be higher on the screen (smaller Y pixel)
            display_y = int(wave_y_end - normalized_val * single_waveform_height)
            display_x = plot_left_x + j * (plot_width // (len(wave_raw_data) - 1))
            points.append((display_x, display_y))

        for j in range(len(points) - 1):
            cv2.line(img, points[j], points[j+1], wave_color, 2)
        
        # Draw dynamic labels on Pressure waveform (Ppeak, PEEP)
        if label == "Pao":
            # Ppeak marker
            p_peak_val = numeric_params['Ppeak']
            p_peak_normalized = (p_peak_val - min_val) / (max_val - min_val)
            p_peak_display_y = int(wave_y_end - p_peak_normalized * single_waveform_height)
            cv2.putText(img, f"Ppeak {p_peak_val:.0f}", (plot_left_x + 5, p_peak_display_y - 5), FONT_SMALL, 0.5, COLOR_WAVE_PRESSURE, 1, cv2.LINE_AA)
            cv2.line(img, (plot_left_x, p_peak_display_y), (plot_right_x, p_peak_display_y), COLOR_WAVE_PRESSURE, 1, cv2.LINE_AA) # Horizontal line

            # PEEP marker
            peep_val = numeric_params['PEEP']
            peep_normalized = (peep_val - min_val) / (max_val - min_val)
            peep_display_y = int(wave_y_end - peep_normalized * single_waveform_height)
            cv2.putText(img, f"PEEP {peep_val:.0f}", (plot_left_x + 5, peep_display_y + 15), FONT_SMALL, 0.5, COLOR_WAVE_PRESSURE, 1, cv2.LINE_AA)
            cv2.line(img, (plot_left_x, peep_display_y), (plot_right_x, peep_display_y), COLOR_WAVE_PRESSURE, 1, cv2.LINE_AA) # Horizontal line


# --- Waveform Generation Functions (More Complex) ---
def generate_pressure_waveform(t, rr, ie_ratio, ppeak, peep, plat_time_ratio=0.3):
    """Generates a realistic pressure waveform."""
    # Convert RR to cycle duration in frames (assuming 20 FPS)
    # Total cycle time = 60 / RR seconds
    # Total frames per cycle = (60 / RR) * FPS
    fps = 20 # from cv2.waitKey(50)
    cycle_duration_frames = int((60 / rr) * fps)
    if cycle_duration_frames == 0: return 0 # Avoid division by zero

    cycle_t = t % cycle_duration_frames

    i_ratio, e_ratio_val = map(int, ie_ratio.split(':'))
    expiratory_ratio = float(e_ratio_val) / i_ratio
    inspiratory_frames = int(cycle_duration_frames / (1 + expiratory_ratio))
    expiratory_frames = cycle_duration_frames - inspiratory_frames
    plateau_frames = int(inspiratory_frames * plat_time_ratio)
    rise_frames = inspiratory_frames - plateau_frames

    if cycle_t < rise_frames:
        # Inspiratory rise phase (from PEEP to Ppeak)
        progress = cycle_t / rise_frames
        # Use an S-curve for smoother transition
        pressure = peep + (ppeak - peep) * (0.5 - 0.5 * math.cos(progress * math.pi))
    elif cycle_t < rise_frames + plateau_frames:
        # Plateau phase (hold at Ppeak)
        pressure = ppeak
    elif cycle_t < cycle_duration_frames:
        # Expiratory phase (from Ppeak to PEEP)
        progress = (cycle_t - (rise_frames + plateau_frames)) / expiratory_frames
        # Exponential decay towards PEEP
        pressure = peep + (ppeak - peep) * math.exp(-3 * progress)
    else:
        pressure = peep # Should not happen with modulo

    return pressure

def generate_flow_waveform(t, rr, ie_ratio, ppeak, peep, volume_data, last_pressure, current_pressure):
    """Generates a realistic flow waveform based on pressure and volume."""
    fps = 20
    cycle_duration_frames = int((60 / rr) * fps)
    if cycle_duration_frames == 0: return 0

    cycle_t = t % cycle_duration_frames

    i_ratio, e_ratio_val = map(int, ie_ratio.split(':'))
    expiratory_ratio = float(e_ratio_val) / i_ratio
    inspiratory_frames = int(cycle_duration_frames / (1 + expiratory_ratio))
    expiratory_frames = cycle_duration_frames - inspiratory_frames
    
    # Simple flow model:
    # Inspiratory: Positive peak, then tapers to 0 during plateau
    # Expiratory: Negative peak, then tapers to 0 at end of expiration
    
    flow_peak_insp = 50 # L/min
    flow_peak_exp = -40 # L/min

    if cycle_t < inspiratory_frames:
        # Inspiration phase
        if current_pressure > last_pressure: # Pressure rising implies inspiratory flow
            progress = cycle_t / inspiratory_frames
            flow = flow_peak_insp * math.sin(progress * math.pi) # Half sine wave
        else: # Plateau, flow drops
            flow = 0
    elif cycle_t < cycle_duration_frames:
        # Expiration phase
        progress = (cycle_t - inspiratory_frames) / expiratory_frames
        flow = flow_peak_exp * math.sin(progress * math.pi) # Negative half sine
    else:
        flow = 0
    
    return flow

def generate_volume_waveform(t, rr, ie_ratio, flow_data):
    """Generates a realistic volume waveform by integrating flow."""
    # Volume is the integral of flow. We can approximate this by summing flow.
    # To avoid ever-increasing volume, we reset it at the start of each cycle.
    
    fps = 20
    cycle_duration_frames = int((60 / rr) * fps)
    if cycle_duration_frames == 0: return 0

    cycle_t = t % cycle_duration_frames
    
    # We need the current volume to integrate. This makes it tricky for a single-point function.
    # For a scrolling graph, `flow_data` will be the recent history.
    # A simpler approach for simulation: based on breathing_wave concept.
    
    # Target tidal volume (e.g., 500 mL)
    tidal_volume = 500
    functional_residual_capacity = 1000 # Baseline volume

    i_ratio, e_ratio_val = map(int, ie_ratio.split(':'))
    expiratory_ratio = float(e_ratio_val) / i_ratio
    inspiratory_frames = int(cycle_duration_frames / (1 + expiratory_ratio))
    
    if cycle_t < inspiratory_frames:
        # Inspiration phase: rise from FRC to FRC + Tidal Volume
        progress = cycle_t / inspiratory_frames
        volume = functional_residual_capacity + tidal_volume * (0.5 - 0.5 * math.cos(progress * math.pi))
    elif cycle_t < cycle_duration_frames:
        # Expiration phase: return to FRC
        progress = (cycle_t - inspiratory_frames) / (cycle_duration_frames - inspiratory_frames)
        volume = functional_residual_capacity + tidal_volume * (0.5 + 0.5 * math.cos(progress * math.pi))
    else:
        volume = functional_residual_capacity

    return volume


# --- Main GUI Drawing Function ---
def draw_mindray_gui(img, waveform_data, numeric_params, current_time, date_str, time_labels):
    img[:] = COLOR_DARK_BLUE # Fill background
    
    draw_top_bar(img, current_time, date_str)
    draw_right_side_bar(img)
    draw_bottom_mode_panel(img)
    draw_numeric_panel(img, numeric_params)
    draw_waveform_panel(img, waveform_data, time_labels, numeric_params)

    # Simplified rotary encoder knob at bottom right (visual only)
    knob_center = (W - 70, H - 35)
    cv2.circle(img, knob_center, 25, COLOR_GREY, -1)
    cv2.circle(img, knob_center, 25, COLOR_WHITE, 1)
    cv2.rectangle(img, (knob_center[0] - 5, knob_center[1] - 30), (knob_center[0] + 5, knob_center[1] - 5), COLOR_WHITE, -1) # Knob indicator

    return img

# --- Main Loop ---
if __name__ == "__main__":
    cv2.namedWindow("Mindray SV800 GUI", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Mindray SV800 GUI", W, H)

    # Initial simulation parameters
    t = 0
    sim_rr = 18.0
    sim_ie_ratio = "1:2"
    sim_ppeak = 25.0
    sim_peep = 5.0

    # History for scrolling waveforms
    waveform_history_length = 300 # Number of points to display for each waveform
    waveform_data = {
        'pressure': [0] * waveform_history_length,
        'flow': [0] * waveform_history_length,
        'volume': [0] * waveform_history_length,
    }

    # Time labels for X-axis
    time_labels = ["-12s", "-8s", "-4s", "0s"]

    # Initial numeric parameters for display
    numeric_params = {
        'Ppeak': sim_ppeak,
        'Pmean': 15.0, # Derived
        'PEEP': sim_peep,
        'Pplat': 20.0, # Derived
        'TVe': 500, # Estimated
        'MV': 9.0, # Estimated
        'RR': sim_rr,
        'FiO2': 21,
        'TVi_IBW': 7.4
    }

    last_pressure_point = 0 # To help calculate flow

    while True:
        current_time = datetime.datetime.now()
        date_str = current_time.strftime("%d-%m-%Y")

        # --- Simulate Dynamic Changes (like the previous script) ---
        sim_rr = 18 + 2 * math.sin(t / 200.0) # Slow oscillation
        sim_ppeak = 25 + 3 * math.sin(t / 150.0)
        sim_peep = 5 + 1 * math.cos(t / 250.0)
        
        # Update numeric parameters based on simulation values
        numeric_params['Ppeak'] = sim_ppeak
        numeric_params['PEEP'] = sim_peep
        numeric_params['RR'] = sim_rr
        # Recalculate derived values (simplified for demo)
        numeric_params['Pmean'] = (sim_ppeak + sim_peep) / 2 + 2 # A bit higher
        numeric_params['Pplat'] = sim_ppeak * 0.8
        numeric_params['TVe'] = 450 + 50 * math.sin(t/100)
        numeric_params['MV'] = numeric_params['TVe'] * numeric_params['RR'] / 1000 # mL to L
        numeric_params['TVi_IBW'] = numeric_params['TVe'] / 60.0 # Assuming IBW ~60kg


        # --- Generate New Waveform Points ---
        new_pressure = generate_pressure_waveform(t, sim_rr, sim_ie_ratio, sim_ppeak, sim_peep)
        new_flow = generate_flow_waveform(t, sim_rr, sim_ie_ratio, sim_ppeak, sim_peep, waveform_data['volume'], last_pressure_point, new_pressure)
        new_volume = generate_volume_waveform(t, sim_rr, sim_ie_ratio, waveform_data['flow']) # This might need to be integrated outside
        
        # Update last pressure for next flow calculation
        last_pressure_point = new_pressure

        # --- Scroll Waveform Data ---
        waveform_data['pressure'].pop(0) # Remove oldest point
        waveform_data['pressure'].append(new_pressure) # Add new point

        waveform_data['flow'].pop(0)
        waveform_data['flow'].append(new_flow)

        waveform_data['volume'].pop(0)
        waveform_data['volume'].append(new_volume)

        # --- Draw GUI ---
        img = np.zeros((H, W, 3), dtype=np.uint8)
        img = draw_mindray_gui(img, waveform_data, numeric_params, current_time, date_str, time_labels)

        cv2.imshow("Mindray SV800 GUI", img)

        t += 1 # Increment simulation time

        if cv2.waitKey(50) & 0xFF == 27: # ESC key to exit (50ms delay = 20 FPS)
            break

    cv2.destroyAllWindows()
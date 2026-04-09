#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Educational Ventilator GUI (Simulation Only)
-------------------------------------------
This is a simplified, educational ventilator GUI built with Tkinter.
It simulates two common modes (VCV and PCV), renders pressure/flow waveforms,
and offers basic alarms. It is NOT a medical device and MUST NOT be used for
real patient care.

Author: ChatGPT
License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time

# -----------------------------
# Simple Lung Model & Ventilator
# -----------------------------

class LungModel:
    """
    Very simplified single-compartment lung model: P = V/C + PEEP + R * flow
    Units (approx):
        - V (mL), C (mL/cmH2O), flow (L/s), R (cmH2O·s/L)
        - Pressures in cmH2O
    This is deliberately simple for educational visualization.
    """
    def __init__(self, compliance_ml_per_cmH2O=50.0, resistance_cmH2O_s_per_L=5.0, peep_cmH2O=5.0):
        self.C = max(1.0, compliance_ml_per_cmH2O)       # mL/cmH2O
        self.R = max(0.1, resistance_cmH2O_s_per_L)      # cmH2O·s/L
        self.PEEP = max(0.0, peep_cmH2O)                 # cmH2O
        self.volume_ml = 0.0                             # above FRC (mL)
        self.flow_Lps = 0.0                              # L/s

    def set_peep(self, peep):
        self.PEEP = max(0.0, peep)

    def step(self, dt, target_flow_Lps):
        """
        Integrate lung response over dt seconds given target (delivered) flow.
        Simple first-order response: we assume delivered flow is what enters the lung.
        Update volume and estimate pressure.
        """
        # Flow in L/s -> convert to mL/s for volume
        self.flow_Lps = float(target_flow_Lps)
        dV_ml = self.flow_Lps * 1000.0 * dt  # L/s -> mL over dt
        self.volume_ml += dV_ml
        # Pressure drop from resistance: R * flow
        pres_resistive = self.R * self.flow_Lps

        # Elastic recoil pressure: V/C (C in mL/cmH2O)
        pres_elastic = self.volume_ml / self.C

        pressure = pres_elastic + pres_resistive + self.PEEP
        return pressure, self.flow_Lps, self.volume_ml


class VentilatorSim:
    """
    Core ventilator logic (highly simplified).
    Supports VCV and PCV with basic timing from RR and I:E ratio or Ti%.
    """
    MODE_VCV = "VCV"
    MODE_PCV = "PCV"

    def __init__(self, lung: LungModel):
        self.lung = lung
        # Settings (reasonable defaults for education only)
        self.mode = self.MODE_VCV
        self.RR_bpm = 14                 # breaths per minute
        self.ie_ratio = 2.0              # I:E = 1:ie_ratio
        self.fiO2 = 40                   # %
        self.target_VT_ml = 450          # for VCV
        self.pinsp_cmH2O = 18            # for PCV (above PEEP)
        self.peep_cmH2O = 5
        self.flow_limit_Lpm = 60         # max flow (L/min) safety clamp

        # Derived timing
        self.cycle_time = 60.0 / self.RR_bpm  # seconds per breath
        self.insp_time = self.cycle_time * (1.0 / (1.0 + self.ie_ratio))
        self.exp_time = self.cycle_time - self.insp_time

        # State
        self.t_in_cycle = 0.0
        self.last_step_ts = None
        self.running = False

        # Alarms
        self.alarm_high_pressure = False
        self.alarm_low_vt = False
        self.alarm_apnea = False
        self.measured_VT_ml = 0.0
        self.last_breath_time = time.time()

        # Limits / thresholds
        self.high_pressure_limit = 40.0  # cmH2O
        self.low_vt_limit = 250.0        # mL
        self.apnea_timeout = 10.0        # s

    def update_timing(self):
        self.lung.set_peep(self.peep_cmH2O)
        self.cycle_time = max(0.5, 60.0 / max(1.0, self.RR_bpm))
        self.insp_time = self.cycle_time * (1.0 / (1.0 + max(0.2, self.ie_ratio)))
        self.exp_time = self.cycle_time - self.insp_time

    def set_mode(self, mode):
        if mode in (self.MODE_VCV, self.MODE_PCV):
            self.mode = mode

    def set_rr(self, rr):
        self.RR_bpm = max(4, min(40, int(rr)))
        self.update_timing()

    def set_ie(self, ie):
        self.ie_ratio = max(0.2, min(5.0, float(ie)))
        self.update_timing()

    def set_fio2(self, fio2):
        self.fiO2 = max(21, min(100, int(fio2)))

    def set_vt(self, vt):
        self.target_VT_ml = max(150, min(800, int(vt)))

    def set_pinsp(self, p):
        self.pinsp_cmH2O = max(5, min(35, int(p)))

    def set_peep(self, peep):
        self.peep_cmH2O = max(0, min(20, int(peep)))
        self.update_timing()

    def set_flow_limit(self, lpm):
        self.flow_limit_Lpm = max(10, min(120, int(lpm)))

    def start(self):
        self.running = True
        self.last_step_ts = time.time()
        self.t_in_cycle = 0.0
        self.measured_VT_ml = 0.0
        self.last_breath_time = time.time()

    def stop(self):
        self.running = False

    def inspiratory(self):
        return self.t_in_cycle < self.insp_time

    def compute_target_flow(self):
        if self.mode == self.MODE_VCV:
            # Deliver VT over insp_time with constant flow
            if self.insp_time <= 0.05:
                flow_Lps = 0.0
            else:
                target_flow_Lps = (self.target_VT_ml / 1000.0) / self.insp_time  # L/s
                flow_Lps = min(target_flow_Lps, self.flow_limit_Lpm / 60.0)
        else:  # PCV
            # Try to achieve PEEP + Pinsp during inspiration using a simple proportional response
            # Very naive: flow proportional to pressure error (with clamp)
            target_pressure = self.peep_cmH2O + self.pinsp_cmH2O
            # Estimate current pressure using lung state
            current_pressure = (self.lung.volume_ml / self.lung.C) + (self.lung.R * self.lung.flow_Lps) + self.peep_cmH2O
            error = max(0.0, target_pressure - current_pressure)
            k = 0.05  # proportional gain
            flow_Lps = k * error
            flow_Lps = min(flow_Lps, self.flow_limit_Lpm / 60.0)
        return flow_Lps

    def step(self, dt):
        """
        Advance ventilator by dt seconds, return (pressure, flow_Lps, volume_ml, phase_changed)
        """
        phase_changed = False
        # Update time in cycle
        self.t_in_cycle += dt
        if self.t_in_cycle >= self.cycle_time:
            # New cycle
            self.t_in_cycle -= self.cycle_time
            phase_changed = True
            self.measured_VT_ml = 0.0
            self.last_breath_time = time.time()

        # Determine target flow
        if self.inspiratory():
            flow_Lps = self.compute_target_flow()
        else:
            # Passive exhalation: simple RC decay towards zero volume above FRC
            tau = max(0.05, (self.lung.R * (self.lung.C / 1000.0)))  # seconds; C converted to L/cmH2O
            # target flow proportional to negative of current volume (approximate)
            flow_Lps = - (self.lung.volume_ml / 1000.0) / tau
            # clamp to flow limit
            if abs(flow_Lps) > (self.flow_limit_Lpm / 60.0):
                flow_Lps = - (self.flow_limit_Lpm / 60.0)

        # Integrate lung
        pressure, flow_Lps, volume_ml = self.lung.step(dt, flow_Lps)

        # Accumulate Vt during inspiration
        if self.inspiratory():
            self.measured_VT_ml += (flow_Lps * 1000.0 * dt)

        # Alarms
        self.alarm_high_pressure = pressure > self.high_pressure_limit
        self.alarm_low_vt = (not self.inspiratory()) and (self.measured_VT_ml < self.low_vt_limit)
        self.alarm_apnea = (time.time() - self.last_breath_time) > self.apnea_timeout

        return pressure, flow_Lps, volume_ml, phase_changed


# -----------------------------
# GUI
# -----------------------------

class Waveform:
    """Simple scrolling waveform plot on a Tkinter Canvas."""
    def __init__(self, canvas: tk.Canvas, y_min, y_max, label=""):
        self.canvas = canvas
        self.y_min = y_min
        self.y_max = y_max
        self.label = label
        self.width = int(canvas["width"])
        self.height = int(canvas["height"])
        self.buffer = [None] * self.width  # holds values mapped to y-pixels
        self.x = 0
        self._draw_axes()

    def _draw_axes(self):
        self.canvas.delete("all")
        # Axis lines
        self.canvas.create_line(0, self.height-1, self.width, self.height-1)
        self.canvas.create_line(0, 0, 0, self.height)
        # Label
        if self.label:
            self.canvas.create_text(6, 10, anchor="w", text=self.label, font=("Segoe UI", 9, "bold"))

    def _map_y(self, value):
        # Map value to canvas Y (0 at top)
        if self.y_max == self.y_min:
            return self.height // 2
        ratio = (value - self.y_min) / (self.y_max - self.y_min)
        y = self.height - int(ratio * self.height)
        return max(0, min(self.height-1, y))

    def push(self, value):
        # Insert value at current x, scroll in-place
        y = self._map_y(value)
        self.buffer[self.x] = y
        # Clear a 1px strip at x, redraw column segment
        self.canvas.create_line(self.x, 0, self.x, self.height, fill="white")
        # Draw from previous point (x-1) to x
        prev_x = (self.x - 1) % self.width
        y_prev = self.buffer[prev_x]
        if y_prev is not None:
            self.canvas.create_line(prev_x, y_prev, self.x, y, fill="black")
        # Advance x
        self.x = (self.x + 1) % self.width
        if self.x == 0:
            # clear and redraw axes when wrapping
            self._draw_axes()


class VentilatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Educational Ventilator (Simulation Only)")
        self.geometry("1050x680")
        self.resizable(False, False)

        # Styles
        style = ttk.Style(self)
        try:
            self.tk.call("source", "azure.tcl")
            style.theme_use("azure")
        except Exception:
            # Fallback to default theme
            pass

        # Ventilator & lung
        self.lung = LungModel()
        self.vent = VentilatorSim(self.lung)

        # Build UI
        self._build_controls()
        self._build_waveforms()
        self._build_status()

        # Loop
        self.dt = 0.02  # 20 ms
        self.sim_after = None
        self.running = False

    def _build_controls(self):
        frm = ttk.Frame(self, padding=8)
        frm.place(x=10, y=10, width=360, height=660)

        ttk.Label(frm, text="Mode").grid(row=0, column=0, sticky="w")
        self.mode_var = tk.StringVar(value=self.vent.mode)
        mode_cmb = ttk.Combobox(frm, textvariable=self.mode_var, values=[VentilatorSim.MODE_VCV, VentilatorSim.MODE_PCV], state="readonly", width=12)
        mode_cmb.grid(row=0, column=1, sticky="ew", pady=2)
        mode_cmb.bind("<<ComboboxSelected>>", self.on_mode_change)

        row = 1
        def add_scale(label, from_, to, init, cmd, fmt="%d"):
            nonlocal row
            ttk.Label(frm, text=label).grid(row=row, column=0, sticky="w")
            var = tk.DoubleVar(value=init)
            sc = ttk.Scale(frm, from_=from_, to=to, orient="horizontal", variable=var, command=lambda val, fn=cmd, v=var: fn(v.get()))
            sc.grid(row=row, column=1, sticky="ew", pady=2)
            val_lbl = ttk.Label(frm, text=fmt % init, width=7)
            val_lbl.grid(row=row, column=2, sticky="w")
            def update_label(val, fmt=fmt, lbl=val_lbl):
                try:
                    lbl.config(text=fmt % float(val))
                except Exception:
                    pass
            sc.configure(command=lambda val, u=update_label, fn=cmd, v=var: (u(val), fn(v.get())))
            row += 1
            return var

        frm.grid_columnconfigure(1, weight=1)

        self.rr_var   = add_scale("RR (bpm)",   4, 40, self.vent.RR_bpm, self.on_rr_change)
        self.ie_var   = add_scale("I:E (1:x)",  0.5, 4.0, self.vent.ie_ratio, self.on_ie_change, fmt="%.1f")
        self.fio2_var = add_scale("FiO2 (%)",   21, 100, self.vent.fiO2, self.on_fio2_change)
        self.vt_var   = add_scale("VT (mL)",    150, 800, self.vent.target_VT_ml, self.on_vt_change)
        self.pinsp_var= add_scale("Pinsp (cmH2O)", 5, 35, self.vent.pinsp_cmH2O, self.on_pinsp_change)
        self.peep_var = add_scale("PEEP (cmH2O)", 0, 20, self.vent.peep_cmH2O, self.on_peep_change)
        self.flow_var = add_scale("Flow limit (L/min)", 10, 120, self.vent.flow_limit_Lpm, self.on_flow_change)

        ttk.Separator(frm).grid(row=row, column=0, columnspan=3, sticky="ew", pady=6)
        row += 1

        ttk.Label(frm, text="Lung Compliance (mL/cmH2O)").grid(row=row, column=0, sticky="w")
        self.c_var = tk.DoubleVar(value=self.lung.C)
        c_sc = ttk.Scale(frm, from_=10, to=100, orient="horizontal", variable=self.c_var, command=lambda val: self.on_compliance_change(self.c_var.get()))
        c_sc.grid(row=row, column=1, sticky="ew", pady=2)
        ttk.Label(frm, textvariable=tk.StringVar(value=f"{self.lung.C:.0f}"), width=7)\
            .grid(row=row, column=2, sticky="w")
        def _c_update(val):
            self.on_compliance_change(self.c_var.get())
        c_sc.configure(command=lambda val: _c_update(val))
        row += 1

        ttk.Label(frm, text="Airway Resistance (cmH2O·s/L)").grid(row=row, column=0, sticky="w")
        self.r_var = tk.DoubleVar(value=self.lung.R)
        r_sc = ttk.Scale(frm, from_=2, to=20, orient="horizontal", variable=self.r_var, command=lambda val: self.on_resistance_change(self.r_var.get()))
        r_sc.grid(row=row, column=1, sticky="ew", pady=2)
        ttk.Label(frm, textvariable=tk.StringVar(value=f"{self.lung.R:.0f}"), width=7)\
            .grid(row=row, column=2, sticky="w")
        def _r_update(val):
            self.on_resistance_change(self.r_var.get())
        r_sc.configure(command=lambda val: _r_update(val))
        row += 1

        ttk.Separator(frm).grid(row=row, column=0, columnspan=3, sticky="ew", pady=6)
        row += 1

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=row, column=0, columnspan=3, sticky="ew")
        start_btn = ttk.Button(btn_frame, text="Start", command=self.start_sim)
        stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_sim)
        reset_btn = ttk.Button(btn_frame, text="Reset", command=self.reset_sim)
        start_btn.pack(side="left", expand=True, fill="x", padx=2)
        stop_btn.pack(side="left", expand=True, fill="x", padx=2)
        reset_btn.pack(side="left", expand=True, fill="x", padx=2)

    def _build_waveforms(self):
        frm = ttk.Frame(self, padding=8)
        frm.place(x=380, y=10, width=660, height=440)

        self.canvas_pressure = tk.Canvas(frm, width=620, height=200, bg="white", highlightthickness=1, highlightbackground="#ccc")
        self.canvas_flow     = tk.Canvas(frm, width=620, height=200, bg="white", highlightthickness=1, highlightbackground="#ccc")
        self.canvas_pressure.grid(row=0, column=0, padx=4, pady=4)
        self.canvas_flow.grid(row=1, column=0, padx=4, pady=4)

        self.wf_pressure = Waveform(self.canvas_pressure, y_min=0, y_max=50, label="Pressure (cmH2O)")
        self.wf_flow     = Waveform(self.canvas_flow, y_min=-1.5, y_max=1.5, label="Flow (L/s)")

    def _build_status(self):
        frm = ttk.Frame(self, padding=8)
        frm.place(x=380, y=460, width=660, height=210)

        info = ttk.Frame(frm)
        info.pack(fill="x", pady=4)

        self.lab_mode = ttk.Label(info, text="Mode: VCV")
        self.lab_rr = ttk.Label(info, text="RR: 14 bpm")
        self.lab_ie = ttk.Label(info, text="I:E: 1:2.0")
        self.lab_fio2 = ttk.Label(info, text="FiO2: 40%")
        self.lab_peep = ttk.Label(info, text="PEEP: 5 cmH2O")
        self.lab_vt = ttk.Label(info, text="VT: 0 mL (measured)")

        for w in (self.lab_mode, self.lab_rr, self.lab_ie, self.lab_fio2, self.lab_peep, self.lab_vt):
            w.pack(side="left", padx=8)

        ttk.Separator(frm).pack(fill="x", pady=6)

        alarm_frame = ttk.LabelFrame(frm, text="Alarms")
        alarm_frame.pack(fill="x", pady=4)
        self.alarm_hp = ttk.Label(alarm_frame, text="High Pressure", foreground="gray")
        self.alarm_lv = ttk.Label(alarm_frame, text="Low Tidal Volume", foreground="gray")
        self.alarm_ap = ttk.Label(alarm_frame, text="Apnea", foreground="gray")
        self.alarm_hp.pack(side="left", padx=8)
        self.alarm_lv.pack(side="left", padx=8)
        self.alarm_ap.pack(side="left", padx=8)

        msg = ttk.Label(frm, text="DISCLAIMER: Simulasi edukasi saja. BUKAN untuk penggunaan medis nyata.", foreground="#a00")
        msg.pack(pady=8)

    # ---------------- Event handlers ----------------

    def on_mode_change(self, _evt=None):
        mode = self.mode_var.get()
        self.vent.set_mode(mode)
        self.lab_mode.config(text=f"Mode: {mode}")

    def on_rr_change(self, val):
        self.vent.set_rr(val)
        self.lab_rr.config(text=f"RR: {self.vent.RR_bpm} bpm")
        self.lab_ie.config(text=f"I:E: 1:{self.vent.ie_ratio:.1f}")

    def on_ie_change(self, val):
        self.vent.set_ie(val)
        self.lab_ie.config(text=f"I:E: 1:{self.vent.ie_ratio:.1f}")

    def on_fio2_change(self, val):
        self.vent.set_fio2(val)
        self.lab_fio2.config(text=f"FiO2: {self.vent.fiO2}%")

    def on_vt_change(self, val):
        self.vent.set_vt(val)

    def on_pinsp_change(self, val):
        self.vent.set_pinsp(val)

    def on_peep_change(self, val):
        self.vent.set_peep(val)
        self.lab_peep.config(text=f"PEEP: {self.vent.peep_cmH2O} cmH2O")

    def on_flow_change(self, val):
        self.vent.set_flow_limit(val)

    def on_compliance_change(self, val):
        self.lung.C = max(10.0, float(val))

    def on_resistance_change(self, val):
        self.lung.R = max(0.5, float(val))

    # ---------------- Simulation control ----------------

    def start_sim(self):
        if not self.running:
            self.running = True
            self.vent.start()
            self._tick()

    def stop_sim(self):
        self.running = False
        if self.sim_after is not None:
            self.after_cancel(self.sim_after)
            self.sim_after = None

    def reset_sim(self):
        self.stop_sim()
        self.lung = LungModel(compliance_ml_per_cmH2O=self.lung.C, resistance_cmH2O_s_per_L=self.lung.R, peep_cmH2O=self.vent.peep_cmH2O)
        self.vent = VentilatorSim(self.lung)
        self.mode_var.set(self.vent.mode)
        self.lab_mode.config(text=f"Mode: {self.vent.mode}")
        self.lab_rr.config(text=f"RR: {self.vent.RR_bpm} bpm")
        self.lab_ie.config(text=f"I:E: 1:{self.vent.ie_ratio:.1f}")
        self.lab_fio2.config(text=f"FiO2: {self.vent.fiO2}%")
        self.lab_peep.config(text=f"PEEP: {self.vent.peep_cmH2O} cmH2O")
        self.lab_vt.config(text=f"VT: 0 mL (measured)")
        self.wf_pressure._draw_axes()
        self.wf_flow._draw_axes()

    # ---------------- Main loop ----------------

    def _tick(self):
        if not self.running:
            return
        # Fixed time-step simulation
        pressure, flow_Lps, volume_ml, phase_changed = self.vent.step(self.dt)

        # Update waveforms
        self.wf_pressure.push(pressure)
        self.wf_flow.push(flow_Lps)

        # Update measured VT display (update at end of inspiration or periodically)
        if phase_changed or self.vent.inspiratory():
            self.lab_vt.config(text=f"VT: {self.vent.measured_VT_ml:.0f} mL (measured)")

        # Update alarms
        self._update_alarms()

        # Schedule next tick
        self.sim_after = self.after(int(self.dt * 1000), self._tick)

    def _update_alarms(self):
        def set_alarm(lbl, active):
            lbl.config(foreground=("red" if active else "gray"))

        set_alarm(self.alarm_hp, self.vent.alarm_high_pressure)
        set_alarm(self.alarm_lv, self.vent.alarm_low_vt)
        set_alarm(self.alarm_ap, self.vent.alarm_apnea)

    # -----------------

def main():
    app = VentilatorGUI()
    def on_close():
        if app.running:
            if messagebox.askokcancel("Quit", "Stop simulation and quit?"):
                app.stop_sim()
                app.destroy()
        else:
            app.destroy()
    app.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()

if __name__ == "__main__":
    main()

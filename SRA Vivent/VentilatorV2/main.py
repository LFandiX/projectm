import math
import random
import cv2
from layout import main
def breathing_wave(t):
    # Complete breathing cycle: 240 frames (longer for smoother transitions)
    cycle = t % 240
    
    # Define lung capacity levels
    functional_residual = 350      # FRC baseline
    tidal_amplitude = 25          # Normal breathing amplitude
    inspiratory_capacity = 250    # Maximum inspiration
    expiratory_reserve = 420      # Below FRC during forced expiration
    
    if cycle < 50:
        # First normal tidal breathing cycle
        wave_progress = (cycle / 50) * 2 * math.pi
        small_wave = tidal_amplitude * math.sin(wave_progress)
        return int(functional_residual - small_wave)
    
    elif cycle < 100:
        # Second normal tidal breathing cycle
        wave_progress = ((cycle - 50) / 50) * 2 * math.pi
        small_wave = tidal_amplitude * math.sin(wave_progress)
        return int(functional_residual - small_wave)
    
    elif cycle < 140:
        # Smooth transition to deep inspiration
        progress = (cycle - 100) / 40.0
        # Start from end of small wave and smoothly rise
        start_y = functional_residual + tidal_amplitude
        target_y = inspiratory_capacity
        smooth_curve = start_y + (target_y - start_y) * (0.5 * (1 - math.cos(progress * math.pi)))
        return int(smooth_curve)
    
    elif cycle < 180:
        # Deep expiration - smooth drop to expiratory reserve
        progress = (cycle - 140) / 40.0
        start_y = inspiratory_capacity
        target_y = expiratory_reserve
        smooth_curve = start_y + (target_y - start_y) * (0.5 * (1 - math.cos(progress * math.pi)))
        return int(smooth_curve)
    
    else:
        # Smooth return to FRC baseline
        progress = (cycle - 180) / 60.0
        start_y = expiratory_reserve
        target_y = functional_residual
        smooth_return = start_y + (target_y - start_y) * (0.5 * (1 - math.cos(progress * math.pi)))
        return int(smooth_return)
graph_points = [(x,400) for x in range(330,970,10)]
t = 0
temp = 22.0
ie_modes = ["1:2","1:3","1:4"]
ie_idx = 0
cv2.namedWindow("Ventilator GUI V2")

while True:
    # if running:
        # update params dinamis
        Pin_val  = 20 + 5*math.sin(t/20)
        Pexp_val = 5 + 2*math.cos(t/25)
        RR_val   = 18 + random.randint(-2,2)
        Temp_val = temp + 0.01*math.sin(t/100)  # lambat berubah
        IE_val   = ie_modes[ie_idx//100 % len(ie_modes)]

        params = [
        ("Pin",  f"{Pin_val:.2f}"),
        ("Pexp", f"{Pexp_val:.2f}"),
        ("I:E",  IE_val),   
        ("RR",   f"{RR_val:.2f}"),
        ("Temp", f"{Temp_val:.2f}")
    ]

        values = [f"{Pin_val:.0f}", f"{Pexp_val:.0f}", IE_val, f"{RR_val}"]

        # Geser grafik
        graph_points = [(x-5, y) for (x,y) in graph_points if x-5 > 330]
        new_x = 970
        # new_y = 300 + int(100*math.sin(t/15))  # gelombang sinus
        new_y = breathing_wave(t)
        graph_points.append((new_x,new_y))
        t += 1

        img = main(params, values, graph_points)
        cv2.imshow("Ventilator GUI V2", img)

        if cv2.waitKey(50) & 0xFF == 27:  # ESC keluar
            break

cv2.destroyAllWindows()
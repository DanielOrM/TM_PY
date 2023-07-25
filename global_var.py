import ctypes

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)   # 1920 pour mon pc
screen_height = user32.GetSystemMetrics(1)  # 1080 pour mon pc

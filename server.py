from flask import Flask
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuration for LED state and text window
on_time_start = datetime.strptime("07:00", "%H:%M").time()  # LED on start time
on_time_end = datetime.strptime("22:30", "%H:%M").time()    # LED on end time
window_start = datetime.strptime("08:00", "%H:%M").time()   # Text window start time
window_end = datetime.strptime("20:00", "%H:%M").time()     # Text window end time



def is_within_time_range(current, start, end):
    """Check if current time is within the specified time range."""
    current_time = current.time()
    return start <= current_time <= end

def calculate_brightness(current_time, start_time, end_time):
    """Calculate the brightness based on the current time within the interval."""
    if current_time < start_time:
        return 0.1
    elif current_time > end_time:
        return 1
    else:
        total_duration = (datetime.combine(datetime.today(), end_time) - 
                          datetime.combine(datetime.today(), start_time)).total_seconds()
        elapsed_duration = (datetime.combine(datetime.today(), current_time) - 
                            datetime.combine(datetime.today(), start_time)).total_seconds()
        # Linear interpolation between 0.1 and 1
        return 0.1 + (elapsed_duration / total_duration) * (1 - 0.1)
    

@app.route('/text')
def time_since():
    """Returns the minutes since a specific start time or the current time if out of window."""
    now = datetime.now()

    if is_within_time_range(now, window_start, window_end):
        # Start date and time for calculating minutes since
        start_time = datetime(2000, 5, 16, hour=8, minute=15)
        diff_minutes = (now - start_time).total_seconds() // 60
        text = str(int(diff_minutes))
    else:
        text = now.strftime("%-H:%M%p").lower()

    return text

@app.route('/control', methods=['GET'])
def control_led_matrix():
    """Controls the LED matrix based on the current time."""
    now = datetime.now()
    led_on = is_within_time_range(now, on_time_start, on_time_end)
    brightness = calculate_brightness(now.time(), on_time_start, window_start) if led_on else 0.1
    on_brightness_value = f"{'1' if led_on else '0'}-{brightness:.2f}"  # Format: "on-{brightness}"
    control = {"on-brightness": on_brightness_value}
    return control

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

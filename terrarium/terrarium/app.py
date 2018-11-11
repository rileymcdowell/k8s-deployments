#!/usr/bin/env python3
import time
import yaml
import datetime
import logging
import six
from flask import Flask
from ouimeaux.environment import Environment

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

time.sleep(10) # Wait for redis container to start.

# Logging stuff
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Globals
WEMO_DEVICES = {}
CONFIG = None

# Read configuration stuff
with open('./config.yaml', 'rb') as f:
    CONFIG = yaml.load(f)

# The Wemo stuff
def found_device(device):
    print('Found WEMO device {}'.format(device))
    # Wemo environment device name is the "code" name
    WEMO_DEVICES[device.name] = device

def refresh_wemo_devices():
    global WEMO_DEVICES
    WEMO_DEVICES = {}
    try:
        env = Environment(found_device, config_filename='./wemo-config.yaml')
        env.start()
        env.discover(seconds=5)
    except Exception as e:
        import traceback
        logger.error(traceback.format_exc())

refresh_wemo_devices()

def reset_wemo_devices():
    for device_name, state in six.iteritems(CONFIG['default-state']):
        device_code = CONFIG['device_to_code'][device_name]
        if not device_code in WEMO_DEVICES:
            logger.warn('Wemo Device {}/{} not found'.format(device_name, device_code))
            logger.warn('Cannot set default state of {}'.format(state))
            continue
        if state is True:
            WEMO_DEVICES[device_code].on()
        elif state is False:
            WEMO_DEVICES[device_code].off()
        else:
            raise NotImplementedError("Unknown Device State {}".format(state))

reset_wemo_devices()

# The apscheduler stuff
def fan_n_fog():
    logger.info('Triggered fan and fog')
    WEMO_DEVICES[CONFIG['device_to_code']['fan']].on()
    time.sleep(CONFIG['fan_n_fog']['fan_time'])
    WEMO_DEVICES[CONFIG['device_to_code']['fan']].off()
    time.sleep(CONFIG['fan_n_fog']['wait_time'])
    WEMO_DEVICES[CONFIG['device_to_code']['fogger']].on()
    time.sleep(CONFIG['fan_n_fog']['fog_time'])
    WEMO_DEVICES[CONFIG['device_to_code']['fogger']].off()

try:
    scheduler = BackgroundScheduler(CONFIG['apscheduler-config'])
    # TODO: switch to hourly.
    scheduler.add_job(fan_n_fog, trigger='cron', hour="*", minute=1)
    scheduler.add_job(refresh_wemo_devices, trigger='cron', hour="*", minute=0)
    scheduler.start()
except Exception as e:
    import traceback
    logger.error(traceback.format_exc())

logger.info("Creating Flask App")

# The flask app stuff
app = Flask(__name__)

@app.route('/')
def ping():

    device_codes = [d for d in WEMO_DEVICES]
    html_items = '\n'.join(['<li>Wemo Device "{}"</li>'.format(i) for i in device_codes])
    now = datetime.datetime.now().strftime('%I:%M %p %Z')

    HTML = """
    <body>
    <h3>Welcome to the terrarium controller</h3>
    <hl>
    <h4>Current time is {}</h4>
    <hl>
    <h5>Currently Discovered Devices (refreshed hourly)</h5>
    <ol>{}</ol>
    <ul>
    <li><h5><a href="/lightsoff/1">Lights off for one minute</a></h5></li>
    <li><h5><a href="/lightsoff/30">Lights off for half hour</a></h5></li>
    <li><h5><a href="/lightsoff/60">Lights off for one hour</a></h5></li>
    <li><h5><a href="/lightsoff/120">Lights off for two hours</a></h5></li>
    <li><h5><a href="/lightsoff/240">Lights off for four hours</a></h5></li>
    </ul>
    Brought to you by Docker and Kubernetes!
    </body>
    """.format(now, html_items)
    return HTML

def light_back_on():
    light_code = CONFIG['device_to_code']['light']
    if light_code in WEMO_DEVICES:
        WEMO_DEVICES[light_code].on()
    else:
        five_minutes_later = datetime.datetime.now() + datetime.timedelta(minutes=5)
        msg = "Light {} not found. Rescheduling for {}"
        logger.warning(msg.format(light_code, five_minutes_later))
        scheduler.add_job(light_back_on, trigger=DateTrigger(run_date=five_minutes_later))

@app.route('/lightsoff/<int:minutes>')
def lightsout(minutes):
    logger.info('Lights out! {} minutes'.format(minutes))
    light_code = CONFIG['device_to_code']['light']
    if light_code in WEMO_DEVICES:
        WEMO_DEVICES[light_code].off()

    back_on_date = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    scheduler.add_job(light_back_on, trigger=DateTrigger(run_date=back_on_date))

    HTML = """
    <h3>Your will be done</h3>
    <h4>Lights back on at {}</h4>
    <h5>Returning to main page in 5 seconds</h5>
    <script>setTimeout("location.href = '/';", 5000)</script>
    """.format(back_on_date.strftime("%I:%M %p %Z"))
    return HTML


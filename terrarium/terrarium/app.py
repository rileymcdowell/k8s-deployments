#!/usr/bin/env python3
import time
import yaml
import datetime
import logging
import six
import traceback

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
        env = Environment(found_device, with_subscribers=False, config_filename='./wemo-config.yaml')
        env.start()
        env.discover(seconds=5)
    except Exception as e:
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
    """
    A surprisingly complex function because of the number of possible
    error conditions when turning on a light.
    """
    light_code = CONFIG['device_to_code']['light']
    light_exists = light_code in WEMO_DEVICES

    # Guess-and-check pattern for if this worked.
    worked = True
    error = None

    try:
        # If the light exists, turn it on and make sure it stays that way.
        if light_exists:
            WEMO_DEVICES[light_code].on()
            time.sleep(CONFIG['light_toggle']['wait_time'])
            if WEMO_DEVICES[light_code].get_state(force_update=True) == False:
                error = "Light {} didn't obtain the 'on' state".format(light_code)
                worked = False
        # If the light doesn't exist, record that too.
        else:
            error = "Light {} not found".format(light_code)
            worked = False
    except:
        # Any kind of error in this process should trigger a retry.
        logger.error(traceback.format_exc())
        error = "Error during turning on light"
        worked = False

    # Handle the failure if needed
    if not worked:
        fail_wait_time = CONFIG['light_toggle']['fail_wait_time']
        retry_time = datetime.datetime.now() + datetime.timedelta(minutes=fail_wait_time)
        msg = "{}. Rescheduling for {}".format(error, retry_time)
        logger.warning(msg)
        scheduler.add_job(light_back_on, trigger=DateTrigger(run_date=retry_time))

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


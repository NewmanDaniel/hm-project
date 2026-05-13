# IoT Payload Parser - Django Project

A simple Django Rest Framework application to ingest and parse IoT payloads.

## Setup Instructions

1.  **Create Virtual Environment & Install Dependencies:**
    ```bash
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
    
2. **Copy settings.py.example to settings.py**
    ``` bash
    cp hmproject/hmproject/settings.py.example  hmproject/hmproject/settings.py
    ```

2.  **Apply Migrations:**
    ```bash
    cd hmproject
    python manage.py migrate
    ```

3.  **Create Admin User:**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create a user.

4.  **Generate Authentication Token:**
    ```bash
    python manage.py drf_create_token <username_you_just_created>
    ```
    **Copy this token.** You will need it for the API requests.

5.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```

## Testing the API

Open a new terminal window to run the test scripts.

Ensure the server is running on `http://127.0.0.1:8000`.

### 1. Send a Passing Status (Data: AQ== -> 01)
``` bash
scripts/send_payload.sh <YOUR_TOKEN> device_abc 1 pass
```

### 2. Send a Failing Status(Data: AA== -> 00)
``` bash
scripts/send_payload.sh <YOUR_TOKEN> device_abc 2 fail
```

### 3. Test Duplicate Rejection (fCnt Failure)
``` bash
scripts/test_duplicate.sh <YOUR_TOKEN> device_xyz
```

### 4. Check Device Statuses
``` bash
scripts/get_devices.sh <YOUR_TOKEN>
```

## Sample Run

``` text
# Below is 
(venv) user@machine:~/repos/hexmodal-project$ scripts/send_payload.sh eb558283e0235ce70bf4834f92594062c566dfb5 device_abc 1 pass
Sending Payload: Device=device_abc, fCnt=1, Status=pass
curl: (7) Failed to connect to 127.0.0.1 port 8000 after 0 ms: Connection refused


(venv) user@machine:~/repos/hexmodal-project$ scripts/send_payload.sh eb558283e0235ce70bf4834f92594062c566dfb5 device_abc 1 pass
Sending Payload: Device=device_abc, fCnt=1, Status=pass
{"status":"success"}

(venv) user@machine:~/repos/hexmodal-project$ scripts/send_payload.sh eb558283e0235ce70bf4834f92594062c566dfb5 device_abc 1 pass # test fCnt
Sending Payload: Device=device_abc, fCnt=1, Status=pass
{"non_field_errors":["Duplicate fCnt for this device."]}

(venv) user@machine:~/repos/hexmodal-project$ scripts/send_payload.sh eb558283e0235ce70bf4834f92594062c566dfb5 device_abc 2 fail
Sending Payload: Device=device_abc, fCnt=2, Status=fail
{"status":"success"}

(venv) user@machine:~/repos/hexmodal-project$ scripts/send_payload.sh eb558283e0235ce70bf4834f92594062c566dfb5 device_def 3 pass
Sending Payload: Device=device_def, fCnt=3, Status=pass
{"status":"success"}

(venv) user@machine:~/repos/hexmodal-project$ scripts/send_payload.sh eb558283e0235ce70bf4834f92594062c566dfb5 device_xyz 4 fail
Sending Payload: Device=device_xyz, fCnt=4, Status=fail
{"status":"success"}

(venv) user@machine:~/repos/hexmodal-project$ scripts
scripts
(venv) user@machine:~/repos/hexmodal-project$ scripts
scripts
(venv) user@machine:~/repos/hexmodal-project$ scripts/get_devices.sh eb558283e0235ce70bf4834f92594062c566dfb5
Fetching Device Statuses...
[{"devEUI":"device_abc","name":"Device device_abc","latest_status":"Failing"},{"devEUI":"device_def","name":"Device device_def","latest_status":"Passing"},{"devEUI":"device_xyz","name":"Device device_xyz","latest_status":"Failing"}]

# Check DB via ORM
(venv) user@machine:~/repos/hexmodal-project/hmproject$ python manage.py shell
10 objects imported automatically (use -v 2 for details).

Python 3.10.12 (main, Mar  3 2026, 11:56:32) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from hmapp.models import *
>>> Payload.objects.all()
<QuerySet [<Payload: Payload 1 from device_abc>, <Payload: Payload 2 from device_abc>, <Payload: Payload 3 from device_def>, <Payload: Payload 4 from device_xyz>]>
>>> Device.objects.all()
<QuerySet [<Device: device_abc>, <Device: device_def>, <Device: device_xyz>]>


```

# Onboard Scripts

Basic script to be run on quad for semi-autonomous flight.

### Setup

Run ```bash env_setup.sh```

If you face some errors , open the file using text editor and type commands one by one in terminal.

Dependencies: mav-proxy, drone-kit, tower-web

### Connect the servers

Once the environment is setup.

Run Simulator: ```dronekit-sitl copter --home=22.33024,87.32371,584,353```

For running on simulator Mav Proxy: ```mavproxy.py --master=tcp:127.0.0.1:5760 --out=udpout:127.0.0.1:14550 --out=udpout:127.0.0.1:14549```

For running on quad Mav Proxy: ```mavproxy.py --master=/dev/serial/by-id/<id> --baudrate 115200 --out=udpout:127.0.0.1:14550 --out=udpout:127.0.0.1:14549```

To view quad on simulator ```tower udpin:127.0.0.1:14550```  then open browser and open ```localhost::14550```

### Going to a point

#### NOTE: Hardcoded GPS Points

Makes quad go to pre-defined set of GPS points and height.
Once mavproxy is running 

Run ```python goToPointGPS.py --connect '127.0.0.1:14550'```

### Drop test

Quad must be connected with a servo on arduino. Quad will rotate the servo once the point and specified height is reached.

Run ```python GPSDrop.py --connect '127.0.0.1:14550'```

### Quad Map Control

Quad will follow the GPS point given to it using the [Quad Map](https://github.com/ash-anand/QuadMap-android) android app.
Once mavproxy is running 

Run ```python QuadMapGPS.py --connect '127.0.0.1:14550'```
Then use to app to connect to the IP at specified port. ( 8000 by default )

Script has 2 modes of operation 
* Mode A : Guides quad to single given point.
* Mode B : Makes Quad follow a set of GPS co-ordinates sent from app.

Script also sends current Quad location to the app using threads.


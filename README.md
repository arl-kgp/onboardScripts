#Onboard Scripts

Dependencies: mav-proxy, drone-kit, tower-web

1. GPS navigation from Points hardcoded 

Run Simulator: ```dronekit-sitl copter --home=22.33024,87.32371,584,353```

Mav Proxy: ```mavproxy.py --master=tcp:127.0.0.1:5760 --out=udpout:127.0.0.1:14550 --out=udpout:127.0.0.1:14549```

or Mav Proxy: ```mavproxy.py --master=/dev/serial/by-id/<id> --baudrate 115200 --out=udpout:127.0.0.1:14550 --out=udpout:127.0.0.1:14549```

Tower: ```tower udpin:127.0.0.1:14550```

Go To Point: ```python goToPointGPS.py --connect '127.0.0.1:14550'```




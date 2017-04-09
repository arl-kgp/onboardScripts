#Onboard Scripts

Run ```bash env_setup.sh```

If you face some errors , open the file using text editor and type commands one by one in terminal.

Dependencies: mav-proxy, drone-kit, tower-web

NOTE: GPS navigation from Points hardcoded 

Once the environment is setup.
Run Simulator: ```dronekit-sitl copter --home=22.33024,87.32371,584,353```

For running on simulator Mav Proxy: ```mavproxy.py --master=tcp:127.0.0.1:5760 --out=udpout:127.0.0.1:14550 --out=udpout:127.0.0.1:14549```

For running on quad Mav Proxy: ```mavproxy.py --master=/dev/serial/by-id/<id> --baudrate 115200 --out=udpout:127.0.0.1:14550 --out=udpout:127.0.0.1:14549```

To view quad on simulator ```tower udpin:127.0.0.1:14550```  then open browser and open ```localhost::14550```

Go To Point: ```python goToPointGPS.py --connect '127.0.0.1:14550'```




# VNA DRIVER

This is a simple VNA driver

## how to use

 Creat VNA object
``` 
vna = vna_driver()
```

Connect VNA

```
vna.connect("COM8")
```

Configurate sweep
```
vna.cfg_sweep(start = 3e9, stop = 6e9, points = 201, n_mean = 5)
```

Calibrate / load calibration
```
vna.calibrate()
vna.save_calib()
```

```
vna.load_calib("path_to_calib")
```

Measure

```
vna.measure()
```

Extract values

```
freq1, s11_real, s11_imaginary = vna.extract_s11()

freq2,s11_mag = vna.extract_s11_mag() 
```

> Look documentation to see all values available

Close connection 
```
vna.close()
```

> ATTENTION: Always close connection to prevent bugs!

## read_s1p
consegue ler comentários, opções e dados
limitações:
- se linha de dados não começar com número, a linha não vai ser lida
- apenas uma linha de opções (#) permitida
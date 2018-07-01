# Piton2000

**Special equipment is required to run these scripts, see the Setup section for more info.**

Piton 2000 is a service that can connect to the Dutch P2000 network to monitor the messages send by alarm centers to the Fire Departments, Police stations, Ambulance services or the KNRM(Royal Dutch Coast Guard).  
Build with Python 3.6.5

## Examples
This section features some small examples on how to use or extend these scripts.

#### Custom Reader
```Python
import rtlsdr


class MyReader(rtlsdr.AbstractReader):

    def act(self, raw):
        line = self.create_line(raw)
        if self.is_line_blacklisted(line):
            print("== LINE IS BLACKLISTED ==")
        else:
            print(str(line))


connection = rtlsdr.Connection()
reader = MyReader()
reader.attach(connection)
```

#### Fetching Capcodes
```Python
from tomzulu import Scraper, Region

scraper = Scraper(Region.FRIESLAND)
landing = scraper.get_landing_page()
links = scraper.get_discipline_links(landing)
units = scraper.get_units()

for discipline in units:
    print("{0} Size = {1}".format(discipline[0].discipline, len(discipline)))
```

## Setup
**I am using Ubuntu 18.04 for this setup, i haven't tested any other Linux versions!!!**

It is only possible to use this service if you have a certain USB radio + antenna.  
- For the Dutch readers, [you can get it from  Bol.com][1].  
- For the international readers, [you can get it from  HackerWarehouse][2].  

Or you could get it anywhere else, as long as it has the `RTL2832U` chipset and a `R820T` tuner, this makes it possible to function as a generic radio.  

To actually get some input from the device we need to jump through some hoops, follow my lead.  

- Install the required libraries:
```console
$ sudo apt-get -y install cmake build-essential libusb-1.0 qt4-qmake libpulse-dev libx11-dev qt4-default
```
- Clone the [rtl-sdr repo][3]
```console
$ git clone https://github.com/osmocom/rtl-sdr.git
```

- Install the rtl-sdr package.
```console
cd rtl-sdr/
mkdir build
cd build
cmake ../ -DINSTALL_UDEV_RULES=ON
make
sudo make install
sudo ldconfig
```

- Blacklist drivers  
Some people are reporting problems with conflicting drivers, so you might want to do this as a precaution.  
```console
$ sudo nano /etc/modprobe.d/blacklist.conf
```
Add the following lines:
```console
blacklist dvb_usb_rtl28xxu
blacklist rtl2832
blacklist rtl2830
```
Now reboot for the changes to take effect:
```console
$ sudo reboot -h 0
```

- Test rtl-sdr  
Run the `rtl_test` command, your output should look something like this:  
`Found X device(s):`, where X is the amount of devices found.
![rtl_test output][4]


Now we can communicate with the antenna, but now we need to listen to the P2000 service.  
According to [wikipedia][5] P2000 is a FLEX protocol that broadcasts on the `169,650 Mhz` band.  
Conclusion, we need some software that can decode the FLEX protocol, for this we use Multimon-NG.  

- Clone the [Multimo-NG repo][6]
```console
$ git clone https://github.com/EliasOenal/multimon-ng
```

- Prepare the build
```console
cd multimon-ng
mkdir build
cd build
```
- Multimong-NG can be build with either Cmake or Qmake, in my case i used Cmake.

  - Cmake
    ```console
    cmake ..
    make
    sudo make install
    ```
  - Qmake
    ```console
    qmake ../multimon-ng.pro
    make
    sudo make install
    ```

Now we are ready to test the device, if you have a stick with a `R820T` tuner use this command with optimized ppm(-p) and gain(-g) settings. The API itself relies on the `R820T` tuner.
```console
$ rtl_fm -f 169.65M -M fm -s 22050 -p 83 -g 30 | multimon-ng -a FLEX -t raw /dev/stdin
```
Else, use this.
```console
$ rtl_fm -f 169.65M -M fm -s 22050 | multimon-ng -a FLEX -t raw /dev/stdin
```

If all went well your output should look something like this:  
![P2000 output 1][7]  

It shouldn't take long for alarms to appear:  
![P2000 output 2][8]

And that's it!






[1]: https://www.bol.com/nl/p/mini-usb-2-0-digitale-dvb-t-tv-stick-ondersteunt-fm-dab-820t2-sdr/9200000077112563/
[2]: https://hackerwarehouse.com/product/rtlsdr/
[3]: https://github.com/osmocom/rtl-sdr
[4]: https://i.imgur.com/CqHmhw3.png
[5]: https://nl.wikipedia.org/wiki/P2000_(netwerk)
[6]: https://github.com/EliasOenal/multimon-ng
[7]: https://i.imgur.com/H7WRYXj.png
[8]: https://i.imgur.com/mg5I2Be.png

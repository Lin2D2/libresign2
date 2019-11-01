# LibreOffice project "LibreSign2"

# Install(not working at the moment, but planned)

To install use pip (only Python 3 is supported)
```
pip install libresign
```
But you can instead use the setup.sh wich can be found abouve.

# Running(not working at the moment, but planned)

```
libresign [ --noinfo ] [ --libresign-home ]

--noinfo: Don't show the information screen.
--libresign-home: Specify the installation directory of libresign. (default: ~/.libresign)
```
But you can instead use the start.sh wich can be found abouve.

# Development


For development, beyond the obvious tools, the following setup is
recommended to run a local version of libresign (note that
irpjs-client is currently placed _inside_ impress-remote-js):

```
apt-get install virtualenv python3-xdo python3-tk
git clone https://github.com/Lin2D2/libresign2.git
git clone https://github.com/rptr/impress-remote-js.git
cd impress-remote-js
git clone https://github.com/rptr/irpjs-client.git
```

(not working at the moment, but planned)
After that, use the supplied debug.sh script to automatically set up and run the program after you've made your changes,

```
cd libresign
./debug.sh

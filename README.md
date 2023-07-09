# HbbTV Blocker

The following repository contains the code for the HbbTV Blocker presented at NDSS 2023 in scope of the paper "I Still Know What You Watched Last Sunday: Privacy of the HbbTV Protocol in the European Smart TV Landscape" (Available: <https://www.ndss-symposium.org/ndss-paper/i-still-know-what-you-watched-last-sunday-privacy-of-the-hbbtv-protocol-in-the-european-smart-tv-landscape/>).

### How to cite the paper:
```
@inproceedings{tagliaro:ndss23:hbbtv,
  title={{I Still Know What You Watched Last Sunday: Privacy of the HbbTV Protocol in the European Smart TV Landscape}},
  author={Tagliaro, Carlotta and Hahn, Florian and Sepe, Riccardo and Aceti, Alessio and Lindorfer, Martina},
  year={2023},
  booktitle={Proc. of the Network and Distributed System Security Symposium (NDSS)}
}
```

## How to run the tool
The tool is based on Django; We adopt Python > v3. Please install with:

```
$ python3 -m pip install Django
```
Then run:
```
$ sudo python3 manage.py runserver
```
And then navigate to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

#### NOTE:
Code is still under work in progress for clean-up and adaptation to new library versions. Some functionalities might be still broken, e.g., with older iptables versions it was possible to specify a domain pattern to block (removed in recent versions). If interested in more details or in the traffic PCAPs for the channels we analyzed, please contact us (contact information below).


### Contact Information:
Carlotta Tagliaro, TUWien (<carlotta@seclab.wien> or <carlotta.tagliaro@tuwien.ac.at>)

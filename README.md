# HbbTV Blocker

The following repository contains the code for the HbbTV Blocker presented at NDSS 2023 in scope of the paper "I Still Know What You Watched Last Sunday: Privacy of the HbbTV Protocol in the European Smart TV Landscape" (Available: <https://www.ndss-symposium.org/ndss-paper/i-still-know-what-you-watched-last-sunday-privacy-of-the-hbbtv-protocol-in-the-european-smart-tv-landscape/>).

### How to cite the paper:
```
@inproceedings{hbbtv:ndss2023,
  title     = {{I Still Know What You Watched Last Sunday: Security and Privacy of the HbbTV Protocol in the European Smart TV Landscape}},
  author    = {Tagliaro, Carlotta and Hahn, Florian and Sepe, Riccardo and Aceti, Alessio and Lindorfer, Martina},
  booktitle = {Proceedings of the 30th Network and Distributed System Security Symposium (NDSS)},
  location  = {San Diego, CA, USA},
  year      = {2023},
  doi       = {10.14722/ndss.2023.24102}
}
```

## LASER

We have further published a paper on the experimental aspects of our work at the Workshop on Learning from Authoritative Security Experiment Results (LASER), February 2023 (co-located with NDSS 2023). The pdf is available in this repository.

### How to cite the paper:
```
@inproceedings{hbbtv:laser2023,
  title     = {{Investigating HbbTV Privacy Invasiveness Across European Countries}},
  author    = {Tagliaro, Carlotta and Hahn, Florian and Sepe, Riccardo and Aceti, Alessio and Lindorfer, Martina},
  booktitle = {Proceedings of the Workshop on Learning from Authoritative Security Experiment Results (LASER)},
  location  = {San Diego, CA, USA},
  year      = {2023},
  doi       = {10.14722/laser-ndss.2023.24102}
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

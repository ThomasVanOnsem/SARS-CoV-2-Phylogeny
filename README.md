# SARS-CoV-2-Phylogeny

## Install

Muscle and FastTree command line tools need to be installed for multiple sequences alignment 
and phylogenetic tree construction.
```
sudo apt install muscle fasttree
```

Furthermore we need to setup a Python3 virtualenv with some packages installed to run the main code
```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Lastly we need a Python2 environment to install and use [Taxtastic](https://github.com/fhcrc/taxtastic), which is used
to create reference packages that are needed by pplacer, which does the fast placements.
The virtualenv needs to have the name 'taxit_venv', otherwise our code won't be able to run it.

```
virtualenv -p /usr/bin/python2.7 taxit_venv
source taxit_venv/bin/activate
pip install taxtastic
```


## Run

To run the site
```
python3 run.py
```


#### Troubleshooting

If making a placement result in an error such as 
```
loadlocale.c:129: _nl_intern_locale_data: Assertion `cnt < (sizeof (_nl_value_type_LC_TIME) / sizeof (_nl_value_type_LC_TIME[0]))' failed.
```

Open a shell and set the language locale
```
LANG=/usr/lib/locale/en_US
```
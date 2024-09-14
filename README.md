<h1 align="center">pomodoro-task-app.py</h1>
<p align="center">Pomodoro todo list app with an integrated internet blocker and timeboxing</p>

> [!IMPORTANT]
> pomodoro-task-app.py assumes that you aren't using a proxy server already since it runs a local proxy server to block the internet.

## Features

- **Cross Platform:** pomodoro-task-app.py is cross-platform and can be used on Windows, macOS and Linux.
- **Internet Blocker:** Internet can be blocked using either a blocklist or an allowlist.
- **Timeboxing:** pomodoro-task-app.py has integrated [timeboxing](https://en.wikipedia.org/wiki/Timeboxing) features.

## Installation

Currently, there is no installer provided. You can run the app by doing the following:

- Install [Python 3.12](https://www.python.org/downloads/) if you haven't already.
- Install [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
- Clone the repository using the command
```sh
git clone https://github.com/kun-codes/pomodoro-task-app.py.git
```
- Change the directory to the repository
```sh
cd pomodoro-task-app.py
```
- Install the dependencies using poetry
```sh
poetry install
```
- Run the app using the command
```sh
poetry run python pomodoro-task-app
```

## Usage
> [!IMPORTANT]
> On your first run of the application, start the timer and then go to [mitm.it](http://mitm.it) on a chromium based browser and install the certificate as per your OS and browser choice. This is required for the internet blocker to work. After installing the certificate, restart the application.

- Start the app using the command mentioned above.

There are four main screens in the app:
1. **Task View:** This is where you can add, delete and view tasks.
 
![image](https://i.ibb.co/6m17JRr/image.png)

2. **Timer View:** This is where you can start the timer and view the time left.

![image](https://i.ibb.co/bmMdB3m/image.png)

3. **Website Filter View:** This is where you can add, delete and view websites to block and choose between a blocklist and a whitelist. Please enter the website without the protocol (http/https) as shown in the image.

![image](https://i.ibb.co/9N0DK9h/image.png)

4. **Workspace Selector View:** This is where you can select the workspace you want to work in. Each workspace has its own adjustable timer and website filter settings. Each workspace also has its own tasks.

![image](https://i.ibb.co/72WN7bP/image.png)

## Known Bugs

- The internet blocker doesn't work as expected when there are no websites in the currently selected list (blocklist or allowlist).

## Credits

- [Super Productivity](https://github.com/johannesjo/super-productivity): The app is inspired by Super Productivity.
- [chomper](https://github.com/aniketpanjwani/chomper): The internet blocker has some functionality inspired by chomper.
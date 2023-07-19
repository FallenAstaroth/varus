<p align="center">
  <img src="logo.svg" width="100">
</p>

## 🗺️ Navigation
* [Current features](#-current-features)
* [Deployment](#%EF%B8%8F-deployment)
  * [Backend](#-backend)
  * [Frontend](#-frontend)

### 📄 Current features
1. Sites that the player supports:
  - [YouTube](https://www.youtube.com)
  - [Anilibria](https://www.anilibria.tv/pages/catalog.php)
2. Synchronization of the following actions:
  - Play
  - Pause
  - Rewind
3. Synchronization of the video player time during playback and rewind events.
4. Chat, as well as its overlay version (pc only) when the player is opened full screen.

### 🛠️ Deployment
#### ⚙️ Backend
1. Open `cmd`.
2. Type in the command:
```
pip install virtualenv
```
3. Go to the `backend` folder:
```
cd path\to\folder
```
4. Create a virtual environment:
```
virtualenv venv
```
5. Activate the virtual environment:

Windows:
```
call venv\Scripts\activate
```
Linux:
```
source venv\bin\activate
```
6. Install dependencies:
```
pip install -r requirements.txt
```
7. Replace the host, port, and origin fields with your own in the file `backend/src/misc.py`.
8. Start the server with the command:

Windows:
```
set PYTHONPATH=path\to\varus\project && python path\to\app.py
```
Linux:
```
PYTHONPATH=path\to\varus\project python path\to\app.py
```
#### 👁️ Frontend
1. Open `cmd`.
2. Go to the `frontend` folder:
```
cd path\to\folder
```
3. Install the modules:
```
npm install
npm install --global serve
```
4. Replace the backend url field in the file `frontend/src/globals.js`.
5. Create an application build:
```
npm run build
```
6. Start the application:
```
serve -s path\to\frontend\folder\dist -l 5000
```

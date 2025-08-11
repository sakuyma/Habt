// main.js
const { app, BrowserWindow, ipcMain } = require("electron");
const path = require('path');
const { PythonShell } = require('python-shell');

const createWindow = () => {
    const win = new BrowserWindow({
        width: 1200,
        height: 750,
        icon: path.join(__dirname, 'icon.png'),
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true
        }
    });
    
    win.setMenuBarVisibility(false);
    win.setTitle("Habt");
    win.loadFile('src/index.html');
}

app.whenReady().then(() => {
    createWindow();
    
    // Инициализация конфига при запуске
    initConfig();
});

app.on('window-all-closed', () => app.quit());

// Функции для работы с конфигом
function initConfig() {
    const options = {
        scriptPath: path.join(__dirname, 'config'),
        args: []
    };
    
    PythonShell.run('config_manager.py', options, (err, results) => {
        if (err) throw err;
        console.log('Config initialized:', results);
    });
}

ipcMain.handle('get-config', async (event) => {
    return new Promise((resolve, reject) => {
        const options = {
            scriptPath: path.join(__dirname, 'config'),
            args: ['get']
        };
        
        PythonShell.run('config_manager.py', options, (err, results) => {
            if (err) {
                reject(err);
                return;
            }
            resolve(JSON.parse(results[0]));
        });
    });
});

ipcMain.handle('update-config', async (event, newValues) => {
    return new Promise((resolve, reject) => {
        const options = {
            scriptPath: path.join(__dirname, 'config'),
            args: ['update', JSON.stringify(newValues)]
        };
        
        PythonShell.run('config_manager.py', options, (err, results) => {
            if (err) {
                reject(err);
                return;
            }
            resolve(JSON.parse(results[0]));
        });
    });
});
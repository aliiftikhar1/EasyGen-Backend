
const { exec } = require('child_process');

// Path to your virtual environment's gunicorn
const gunicornPath = process.env.HOME + '/Zylo/Easygen/EasyGen-Backend/venv/bin/gunicorn';
const projectPath = process.env.HOME + '/Zylo/Easygen/EasyGen-Backend';

// Start Gunicorn
const gunicorn = exec(`${gunicornPath} --workers 3 --bind 127.0.0.1:8000 easygen.wsgi:application`, {
  cwd: projectPath
});

// Forward stdout and stderr
gunicorn.stdout.on('data', (data) => {
  console.log(data);
});

gunicorn.stderr.on('data', (data) => {
  console.error(data);
});

gunicorn.on('close', (code) => {
  console.log(`Gunicorn process exited with code ${code}`);
});

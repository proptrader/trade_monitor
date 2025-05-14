@echo off
echo Starting Trade Monitor servers...

:: Start backend server
start "Trade Monitor Backend" cmd /k "cd backend && python run.py"

:: Wait for 2 seconds to ensure backend starts first
timeout /t 2 /nobreak > nul

:: Start frontend server
start "Trade Monitor Frontend" cmd /k "cd frontend && python app.py"

echo Servers started! Access the application at http://localhost:3000 
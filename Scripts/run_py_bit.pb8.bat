@echo off
setlocal

rem Get the path of the batch file directory
set "batch_dir=%~dp0"

rem Set the path to the Python script relative to the batch file
set "python_script=%batch_dir%batchIntegration.py"

rem Get the file to read from the command line argument
set "file_to_read=%~1"

rem Check if the file exists
if not exist "%file_to_read%" (
  echo File does not exist: "%file_to_read%"
  pause
  exit /b
)

rem Run the Python script with the file as a parameter
python "%python_script%" "%file_to_read%"

pause

endlocal
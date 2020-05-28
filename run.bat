REM export_csv.bat
SET PATH=E:\oracle\instantclient_11_2;%PATH%
SET PATH=C:\Users\yinhb\AppData\Local\Programs\Python\Python37;%PATH%

SET WORK_DIR=C:\Users\yinhb\Desktop\tasks\humiao
cd %WORK_DIR%
python exports.py 

@ECHO "Finished!"
pause

set now_d=%cd%
cd..
set back_d=%cd%
pyuic4 -o %back_d%\ui_Editor_Report.py %now_d%\Editor_Report.ui
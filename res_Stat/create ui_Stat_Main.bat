set now_d=%cd%
cd..
set back_d=%cd%
pyuic4 -o %back_d%\ui_Stat_Main.py %now_d%\Stat_Main.ui
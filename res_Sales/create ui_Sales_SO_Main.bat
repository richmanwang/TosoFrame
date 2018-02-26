set now_d=%cd%
cd..
set back_d=%cd%
pyuic4 -o %back_d%\ui_Sales_SO_Main.py %now_d%\Sales_SO_Main.ui
set now_d=%cd%
cd..
set back_d=%cd%
pyuic4 -o %back_d%\ui_Nitori_Keyword.py %now_d%\Nitori_Keyword.ui
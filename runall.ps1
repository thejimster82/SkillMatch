Set-ExecutionPolicy RemoteSigned

#install requirements
$requirements = (Get-Location).ToString() + "\requirements.txt"
pip.exe install -r $requirements

#perform server migrations
$manage = (Get-Location).ToString() + "\manage.py"
python.exe $manage makemigrations
python.exe $manage migrate

#start server
python.exe $manage runserver --insecure
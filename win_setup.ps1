param($Work)

if(!$Work) {
    powershell.exe -NoExit ./win_setup.ps1 1
}

pip install virtualenv

if( -not (Test-Path .\robot\)) {
    virtualenv.exe .\robot\
}

.\robot\Scripts\activate.ps1

pip install -r .\requirements.txt
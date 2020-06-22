c:
cd C:\Users\johnS\PycharmProjects\EVNews
venv\scripts\activate
py update_articles.py
py autoblog.py
deactivate
# exit
Write-Host -NoNewLine 'Press any key to continue...';
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
"Closing"
start-sleep -s 3

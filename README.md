--Compilando--


Baixe o Python.

Baixe o Pycharm.

Instale as bibliotecas necessárias:

  pip install kivy
  
  pip install zipfile
  
  pip install shutil
  
  pip install requests
  
  pip install pyinstaller
  
execute:

  pyinstaller --onefile --windowed launcher.py

Adicionando Background e Som:


Como nosso aplicativo depende de arquivos externos (como imagens ou sons), você precisará instruir o PyInstaller a incluí-los. Você pode fazer isso criando um arquivo .spec (gerado automaticamente na primeira vez que você executa o PyInstaller) e modificando-o para adicionar esses arquivos.
Depois de gerar o .spec pela primeira vez, abra-o e procure por uma lista chamada datas=[]. Você pode adicionar seus arquivos aqui no formato ('caminho/do/arquivo/origem', 'destino').

Depois de modificar o arquivo .spec para incluir os arquivos necessários, recompile seu aplicativo usando o PyInstaller com o arquivo .spec como argumento, assim:
  pyinstaller launcher.spec

Pronto!

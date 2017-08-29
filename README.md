Criar um novo projeto
---------------------
Por padrão o nome do ambiente virtual é **.venv**, mas você pode mudar assim:
```
./bootstrap.sh my_venv
```

Ativar o ambiente virtual
-------------------------
```
source VENV_PATH/bin/activate
```

Configurar banco de dados
-------------------------
O projeto está configurado para criar o banco **db.sqlite3**, caso deseje alterar esse **nome** altere a constante DATABASE_NAME no arquivo settings.py.

A engine de banco de dados pode ser alterada via variável de ambiente conforme exemplo:
```
export DATABASE_URL="postgres://postgres@localhost/my_db"
```

Para mais opções de configuração do banco de dados consulte a documentação do projeto [dj-database-url](https://github.com/kennethreitz/dj-database-url#url-schema)


Servidor de desenvolvimento
===========================
```
python manage.py collectstatic
```

Referências
===========

* [django-debug-toolbar](http://django-debug-toolbar.readthedocs.io/en/stable/index.html)
* [model-mommy](http://model-mommy.readthedocs.io/en/latest/index.html)
* [django-extensions](https://django-extensions.readthedocs.io/en/latest/)
* [coverage.py](https://coverage.readthedocs.io/en/coverage-4.3.4/)

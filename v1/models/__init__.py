# Este arquivo faz com que o diretório 'models' seja tratado como um pacote Python.

# Você pode simplificar o acesso aos menus principais de cada módulo
# importando-os aqui.
from .customer import main as customer_main
from .order import main as order_main
from .category import main as category_main
from .catalog import main as catalog_main

# Define o que será importado quando se usar "from models import *"
__all__ = ['customer_main', 'order_main', 'category_main', 'catalog_main']

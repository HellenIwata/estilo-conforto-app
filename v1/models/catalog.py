# Sistema de gernciamento de pedidos - Catalogos - V1.0.0
import uuid
from .category import categories, insert_category


products = {}
skus = {}

def generate_sku(brand, category_name):
  base_sku = (category_name[0] + brand[0] + brand[2] ).upper()
  
  count = skus.get(base_sku, 0) + 1
  skus[base_sku] = count
  
  # Formata o SKU final com um número sequencial (ex: CCC001)
  final_sku = f"{base_sku}{count:03d}"
  return final_sku


def insert_product():
  name = input("Digite o nome do produto: ").lower()
  brand = input("Digite a marca do produto: ").lower()
  category_name_input = input("Digite o nome da categoria do produto: ").lower()
  description = input("Digite a descrição do produto: ").lower()
  sizes = input("Digite o tamanho do produto: ")
  try:
    price = float(input("Digite o preço do produto: "))
  except ValueError:
    print("Erro: O preço deve ser um número.")
    return

  if name and description and price and brand and sizes and category_name_input:
    # Procura pelo ID da categoria com base no nome fornecido
    found_category = None
    for cat_id, cat_info in categories.items():
        if cat_info['name'].lower() == category_name_input:
            found_category = cat_info
            break

    if not found_category:
      print(f"ERRO: Categoria '{category_name_input}' não encontrada. Cadastre-a primeiro.")
      return insert_category()

    sku = generate_sku(brand, found_category['name'])
    product_id = str(uuid.uuid4())
    products[product_id] = {
      'sku': sku,
      'name': name,
      'brand': brand,
      'category': found_category, # Armazena o dicionário completo da categoria
      'description': description,
      'sizes': sizes,
      'price': price
    }
    print(f"\nProduto '{name}' cadastrado com sucesso! SKU: {sku} (ID: {product_id})")
  else:
    print("Erro: algum dado esta vazio, verifique!")


def get_product():
  print("\n--- Lista de Produtos ---")
  if not products:
    print("Nenhum produto cadastrado.")
    return
  for product_id, info in products.items():
    print(f'''ID: {product_id}
SKU: {info['sku']}
Nome: {info['name']},
Marca: {info['brand']},
Categoria: {info['category']['name']},
Descrição: {info['description']},
Tamanho: {info['sizes']},
Preço: R$ {info['price']:.2f}''')
  print("-------------------------\n")


def search_product():
  print('''
  -----* Buscar Produto *-----
  [1] Buscar por nome
  [2] Buscar por descrição
  [0] Voltar ao menu principal
  ''')
  search_results_ids = []
  opcao = input("Digite a opção desejada: ")

  match opcao:
    case '0':
      return []
    case '1':
      search_key = 'name'
      name = input("Digite o nome do produto: ").lower()
      search_value = name
    case '2':
      search_key = 'description'
      description = input("Digite a descrição do produto: ").lower()
      search_value = description
    case _:
      print("Opção inválida.")
      return []

  search_results_ids = [
    pid for pid, pdata in products.items()
    if search_value in pdata[search_key].lower()
  ]

  if not search_results_ids:
    print("\nNenhum produto foi encontrado com esse critério.")
  else:
    print("\n--- Produtos Encontrados ---")
    for product_id in search_results_ids:
      info = products[product_id]
      print(f'''ID: {product_id}
SKU: {info['sku']}
Nome: {info['name']},
Descrição: {info['description']},
Preço: R$ {info['price']:.2f}''')
  print("--------------------------\n")

  return search_results_ids


def update_product():
  print("\n--- Atualizar Produto ---")
  if not products:
    print("Nenhum produto cadastrado.")
    return

  found_ids = search_product()

  if not found_ids:
    return

  product_id_to_update = -1

  if len(found_ids) == 1:
    product_id_to_update = found_ids[0]
    print(f'''Produto com ID {product_id_to_update}
    selecionado para atualização.''')
  else:
    print("Múltiplos produtos encontrados.")
    try:
      chosen_id = int(input('''Digite o ID do produto
      que deseja atualizar: '''))
      if chosen_id in found_ids:
        product_id_to_update = chosen_id
      else:
        print("Erro: O ID digitado não está na lista de resultados.")
        return
    except ValueError:
      print("Erro: ID inválido. Por favor, digite um número.")
      return

  if product_id_to_update != -1:
    print("\nDeixe o campo em branco para manter a informação atual.")
    product_data = products[product_id_to_update]

    products[product_id_to_update]['name'] = input(f"Novo nome ({product_data['name']}): ") or product_data['name']

    products[product_id_to_update]['description'] = input(f"Nova descrição ({product_data['description']}): ") or product_data['description']

    products[product_id_to_update]['price'] = input(f"Novo preço ({product_data['price']}): ") or product_data['price']

    print(f"\nProduto ID {product_id_to_update} atualizado com sucesso!")


def delete_product():
  print("\n--- Deletar Produto ---")
  if not products:
    print("Nenhum produto cadastrado.")
    return

  found_ids = search_product()

  if not found_ids:
    return
  
  product_id_to_delete = -1

  if len(found_ids) == 1:
    product_id_to_delete = found_ids[0]
    print(f'''Produto com ID {product_id_to_delete}
    selecionado para deleção.''')
  else:
    print("Múltiplos produtos encontrados.")
    try:
      chosen_id = int(input('''Digite o ID do produto
      que deseja deletar: '''))
      if chosen_id in found_ids:
        product_id_to_delete = chosen_id
      else:
        print("ERRO: O ID digitado não está na lista de resultados.")
        return
    except ValueError:
      print("ERRO: ID inválido. Por favor, digite um número.")
      return

  if product_id_to_delete != -1:
    del products[product_id_to_delete]
    print(f"\nProduto ID {product_id_to_delete} deletado com sucesso!")

def show_main_menu():
  print("\n" + "-"*50)
  print('''
  [1] Cadastrar Produto
  [2] Listar Produtos
  [3] Buscar Produto
  [4] Atualizar Produto
  [5] Deletar Produto
  [0] Sair 
''')
  print("-"*50)


def main():
  show_main_menu()

  opcao = input("Digite a opção desejada: ")
  match opcao:
    case '1':
      insert_product()
    case '2':
      get_product()
    case '3':
      search_product()
    case '4':
      update_product()
    case '5':
      delete_product()
    case '0':
      print("Saindo do programa...")
      return False
    case _:
      print("Opção inválida. Tente novamente.")
  return True

# Sistema de gerenciamento de pedidos - Categoria de produtos - V1.0.0

import uuid


categories = {}
def show_main_menu():
  print("\n" + "-"*50)
  print('''
  [1] Cadastrar Categoria
  [2] Listar Categorias
  [3] Buscar Categoria
  [4] Atualizar Categoria
  [5] Deletar Categoria
  [0] Sair 
''')
  print("-"*50)

  while True:
    opcao = input("Digite a opção desejada: ")

    match opcao:
      case '1':
        insert_category()
      case '2':
        get_category()
      case '3':
        search_category()
      case '4':
        upadte_category()
      case '5':
        delete_category()
      case '0':
        print("Saindo do programa...")
        break
      case _:
        print("Opção inválida. Tente novamente.")
    return True

def insert_category():
  name = input("Digite o nome da categoria: ")
  description = input("Digite a descrição da categoria: ")

  if name and description:
    category_id = str(uuid.uuid4())
    categories[category_id] = {
      'name': name,
      'description': description
    }
    print(f"Categoria '{name}' cadastrada sob o ID: {category_id}")
  else:
    print("Erro: algum dado esta vazio, verifique!")


def get_category():
  print("\n--- Lista de Categorias ---")
  if not categories:
    print("Nenhuma categoria cadastrada.")
    return show_main_menu()

  
  for category_id, info in categories.items():
    print(f'''ID: {category_id}
Nome: {info['name']},
Descrição: {info['description']}''')
  print("-------------------------\n")


def search_category():
  print('''
  -----* Buscar Categoria *-----
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
      name = input("Digite o nome da categoria: ").lower()
      search_value = name
    case '2':
      search_key = 'description'
      description = input("Digite a descrição da categoria: ").lower()
      search_value = description
    case _:
      print("Opção inválida.")
      return []
  
  search_results_ids = [
    cid for cid, cdata in categories.items()
    if search_value in cdata[search_key].lower()
  ]

  if not search_results_ids:
    print("\nNenhuma categoria foi encontrada com esse critério.")
    return 
  else:
    print("\n--- Categorias Encontradas ---")
    for category_id in search_results_ids:
      info = categories[category_id]
      print(f'''ID: {category_id}
      Nome: {info['name']},
      Descrição: {info['description']}''')
  print("--------------------------\n")

  return search_results_ids


def upadte_category():
  print("\n--- Atualizar Categoria ---")

  if not categories:
    print("Nenhuma categoria cadastrada.")
    return show_main_menu()

  found_ids = search_category()

  if not found_ids:
    return

  category_id_to_update = -1

  if len(found_ids) == 1:
    category_id_to_update = found_ids[0]
    print(f'''Categoria com ID {category_id_to_update}
    selecionado para atualização.''')
  else:
    print("Múltiplas categorias encontradas.")
    try:
      chosen_id = int(input('''Digite o ID da categoria
      que deseja atualizar: '''))
      if chosen_id in found_ids:
        category_id_to_update = chosen_id
      else:
        print("Erro: O ID digitado não está na lista de resultados.")
        return
    except ValueError:
      print("Erro: ID inválido. Por favor, digite um número.")
      return
  
  if category_id_to_update != -1:
    print("\nDeixe o campo em branco para manter a informação atual.")
    category_data = categories[category_id_to_update]

    categories[category_id_to_update]['name'] = input(f"Novo nome ({category_data['name']}): ") or category_data['name']

    categories[category_id_to_update]['description'] = input(f"Nova descrição ({category_data['description']}): ") or category_data['description']

    print(f"\nCategoria ID {category_id_to_update} atualizada com sucesso!")


def delete_category():
  print("\n--- Deletar Categoria ---")

  if not categories:
    print("Nenhuma categoria cadastrada.")
    return show_main_menu()


  found_ids = search_category()

  if not found_ids:
    return
  category_id_to_delete = -1
  if len(found_ids) == 1:
    category_id_to_delete = found_ids[0]
    print(f'''Produto com ID {category_id_to_delete}
    selecionado para deleção.''')
  else:
    print("Múltiplas categorias encontradas.")
    try:
      chosen_id = int(input('''Digite o ID da categoria
      que deseja deletar: '''))
      if chosen_id in found_ids:
        category_id_to_delete = chosen_id
      else:
        print("ERRO: O ID digitado não está na lista de resultados.")
        return
    except ValueError:
      print("ERRO: ID inválido. Por favor, digite um número.")
      return

  if category_id_to_delete != -1:
    del categories[category_id_to_delete]
    print(f"\nCategoria ID {category_id_to_delete} deletada com sucesso!")




def main():
  show_main_menu()

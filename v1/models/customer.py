# Sistema de gerenciamento de pedidos - Clientes - V1.0.0

customers = {}
next_id = 1


def insert_customer():
  global next_id
  nome = input("Digite o nome: ")
  fone = input("Digite o telefone: ")
  endereco = input("Digite o endereço: ")
  email = input("Digite o email: ")
  if nome and fone and endereco and email:
    customers[next_id] = {
      'nome': nome,
      'telefone': fone,
      'endereco': endereco,
      'email': email
    }
    print(f"Cliente '{nome}' cadastrado sob o ID: {next_id}")
    next_id += 1
  else:
    print("Erro: algum dado esta vazio, verifique!")


def get_customer():
  print("\n--- Lista de Clientes ---")
  if not customers:
    print("Nenhum cliente cadastrado.")
    return
  for customer_id, info in customers.items():
    print(f'''ID: {customer_id}
Nome: {info['nome']},
Telefone: {info['telefone']},
Endereço: {info['endereco']},
Email: {info['email']}''')
  print("-------------------------\n")


def search_customer():
  print('''
  -----* Buscar Cliente *-----
  [1] Buscar por nome
  [2] Buscar por telefone
  [3] Buscar por email
  [0] Voltar ao menu principal
  ''')
  search_results_ids = []
  opcao = input("Digite a opção desejada: ")
  match opcao:
    case '0':
      return []
    case '1':
      search_key = 'nome'
      nome = input("Digite o nome do cliente: ").lower()
      search_value = nome
    case '2':
      search_key = 'telefone'
      fone = input("Digite o telefone do cliente: ")
      search_value = fone
    case '3':
      search_key = 'email'
      email = input("Digite o email do cliente: ").lower()
      search_value = email
    case _:
      print("Opção inválida.")
      return []
  search_results_ids = [
      cid for cid, cdata in customers.items()
      if search_value in cdata[search_key].lower()
  ]

  if not search_results_ids:
    print("\nNenhum cliente foi encontrado com esse critério.")
  else:
    print("\n--- Clientes Encontrados ---")
    for customer_id in search_results_ids:
      info = customers[customer_id]
      print(f'''
  ID: {customer_id}
  Nome: {info['nome']},
  Telefone: {info['telefone']},
  Endereço: {info['endereco']},
  Email: {info['email']}''')
  print("--------------------------\n")

  return search_results_ids


def update_customer():
  print("\n--- Atualizar Cliente ---")
  if not customers:
    print("Nenhum cliente cadastrado.")
    return

  found_ids = search_customer()

  if not found_ids:
    return

  cusomer_id_to_update = -1

  if len(found_ids) == 1:
    customer_id_to_update = found_ids[0]
    print(f'''Cliente com ID {customer_id_to_update}
    selecionado para atualização.''')
  else:
    print("Múltiplos clientes encontrados.")
    try:
      chosen_id = int(input('''Digite o ID do cliente
      que deseja atualizar: '''))
      if chosen_id in found_ids:
        customer_id_to_update = chosen_id
      else:
        print("Erro: O ID digitado não está na lista de resultados.")
        return
    except ValueError:
      print("Erro: ID inválido. Por favor, digite um número.")
      return

  if customer_id_to_update != -1:
    print("\nDeixe o campo em branco para manter a informação atual.")
    customer_data = customers[customer_id_to_update]

    customers[customer_id_to_update]['nome'] = input(f"Novo nome ({customer_data['nome']}): ") or customer_data['nome']

    customers[customer_id_to_update]['telefone'] = input(f"Novo telefone ({customer_data['telefone']}): ") or customer_data['telefone']

    customers[customer_id_to_update]['endereco'] = input(f"Novo endereço ({customer_data['endereco']}): ") or customer_data['endereco']

    customers[customer_id_to_update]['email'] = input(f"Novo email ({customer_data['email']}): ") or customer_data['email']

    print(f"\nCliente ID {customer_id_to_update} atualizado com sucesso!")


def main():
  opcao = input('''Escolha uma opção
  [1] Cadastrar Cliente
  [2] Listar Clientes
  [3] Buscar Cliente
  [4] Atualizar Cliente
  [0] Sair 
  ''')
  match opcao:
    case '1':
      insert_customer()
    case '2':
      get_customer()
    case '3':
      search_customer()
    case '4':
      update_customer()
    case '0':
      print("Saindo do programa...")
      return False
    case _:
      print("Opção inválida. Tente novamente.")
  return True
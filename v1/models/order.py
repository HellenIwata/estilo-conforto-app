# Sistema de gerenciamento de pedidos - Pedidos - V1.0.0
from .customer import customers, search_customer
from .catalog import products

orders = {}
next_id = 1


def insert_order():
    global next_id
    print("\n--- Vincular Cliente ao Pedido ---")
    found_customer_ids = search_customer()
    if not found_customer_ids:
        print('''Nenhum cliente encontrado.
Cancele a operação ou cadastre um cliente primeiro.''')
        return

    try:
        customer_id = int(input("Digite o ID do cliente para este pedido: "))
        if customer_id not in customers:
            print("Erro: ID de cliente inválido.")
            return
    except ValueError:
        print("Erro: ID de cliente inválido.")
        return

    new_order_items = []
    print('''\n--- Adicionar Item ao Pedido ---''')
    while True:
        
        sku = input("Informe o SKU do produto: ").strip().upper()
        if not sku:
            print("Para adicionar um produto é necessário informar o SKU.")
            break

        # Procura o produto pelo SKU informado
        found_product = None
        for prod_id, prod_data in products.items():
            if prod_data.get('sku') == sku:
                found_product = prod_data
                break

        if not found_product:
            print(f"Erro: Produto com SKU '{sku}' não encontrado.")
            break

        try:
            quantity = int(input("Quantidade: "))
        except ValueError:
            print("Erro: A quantidade deve ser um número inteiro.")
            break

        if quantity <= 0:
            print("Erro: A quantidade deve ser maior que zero.")
            break

        new_order_items.append({
            'sku': sku,
            'item_name': found_product['name'],
            'description': found_product['description'],
            'quantity': quantity,
            'brand': found_product['brand'],
            'category': found_product['category']['name'],
            'unit_price': found_product['price']
        })
        print(f"Item '{found_product['name']}' adicionado.")
        more = input("Deseja adicionar mais item? (S/N): ").strip().upper()
        if more != 'S':
            break

    if new_order_items:
        print("\n--- Detalhes do Pedido ---")

        total_value = sum(item['quantity'] * item['unit_price'] for item in new_order_items)

        order_id_formatted = f"{next_id:04d}"
        orders[order_id_formatted] = {
            'customer_id': customer_id,
            'items': new_order_items,
            'total_value': total_value
        }
        print(f"\nPedido ID {order_id_formatted} cadastrado com sucesso para o cliente ID {customer_id}!")
        next_id += 1
    else:
        print("Nenhum item adicionado ao pedido.")
        


def _print_order_details(order_id, info):
    print(f"\n--- Detalhes do Pedido ID: {order_id} ---")
    print(f'''
Cliente: {customers.get(info['customer_id'], {}).get('nome', 'N/A')}
(ID: {info['customer_id']})''')
    print("Itens do Pedido:")
    if not info['items']:
        print("  (Nenhum item neste pedido)")
    else:
        for item in info['items']:
            subtotal = item['quantity'] * item['unit_price']
            print(f"- Item: {item['description']}, Qtd: {item['quantity']}, V. Unit.: R$ {item['unit_price']:.2f}, Subtotal: R$ {subtotal:.2f}")
    print(f"VALOR TOTAL DO PEDIDO: R$ {info['total_value']:.2f}")


def get_order():
    print("\n--- Lista de pedidos ---")
    if not orders:
        print("Nenhum pedido cadastrado.")
        return
    for order_id, info in orders.items():
        _print_order_details(order_id, info)
    print("-------------------------\n")


def search_order():
    print('''
-----* Buscar Pedido *-----
[1] Buscar por descrição do item
[0] Voltar ao menu principal
    ''')
    search_results_ids = []
    opcao = input("Digite a opção desejada: ")
    if opcao == '1':
        item_search = input("Digite a descrição do item a ser buscado no pedido: ").lower()
        for order_id, info in orders.items():
            for item in info.get('items', []):
                if item_search in item['description'].lower() and order_id not in search_results_ids:
                    search_results_ids.append(order_id)
    elif opcao == '0':
        return []
    else:
        print("Opção inválida.")
        return []

    if not search_results_ids:
        print("\nNenhum pedido foi encontrado com esse critério.")
    else:
        print("\n--- Pedidos Encontrados ---")
        for order_id in search_results_ids:
            _print_order_details(order_id, orders[order_id])
        print("--------------------------\n")

    return search_results_ids


def update_order():
    print("\n--- Atualizar Pedido ---")
    if not orders:
        print("Nenhum pedido cadastrado.")
        return

    found_ids = search_order()

    if not found_ids:
        return

    order_id_to_update = -1

    if len(found_ids) == 1:
        order_id_to_update = found_ids[0]
        print(f'''Pedido com ID {order_id_to_update}
selecionado para atualização.''')
    else:
        print("Múltiplos pedidos encontrados.")
        try:
            # O ID agora é uma string, não precisa converter para int
            chosen_id = input('''Digite o ID do pedido que deseja atualizar: ''')
            if str(chosen_id) in found_ids:
                order_id_to_update = chosen_id
            else:
                print("Erro: O ID digitado não está na lista de resultados.")
                return
        except ValueError:
            print("Erro: ID inválido. Por favor, digite um número.")
            return

    order_data = orders[order_id_to_update]
    while True:
        _print_order_details(order_id_to_update, order_data)
        print('''
O que você deseja fazer?
[1] Adicionar novo item
[2] Remover item existente
[0] Concluir atualização
        ''')
        action = input("Escolha uma opção: ")

        if action == '1':
            # Adicionar item
            item_name = input("Nome do novo item: ").strip()
            if item_name:
                try:
                    quantity = int(input("Quantidade: "))
                    unit_price = float(input("Valor Unitário: "))
                    order_data['items'].append({
                        'item_name': item_name,
                        'quantity': quantity,
                        'unit_price': unit_price
                    })
                    print(f"Item '{item_name}' adicionado.")
                except ValueError:
                    print("Erro: Quantidade e valor devem ser números.")

        elif action == '2':
            # Remover item
            if not order_data['items']:
                print("Não há itens para remover.")
                continue
            item_to_remove_name = input("Digite o nome exato do item a ser removido: ").strip()
            item_found = False
            
            # Filtra a lista, mantendo apenas os itens que não correspondem ao nome a ser removido
            initial_item_count = len(order_data['items'])
            order_data['items'] = [item for item in order_data['items'] if item['item_name'].lower() != item_to_remove_name.lower()]
            
            if len(order_data['items']) < initial_item_count:
                item_found = True
                print(f"Item(s) '{item_to_remove_name}' removido(s).")

            if not item_found:
                print("Item não encontrado.")

        elif action == '0':
            # Recalcular o total e sair
            order_data['total_value'] = sum(item['quantity'] * item['unit_price'] for item in order_data['items'])
            print(f"\nPedido ID {order_id_to_update} atualizado com sucesso!")
            _print_order_details(order_id_to_update, order_data)
            break

        else:
            print("Opção inválida.")


def main():
    print('''Escolha uma opção
[1] Cadastrar Pedido
[2] Listar Pedidos
[3] Buscar Pedido
[4] Atualizar Pedido
[0] Sair
''')
    opcao = input("Digite a opção desejada: ")
    match opcao:
        case '1':
            insert_order()
        case '2':
            get_order()
        case '3':
            search_order()
        case '4':
            update_order()
        case '0':
            print("Saindo do programa...")
            return False
        case _:
            print("Opção inválida. Tente novamente.")
    return True
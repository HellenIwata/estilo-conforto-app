# Sistema de gerenciamento de pedidos - Pedidos - V1.0.0
import datetime
import os
from fpdf import FPDF
from .config_manager_mongo import get_settings
from .customer import customers, search_customer
from .catalog import products

orders = {}
next_id = 1

def get_payment_details(total_value):
    payment_conditions = input('''
------ CONDIÇÕES DE PAGAMENTO ------
[1] À VISTA
[2] PARCELADO
''').strip()

    installments = 1
    installment_value = total_value

    if payment_conditions == '1':
        payment_conditions = 'À VISTA'
    elif payment_conditions == '2':
        payment_conditions = 'PARCELADO'
        try:
            installments = int(input("Digite o número de parcelas: "))
            if installments > 0:
                installment_value = total_value / installments
            else:
                installments = 1
        except ValueError:
            print("Número de parcelas inválido. Assumindo 1 parcela.")
            installments = 1

    payment_method = input("Digite o método de pagamento: ").strip().upper()


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
        print(f"Valor total dos itens: R$ {total_value:.2f}")

        try:
            discount_str = input("Digite o desconto (R$) ou deixe em branco para 0: ").replace(',', '.')
            discount = float(discount_str) if discount_str else 0.0
        except ValueError:
            print("Valor de desconto inválido. Desconto não aplicado.")
            discount = 0.0

        final_value = total_value - discount
        print(f"Valor final com desconto: R$ {final_value:.2f}")

        payment_details = get_payment_details(final_value)

        order_id_formatted = f"{next_id:04d}"
        orders[order_id_formatted] = {
            'customer_id': customer_id,
            'items': new_order_items,
            'total_value': final_value,
            'discount': discount,
            **payment_details
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


def get_order_by_id(order_id):
    if order_id in orders:
        return orders[order_id]

def update_order():
    print("\n--- Atualizar Pedido ---")
    if not orders:
        print("Nenhum pedido cadastrado.")
        return

    order_id = input("Digite o ID do pedido que deseja atualizar: ")

    found_ids = get_order_by_id(order_id)

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

def generate_order_pdf_by_id(order_id, order_data):
    settings = get_settings()
    logo_path = '../assets/logo2.png'
    save_dir = settings.get('pdf_output_path', '../output/pdfs')
    
    customer = customers.get(order_data['customer_id'], {})
    customer_name = customer.get('nome', 'N/A')
    customer_phone = customer.get('telefone', 'N/A')
    order_discount = order_data.get('discount', 0)

    # --- CREATE PDF ---
    pdf = FPDF()
    pdf.add_page()

    # --- HEADER ---
    if logo_path and os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=25)
    pdf.set_xy(40, 10)
    pdf.set_font("Helvetica", "B",size=16)
    pdf.cell(0, 15, "PEDIDO", ln=True, align="L")

    pdf.set_line_width(0.5)
    pdf.line(10,35,200,35)
    pdf.ln(10)

    # --- BODY ---
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"PEDIDO Nº: {order_id}", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"DATA: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(0, 8, f"CLIENTE: {customer_name}", ln=True)
    pdf.cell(0, 8, f"TELEFONE: {customer_phone}", ln=True)
    pdf.ln(5)

    pdf.set_line_width(0.6)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    # --- TABLE HEADER  ---
    if not order_data['items']:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0,10, "NENHUM ITEM NESTE PEDIDO", align="C", ln=True)
    else:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(10, 10, "ID", border=0, align="C")
        pdf.cell(80, 10, "DESCRIÇÃO PRODUTO", border=0, align="L")
        pdf.cell(30, 10, "VALOR UNIT.", border=0, align="R")
        pdf.cell(30, 10, "QTD", border=0, align="C")
        pdf.cell(30, 10, "VALOR TOTAL", border=0, align="R")
        pdf.ln(8)
        pdf.set_line_width(0.4)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        

        # --- Order Details ---
        pdf.set_font("Helvetica", "", 10)
        subtotal = 0
        for idx, item in enumerate(order_data['items'], start=1):
            desc = item['description']
            unit_price = item['unit_price']
            quantity = item['quantity']
            total_item = unit_price * quantity
            subtotal += total_item

            pdf.cell(10,8, str(idx), border=0, align="C")
            pdf.multi_cell(80, 8, desc, border=0, align="L")
            y = pdf.get_y()
            pdf.set_xy(100, y - 8)
            pdf.cell(30, 8, f"R$ {unit_price:.2f}", border=0, align="R")
            pdf.cell(30, 8, str(quantity), border=0, align="C")
            pdf.cell(30, 8, f"R$ {total_item:.2f}", border=0, align="R")
            pdf.ln(8)
        pdf.ln(5)
        pdf.dashed_line(10, pdf.get_y(), 200, pdf.get_y(), 1, 1)
        pdf.ln(5)

    # --- Total --
    payments_conditions = order_data.get('payment_conditions', 'À VISTA')
    payment_method = order_data.get('payment_method', 'PIX')
    payment_discount = order_data.get('discount', 0.0)
    total_final = subtotal - payment_discount
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(70, 8, "CONDIÇÕES DE PAGAMENTO: ", align="L")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(50, 8, payments_conditions, ln=True)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(70,8, "METODO DE PAGAMENTO: ", align="L")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(50, 8, payment_method, ln=True)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(30, 8, "SUBTOTAL: R$ ", border=0, align="R")
    pdf.cell(40, 8, f"{subtotal:.2f}", align="R", ln=True)

    pdf.cell(140,8, "DESCONTO", align="R")
    pdf.cell(40, 8, f"R$ {order_discount:.2f}", align="R", ln=True)
    pdf.dashed_line(10, pdf.get_y(), 200, pdf.get_y(), 1, 1)

    pdf.cell(140, 8, "VALOR TOTAL", align="R")
    pdf.cell(40, 8, f"R$ {total_final:.2f}", align="R", ln=True)

    # --- SALVE ---
    os.makedirs(save_dir, exist_ok=True)
    output_path = os.path.join(save_dir, f"pedido_{customer_name}_{order_id}.pdf")
    pdf.output(output_path)
    print(f'PDF gerado com sucesso: {output_path}')


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
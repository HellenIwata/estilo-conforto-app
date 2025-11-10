from models import customer_main, order_main, catalog_main

def show_main_menu():
  print("\n" + "-"*50)
  option = input('''
Escolha uma opção
[1] Gerenciar Clientes
[2] Gerenciar Pedidos
[3] Gerenciar Catalogo
[0] Sair
''')
  print("-"*50)
  return option

def main():
  while True:
    option = show_main_menu()
    match option:
      case '1':
        customer_main()
      case '2':
        order_main()
      case '3':
        catalog_main()
      case '0':
        print("Saindo do programa...")
        break # Encerra o loop while
      case _:
        print("Opção inválida. Tente novamente.")


if __name__ == '__main__':
  main()
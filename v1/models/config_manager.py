# config_manager.py
# =====================================
# Gerencia a configuração local do caminho de salvamento dos PDFs
# =====================================

import json
import os

# Caminho do arquivo de configuração local
LOCAL_CONFIG_PATH = "./local_config.json"

def get_settings():
    """
    Carrega as configurações salvas localmente.
    Retorna um dicionário com o caminho de saída dos PDFs.
    """
    if os.path.exists(LOCAL_CONFIG_PATH):
        try:
            with open(LOCAL_CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("[AVISO] Erro ao ler local_config.json, recriando arquivo padrão.")
    # Caso o arquivo não exista ou esteja corrompido
    default = {"pdf_output_path": "./pdfs"}
    save_settings(default)
    return default


def save_settings(settings: dict):
    """Salva as configurações no arquivo local_config.json"""
    with open(LOCAL_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)
    print("💾 Configurações salvas com sucesso.")


def update_pdf_path(new_path: str):
    """Atualiza apenas o caminho onde os PDFs serão salvos"""
    settings = get_settings()
    settings["pdf_output_path"] = new_path
    save_settings(settings)
    print(f"✅ Caminho atualizado para: {new_path}")


def print_settings():
    """Exibe as configurações atuais"""
    settings = get_settings()
    print("\n=== Configurações Atuais ===")
    print(f"Diretório de saída dos PDFs: {settings.get('pdf_output_path')}")
    print("============================\n")

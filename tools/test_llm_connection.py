import os

def load_env():
    """Carrega manualmente as variáveis de ambiente do .env, útil se o python-dotenv não estiver instalado."""
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, val = line.strip().split("=", 1)
                    os.environ[key.strip()] = val.strip()

def test_connection():
    load_env()
    # Verifica tanto Gemini quanto OpenAI
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ ERRO: Nenhuma chave de API foi encontrada no arquivo .env.")
        print("Por favor, adicione sua chave ao arquivo .env na forma: GEMINI_API_KEY=sua_chave_aqui")
        return False
        
    print(f"✅ Sucesso: Uma chave de API foi detectada (Tamanho: {len(api_key)} caracteres).")
    print("O Handshake inicial foi concluído!")
    return True

if __name__ == "__main__":
    print("--- Teste de Link (Handshake) ---")
    test_connection()

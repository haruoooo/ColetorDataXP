from playwright.sync_api import sync_playwright
from datetime import datetime
import json
import os

def rastrear_acoes(output_path='data/acoes_usuario.json'):
    dados = []

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False)
        pagina = navegador.new_page()

        print("Carregando o site...")
        pagina.goto("https://casino.bet365.bet.br/home/br?country=28", timeout=60000)

        pagina.wait_for_timeout(10000)  

        botoes = pagina.query_selector_all("button")
        print(f"{len(botoes)} botões encontrados.")

        for botao in botoes:
            try:
                texto = botao.inner_text().strip()

                if not texto:
                    continue

                acao = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "tipo": "button",
                    "url": pagina.url,
                    "detalhes": texto
                }
                print("Botão detectado:", texto)
                dados.append(acao)
            except:
                continue

        print("Interaja com o site. Feche a aba do navegador quando terminar.")
        pagina.wait_for_event("close", timeout=0)
        navegador.close()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

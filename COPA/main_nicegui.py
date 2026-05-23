from nicegui import ui
from services.partidas import listar_partidas

@ui.page('/')
def home():
    ui.label('🏆 Copa do Mundo 2026').classes('text-2xl font-bold')

    ui.button('🎮 Games', on_click=lambda: ui.navigate.to('/games'))

    ui.separator()

    partidas = listar_partidas()

    for p in partidas:
        with ui.card().classes('w-full'):
            ui.label(f"{p['selecao_casa']} vs {p['selecao_fora']}").classes('text-lg font-bold')
            ui.label(f"Grupo: {p['grupo']}")
            ui.label(f"Estádio: {p['estadio'] or 'A definir'}")
            ui.label(f"Árbitro: {p['arbitro'] or 'A definir'}")


@ui.page('/games')
def games():
    ui.label('🎮 Games').classes('text-2xl font-bold')
    ui.label('🚧 Coming Soon').classes('text-xl text-gray')

    ui.button('⬅ Voltar', on_click=lambda: ui.navigate.to('/'))

ui.run()
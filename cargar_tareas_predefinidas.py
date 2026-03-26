import json
import os

# Script para cargar todas las tareas predefinidas de transporte

TASKS_FILE = 'tareas.json'

# Definición de tareas por tipo de servicio
TAREAS_PREDEFINIDAS = {
    'Monday': [
        # TAXI
        {'nombre': 'TAXI', 'hora': '03:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '06:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '12:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '15:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '20:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '22:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        # BUS INTERURBANO
        {'nombre': 'BUS INTERURBANO', 'hora': '09:00', 'tipo': 'bus_interurbano', 'mensaje': '', 'enviado': False},
        {'nombre': 'BUS INTERURBANO', 'hora': '19:00', 'tipo': 'bus_interurbano', 'mensaje': '', 'enviado': False},
        # BUS URBANO
        {'nombre': 'BUS URBANO', 'hora': '01:00', 'tipo': 'bus_urbano', 'mensaje': '', 'enviado': False},
        # CLIENTE VIP
        {'nombre': 'CLIENTE VIP', 'hora': '02:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '13:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '18:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '23:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        # MUDANZA
        {'nombre': 'MUDANZA', 'hora': '04:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '08:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '17:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '21:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '23:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
    ],
    'Tuesday': [
        # TAXI
        {'nombre': 'TAXI', 'hora': '03:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '06:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '12:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '15:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '20:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '22:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        # BUS INTERURBANO
        {'nombre': 'BUS INTERURBANO', 'hora': '09:00', 'tipo': 'bus_interurbano', 'mensaje': '', 'enviado': False},
        {'nombre': 'BUS INTERURBANO', 'hora': '19:00', 'tipo': 'bus_interurbano', 'mensaje': '', 'enviado': False},
        # BUS URBANO
        {'nombre': 'BUS URBANO', 'hora': '01:00', 'tipo': 'bus_urbano', 'mensaje': '', 'enviado': False},
        # CLIENTE VIP
        {'nombre': 'CLIENTE VIP', 'hora': '02:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '13:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '18:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '23:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        # MUDANZA
        {'nombre': 'MUDANZA', 'hora': '04:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '08:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '17:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '21:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '23:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
    ],
    'Wednesday': [
        # TAXI
        {'nombre': 'TAXI', 'hora': '03:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '06:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '12:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '15:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '20:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '22:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        # BUS INTERURBANO
        {'nombre': 'BUS INTERURBANO', 'hora': '09:00', 'tipo': 'bus_interurbano', 'mensaje': '', 'enviado': False},
        {'nombre': 'BUS INTERURBANO', 'hora': '19:00', 'tipo': 'bus_interurbano', 'mensaje': '', 'enviado': False},
        # BUS URBANO
        {'nombre': 'BUS URBANO', 'hora': '01:00', 'tipo': 'bus_urbano', 'mensaje': '', 'enviado': False},
        # CLIENTE VIP
        {'nombre': 'CLIENTE VIP', 'hora': '02:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '13:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '18:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '23:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        # MUDANZA
        {'nombre': 'MUDANZA', 'hora': '04:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '08:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '17:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '21:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '23:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
    ],
    'Thursday': [
        # TAXI
        {'nombre': 'TAXI', 'hora': '03:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '06:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '12:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '15:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '20:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '22:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        # BUS INTERURBANO
        {'nombre': 'BUS INTERURBANO', 'hora': '09:00', 'tipo': 'bus_interurbano', 'mensaje': '', 'enviado': False},
        {'nombre': 'BUS INTERURBANO', 'hora': '19:00', 'tipo': 'bus_interurbano', 'mensaje': '', 'enviado': False},
        # BUS URBANO
        {'nombre': 'BUS URBANO', 'hora': '01:00', 'tipo': 'bus_urbano', 'mensaje': '', 'enviado': False},
        # CLIENTE VIP
        {'nombre': 'CLIENTE VIP', 'hora': '02:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '13:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '18:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '23:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        # MUDANZA
        {'nombre': 'MUDANZA', 'hora': '04:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '08:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '17:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '21:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '23:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
    ],
    'Friday': [
        # TAXI
        {'nombre': 'TAXI', 'hora': '03:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '06:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '12:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '15:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '20:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '22:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        # BUS INTERURBANO
        {'nombre': 'BUS INTERURBANO', 'hora': '09:00', 'tipo': 'bus_interurbano', 'mensaje': '', 'enviado': False},
        {'nombre': 'BUS INTERURBANO', 'hora': '19:00', 'tipo': 'bus_interurbano', 'mensaje': '', 'enviado': False},
        # BUS URBANO
        {'nombre': 'BUS URBANO', 'hora': '01:00', 'tipo': 'bus_urbano', 'mensaje': '', 'enviado': False},
        # CLIENTE VIP
        {'nombre': 'CLIENTE VIP', 'hora': '02:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '13:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '18:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '23:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        # MUDANZA
        {'nombre': 'MUDANZA', 'hora': '04:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '08:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '17:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '21:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '23:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
    ],
    'Saturday': [
        # TAXI
        {'nombre': 'TAXI', 'hora': '03:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '06:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '12:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '15:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '20:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '22:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        # BUS INTERURBANO
        {'nombre': 'BUS INTERURBANO', 'hora': '09:00', 'tipo': 'bus_interurbano', 'mensaje': '', 'enviado': False},
        {'nombre': 'BUS INTERURBANO', 'hora': '19:00', 'tipo': 'bus_interurbano', 'mensaje': '', 'enviado': False},
        # BUS URBANO
        {'nombre': 'BUS URBANO', 'hora': '01:00', 'tipo': 'bus_urbano', 'mensaje': '', 'enviado': False},
        # CLIENTE VIP
        {'nombre': 'CLIENTE VIP', 'hora': '02:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '13:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '18:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '23:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        # MUDANZA
        {'nombre': 'MUDANZA', 'hora': '04:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '08:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '17:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '21:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '23:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
    ],
    'Sunday': [
        # TAXI
        {'nombre': 'TAXI', 'hora': '03:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '06:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '12:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '15:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '20:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        {'nombre': 'TAXI', 'hora': '22:00', 'tipo': 'taxi', 'mensaje': '', 'enviado': False},
        # BUS INTERURBANO
        {'nombre': 'BUS INTERURBANO', 'hora': '09:00', 'tipo': 'bus_interurbano', 'mensaje': '', 'enviado': False},
        {'nombre': 'BUS INTERURBANO', 'hora': '19:00', 'tipo': 'bus_interurbano', 'mensaje': '', 'enviado': False},
        # BUS URBANO
        {'nombre': 'BUS URBANO', 'hora': '01:00', 'tipo': 'bus_urbano', 'mensaje': '', 'enviado': False},
        # CLIENTE VIP
        {'nombre': 'CLIENTE VIP', 'hora': '02:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '13:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '18:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        {'nombre': 'CLIENTE VIP', 'hora': '23:00', 'tipo': 'cliente_vip', 'mensaje': '', 'enviado': False},
        # MUDANZA
        {'nombre': 'MUDANZA', 'hora': '04:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '08:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '17:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '21:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
        {'nombre': 'MUDANZA', 'hora': '23:00', 'tipo': 'mudanza', 'mensaje': '', 'enviado': False},
    ]
}

def guardar_tareas(tareas):
    """Guarda las tareas en el archivo JSON"""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    # Cargar las tareas predefinidas
    guardar_tareas(TAREAS_PREDEFINIDAS)
    print(f"✅ {TASKS_FILE} creado con todas las tareas predefinidas")
    print("\nResumen:")
    for dia, tareas in TAREAS_PREDEFINIDAS.items():
        print(f"  {dia}: {len(tareas)} tareas")

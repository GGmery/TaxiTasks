import discord
from discord.ext import commands, tasks
import json
from datetime import datetime, time
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar intenciones
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Variables globales
TASKS_FILE = 'tareas.json'
CHANNEL_ID = None  # Se configurará cuando se execute el comando setup
ROLE_ID = None  # ID del rol a mencionar (se configurará con !setup)

# Cargar tareas desde el archivo JSON
def cargar_tareas():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Evento para responder a menciones sobre tareas próximas
@bot.event
async def on_message(message):
    try:
        if message.author.bot:
            return
        # Si mencionan al bot y preguntan por tareas próximas
        if bot.user in message.mentions and ("tarea" in message.content.lower() or "tareas" in message.content.lower()):
            ahora = datetime.now()
            tareas = cargar_tareas()
            dia_actual = ahora.strftime('%A')
            lista_tarea = tareas.get(dia_actual, [])
            proximas = []
            for tarea in lista_tarea:
                hora_tarea = datetime.strptime(tarea['hora'], '%H:%M').replace(year=ahora.year, month=ahora.month, day=ahora.day)
                minutos = int((hora_tarea - ahora).total_seconds() // 60)
                if 0 <= minutos < 60:
                    proximas.append((minutos, tarea))
            if proximas:
                proximas.sort()
                respuesta = "🟢 Sí, en las próximas tareas: \n"
                for minutos, tarea in proximas:
                    tipo = tarea.get('tipo', 'general')
                    emoji = {
                        'taxi': '🚕',
                        'bus_interurbano': '🚌',
                        'bus_urbano': '🚌',
                        'cliente_vip': '🥂',
                        'mudanza': '🚚'
                    }.get(tipo, '📋')
                    respuesta += f"{emoji} {tarea['nombre']} en {minutos} minuto{'s' if minutos != 1 else ''} (a las {tarea['hora']})\n"
                await message.reply(respuesta)
            else:
                await message.reply("🔴 No hay tareas programadas en la próxima hora.")
        else:
            await bot.process_commands(message)
    except Exception as e:
        print(f"[on_message ERROR] {e}")
        import traceback
        traceback.print_exc()
import discord
from discord.ext import commands, tasks
import json
from datetime import datetime, time
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar intenciones
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Variables globales
TASKS_FILE = 'tareas.json'
CHANNEL_ID = None  # Se configurará cuando se execute el comando setup
ROLE_ID = None  # ID del rol a mencionar (se configurará con !setup)

# Cargar tareas desde el archivo JSON
def cargar_tareas():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Guardar tareas en el archivo JSON
def guardar_tareas(tareas):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)

# Evento cuando el bot se conecta
@bot.event
async def on_ready():
    print(f'{bot.user} se ha conectado a Discord!')
    revisar_tareas.start()

# Comando para configurar el canal y rol
@bot.command(name='setup')
async def setup(ctx, canal: discord.TextChannel = None, rol: discord.Role = None):
    """Configura el canal donde se enviarán los recordatorios y el rol a mencionar
    Uso: !setup #nombre-canal @nombre-rol
    """
    global CHANNEL_ID, ROLE_ID
    if canal is None:
        canal = ctx.channel
    if rol is None:
        rol = None
    
    CHANNEL_ID = canal.id
    ROLE_ID = rol.id if rol else None
    
    await ctx.send(f"✅ Canal configurado: {canal.mention}")
    if rol:
        await ctx.send(f"✅ Rol a mencionar: {rol.mention}")
    print(f"Canal configurado: {CHANNEL_ID}")
    if ROLE_ID:
        print(f"Rol configurado: {ROLE_ID}")

# Función para obtener el formato personalizado del mensaje
def obtener_embed_tarea(tarea, hora_actual):
    """Retorna un embed personalizado según el tipo de servicio"""
    tipo = tarea.get('tipo', 'general')
    nombre = tarea['nombre']
    mensaje = tarea.get('mensaje', '')
    
    # Definir colores y emojis por tipo
    config_tipos = {
        'taxi': {
            'color': discord.Color.from_rgb(255, 215, 0),  # Oro
            'emoji': '🚕',
            'titulo': '¡ATENCIÓN! 🚕 TAXI DISPONIBLE'
        },
        'bus_interurbano': {
            'color': discord.Color.from_rgb(70, 130, 180),  # Azul acero
            'emoji': '🚌',
            'titulo': '¡RUTA LARGA! 🚌 SALIDA INTERURBANA'
        },
        'bus_urbano': {
            'color': discord.Color.from_rgb(100, 149, 237),  # Azul cornflower
            'emoji': '🚌',
            'titulo': '¡TURNO DE CIUDAD! 🚌 BUS URBANO'
        },
        'cliente_vip': {
            'color': discord.Color.from_rgb(218, 165, 32),  # Goldenrod
            'emoji': '🥂',
            'titulo': '¡SERVICIO DE ÉLITE! 🥂 CLIENTE VIP'
        },
        'mudanza': {
            'color': discord.Color.from_rgb(220, 20, 60),  # Crimson
            'emoji': '🚚',
            'titulo': '¡HAY TRABAJO! 🚚 MUDANZA LISTA'
        }
    }
    
    config = config_tipos.get(tipo, {
        'color': discord.Color.blue(),
        'emoji': '📋',
        'titulo': nombre
    })
    
    embed = discord.Embed(
        title=config['titulo'],
        color=config['color']
    )
    
    embed.add_field(name="🕒 Hora", value=f"{hora_actual} — ¡Encended motores!" if tipo == 'taxi' 
                                  else f"{hora_actual} — ¡A la terminal!" if tipo == 'bus_interurbano'
                                  else f"{hora_actual} — ¡Ruta nocturna activa!" if tipo == 'bus_urbano'
                                  else f"{hora_actual} — ¡Coche impecable!" if tipo == 'cliente_vip'
                                  else f"{hora_actual} — ¡A cargar cajas!" if tipo == 'mudanza'
                                  else f"{hora_actual}", inline=False)
    
    if mensaje:
        embed.add_field(name="📝 Detalles", value=mensaje, inline=False)
    
    return embed

# Tarea que revisa si hay tareas para el día actual
@tasks.loop(minutes=1)
async def revisar_tareas():
    """Revisa cada minuto si hay tareas que enviar"""
    try:
        if CHANNEL_ID is None:
            print("[revisar_tareas] CHANNEL_ID no configurado")
            return
        tareas = cargar_tareas()
        ahora = datetime.now()
        dia_actual = ahora.strftime('%A').lower()
        hora_actual = ahora.strftime('%H:%M')
        canal = bot.get_channel(CHANNEL_ID)
        if canal is None:
            print(f"[revisar_tareas] Canal con ID {CHANNEL_ID} no encontrado")
            return
        # Revisar cada día
        for dia, lista_tareas in tareas.items():
            if dia.lower() == dia_actual:
                for tarea in lista_tareas:
                    if tarea['hora'] == hora_actual and not tarea.get('enviado', False):
                        # Crear embed personalizado
                        embed = obtener_embed_tarea(tarea, hora_actual)
                        # Mencionar rol si está configurado
                        menciones = ""
                        if ROLE_ID:
                            rol = bot.get_guild(canal.guild.id).get_role(ROLE_ID) if canal.guild else None
                            menciones = f"{rol.mention} " if rol else ""
                        mensaje_texto = f"{menciones}¡Hay gente esperando en la calle, no los hagáis esperar!" if tarea.get('tipo') == 'taxi' \
                                       else f"{menciones}El bus no se conduce solo, ¡arrancad ya!" if tarea.get('tipo') == 'bus_interurbano' \
                                       else f"{menciones}Los trasnochadores necesitan volver a casa. ¡Moveros!" if tarea.get('tipo') == 'bus_urbano' \
                                       else f"{menciones}Alguien importante requiere vuestros servicios. ¡Rápido!" if tarea.get('tipo') == 'cliente_vip' \
                                       else f"{menciones}Se necesita fuerza y maña. ¡Al almacén ya mismo!" if tarea.get('tipo') == 'mudanza' \
                                       else menciones
                        # Enviar mensajes al canal
                        await canal.send(embed=embed)
                        if mensaje_texto:
                            await canal.send(mensaje_texto)
                        # Marcar como enviado
                        tarea['enviado'] = True
                        guardar_tareas(tareas)
    except Exception as e:
        print(f"[revisar_tareas ERROR] {e}")
        import traceback
        traceback.print_exc()

# Comando para agregar una tarea
@bot.command(name='addtarea')
async def agregar_tarea(ctx, dia: str, hora: str, tipo: str, *, nombre: str):
    """
    Agrega una nueva tarea
    Uso: !addtarea Monday 09:00 taxi Recordatorio de taxi
    Tipos: taxi, bus_interurbano, bus_urbano, cliente_vip, mudanza
    """
    dias_validos = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    tipos_validos = ['taxi', 'bus_interurbano', 'bus_urbano', 'cliente_vip', 'mudanza']
    
    if dia not in dias_validos:
        await ctx.send(f"❌ Día inválido. Usa: {', '.join(dias_validos)}")
        return
    
    if tipo not in tipos_validos:
        await ctx.send(f"❌ Tipo inválido. Usa: {', '.join(tipos_validos)}")
        return
    
    try:
        # Validar formato de hora
        datetime.strptime(hora, '%H:%M')
    except ValueError:
        await ctx.send("❌ Formato de hora inválido. Usa HH:MM (ej: 09:00)")
        return
    
    tareas = cargar_tareas()
    
    if dia not in tareas:
        tareas[dia] = []
    
    nueva_tarea = {
        'nombre': nombre,
        'mensaje': '',
        'hora': hora,
        'tipo': tipo,
        'enviado': False
    }
    
    tareas[dia].append(nueva_tarea)
    guardar_tareas(tareas)
    
    await ctx.send(f"✅ Tarea agregada para {dia} a las {hora}")

# Comando para ver todas las tareas
@bot.command(name='listatareas')
async def listar_tareas(ctx):
    """Muestra todas las tareas configuradas del día"""
    tareas = cargar_tareas()
    
    if not tareas:
        await ctx.send("📭 No hay tareas configuradas")
        return
    
    # Emojis por tipo de servicio
    emojis_tipo = {
        'taxi': '🚕',
        'bus_interurbano': '🚌',
        'bus_urbano': '🚌',
        'cliente_vip': '🥂',
        'mudanza': '🚚'
    }
    
    # Usar las tareas del lunes como referencia (todas los días son iguales)
    lista_tarea = tareas.get('Monday', [])
    
    if not lista_tarea:
        await ctx.send("📭 No hay tareas configuradas")
        return
    
    # Agrupar tareas por hora
    tareas_por_hora = {}
    for tarea in lista_tarea:
        hora = tarea['hora']
        if hora not in tareas_por_hora:
            tareas_por_hora[hora] = []
        tareas_por_hora[hora].append({
            'tipo': tarea.get('tipo', 'general'),
            'nombre': tarea['nombre']
        })
    
    # Ordenar horas
    horas_ordenadas = sorted(tareas_por_hora.keys())
    
    # Crear embed
    embed = discord.Embed(
        title="⏰ TAREAS PROGRAMADAS",
        description="📅 Rutina diaria de transporte",
        color=discord.Color.from_rgb(255, 165, 0)  # Naranja
    )
    
    # Agregar tareas por hora
    for hora in horas_ordenadas:
        lista_tareas_hora = tareas_por_hora[hora]
        
        # Construir contenido
        contenido = ""
        for tarea in lista_tareas_hora:
            tipo = tarea['tipo']
            emoji = emojis_tipo.get(tipo, '📋')
            contenido += f"{emoji} {tarea['nombre']}\n"
        
        # Título del campo con la cantidad
        cantidad = len(lista_tareas_hora)
        titulo_hora = f"🕐 {hora} - {cantidad} tarea{'s' if cantidad > 1 else ''}"
        
        embed.add_field(name=titulo_hora, value=contenido, inline=False)
    
    await ctx.send(embed=embed)

# Comando para eliminar una tarea
@bot.command(name='deltarea')
async def eliminar_tarea(ctx, dia: str, indice: int):
    """
    Elimina una tarea
    Uso: !deltarea Monday 0 (elimina la primera tarea del lunes)
    """
    tareas = cargar_tareas()
    
    if dia not in tareas or indice < 0 or indice >= len(tareas[dia]):
        await ctx.send("❌ Día o índice de tarea inválido")
        return
    
    tarea_eliminada = tareas[dia].pop(indice)
    guardar_tareas(tareas)
    
    await ctx.send(f"✅ Tarea eliminada: {tarea_eliminada['nombre']}")

# Comando para resetear las tareas del día
@bot.command(name='reseteardia')
async def resetear_dia(ctx, dia: str = None):
    """
    Resetea las tareas del día (marca como no enviadas)
    Usa !reseteardia Monday para un día específico, o !reseteardia para el día actual
    """
    tareas = cargar_tareas()
    
    if dia is None:
        dia = datetime.now().strftime('%A')
    
    if dia not in tareas:
        await ctx.send(f"❌ No hay tareas para {dia}")
        return
    
    for tarea in tareas[dia]:
        tarea['enviado'] = False
    
    guardar_tareas(tareas)
    await ctx.send(f"✅ Tareas de {dia} marcadas como no enviadas")

# Ejecutar el bot
if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if not TOKEN:
        print("❌ ERROR: DISCORD_TOKEN no configurado en .env")
        print("Sigue estos pasos:")
        print("1. Copia .env.example a .env")
        print("2. Edita .env y pega tu token de Discord")
        print("3. Guarda el archivo")
        print("4. Ejecuta este script de nuevo")
        exit()
    
    bot.run(TOKEN)

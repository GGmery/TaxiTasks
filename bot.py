import discord
from discord.ext import commands, tasks
import json
from datetime import datetime, timedelta
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
CHANNEL_ID = None  # Se configurará con !setup en el servidor
ROLE_ID = None  # Se configurará con !setup en el servidor

DIAS_VALIDOS = {
    'monday': 'Monday',
    'tuesday': 'Tuesday',
    'wednesday': 'Wednesday',
    'thursday': 'Thursday',
    'friday': 'Friday',
    'saturday': 'Saturday',
    'sunday': 'Sunday'
}

TIPOS_VALIDOS = ['taxi', 'bus_interurbano', 'bus_urbano', 'cliente_vip', 'mudanza']

# Cargar tareas desde el archivo JSON
def cargar_tareas():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# helper day normalization
def normalizar_dia(dia):
    if not dia:
        return None
    clave = dia.strip().lower()
    return DIAS_VALIDOS.get(clave)

# Handler para comandos desconocidos
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        comandos = [
            '!setup',
            '!addtarea',
            '!listatareas',
            '!deltarea',
            '!reseteardia'
        ]
        ayuda = '\n'.join(comandos)
        await ctx.send(f"❌ No te he entendido. Puedes usar estos comandos:\n{ayuda}")
    else:
        raise error

# Evento para responder a menciones sobre tareas próximas
@bot.event
async def on_message(message):
    try:
        if message.author.bot:
            return
        # Solo responder si mencionan al bot Y preguntan por tareas
        if bot.user in message.mentions and ("tarea" in message.content.lower() or "tareas" in message.content.lower()):
            ahora = datetime.now()
            tareas = cargar_tareas()
            
            # Obtener solo las tareas del día actual
            dia_actual = ahora.strftime('%A')  # Formato: Monday, Tuesday, etc.
            todas_tareas = tareas.get(dia_actual, [])
            
            # Tareas activas ahora (asumiendo duran 1 hora)
            activas = []
            proxima_tarea = None
            tiempo_proxima = float('inf')
            
            for tarea in todas_tareas:
                try:
                    hora_tarea = datetime.strptime(tarea['hora'], '%H:%M').replace(year=ahora.year, month=ahora.month, day=ahora.day)
                    hora_fin = hora_tarea + timedelta(hours=1)
                    
                    if hora_tarea <= ahora < hora_fin:
                        # Activa ahora
                        activas.append(tarea)
                    else:
                        # Buscar la más próxima dentro de 15 minutos
                        minutos_falta = (hora_tarea - ahora).total_seconds() / 60
                        if 0 <= minutos_falta < 15 and minutos_falta < tiempo_proxima:
                            proxima_tarea = tarea
                            tiempo_proxima = minutos_falta
                except Exception:
                    continue
            
            # Construir respuesta amigable
            usuario = message.author.mention
            respuesta = f"¡Hola {usuario}!\n\n"
            
            # Tareas activas
            if activas:
                if len(activas) == 1:
                    tarea = activas[0]
                    tipo = tarea.get('tipo', 'general')
                    emoji = {
                        'taxi': '🚕',
                        'bus_interurbano': '🚌',
                        'bus_urbano': '🚌',
                        'cliente_vip': '🥂',
                        'mudanza': '🚚'
                    }.get(tipo, '📋')
                    respuesta += f"📌 **Ahora mismo:** {emoji} {tarea.get('nombre', '<sin nombre>')}\n"
                else:
                    respuesta += "📌 **Ahora mismo tienes varias tareas:**\n"
                    for tarea in activas:
                        tipo = tarea.get('tipo', 'general')
                        emoji = {
                            'taxi': '🚕',
                            'bus_interurbano': '🚌',
                            'bus_urbano': '🚌',
                            'cliente_vip': '🥂',
                            'mudanza': '🚚'
                        }.get(tipo, '📋')
                        respuesta += f"  {emoji} {tarea.get('nombre', '<sin nombre>')}\n"
            else:
                respuesta += "📌 **Ahora mismo:** Estás libre\n"
            
            respuesta += "\n"
            
            # Próxima tarea
            if proxima_tarea:
                tipo = proxima_tarea.get('tipo', 'general')
                emoji = {
                    'taxi': '🚕',
                    'bus_interurbano': '🚌',
                    'bus_urbano': '🚌',
                    'cliente_vip': '🥂',
                    'mudanza': '🚚'
                }.get(tipo, '📋')
                hora_prox = proxima_tarea.get('hora', 'N/A')
                minutos = int(tiempo_proxima)
                respuesta += f"⏰ **Próxima tarea:** {emoji} {proxima_tarea.get('nombre', '<sin nombre>')}\n    En {minutos} minutos (a las {hora_prox})"
            else:
                respuesta += "⏰ **Próximas horas:** ¡Tienes las horas libres, descansa! 😎"
            
            await message.reply(respuesta)
        else:
            await bot.process_commands(message)
    except Exception as e:
        print(f"[on_message ERROR] {e}")
        import traceback
        traceback.print_exc()

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
async def setup(ctx, canal: str = None, rol: str = None):
    """Configura el canal donde se enviarán los recordatorios y el rol a mencionar
    Uso: !setup #nombre-canal @nombre-rol
    Si no especificas canal, usa el actual.
    """
    global CHANNEL_ID, ROLE_ID
    try:
        if canal is None:
            canal_obj = ctx.channel
        else:
            # Convertir string a canal
            canal_obj = await commands.TextChannelConverter().convert(ctx, canal)
        
        rol_obj = None
        if rol is not None:
            # Convertir string a rol
            rol_obj = await commands.RoleConverter().convert(ctx, rol)
        
        CHANNEL_ID = canal_obj.id
        ROLE_ID = rol_obj.id if rol_obj else None
        
        await ctx.send(f"✅ Canal configurado: {canal_obj.mention}")
        if rol_obj:
            await ctx.send(f"✅ Rol a mencionar: {rol_obj.mention}")
    except commands.ChannelNotFound:
        await ctx.send("❌ Canal no encontrado. Usa !setup #nombre-del-canal")
    except commands.RoleNotFound:
        await ctx.send("❌ Rol no encontrado. Usa !setup #canal @nombre-del-rol")
    except Exception as e:
        await ctx.send(f"❌ Error al configurar: {e}")
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
            return  # Espera configuración con !setup
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
    dia_normal = normalizar_dia(dia)
    if not dia_normal:
        await ctx.send(f"❌ Día inválido. Usa: {', '.join(DIAS_VALIDOS.values())}")
        return

    if tipo not in TIPOS_VALIDOS:
        await ctx.send(f"❌ Tipo inválido. Usa: {', '.join(TIPOS_VALIDOS)}")
        return
    
    try:
        # Validar formato de hora
        datetime.strptime(hora, '%H:%M')
    except ValueError:
        await ctx.send("❌ Formato de hora inválido. Usa HH:MM (ej: 09:00)")
        return
    
    tareas = cargar_tareas()
    
    if dia_normal not in tareas:
        tareas[dia_normal] = []
    
    nueva_tarea = {
        'nombre': nombre,
        'mensaje': '',
        'hora': hora,
        'tipo': tipo,
        'enviado': False
    }
    
    tareas[dia_normal].append(nueva_tarea)
    guardar_tareas(tareas)
    
    await ctx.send(f"✅ Tarea agregada para {dia_normal} a las {hora}")

# Comando para ver todas las tareas
@bot.command(name='listatareas')
async def listar_tareas(ctx, dia: str = None):
    """
    Lista las tareas del día especificado, o del día actual si no se especifica
    Uso: !listatareas o !listatareas Monday
    """
    import discord
    tareas = cargar_tareas()
    DIAS_ESP = {
        'Monday': 'Lunes',
        'Tuesday': 'Martes',
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    if dia is None:
        # Si no especifica día, usa el actual
        dia_mostrar = datetime.now().strftime('%A')
    else:
        dia_mostrar = normalizar_dia(dia)
        if not dia_mostrar:
            await ctx.send(f"❌ Día inválido. Usa: {', '.join(DIAS_VALIDOS.values())}")
            return
    lista_tareas = tareas.get(dia_mostrar, [])
    if not lista_tareas:
        await ctx.send(f"No hay tareas para {DIAS_ESP.get(dia_mostrar, dia_mostrar)}")
        return
    # Agrupar tareas por hora
    tareas_por_hora = {}
    for tarea in lista_tareas:
        hora = tarea.get('hora', 'N/A')
        if hora not in tareas_por_hora:
            tareas_por_hora[hora] = []
        tareas_por_hora[hora].append(tarea)
    horas_ordenadas = sorted(tareas_por_hora.keys())
    # Crear embed
    embed = discord.Embed(
        title=f"⏰ {DIAS_ESP.get(dia_mostrar, dia_mostrar)} - TAREAS PROGRAMADAS",
        description="📅 Rutina semanal de transporte",
        color=discord.Color.blue()
    )
    for hora in horas_ordenadas:
        tareas_hora = tareas_por_hora[hora]
        field_value = f"🕐 {hora} - {len(tareas_hora)} tarea{'s' if len(tareas_hora) > 1 else ''}\n"
        for tarea in tareas_hora:
            tipo = tarea.get('tipo', 'general')
            emoji = {
                'taxi': '🚕',
                'bus_interurbano': '🚌',
                'bus_urbano': '🚌',
                'cliente_vip': '🥂',
                'mudanza': '🚚'
            }.get(tipo, '📋')
            nombre = tarea.get('nombre', '<sin nombre>')
            field_value += f"{hora} - {emoji} {nombre}\n"
        embed.add_field(name="", value=field_value, inline=False)
    await ctx.send(embed=embed)

# Comando para eliminar una tarea
@bot.command(name='deltarea')
async def eliminar_tarea(ctx, dia: str, indice: int):
    """
    Elimina una tarea
    Uso: !deltarea Monday 0 (elimina la primera tarea del lunes)
    """
    dia_normal = normalizar_dia(dia)
    if not dia_normal:
        await ctx.send("❌ Día inválido")
        return

    tareas = cargar_tareas()

    if dia_normal not in tareas or indice < 0 or indice >= len(tareas[dia_normal]):
        await ctx.send("❌ Día o índice de tarea inválido")
        return

    tarea_eliminada = tareas[dia_normal].pop(indice)
    guardar_tareas(tareas)

    await ctx.send(f"✅ Tarea eliminada: {tarea_eliminada['nombre']}")

# Comando para resetear las tareas del día
@bot.command(name='reseteardia')
async def resetear_dia(ctx, dia: str = None):
    """
    Resetea las tareas del día (marca como no enviadas)
    Usa !reseteardia Monday para un día específico, o !reseteardia para el día actual
    """
    if dia is None:
        dia = datetime.now().strftime('%A')

    dia_normal = normalizar_dia(dia)
    if not dia_normal:
        await ctx.send('❌ Día inválido')
        return

    tareas = cargar_tareas()
    
    if dia_normal not in tareas:
        await ctx.send(f"❌ No hay tareas para {dia_normal}")
        return
    
    for tarea in tareas[dia_normal]:
        tarea['enviado'] = False
    
    guardar_tareas(tareas)
    await ctx.send(f"✅ Tareas de {dia_normal} marcadas como no enviadas")

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

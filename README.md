# TaxiTasks - Bot de Discord para Recordatorios de Tareas de Transporte

Un bot de Discord que te avisa de las tareas que debes hacer cada día de la semana.

## Instalación

1. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

2. **Configura el token:**
   - Copia el archivo `.env.example` a `.env`
   ```bash
   copy .env.example .env
   ```
   - Abre el archivo `.env` y reemplaza `tu_token_secreto_aqui` con tu token real
   - **⚠️ IMPORTANTE: Nunca subas el archivo `.env` a GitHub (está en `.gitignore`)**

3. **Obtén tu token de Discord:**
   - Ve a [Discord Developer Portal](https://discord.com/developers/applications)
   - Crea una nueva aplicación
   - Ve a la sección "Bot" y crea un bot
   - Copia el token y pégalo en `.env`

4. **Invita el bot a tu servidor:**
   - En Developer Portal, ve a OAuth2 > URL Generator
   - Selecciona los scopes: `bot`
   - Selecciona los permisos: `Send Messages`, `Embed Links`
   - Abre la URL generada y selecciona tu servidor

## Uso

### Comandos del Bot

**1. Configurar canal (obligatorio primero):**
```
!setup #nombre-del-canal
```
Si no especificas canal, usa el canal actual.

**2. Agregar una tarea:**
```
!addtarea DíaDeLaSemana HH:MM Nombre de la tarea - Descripción del mensaje
```

**Ejemplo:**
```
!addtarea Monday 09:00 Reunión - Recordatorio: Reunión de equipo a las 9:00 AM
!addtarea Wednesday 14:30 Entregar reporte - No olvides entregar el reporte
```

Días válidos: `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday`, `Sunday`

**3. Ver todas las tareas:**
```
!listatareas
```

**4. Eliminar una tarea:**
```
!deltarea DíaDeLaSemana índice
```

**Ejemplo:**
```
!deltarea Monday 0  (elimina la primera tarea del lunes)
```

**5. Resetear tareas del día:**
```
!reseteardia DíaDeLaSemana
```
O sin especificar para el día actual:
```
!reseteardia
```

## Estructura de Archivos

```
TaxiTasks/
├── bot.py                          # Archivo principal del bot
├── cargar_tareas_predefinidas.py   # Script para cargar tareas
├── requirements.txt                # Dependencias
├── .env.example                    # Plantilla de configuración (COPIA a .env)
├── .env                            # ⚠️ NO SE SUBE (contiene token secreto)
├── .gitignore                      # Archivos que NO se suben a GitHub
├── tareas.json                     # Se crea automáticamente con las tareas
└── README.md                       # Este archivo
```

## Seguridad ⚠️

- El archivo `.env` **NUNCA** se sube a GitHub (está en `.gitignore`)
- El token en `.env.example` es solo un ejemplo
- Todos los tokens sensibles están protegidos en `.gitignore`

## Notas

- El archivo `tareas.json` se crea automáticamente cuando agregas la primera tarea
- Las tareas se almacenan en formato JSON
- El bot revisa las tareas cada minuto
- Los horarios deben estar en formato 24 horas (HH:MM)
## Ejecución

1. **Carga las tareas predefinidas:**
```powershell
python cargar_tareas_predefinidas.py
```

2. **Ejecuta el bot:**
```powershell
python bot.py
```

3. **En Discord, configura el bot:**
```
!setup #canal-recordatorios @RolATaxistas
```

El bot empezará a enviar recordatorios automáticos cada día
- Qué tipo de mensajes quieres recibir (simples, con emojis, detalladoss, etc.)

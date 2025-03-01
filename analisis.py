import sqlite3
import pandas as pd
from datetime import datetime

# 1) Conectamos y leemos los datos
conn = sqlite3.connect("incidencias.db")
df_tickets = pd.read_sql_query("SELECT * FROM tickets", conn)
df_contactos = pd.read_sql_query("SELECT * FROM contactos_empleados", conn)
conn.close()

# 2) Convertimos las columnas de fecha a tipo datetime
df_tickets["fecha_apertura"] = pd.to_datetime(df_tickets["fecha_apertura"])
df_tickets["fecha_cierre"]   = pd.to_datetime(df_tickets["fecha_cierre"])
df_contactos["fecha"]        = pd.to_datetime(df_contactos["fecha"])

# 3) Calculamos la fecha de último contacto de cada ticket
df_max_contact = (
    df_contactos.groupby("id_ticket")["fecha"]
    .max()                               # fecha máxima por ticket
    .reset_index(name="last_contact")
)

# 4) Hacemos un merge para añadir esa columna a df_tickets
df_tickets = df_tickets.merge(df_max_contact, on="id_ticket", how="left")

# 5) Sobrescribimos fecha_cierre con la última actuación (si es mayor)
#    Para ello, tomamos el máximo entre [fecha_cierre original, last_contact]
df_tickets["fecha_cierre"] = df_tickets[["fecha_cierre", "last_contact"]].max(axis=1)

# -----------------------------------------------------------------------------
#                                   Análisis
# -----------------------------------------------------------------------------

# 1) Número de incidencias totales
total_incidencias = len(df_tickets)

# 2) Incidencias con satisfaccion_cliente >= 5
df_satis_5 = df_tickets[df_tickets["satisfaccion_cliente"] >= 5]
num_satis_5 = len(df_satis_5)

# Media y desviación std del total de incidencias (con sat >=5) por cliente
group_satis = df_satis_5.groupby("cliente").size()
media_satis_5 = group_satis.mean()
std_satis_5 = group_satis.std(ddof=1)

# 3) Media y std de número de incidentes por cliente
group_incidencias = df_tickets.groupby("cliente").size()
media_incid = group_incidencias.mean()
std_incid = group_incidencias.std(ddof=1)

# 4) Sumar horas de cada incidencia
horas_por_ticket = df_contactos.groupby("id_ticket")["tiempo"].sum().reset_index()
horas_por_ticket.columns = ["id_ticket", "horas_totales_incidente"]

media_horas = horas_por_ticket["horas_totales_incidente"].mean()
std_horas = horas_por_ticket["horas_totales_incidente"].std(ddof=1)

# 5) Mín y máx del total de horas realizadas por los empleados
horas_por_empleado = df_contactos.groupby("id_emp")["tiempo"].sum().reset_index()
min_horas = horas_por_empleado["tiempo"].min()
max_horas = horas_por_empleado["tiempo"].max()

# 6) Mín y máx del tiempo entre apertura y cierre en días
#    (Ya con fecha_cierre corregida)
df_tickets["duracion_dias"] = (df_tickets["fecha_cierre"] - df_tickets["fecha_apertura"]).dt.days
min_duracion = df_tickets["duracion_dias"].min()
max_duracion = df_tickets["duracion_dias"].max()

# 7) Mín y máx del número de incidentes atendidos por cada empleado
tickets_por_empleado = df_contactos.groupby("id_emp")["id_ticket"].nunique().reset_index()
min_incid_emp = tickets_por_empleado["id_ticket"].min()
max_incid_emp = tickets_por_empleado["id_ticket"].max()

# -----------------------------------------------------------------------------
# Mostramos los resultados
# -----------------------------------------------------------------------------
print(f"Total de incidencias: {total_incidencias}")
print(f"Media de incidencias (con sat >= 5) por cliente: {media_satis_5:.2f}, Desv: {std_satis_5:.2f}")
print(f"Media de incidencias por cliente: {media_incid:.2f}, Desv: {std_incid:.2f}")
print(f"Media de horas por incidencia: {media_horas:.2f}, Desv: {std_horas:.2f}")
print(f"Mín de horas totales por empleado: {min_horas:.2f}, Máx: {max_horas:.2f}")
print(f"Mín de duración (días) de un ticket: {min_duracion}, Máx: {max_duracion}")
print(f"Mín # incidencias atendidas por un empleado: {min_incid_emp}, Máx: {max_incid_emp}")

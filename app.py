from flask import Flask, render_template
import analisis

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/resultados")
def resultados():
    # Variables generales de analisis.py
    total_incid = analisis.total_incidencias
    media_satis_5 = analisis.media_satis_5
    std_satis_5 = analisis.std_satis_5
    media_incid = analisis.media_incid
    std_incid = analisis.std_incid
    media_horas = analisis.media_horas
    std_horas = analisis.std_horas
    min_horas = analisis.min_horas
    max_horas = analisis.max_horas
    min_duracion = analisis.min_duracion
    max_duracion = analisis.max_duracion
    min_incid_emp = analisis.min_incid_emp
    max_incid_emp = analisis.max_incid_emp

    # Diccionario con los resultados de las agrupaciones
    agrupaciones = {
        "Empleado": {
            "tabla": analisis.group_empleado.to_html(classes="table", index=False),
            "estadisticas": {
                "Mediana": analisis.mediana_empleado,
                "Media": analisis.media_empleado,
                "Varianza": analisis.varianza_empleado,
                "Máximo": analisis.max_empleado,
                "Mínimo": analisis.min_empleado
            }
        },
        "Nivel": {
            "tabla": analisis.group_nivel.to_html(classes="table", index=False),
            "estadisticas": {
                "Mediana": analisis.mediana_nivel,
                "Media": analisis.media_nivel,
                "Varianza": analisis.varianza_nivel,
                "Máximo": analisis.max_nivel,
                "Mínimo": analisis.min_nivel
            }
        },
        "Cliente": {
            "tabla": analisis.group_cliente.to_html(classes="table", index=False),
            "estadisticas": {
                "Mediana": analisis.mediana_cliente,
                "Media": analisis.media_cliente,
                "Varianza": analisis.varianza_cliente,
                "Máximo": analisis.max_cliente,
                "Mínimo": analisis.min_cliente
            }
        },
        "Tipo incidencia": {
            "tabla": analisis.group_incidencia.to_html(classes="table", index=False),
            "estadisticas": {
                "Mediana": analisis.mediana_incidencia,
                "Media": analisis.media_incidencia,
                "Varianza": analisis.varianza_incidencia,
                "Máximo": analisis.max_incidencia,
                "Mínimo": analisis.min_incidencia
            }
        },
        "Día de la semana": {
            "tabla": analisis.group_dia.to_html(classes="table", index=False),
            "estadisticas": {
                "Mediana": analisis.mediana_dia,
                "Media": analisis.media_dia,
                "Varianza": analisis.varianza_dia,
                "Máximo": analisis.max_dia,
                "Mínimo": analisis.min_dia
            }
        }
    }

    return render_template(
        "resultados.html",
        total=total_incid,
        media_satis_5=media_satis_5,
        std_satis_5=std_satis_5,
        media_incid=media_incid,
        std_incid=std_incid,
        media_horas=media_horas,
        std_horas=std_horas,
        min_horas=min_horas,
        max_horas=max_horas,
        min_duracion=min_duracion,
        max_duracion=max_duracion,
        min_incid_emp=min_incid_emp,
        max_incid_emp=max_incid_emp,
        agrupaciones=agrupaciones  # Pasamos el diccionario al template
    )

if __name__ == "__main__":
    app.run(debug=True)

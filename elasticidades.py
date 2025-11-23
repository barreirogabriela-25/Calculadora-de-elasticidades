import sympy as sp

# Definimos las variables simbolicas
ingreso, precio1, precio2 = sp.symbols('I p1 p2', real=True)

def clasificar_elasticidad(valor_elasticidad):
    """
    Clasifica la elasticidad por magnitud y devuelve:
    (clasificacion_texto, descripcion_corta, explicacion_magnitud)
    """
    # protección por si llega None
    if valor_elasticidad is None:
        return "NO DISPONIBLE", "-", "-"

    valor_absoluto = abs(valor_elasticidad)
    if valor_elasticidad == 0:
        clasificacion = "PERFECTAMENTE INELÁSTICA"
        descripcion = "La demanda no cambia cuando cambia el precio."
        explicacion = "Cambio en cantidad = 0 ante cambio en precio."
    elif 0 < valor_absoluto < 1:
        clasificacion = "INELÁSTICA"
        descripcion = "La demanda es poco sensible a cambios de precio."
        explicacion = "El cambio porcentual en cantidad es menor que el del precio."
    elif valor_absoluto == 1:
        clasificacion = "ELASTICIDAD UNITARIA"
        descripcion = "El cambio porcentual en cantidad = cambio porcentual en precio."
        explicacion = "Ingreso total se mantiene aproximadamente constante."
    elif valor_absoluto > 1:
        clasificacion = "ELÁSTICA"
        descripcion = "La demanda es muy sensible a cambios de precio."
        explicacion = "El cambio porcentual en cantidad es mayor que el del precio."
    else:
        clasificacion = "NO CLASIFICABLE"
        descripcion = "Valor fuera del rango interpretativo."
        explicacion = "-"
    return clasificacion, descripcion, explicacion

# --- Inicio del programa ---
print("=" * 70)
print("ANALIZADOR DE ELASTICIDADES DE DEMANDA")
print("=" * 70)
print("\n INSTRUCCIONES PARA INGRESAR LA FUNCIÓN:")
print("• Use '*' para multiplicación: ej: 2*p1, 0.5*I")
print("• Use '**' para exponentes: ej: p1**2, I**0.5")
print("• Variables disponibles: p1 (precio propio), p2 (precio otro bien), I (ingreso)")
print("• Operadores: +, -, *, /, **")
print("\n EJEMPLOS VÁLIDOS:")
print("  • 100 - 2*p1 + 0.5*p2")
print("  • 50/(1 + p1**2) + 0.3*I")
print("  • 20*p1**(-0.5) + 1.5*p2 + 0.1*I")
print("  • (100 - p1)**2 + 2*I")
print("=" * 70)

funcion_ingresada = input("\nIngrese la función de Demanda: ").strip()

try:
    funcion = sp.sympify(funcion_ingresada, locals={'I': ingreso, 'p1': precio1, 'p2': precio2})
except sp.SympifyError:
    print("\n Error: La función ingresada no es válida.")
    print("Revise que:")
    print("  • Use '*' para multiplicaciones")
    print("  • Use '**' para potencias")
    print("  • Los paréntesis estén balanceados")
    print("  • Solo use las variables p1, p2, I")
    funcion = None
except Exception as error:
    print(f"\n Error inesperado: {error}")
    funcion = None

if funcion:
    # Calculamos las derivadas
    derivada_ingreso = sp.diff(funcion, ingreso)
    derivada_precio1 = sp.diff(funcion, precio1)
    derivada_precio2 = sp.diff(funcion, precio2)

    # Detectar qué variables están presentes
    variables_en_funcion = []
    derivadas_fijas = []

    # Verificar si cada variable está presente en la función
    if funcion.has(precio1):
        variables_en_funcion.append('precio1')
        # Verificar si la derivada es constante
        if not (derivada_precio1.has(precio1) or derivada_precio1.has(precio2) or derivada_precio1.has(ingreso)):
            derivadas_fijas.append('precio1')

    if funcion.has(precio2):
        variables_en_funcion.append('precio2')
        if not (derivada_precio2.has(precio1) or derivada_precio2.has(precio2) or derivada_precio2.has(ingreso)):
            derivadas_fijas.append('precio2')

    if funcion.has(ingreso):
        variables_en_funcion.append('ingreso')
        if not (derivada_ingreso.has(precio1) or derivada_ingreso.has(precio2) or derivada_ingreso.has(ingreso)):
            derivadas_fijas.append('ingreso')

    # Ingreso de valores numéricos - solo para variables presentes
    try:
        print("\n" + "=" * 50)
        print("INGRESO DE VALORES NUMÉRICOS")
        print("=" * 50)

        valores_sustitucion = {}

        # Solo pedir precio1 si está presente en la función
        if 'precio1' in variables_en_funcion and 'precio1' not in derivadas_fijas:
            valor_precio1 = float(input("Ingrese el valor del precio propio (p1): "))
            valores_sustitucion[precio1] = valor_precio1
        elif 'precio1' in derivadas_fijas:
            print("precio1: Derivada constante - no requiere valor específico")
            valor_precio1 = 1
            valores_sustitucion[precio1] = valor_precio1

        # Solo pedir precio2 si está presente en la función
        if 'precio2' in variables_en_funcion and 'precio2' not in derivadas_fijas:
            valor_precio2 = float(input("Ingrese el valor del precio del otro bien (p2): "))
            valores_sustitucion[precio2] = valor_precio2
        elif 'precio2' in derivadas_fijas:
            print("precio2: Derivada constante - no requiere valor específico")
            valor_precio2 = 1
            valores_sustitucion[precio2] = valor_precio2

        # Solo pedir ingreso si está presente en la función
        if 'ingreso' in variables_en_funcion and 'ingreso' not in derivadas_fijas:
            valor_ingreso = float(input("Ingrese el valor del ingreso (I): "))
            valores_sustitucion[ingreso] = valor_ingreso
        elif 'ingreso' in derivadas_fijas:
            print("ingreso: Derivada constante - no requiere valor específico")
            valor_ingreso = 1
            valores_sustitucion[ingreso] = valor_ingreso

        # Si no hay variables presentes, usar valores por defecto
        if not variables_en_funcion:
            print("Función constante - usando valores por defecto para cálculo")
            valor_precio1, valor_precio2, valor_ingreso = 1, 1, 1
            valores_sustitucion = {precio1: valor_precio1, precio2: valor_precio2, ingreso: valor_ingreso}
        else:
            # Completar con valores por defecto para variables no presentes
            if precio1 not in valores_sustitucion:
                valor_precio1 = 1
                valores_sustitucion[precio1] = valor_precio1
            else:
                valor_precio1 = valores_sustitucion[precio1]

            if precio2 not in valores_sustitucion:
                valor_precio2 = 1
                valores_sustitucion[precio2] = valor_precio2
            else:
                valor_precio2 = valores_sustitucion[precio2]

            if ingreso not in valores_sustitucion:
                valor_ingreso = 1
                valores_sustitucion[ingreso] = valor_ingreso
            else:
                valor_ingreso = valores_sustitucion[ingreso]

        # Evaluar la función y las derivadas en el punto
        valor_funcion = float(funcion.subs(valores_sustitucion))

        # Control: división por cero
        if abs(valor_funcion) < 1e-12:
            print("Error: La función evaluada es 0 → no se puede calcular elasticidad (división por cero).")
        else:
            # Valores numéricos de las derivadas
            derivada_precio1_num = float(derivada_precio1.subs(valores_sustitucion))
            derivada_precio2_num = float(derivada_precio2.subs(valores_sustitucion))
            derivada_ingreso_num  = float(derivada_ingreso.subs(valores_sustitucion))

            # Cálculo de elasticidades
            elasticidad_precio1 = derivada_precio1_num * (valor_precio1 / valor_funcion) if 'precio1' in variables_en_funcion else 0
            elasticidad_precio2 = derivada_precio2_num * (valor_precio2 / valor_funcion) if 'precio2' in variables_en_funcion else 0
            elasticidad_ingreso  = derivada_ingreso_num  * (valor_ingreso  / valor_funcion) if 'ingreso' in variables_en_funcion else 0

            # Redondeo de valores para mostrar
            derivada_precio1_red = round(derivada_precio1_num, 2)
            derivada_precio2_red = round(derivada_precio2_num, 2)
            derivada_ingreso_red  = round(derivada_ingreso_num, 2)

            elasticidad_precio1_red = round(elasticidad_precio1, 2) if 'precio1' in variables_en_funcion else 0
            elasticidad_precio2_red = round(elasticidad_precio2, 2) if 'precio2' in variables_en_funcion else 0
            elasticidad_ingreso_red  = round(elasticidad_ingreso, 2) if 'ingreso' in variables_en_funcion else 0

            # --- Impresión de resultados ---
            print("\n" + "="*60)
            print("RESULTADOS DE ELASTICIDAD Y CLASIFICACIÓN DE BIENES")
            print("="*60)

            # --- Elasticidad precio propia ---
            if 'precio1' not in variables_en_funcion:
                print("\nElasticidad precio propia:")
                print("La función no depende del precio propio → no corresponde calcular elasticidad precio propia.")
            elif derivada_precio1_num == 0:
                print("\nElasticidad precio propia:")
                print("Derivada respecto al precio propio es cero → elasticidad cero.")
            else:
                clasif_precio1, desc_precio1, exp_precio1 = clasificar_elasticidad(elasticidad_precio1_red)
                print("\nElasticidad precio propia:")
                print(f"Derivada evaluada: {derivada_precio1_red}")
                print(f"Elasticidad: {elasticidad_precio1_red}")
                print(f"Clasificación: {clasif_precio1}")

                # Tipo de bien según signo de la derivada
                if derivada_precio1_num < 0:
                    tipo_bien = "TÍPICO"
                elif derivada_precio1_num > 0:
                    tipo_bien = "GIFFEN"
                else:
                    tipo_bien = "INDEPENDIENTE"

                print(f"Tipo de bien: {tipo_bien}")
                print(f"Descripción: {desc_precio1}")
                print(f"Explicación: {exp_precio1}")

            # --- Elasticidad cruzada ---
            if 'precio2' not in variables_en_funcion:
                print("\nElasticidad cruzada:")
                print("La función no depende del precio del otro bien → no corresponde calcular elasticidad cruzada.")
            elif derivada_precio2_num == 0:
                print("\nElasticidad cruzada:")
                print("Derivada respecto al precio del otro bien es cero → elasticidad cruzada cero.")
            else:
                print("\nElasticidad cruzada:")
                print(f"Derivada evaluada: {derivada_precio2_red}")
                print(f"Elasticidad cruzada: {elasticidad_precio2_red}")
                if elasticidad_precio2_red > 0:
                    tipo_relacion = "SUSTITUTO"
                    exp_relacion = "La demanda del bien 1 aumenta si sube el precio del bien 2."
                elif elasticidad_precio2_red < 0:
                    tipo_relacion = "COMPLEMENTARIO"
                    exp_relacion = "La demanda del bien 1 disminuye si sube el precio del bien 2."
                else:
                    tipo_relacion = "INDEPENDIENTE"
                    exp_relacion = "No hay efecto del precio del bien 2 sobre la demanda del bien 1."

                print(f"Tipo de relación: {tipo_relacion}")
                print(f"Descripción: {exp_relacion}")

            # --- Elasticidad ingreso ---
            if 'ingreso' not in variables_en_funcion:
                print("\nElasticidad ingreso:")
                print("La función no depende del ingreso → no corresponde calcular elasticidad ingreso.")
            elif derivada_ingreso_num == 0:
                print("\nElasticidad ingreso:")
                print("Derivada respecto al ingreso es cero → elasticidad ingreso cero.")
            else:
                # Tipo según derivada y magnitud
                if derivada_ingreso_num > 0:
                    if elasticidad_ingreso_red > 1:
                        tipo_por_ingreso = "LUJO"
                        exp_ingreso = "La demanda aumenta más que proporcionalmente al ingreso."
                    elif 0 < elasticidad_ingreso_red <= 1:
                        tipo_por_ingreso = "NECESARIO"
                        exp_ingreso = "La demanda aumenta menos que proporcionalmente al ingreso."
                    else:
                        tipo_por_ingreso = "NEUTRO"
                        exp_ingreso = "Efecto del ingreso prácticamente nulo."
                else:
                    tipo_por_ingreso = "INFERIOR"
                    exp_ingreso = "La demanda disminuye cuando aumenta el ingreso."

                print("\nElasticidad ingreso:")
                print(f"Derivada evaluada: {derivada_ingreso_red}")
                print(f"Elasticidad: {elasticidad_ingreso_red}")
                print(f"Clasificación según ingreso: {tipo_por_ingreso}")
                print(f"Explicación: {exp_ingreso}")

            print("\n" + "="*60)

    except ValueError:
        print("Error en ingreso de número, ingrese un valor valido para las variables solicitadas")

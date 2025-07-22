import pygame, math,subprocess
import tablero
import constantes

pygame.init()

x, y = (pygame.display.Info().current_w, pygame.display.Info().current_h)
largo_utilizable = y * 500 / 433
pantalla = pygame.display.set_mode((x, y))
pygame.display.set_caption('Estanciero by Guille')
fuente_encabezado = pygame.font.SysFont('Arial', int(y / 20))
fuente_botones = pygame.font.SysFont('helvetica', int(y / 30))



def inicio():
    seguir = True
    while seguir:
        fondo()
        btn_reglas = pygame.draw.rect(pantalla, constantes.verde, (x * 5 / 16, y / 2, x / 8, y / 12), 0, y // 24)
        btn_como_jugar = pygame.draw.rect(pantalla, constantes.verde, (x * 9 / 16, y / 2, x / 8, y / 12), 0, y // 24)
        btn_jugar = pygame.draw.rect(pantalla, constantes.azul, (x * 7 / 16, y * 7 / 12, x / 8, y / 12), 0, y // 24)
        renglon1 = fuente_encabezado.render('Bienvenido al juego ESTANCIERO', True, constantes.negro)
        rect_renglon1 = renglon1.get_rect()
        rect_renglon1.center = (x / 2, y / 3)
        txt_btn_reglas = fuente_botones.render('Reglas', True, constantes.negro)
        rect_txt_reglas = txt_btn_reglas.get_rect()
        rect_txt_reglas.center = btn_reglas.center
        txt_btn_jugar = fuente_botones.render('Jugar', True, constantes.blanco)
        rect_txt_jugar = txt_btn_jugar.get_rect()
        rect_txt_jugar.center = btn_jugar.center
        txt_btn_como_jugar = fuente_botones.render('Como jugar', True, constantes.negro)
        rect_txt_como_jugar = txt_btn_como_jugar.get_rect()
        rect_txt_como_jugar.center = btn_como_jugar.center
        pantalla.blits(blit_sequence=((renglon1, rect_renglon1), (txt_btn_reglas, rect_txt_reglas), (txt_btn_jugar, rect_txt_jugar), (txt_btn_como_jugar, rect_txt_como_jugar)))
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                raton = pygame.mouse.get_pos()
                if btn_jugar.collidepoint(raton):
                    seguir = False
                    return seleccionar_jugadores()
                elif btn_reglas.collidepoint(raton):
                    path = 'Reglamento.pdf'
                    subprocess.Popen([path], shell=True)
                elif btn_como_jugar.collidepoint(raton):
                    path = 'Como_jugar.pdf'
                    subprocess.Popen([path], shell=True)


def seleccionar_jugadores():
    fondo()
    renglon1 = fuente_encabezado.render('Seleccione la cantidad de jugadores', True, constantes.negro)
    rect_renglon1 = renglon1.get_rect()
    rect_renglon1.center = (x / 2, y / 3)
    pantalla.blit(renglon1, rect_renglon1)
    botones = []
    for n in range(2, 7):
        x1 = x / 4 + (x / 10) * (n - 2) + 40
        boton = pygame.draw.rect(pantalla, (0, 255, 0), (x1, y * .5, 40, 40), border_radius=10)
        numero = fuente_botones.render(str(n), True, constantes.negro)
        rect_numero = numero.get_rect()
        rect_numero.center = (x1 + 20, y / 2 + 20)
        pantalla.blit(numero, rect_numero)
        botones.append(boton)
    pygame.display.update()
    seguir = True
    while seguir:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                raton = pygame.mouse.get_pos()
                cont = 1
                for boton in botones:
                    cont += 1
                    if boton.collidepoint(raton):
                        cantidad_jugadores = cont
                        print(cantidad_jugadores)
                        seguir = False
    return cantidad_jugadores

def vista_reglas():
    seguir = True
    while seguir:
        fondo()
        titulo = fuente_encabezado.render('Reglamento estanciero', True, constantes.negro)
        rect_titulo = titulo.get_rect()
        rect_titulo.center = (x / 2, y / 2)
        pantalla.blit(titulo, rect_titulo)
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                raton = pygame.mouse.get_pos()
                seguir = False



def fondo():
    pantalla.fill(constantes.azul)
    recuadro = pygame.draw.rect(pantalla, (255, 255, 255), (x / 4, y / 4, x / 2, y / 2))
    # pygame.display.update()



def panel_opciones(opciones_disponibles, jugador, jugadores_activos):
    info_jugador(jugador, jugadores_activos)
    ancho = (x - largo_utilizable) / 1.99
    opciones_totales = ((1, 'Tirar dados'), (2, 'Comprar chacras/estancias'), (3, 'Vender chacras/estancias'), (4, 'Listar Propiedades y saldo'), (5, 'Hipotecar propiedades'), (6, 'Des-hipotecar propiedades'), (7, 'Comerciar con otro jugador'), (8, 'Subastar propiedad'), (0, 'Terminar turno'))
    cont = 0
    botones = []
    nombre = fuente_encabezado.render(jugador.nombre, True, constantes.verde)
    rect_nombre = nombre.get_rect()
    rect_nombre.center = (ancho / 2, ancho / 4)
    pantalla.blit(nombre, rect_nombre)
    for opcion in opciones_totales:
        cont += 1
        texto = fuente_botones.render(opcion[1], True, constantes.negro)
        rect_texto = texto.get_rect()
        rect_texto.center = (ancho / 2, ancho / 4 * (cont + .2) + ancho / 3)
        color = constantes.verde_oscuro
        if opcion[0] in opciones_disponibles:
            color = constantes.verde
        boton = pygame.draw.rect(pantalla, color, (0, ancho / 4 * cont + ancho / 3, ancho, ancho / 6))
        if opcion[0] in opciones_disponibles:
            botones.append((boton, opcion[0]))
        pantalla.blit(texto, rect_texto)
        pygame.display.update()
    return botones


def info_jugador(jugador, jugadores_activos):
    pygame.draw.rect(pantalla, (230, 230, 100), (5 * x / 6, y / 20, x / 6, 9 * y / 10))
    if jugador.peon == 'Negro':
        color_letra = constantes.blanco
    else:
        color_letra = constantes.negro
    nombre = fuente_encabezado.render('Jugador: ' + jugador.nombre, True, color_letra, constantes.peones_dic[jugador.peon])
    rect_nombre = nombre.get_rect()
    if rect_nombre[2] > x / 12:
        rect_nombre.midright = (79 / 80 * x, 2 * y / 22)
    else:
        rect_nombre.center = (5.5 * x / 6, 2 * y / 22)
    casillero = fuente_botones.render('Ubicacion: ' + str(jugador.ubicacion), True, constantes.negro)
    rect_casillero = casillero.get_rect()
    rect_casillero.center = (5.5 * x / 6, 3 * y / 22)
    saldo = fuente_botones.render('Saldo: $' + str(jugador.dinero), True, constantes.negro)
    rect_saldo = saldo.get_rect()
    rect_saldo.center = (5.5 * x / 6, 4 * y / 22)
    propiedades = fuente_botones.render('Propiedades:', True, constantes.negro)
    rect_propiedades = propiedades.get_rect()
    rect_propiedades.center = (5.5 * x / 6, 5 * y / 22)
    pantalla.blits(blit_sequence=((nombre, rect_nombre), (casillero, rect_casillero), (saldo, rect_saldo), (propiedades, rect_propiedades)))
    final_prop = 0
    for index in range(len(jugador.propiedades)):
        x1 = 5 * x / 6 + ((index % 4) + 2) * x / 36
        y1 = 6 * y / 22 + (index // 4) * y / 20
        estado = jugador.propiedades[index].estado
        if isinstance(jugador.propiedades[index], tablero.Campo) and (estado != 'Solo campo' and estado != 'Hipotecado'):
            pygame.draw.rect(pantalla, jugador.propiedades[index].color, (x1 - y / 50, y1 - y / 50, y / 25, y / 25))
        elif isinstance(jugador.propiedades[index], tablero.Compañia):
            letra = fuente_encabezado.render('C', True, constantes.rojo)
            rect_letra = letra.get_rect()
            rect_letra.center = (x1, y1)
            pantalla.blit(letra, rect_letra)
        elif isinstance(jugador.propiedades[index], tablero.Ferrocarril):
            letra = fuente_encabezado.render('T', True, constantes.rojo)
            rect_letra = letra.get_rect()
            rect_letra.center = (x1, y1)
            pantalla.blit(letra, rect_letra)
        else:
            pygame.draw.circle(pantalla, jugador.propiedades[index].color, (x1, y1), y / 50)
        propiedad = fuente_botones.render(str(jugador.propiedades[index].numero), True, constantes.negro)
        rect_propiedad = propiedad.get_rect()
        rect_propiedad.center = (x1, y1)
        pantalla.blit(propiedad, rect_propiedad)
    final_prop = (73 / 110) * y
    resto = 19 / 20 * y - final_prop
    otros_jugadores = jugadores_activos.copy()
    otros_jugadores.remove(jugador)
    separacion = resto // len(otros_jugadores)
    for otro in otros_jugadores:
        if otro.peon == 'Negro':
            color_letra = constantes.blanco
        else:
            color_letra = constantes.negro
        if len(otro.nombre) > 9:
            txt_nombre = otro.nombre[:7] + '...'
        else:
            txt_nombre = otro.nombre
        nombre = fuente_botones.render(txt_nombre, True, color_letra, constantes.peones_dic[otro.peon])
        rect_nombre = nombre.get_rect()
        rect_nombre.centery = final_prop + separacion * otros_jugadores.index(otro)
        rect_nombre.left = 61 / 72 * x
        saldo = fuente_botones.render('$' + str(otro.dinero), True, constantes.negro)
        rect_saldo = saldo.get_rect()
        rect_saldo.centery = rect_nombre.centery
        rect_saldo.right = 143 / 144 * x
        pantalla.blits(blit_sequence=((nombre, rect_nombre), (saldo, rect_saldo)))
    pass



def opcion_compra(jugador, propiedad):
    pygame.draw.rect(pantalla, constantes.blanco, (x / 4, y / 4, x / 2, y / 2), border_radius=int(x / 5))
    nombre = fuente_encabezado.render(jugador.nombre, True, constantes.negro)
    rect_nombre = nombre.get_rect()
    rect_nombre.center = (x / 2, y / 3)
    renglon1 = fuente_botones.render('¿Desea comprar', True, constantes.negro)
    rect_renglon1 = renglon1.get_rect()
    rect_renglon1.center = (x / 2, y / 3 + y / 15)
    renglon2 = fuente_encabezado.render(propiedad.nombre, True, constantes.negro)
    rect_renglon2 = renglon2.get_rect()
    rect_renglon2.center = (x / 2, y / 3 + 2 * y / 15)
    renglon3 = fuente_botones.render('Por $' + str(propiedad.valor) + '?', True, constantes.negro)
    rect_renglon3 = renglon3.get_rect()
    rect_renglon3.center = (x / 2, y / 3 + 3 * y / 15)
    btn_si = pygame.draw.rect(pantalla, constantes.verde, (x / 2 - x / 9, y / 1.5, x / 10, y / 20), border_radius=int(x / 25))
    si = fuente_botones.render('SI', True, constantes.negro)
    rect_si = si.get_rect()
    rect_si.center = btn_si.center
    btn_no = pygame.draw.rect(pantalla, constantes.verde, (x / 2 + x / 9 - x / 10, y / 1.5, x / 10, y / 20), border_radius=int(x / 25))
    no = fuente_botones.render('NO', True, constantes.negro)
    rect_no = no.get_rect()
    rect_no.center = btn_no.center
    pantalla.blits(blit_sequence=((nombre, rect_nombre), (si, rect_si), (no, rect_no), (renglon1, rect_renglon1), (renglon2, rect_renglon2), (renglon3, rect_renglon3)))
    pygame.display.update()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                raton = pygame.mouse.get_pos()
                if btn_si.collidepoint(raton):
                    return 'S'
                elif btn_no.collidepoint(raton):
                    return 'N'


def salir_carcel(jugador):
    pygame.draw.rect(pantalla, constantes.blanco, (x / 4, y / 4, x / 2, y / 2), border_radius=int(x / 5))
    nombre = fuente_encabezado.render(jugador.nombre, True, constantes.negro)
    rect_nombre = nombre.get_rect()
    rect_nombre.center = (x / 2, y / 3)
    renglon1 = fuente_botones.render('Usted esta detenido, para salir, puede:', True, constantes.negro)
    rect_renglon1 = renglon1.get_rect()
    rect_renglon1.center = (x / 2, y / 3 + y / 15)
    renglon2 = fuente_botones.render('Sacar doble en los dados(3 intentos, 1 por turno). Restan ' + str(jugador.intentos_salir) + ' intentos', True, constantes.negro)
    rect_renglon2 = renglon2.get_rect()
    rect_renglon2.center = (x / 2, y / 3 + 2 * y / 15)
    renglon3 = fuente_botones.render('Pagar una multa de $1000 al banco', True, constantes.negro)
    rect_renglon3 = renglon3.get_rect()
    rect_renglon3.center = (x / 2, y / 3 + 3 * y / 15)
    renglon4 = fuente_botones.render('Usar una tarjeta, si la tiene, de Habeas corpus', True, constantes.negro)
    rect_renglon4 = renglon4.get_rect()
    rect_renglon4.center = (x / 2, y / 3 + 4 * y / 15)
    color_op_tarjeta = constantes.verde_oscuro
    color_op_multa = constantes.verde_oscuro
    if len(jugador.tarjetas) > 0:
        color_op_tarjeta = constantes.verde
    if jugador.dinero >= 1000:
        color_op_multa = constantes.verde
    btn_doble = pygame.draw.rect(pantalla, constantes.verde, (3 * x / 8 - x / 20, y / 1.5, x / 10, y / 20), border_radius=int(x / 25))
    doble = fuente_botones.render('Tirar dados', True, constantes.negro)
    rect_doble = doble.get_rect()
    rect_doble.center = btn_doble.center
    btn_pagar = pygame.draw.rect(pantalla, color_op_multa, (x / 2 - x / 20, y / 1.5, x / 10, y / 20), border_radius=int(x / 25))
    pagar = fuente_botones.render('Pagar multa', True, constantes.negro)
    rect_pagar = pagar.get_rect()
    rect_pagar.center = btn_pagar.center
    btn_tarjeta = pygame.draw.rect(pantalla, color_op_tarjeta, (5 * x / 8 - x / 20, y / 1.5, x / 10, y / 20), border_radius=int(x / 25))
    tarjeta = fuente_botones.render('Usar tarjeta', True, constantes.negro)
    rect_tarjeta = tarjeta.get_rect()
    rect_tarjeta.center = btn_tarjeta.center
    pantalla.blits(blit_sequence = ((nombre, rect_nombre), (doble, rect_doble), (pagar, rect_pagar), (tarjeta, rect_tarjeta), (renglon1, rect_renglon1), (renglon2, rect_renglon2), (renglon3, rect_renglon3), (renglon4, rect_renglon4)))
    pygame.display.update()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                raton = pygame.mouse.get_pos()
                if btn_pagar.collidepoint(raton) and jugador.dinero >= 1000:
                    return 1
                elif btn_doble.collidepoint(raton):
                    return 2
                elif btn_tarjeta.collidepoint(raton) and len(jugador.tarjetas) > 0:
                    return 3


def mostrar_mensaje(mensaje, botones = False):
    pygame.draw.rect(pantalla, constantes.blanco, (x / 4, y / 4, x / 2, (y / 10) * (len(mensaje) + 2)))
    cont = 0
    for linea in mensaje:
        if linea[1] == 0:
            renglon = fuente_botones.render(linea[0], True, constantes.negro)
        else:
            renglon = fuente_encabezado.render(linea[0], True, constantes.negro)
        cont += 1
        rect_renglon = renglon.get_rect()
        rect_renglon.center = (x / 2, y / 4 + cont * y / 13)
        pantalla.blit(renglon, rect_renglon)
    if botones:
        pygame.draw.rect(pantalla, constantes.rojo,
                         (x / 3, y / 4 + (y / 10) * len(mensaje), x / 3, y / 10),
                         border_radius=int(y / 20))
        btn_si = pygame.draw.rect(pantalla, constantes.verde,
                                  (x / 2 - x / 9, y / 4 + (y / 10) * len(mensaje) + y / 40, x / 10, y / 20),
                                  border_radius=int(x / 25))
        si = fuente_botones.render('SI', True, constantes.negro)
        rect_si = si.get_rect()
        rect_si.center = btn_si.center
        btn_no = pygame.draw.rect(pantalla, constantes.verde,
                                   (x / 2 + x / 9 - x / 10, y / 4 + (y / 10) * len(mensaje) + y / 40, x / 10, y / 20),
                                   border_radius=int(x / 25))
        no = fuente_botones.render('NO', True, constantes.negro)
        rect_no = no.get_rect()
        rect_no.center = btn_no.center
        pantalla.blits(blit_sequence=((si, rect_si), (no, rect_no)))
    else:
        btn_cerrar = pygame.draw.rect(pantalla, constantes.rojo,
                                      (x / 2 - x / 20, y / 4 + (y / 10) * len(mensaje) - y / 40, x / 10, y / 20),
                                      border_radius=int(x / 25))
        txt_cerrar = fuente_botones.render('Cerrar', True, constantes.blanco)
        rect_cerrar = txt_cerrar.get_rect()
        rect_cerrar.center = btn_cerrar.center
        pantalla.blit(txt_cerrar, rect_cerrar)
    pygame.display.update()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                raton = pygame.mouse.get_pos()
                if botones:
                    if btn_si.collidepoint(raton):
                        return 'S'
                    elif btn_no.collidepoint(raton):
                        return 'N'
                elif btn_cerrar.collidepoint(raton):
                    return None



def seleccionar_propiedad(seleccionables, jugadoresActivos, accion, seleccionados=[]):
    pintar_tablero(pantalla, largo_utilizable, x, y, jugadoresActivos, seleccionables, accion, seleccionados)
    pygame.draw.rect(pantalla, constantes.blanco, (x / 3, y / 3, x / 3, y / 3), border_radius=int(x / 15))
    texto_btn = 'Terminar'
    if accion=='Edificar':
        renglon1 = fuente_botones.render('Seleccione el campo donde desea construir', True, constantes.negro)
    elif accion == 'Vender chacras':
        renglon1 = fuente_botones.render('Seleccione la chacra/estancia que desea vender', True, constantes.negro)
    elif accion == 'Hipotecar':
        renglon1 = fuente_botones.render('Seleccione el campo a hipotecar', True, constantes.negro)
    elif accion == 'Deshipotecar':
        renglon1 = fuente_botones.render('Seleccione el campo a des-hipotecar', True, constantes.negro)
    if accion == 'Pedir' or accion == 'Ofrecer' or accion == 'Subastar':
        renglon1 = fuente_botones.render('Seleccione la/s propiedad/es que desea ' + accion, True, constantes.negro)
        renglon2 = fuente_botones.render('(al finalizar presione LISTO)', True, constantes.negro)
        texto_btn = 'Listo'
        if accion == 'Subastar':
            renglon1 = fuente_botones.render('Seleccione la propiedad que desea ' + accion, True, constantes.negro)
    else:
        renglon2 = fuente_botones.render('(los campos posibles estan en verde)', True, constantes.negro)
    rect_renglon1 = renglon1.get_rect()
    rect_renglon1.center = (x / 2, y / 3 + y / 12)
    rect_renglon2 = renglon2.get_rect()
    rect_renglon2.center = (x / 2, y / 3 + y / 6)
    btn_cancelar = pygame.draw.rect(pantalla, constantes.rojo, ((x / 2 - x / 20), (y / 3 + y / 4 - y / 40), x / 10, y / 20))
    cancelar = fuente_botones.render(texto_btn, True, constantes.negro)
    rect_cancelar = cancelar.get_rect()
    rect_cancelar.center = btn_cancelar.center
    pantalla.blits(blit_sequence=((renglon1, rect_renglon1), (renglon2, rect_renglon2), (cancelar, rect_cancelar)))
    casillero = None
    pygame.display.update()
    while (casillero not in seleccionables and casillero != 'C'):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                casillero = identificar_click([(btn_cancelar, 'C')], pygame.mouse.get_pos())
            elif accion in constantes.acciones_con_marca and evento.type == pygame.MOUSEMOTION:
                pintar_tablero(pantalla, largo_utilizable, x, y, jugadoresActivos, seleccionables, accion, seleccionados)
                pygame.draw.rect(pantalla, constantes.blanco, (x / 3, y / 3, x / 3, y / 3), border_radius=int(x / 15))
                btn_cancelar = pygame.draw.rect(pantalla, constantes.rojo, ((x / 2 - x / 20), (y / 3 + y / 4 - y / 40), x / 10, y / 20))
                pantalla.blits(blit_sequence=((renglon1, rect_renglon1), (renglon2, rect_renglon2), (cancelar, rect_cancelar)))
                casillero_apuntado = identificar_click([], pygame.mouse.get_pos())
                if casillero_apuntado in seleccionables:
                    if accion == 'Edificar':
                        color_marco = constantes.rojo
                        txt = int(casillero_apuntado.precioChacra)
                    if accion == 'Vender chacras':
                        color_marco = constantes.verde_oscuro
                        txt = int(casillero_apuntado.precioChacra / 2)
                    if accion == 'Hipotecar':
                        color_marco = constantes.verde_oscuro
                        txt = int(casillero_apuntado.valorHipotecado * .9)
                    if accion == 'Deshipotecar':
                        color_marco = constantes.rojo
                        txt = int(casillero_apuntado.valorHipotecado)
                    if accion == 'Pedir':
                        color_marco = constantes.negro
                        txt = casillero_apuntado.titular
                    marco = pygame.draw.rect(pantalla, color_marco, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], x / 20, y / 20))
                    texto = fuente_botones.render(str(txt), True, constantes.blanco)
                    rect_texto = texto.get_rect()
                    rect_texto.center = marco.center
                    pantalla.blit(texto, rect_texto)
                pygame.display.update()
    return casillero


def listar_propiedades(jugadores_activos:tuple):
    seguir = True
    while seguir:
        pantalla.fill(constantes.blanco)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                seguir = False
        encabezado = fuente_encabezado.render('Propiedades y saldo', True, constantes.negro)
        rect_encabezado = encabezado.get_rect()
        rect_encabezado.center = (x / 2, y / 12)
        for jugador in jugadores_activos:
            propiedades_list = []
            for propiedad in jugador.propiedades:
                propiedades_list.append(propiedad.numero)
            nombre = fuente_encabezado.render(jugador.nombre, True, constantes.negro)
            rect_nombre = nombre.get_rect()
            rect_nombre.center = (x / 2, y / 7 * (jugadores_activos.index(jugador) + 1))
            propiedades = fuente_botones.render('Propiedades: ' + str(propiedades_list), True, constantes.negro)
            rect_propiedades = propiedades.get_rect()
            rect_propiedades.center = (x / 2, y / 7 * (jugadores_activos.index(jugador) + 1) + y / 20)
            saldo = fuente_botones.render('Saldo: $' + str(jugador.dinero), True, constantes.negro)
            rect_saldo = saldo.get_rect()
            rect_saldo.center = (x / 2, y / 7 * (jugadores_activos.index(jugador) + 1) + y / 12)
            pygame.draw.circle(pantalla, constantes.peones_dic[jugador.peon], (rect_nombre.right + y / 20, rect_nombre.centery), y / 40)
            pygame.draw.circle(pantalla, constantes.negro, (rect_nombre.right + y / 20, rect_nombre.centery), y / 40, 2)
            pantalla.blits(blit_sequence=((nombre, rect_nombre), (propiedades, rect_propiedades), (encabezado, rect_encabezado), (saldo, rect_saldo)))
        pygame.display.update()


def comerciar(comerciables, jugadoresActivos, jugador):
    # mostrar_mensaje((('Reglas de comercio entre jugadores',1),
    # ('Se podran realizar transacciones con un solo jugador a la vez.',0),
    # ('Solo se podran comerciar propiedades sin edificaciones.',0),
    # ('Si alguna/s de las propiedades involucradas en la transaccion',0),
    # ('se encuentra hipotecada. El nuevo titular debera pagar en el momento',0),
    # ('el 10% del valor de la hipoteca al banco, y si no levanta la hipoteca en',0),
    # ('el momento, debera abonar otro 10% al banco, al levantar dicha Hipoteca.',0) 
    # ))
    # mostrar_mensaje((('Para ralizar una oferta a otro jugador',0),
    # ('Seleccione del tablero todas las propiedades (suyas) que desea incluir en la ',0),
    # ('transaccion, Luego haga click en "LISTO".',0),
    # ('Repitalos pasos con las propiedades del otro jugador,0)'
    # ('A continuacion, introduzca los importes de la oferta (pedidos u ofrecidos).',0),
    # ('Verifique que la oferta es correcta (una vez enviada, no podra cancelarla).',0),
    # ('Para finalizar presione en "OFERTAR".',0) 
    # ))
    mis_propiedades = []
    otros_propiedades = []
    for propiedad in comerciables:
        if propiedad.titular == jugador.nombre:
            mis_propiedades.append(propiedad)
        else:
            otros_propiedades.append(propiedad)
    prop_ofrecidas = propiedades_comerciar(mis_propiedades, jugadoresActivos, 'Ofrecer')
    prop_pedidas = propiedades_comerciar(otros_propiedades, jugadoresActivos, 'Pedir')

    texto_importe = ''
    seguir = True
    cont = 0
    color_cursor = constantes.verde
    contraparte = ''
    while seguir:
        if len(prop_ofrecidas) + len(prop_pedidas) == 0:
            pintar_tablero(pantalla, largo_utilizable, x, y, jugadoresActivos)
            mostrar_mensaje((('Para realizar una transaccion', 0), ('debe seleccionar por lo menos', 0), ('una propiedad', 0)))
            seguir = False
            return 'C'
        elif len(prop_pedidas) == 0:
            if len(jugadoresActivos) > 2:
                cont_mensaje = 0
                while contraparte == '':
                    if cont_mensaje == 0:
                        pintar_tablero(pantalla, largo_utilizable, x, y, jugadoresActivos)
                        mostrar_mensaje((('Seleccione el jugador', 0), ('a quien desea hacer la oferta', 0)))
                        cont_mensaje += 1
                    pintar_tablero(pantalla, largo_utilizable, x, y, jugadoresActivos)
                    pygame.draw.rect(pantalla, constantes.blanco, (x/3, y/10, x/3, len(jugadoresActivos)*y/10), 0, int(x/20))
                    otros_jugadores = jugadoresActivos.copy()
                    otros_jugadores.remove(jugador)
                    botones_jugadores = []
                    for otro in otros_jugadores:
                        btn_jugador = (pygame.draw.rect(pantalla, constantes.verde, (x/3+5, y/10 + y/11 * (otros_jugadores.index(otro)+1), x/3-10, y/20)), otro)
                        nombre = fuente_botones.render(otro.nombre, True, constantes.negro)
                        rect_nombre = nombre.get_rect()
                        rect_nombre.center = btn_jugador[0].center
                        pantalla.blit(nombre, rect_nombre)
                        botones_jugadores.append(btn_jugador)
                    pygame.display.update()
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                        elif evento.type == pygame.MOUSEBUTTONDOWN:
                            raton = pygame.mouse.get_pos()
                            for boton in botones_jugadores:
                                if boton[0].collidepoint(raton):
                                    contraparte = boton[1]
            else:
                for it in jugadoresActivos:
                    if it != jugador:
                        contraparte = it
            pintar_tablero(pantalla, largo_utilizable, x, y, jugadoresActivos)
            pygame.draw.rect(pantalla, constantes.blanco, (x/4, y/4, x/2, y/2), 0, int(x/15))
            btn_pedir = boton_pedir()
            btn_ofrecer = pygame.draw.rect(pantalla, constantes.negro, (0, 0, 0, 0))
            texto = fuente_encabezado.render('Ingrese el monto a pedir en la transaccion', True, constantes.negro)
        elif len(prop_ofrecidas) == 0:
            for jugador_activo in jugadoresActivos:
                if jugador_activo.nombre == prop_pedidas[0].titular:
                    contraparte = jugador_activo
            pygame.draw.rect(pantalla, constantes.blanco, (x/4, y/4, x/2, y/2), 0, int(x/15))
            btn_ofrecer = boton_ofrecer()
            btn_pedir = pygame.draw.rect(pantalla, constantes.negro, (0, 0, 0, 0))
            texto = fuente_encabezado.render('Ingrese el monto a ofrecer en la transaccion', True, constantes.negro)
        else:
            for jugador_activo in jugadoresActivos:
                if jugador_activo.nombre == prop_pedidas[0].titular:
                    contraparte = jugador_activo
            pygame.draw.rect(pantalla, constantes.blanco, (x/4, y/4, x/2, y/2), 0, int(x / 15))
            btn_pedir = boton_pedir()
            btn_ofrecer = boton_ofrecer()
            texto = fuente_botones.render('Ingrese el monto a ofrecer o pedir en la transaccion', True, constantes.negro)
        cont += 1
        cuadro_texto = pygame.draw.rect(pantalla, constantes.negro, (2*x/5, y/2, x/5, y/15), 0, int(x / 15))
        importe = fuente_encabezado.render(texto_importe, True, constantes.verde)
        rect_importe = importe.get_rect()
        rect_importe.centery = cuadro_texto.centery
        rect_importe.right = cuadro_texto.right-x/50
        signo = fuente_encabezado.render('$ ', True, constantes.verde)
        rect_signo = signo.get_rect()
        rect_signo.right = rect_importe.left
        rect_signo.centery = rect_importe.centery
        rect_texto = texto.get_rect()
        rect_texto.center = (x / 2, y / 3 + y / 15)
        if cont % 100 == 0:
            if color_cursor == constantes.verde:
                color_cursor = constantes.negro
            else:
                color_cursor = constantes.verde
        cursor = fuente_encabezado.render('  |', True, color_cursor)
        rect_cursor = cursor.get_rect()
        rect_cursor.centery = cuadro_texto.centery - y / 100
        rect_cursor.right = cuadro_texto.right - x / 75
        pantalla.blits(blit_sequence=((texto, rect_texto), (importe, rect_importe), (signo, rect_signo), (cursor, rect_cursor)))
        pygame.display.update()
        monto_ofrecido = '0'
        monto_pedido = '0'
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                raton = pygame.mouse.get_pos()
                if btn_ofrecer.collidepoint(raton):
                    monto_ofrecido = texto_importe
                    seguir = False
                if btn_pedir.collidepoint(raton):
                    monto_pedido = texto_importe
                    seguir = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    texto_importe = texto_importe[:-1]
                elif evento.unicode.isdigit():
                    texto_importe += evento.unicode
        pygame.display.update()
    seguir = True
    while seguir:
        prop_ofrecidas_numero = []
        prop_pedidas_numero = []
        for ofrecida in prop_ofrecidas:
            prop_ofrecidas_numero.append(ofrecida.numero)
        for pedida in prop_pedidas:
            prop_pedidas_numero.append(pedida.numero)
        pygame.draw.rect(pantalla, constantes.blanco, (x / 4, y / 4, x / 2, y / 2), 0, int(x / 15))
        btn_aceptar = pygame.draw.rect(pantalla, constantes.verde, (x / 2 - x / 8, 3 * y / 4.5, x / 10, y / 20), 0, int(y / 50))
        btn_rechazar = pygame.draw.rect(pantalla, constantes.rojo, (x / 2 + x / 8 - x / 10, 3 * y / 4.5, x / 10, y / 20), 0, int(y / 50))
        renglon1 = fuente_encabezado.render(contraparte.nombre, True, constantes.negro)
        rect_renglon1 = renglon1.get_rect()
        renglon2 = fuente_botones.render(jugador.nombre+' Ofrece:', True, constantes.negro)
        rect_renglon2 = renglon2.get_rect()
        renglon3 = fuente_botones.render(str(prop_ofrecidas_numero), True, constantes.negro)
        rect_renglon3 = renglon3.get_rect()
        renglon4 = fuente_botones.render('$'+monto_ofrecido, True, constantes.negro)
        rect_renglon4 = renglon4.get_rect()
        renglon5 = fuente_botones.render('A cambio de:', True, constantes.negro)
        rect_renglon5 = renglon5.get_rect()
        renglon6 = fuente_botones.render(str(prop_pedidas_numero), True, constantes.negro)
        rect_renglon6 = renglon6.get_rect()
        renglon7 = fuente_botones.render('$'+monto_pedido, True, constantes.negro)
        rect_renglon7 = renglon7.get_rect()
        aceptar = fuente_botones.render('Aceptar', True, constantes.negro)
        rect_aceptar = aceptar.get_rect()
        rechazar = fuente_botones.render('Rechazar', True, constantes.blanco)
        rect_rechazar = rechazar.get_rect()
        rect_renglon1.center = (x / 2, y / 4 + y / 20)
        rect_renglon2.center = (x / 2, y / 4 + 2 * y / 20)
        rect_renglon3.center = (x / 2, y / 4 + 3 * y / 20)
        rect_renglon4.center = (x / 2, y / 4 + 4 * y / 20)
        rect_renglon5.center = (x / 2, y / 4 + 6 * y / 20)
        rect_renglon6.center = (x / 2, y / 4 + 7 * y / 20)
        rect_renglon7.center = (x / 2, y / 4 + 8 * y / 20)
        rect_aceptar.center = btn_aceptar.center
        rect_rechazar.center = btn_rechazar.center
        textos = [(renglon1, rect_renglon1), (renglon2, rect_renglon2), (renglon5, rect_renglon5), (aceptar, rect_aceptar), (rechazar, rect_rechazar)]
        if len(prop_ofrecidas) > 0:
            textos.append((renglon3, rect_renglon3))
        if len(prop_pedidas) > 0:
            textos.append((renglon6, rect_renglon6))
        if monto_ofrecido != '0':
            textos.append((renglon4, rect_renglon4))
        if monto_pedido != '0':
            textos.append((renglon7, rect_renglon7))
        pantalla.blits(blit_sequence = (textos))
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                raton = pygame.mouse.get_pos()
                pintar_tablero(pantalla, largo_utilizable, x, y, jugadoresActivos)
                if btn_aceptar.collidepoint(raton):
                    mostrar_mensaje(((contraparte.nombre, 0), (' acepta la oferta', 0)))
                    return (prop_ofrecidas, monto_ofrecido, prop_pedidas, monto_pedido, contraparte)
                if btn_rechazar.collidepoint(raton):
                    mostrar_mensaje(((contraparte.nombre, 0), (' rechaza la oferta', 0)))
                    return 'C'


def propiedades_comerciar(comerciables, jugadoresActivos, accion):
    propiedades = []
    comerciables2 = comerciables.copy()
    while 'C' not in propiedades:
        borrables = []
        if len(propiedades) > 0:
            for it in comerciables2:
                if propiedades[0].titular != it.titular:
                    borrables.append(it)
            for borrable in borrables:
                comerciables2.remove(borrable)
        else:
            comerciables2 = comerciables.copy()
        propiedad = seleccionar_propiedad(comerciables2, jugadoresActivos, accion, propiedades)
        if propiedad:
            if propiedad in propiedades:
                propiedades.remove(propiedad)
                print(propiedad)
            else:
                propiedades.append(propiedad)
    propiedades.remove('C')
    return propiedades

def boton_pedir():
    btn_pedir = pygame.draw.rect(pantalla, constantes.verde, (x / 2 - x / 8, 3 * y / 4.5, x / 10, y / 20), 0, int(y / 50))
    pedir = fuente_botones.render('Pedir', True, constantes.negro)
    rect_pedir = pedir.get_rect()
    rect_pedir.center = btn_pedir.center
    pantalla.blit(pedir, rect_pedir)
    return btn_pedir

def boton_ofrecer():
    btn_ofrecer = pygame.draw.rect(pantalla, constantes.verde, (x / 2 + x / 8 - x / 10, 3 * y / 4.5, x / 10, y / 20), 0, int(y / 50))
    ofrecer = fuente_botones.render('Ofrecer', True, constantes.negro)
    rect_ofrecer = ofrecer.get_rect()
    rect_ofrecer.center = btn_ofrecer.center
    pantalla.blit(ofrecer, rect_ofrecer)
    return btn_ofrecer

def rematar(jugador, jugadores_activos):
    if len(jugadores_activos) > 2:
        subastables = jugador.propiedades.copy()
        for prop in jugador.propiedades:
            if isinstance(prop, tablero.Campo) and prop.edificaciones > 0:
                subastables.remove(prop)
        a_subastar = seleccionar_propiedad(subastables, jugadores_activos, 'Subastar')
        if a_subastar == 'C':
            return None
        otros = jugadores_activos.copy()
        otros.remove(jugador)
        texto_importe = '0'
        oferta_vigente = [0, jugador]
        jugadores_declinados = []
        while len(otros) > 1 or (len(otros) == 1 and oferta_vigente[0] == 0):
            for declinado in jugadores_declinados:
                otros.remove(declinado)
            cont = 0
            jugadores_declinados = []
            for oferente in otros:
                seguir = True
                color_cursor = constantes.verde
                while seguir:
                    pygame.draw.rect(pantalla, constantes.blanco, (0, 0, x / 5, y))
                    for otro in otros:
                        btn_jugador = (pygame.draw.rect(pantalla, constantes.verde,
                                                         (x / 300,
                                                          y / 10 + y / 11 * (otros.index(otro) + 1),
                                                          x / 6, y / 20)), otro)
                        nombre = fuente_botones.render(otro.nombre, True, constantes.negro)
                        rect_nombre = nombre.get_rect()
                        rect_nombre.center = btn_jugador[0].center
                        pantalla.blit(nombre, rect_nombre)
                    cont += 1
                    ventana = pygame.draw.rect(pantalla, constantes.blanco,
                                               (x / 4, y / 4, x / 2, y / 2),
                                                0, int(x / 15))
                    btn_mas_cien = pygame.draw.rect(pantalla, constantes.azul,
                                                    (x / 2 - x / 20, 3 * y / 4.5, x / 10, y / 20),
                                                    0, int(y / 50))
                    text_mas_cien = fuente_botones.render('+ 100', True, constantes.blanco)
                    rect_text_mas_cien = text_mas_cien.get_rect()
                    rect_text_mas_cien.center = btn_mas_cien.center
                    btn_ofertar = pygame.draw.rect(pantalla,
                                                   constantes.verde,
                                                   (x / 2 + x / 8 - x / 20,
                                                    3 * y / 4.5,
                                                    x / 10, y / 20),
                                                   0, int(y / 50))
                    text_ofertar = fuente_botones.render('Ofertar', True, constantes.blanco)
                    rect_text_ofertar = text_ofertar.get_rect()
                    rect_text_ofertar.center = btn_ofertar.center
                    btn_declinar = pygame.draw.rect(pantalla, constantes.rojo,
                                                     (x * (13 / 40),
                                                      3 * y / 4.5, x / 10,
                                                      y / 20), 0, int(y / 50))
                    text_declinar = fuente_botones.render('Declinar', True, constantes.blanco)
                    rect_text_declinar = text_declinar.get_rect()
                    rect_text_declinar.center = btn_declinar.center
                    cuadro_texto = pygame.draw.rect(pantalla, constantes.negro,
                                                    (2 * x / 5, y / 2 + y / 20, x / 5, y / 15),
                                                      0, int(x / 15))
                    importe = fuente_encabezado.render((texto_importe), True, constantes.verde)
                    rect_importe = importe.get_rect()
                    rect_importe.centery = cuadro_texto.centery
                    rect_importe.right = cuadro_texto.right - x / 50
                    signo = fuente_encabezado.render('$ ', True, constantes.verde)
                    rect_signo = signo.get_rect()
                    rect_signo.right = rect_importe.left
                    rect_signo.centery = rect_importe.centery
                    if cont % 100 == 0:
                        if color_cursor == constantes.verde:
                            color_cursor = constantes.negro
                        else:
                            color_cursor = constantes.verde
                    cursor = fuente_encabezado.render('  |', True, color_cursor)
                    rect_cursor = cursor.get_rect()
                    rect_cursor.centery = cuadro_texto.centery - y / 100
                    rect_cursor.right = cuadro_texto.right - x / 75
                    nombre = fuente_encabezado.render(oferente.nombre, True, constantes.negro)
                    rect_nombre = nombre.get_rect()
                    rect_nombre.top = (y / 4)
                    rect_nombre.centerx = (x / 2)
                    en_subasta = fuente_botones.render(f"Subasta: {a_subastar.nombre} ({a_subastar.estado})",
                                                       True, constantes.negro)
                    rect_en_subasta = en_subasta.get_rect()
                    rect_en_subasta.center = (x / 2, y / 3 + y / 15)
                    actual = fuente_botones.render(f'La oferta actual es: ${oferta_vigente[0]} por {oferta_vigente[1].nombre}', True, constantes.negro)
                    rect_actual = actual.get_rect()
                    rect_actual.center = (x / 2, y / 2)
                    pantalla.blits(blit_sequence = ((nombre, rect_nombre),
                                                    (en_subasta, rect_en_subasta),
                                                    (actual, rect_actual),
                                                    (text_declinar, rect_text_declinar),
                                                    (text_ofertar, rect_text_ofertar),
                                                    (text_mas_cien, rect_text_mas_cien),
                                                    (signo, rect_signo),
                                                    (cursor, rect_cursor),
                                                    (importe, rect_importe)))
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                        elif evento.type == pygame.MOUSEBUTTONDOWN:
                            raton = pygame.mouse.get_pos()
                            if btn_declinar.collidepoint(raton):
                                seguir = False
                                jugadores_declinados.append(oferente)
                                if len(jugadores_declinados) + 1 == len(otros):
                                    for declinado in jugadores_declinados:
                                        otros.remove(declinado)
                            if btn_mas_cien.collidepoint(raton):
                                texto_importe = str(int(texto_importe) + 100)
                            if btn_ofertar.collidepoint(raton):
                                if int(texto_importe) > oferta_vigente[0]:
                                    oferta_vigente = (int(texto_importe), oferente)
                                    seguir = False
                                else:
                                    mostrar_mensaje((('La oferta debe ser superior a la vigente', 0),
                                                     ('', 0)))
                        elif evento.type == pygame.KEYDOWN:
                            if evento.key == pygame.K_BACKSPACE:
                                texto_importe = texto_importe[:-1]
                            elif evento.unicode.isdigit():
                                texto_importe += evento.unicode
                    pygame.display.update()
        if oferta_vigente[0] > 0:
            mostrar_mensaje(((oferta_vigente[1].nombre, 1),
                             ('Ha resultado ganador de la subasta', 1),
                             ('Ha comprado ' + a_subastar.nombre, 0),
                             ('por $' + str(oferta_vigente[0]), 0)))
            return oferta_vigente, a_subastar


    else:
        mostrar_mensaje(((jugador.nombre, 1),('Para realizar una subasta', 0),
                         ('debe haber por lo menos 2 jugadores aparte de usted', 0)))


def saldo_negativo(jugador,jugadores_activos):
    pintar_tablero(pantalla,largo_utilizable,x,y,jugadores_activos)
    info_jugador(jugador,jugadores_activos)
    mostrar_mensaje(((jugador.nombre, 1), ('Su saldo es: -$'+str(-jugador.dinero), 0),
                     ('debera saldar su deuda antes de poder seguir', 0),
                     ('de no poder hacerlo, sera declarado en', 0),
                     ('BANCARROTA', 1), ('y quedara fuera de juego.', 0)))
    pintar_tablero(pantalla,largo_utilizable,x,y,jugadores_activos)
    seguir = True
    while seguir:
        pygame.draw.rect(pantalla, constantes.naranja, (x / 4, y / 4, x / 2, y / 2), 0, int(x / 20))
        linea1 = fuente_encabezado.render('Para saldar su deuda, usted podra:', True, constantes.blanco)
        rect_linea1 = linea1.get_rect()
        linea2 = fuente_botones.render('» Vender sus edificaciones.', True, constantes.blanco)
        rect_linea2 = linea2.get_rect()
        linea3 = fuente_botones.render('» Hipotecar sus propiedades.', True, constantes.blanco)
        rect_linea3 = linea3.get_rect()
        linea4 = fuente_botones.render('» Vender sus propiedades.', True, constantes.blanco)
        rect_linea4 = linea4.get_rect()
        linea5 = fuente_botones.render('» Poner en remate sus propiedades', True, constantes.blanco)
        rect_linea5 = linea5.get_rect()
        linea6 = fuente_botones.render('O bien, declararse en banca rota', True, constantes.blanco)
        rect_linea6 = linea6.get_rect()
        x_de_botones = (max((rect_linea2[2]), (rect_linea3[2]), (rect_linea4[2]), (rect_linea5[2]), (rect_linea6[2]))) + x / 20 + x / 3.5
        txt_edificaciones = fuente_botones.render('Vender edificaciones', True, constantes.negro)
        rect_txt_edificaciones = txt_edificaciones.get_rect()
        txt_hipotecar = fuente_botones.render('Hipotecar propiedades', True, constantes.negro)
        rect_txt_hipotecar = txt_hipotecar.get_rect()
        txt_propiedades = fuente_botones.render('Vender propiedades', True, constantes.negro)
        rect_txt_propiedades = txt_propiedades.get_rect()
        txt_rematar = fuente_botones.render('Rematar', True, constantes.negro)
        rect_txt_rematar = txt_rematar.get_rect()
        txt_bancarrota = fuente_botones.render('Bancarrota', True, constantes.negro)
        rect_txt_bancarrota = txt_bancarrota.get_rect()
        ancho_botones = max(rect_txt_edificaciones[2], rect_txt_hipotecar[2], rect_txt_propiedades[2], rect_txt_rematar[2], rect_txt_bancarrota[2]) + x / 40
        color1 = constantes.verde
        color2 = constantes.verde
        color3 = constantes.verde_oscuro
        color4 = constantes.verde_oscuro
        btn_edificaciones_habilitado = True
        btn_hipotecar_habilitado = True
        btn_propiedades_habilitado = False
        btn_rematar_habilitado = False
        btn_bancarrota_habilitado = True
        if jugador.chacras == 0:
            color1 = constantes.verde_oscuro
            btn_edificaciones_habilitado = False
        if len(jugador.propiedades) == jugador.hipotecadas:
            color2 = constantes.verde_oscuro
            btn_hipotecar_habilitado = False
        if len(jugador.propiedades) > 0:
            for propiedad in jugador.propiedades:
                if not isinstance(propiedad,tablero.Campo) or propiedad.edificaciones == 0:
                    color3 = constantes.verde
                    color4 = constantes.verde
                    btn_propiedades_habilitado = True
                    btn_rematar_habilitado = True
        btn_edificaciones = (pygame.draw.rect(pantalla, color1,
                                              (x_de_botones, y / 4 + 3 * y / 20,
                                               ancho_botones,
                                               y / 30), 0, int( y / 15)),
                                               'edifcaciones',
                                               btn_edificaciones_habilitado)
        btn_hipotecar = (pygame.draw.rect(pantalla, color2,
                                           (x_de_botones, y / 4 + 4 * y / 20,
                                            ancho_botones,
                                            y / 30), 0, int(y / 15)), 'hipotecar',
                                           btn_hipotecar_habilitado)
        btn_propiedades = (pygame.draw.rect(pantalla, color3,
                                             (x_de_botones, y / 4 + 5 * y / 20,
                                              ancho_botones,
                                              y / 30), 0, int(y / 15)), 'propiedades',
                                             btn_propiedades_habilitado)
        btn_rematar = (pygame.draw.rect(pantalla, color4,
                                         (x_de_botones, y / 4 + 6 * y / 20,
                                          ancho_botones,
                                          y / 30), 0, int(y / 15)), 'rematar',
                                         btn_rematar_habilitado)
        btn_bancarrota = (pygame.draw.rect(pantalla, constantes.rojo,
                                            (x_de_botones, y / 4 + 8 * y / 20,
                                             ancho_botones,
                                             y / 30), 0, int(y / 15)), 'bancarrota',
                                           btn_bancarrota_habilitado)
        pygame.draw.rect(pantalla, constantes.negro,
                         (x_de_botones, y / 4 + 8 * y / 20,
                          ancho_botones, y / 30), 2, int(y / 15))
        botones = (btn_edificaciones, btn_hipotecar, btn_propiedades, btn_rematar, btn_bancarrota)
        rect_linea1.left = x / 3.5
        rect_linea2.left = rect_linea1.left + x / 40
        rect_linea3.left = rect_linea1.left + x / 40
        rect_linea4.left = rect_linea1.left + x / 40
        rect_linea5.left = rect_linea1.left + x / 40
        rect_linea6.left = x / 3.5
        rect_linea1.centery = y / 4 + y / 20
        rect_linea2.centery = btn_edificaciones[0].centery
        rect_linea3.centery = btn_hipotecar[0].centery
        rect_linea4.centery = btn_propiedades[0].centery
        rect_linea5.centery = btn_rematar[0].centery
        rect_linea6.centery = btn_bancarrota[0].centery
        rect_txt_edificaciones.center = btn_edificaciones[0].center
        rect_txt_hipotecar.center = btn_hipotecar[0].center
        rect_txt_propiedades.center = btn_propiedades[0].center
        rect_txt_rematar.center = btn_rematar[0].center
        rect_txt_bancarrota.center = btn_bancarrota[0].center
        pantalla.blits(blit_sequence = ((linea1, rect_linea1),
                                        (linea2, rect_linea2),
                                        (linea3, rect_linea3),
                                        (linea4, rect_linea4),
                                        (linea5, rect_linea5),
                                        (linea6, rect_linea6),
                                        (txt_edificaciones, rect_txt_edificaciones),
                                        (txt_hipotecar, rect_txt_hipotecar),
                                        (txt_propiedades, rect_txt_propiedades),
                                        (txt_rematar, rect_txt_rematar),
                                        (txt_bancarrota, rect_txt_bancarrota)))
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                raton = pygame.mouse.get_pos()
                for btn in botones:
                    if btn[0].collidepoint(raton) and btn[2]:
                        return btn[1]


def nombrar_jugador(num_jugador, jugadoresActivos):
    pygame.draw.rect(pantalla, constantes.blanco, (x / 4, y / 4, x / 2, y / 2), 0, int(x / 50))
    renglon1 = fuente_encabezado.render('Ingrese el nombre del jugador N° ' + str(num_jugador), True, constantes.negro)
    rect_renglon1 = renglon1.get_rect()
    rect_renglon1.center = (x / 2, y / 3)
    renglon2 = fuente_encabezado.render('Y seleccione el color', True, constantes.negro)
    rect_renglon2 = renglon2.get_rect()
    rect_renglon2.center = (x / 2, y / 2.5)
    btns_peones = []
    for peon in constantes.peones:
        x_peon = x / 4 + x / (2 * len(constantes.peones)) * constantes.peones.index(peon) + y / 40
        btn = pygame.draw.rect(pantalla, constantes.peones_dic[peon], (x_peon, 2 * y / 3, y / 20, y / 20), 0, y // 40)
        pygame.draw.rect(pantalla, constantes.negro, (x_peon, 2 * y / 3, y / 20, y / 20), 2, y // 40)
        btns_peones.append((btn, peon))
    cont = 0
    txt_nombre = ''
    color_cursor = constantes.verde
    seguir = True
    peon_seleccionado =''
    while seguir:
        cont += 1
        cuadro_texto = pygame.draw.rect(pantalla, constantes.negro, (2 * x / 5, y / 2, x / 5, y / 15), 0, int(x / 15))
        nombre = fuente_encabezado.render(txt_nombre, True, constantes.verde)
        rect_nombre = nombre.get_rect()
        rect_nombre.center = cuadro_texto.center
        if cont % 100 == 0:
            if color_cursor == constantes.verde:
                color_cursor = constantes.negro
            else:
                color_cursor = constantes.verde
        cursor = fuente_encabezado.render('|', True, color_cursor)
        rect_cursor = cursor.get_rect()
        rect_cursor.centery = cuadro_texto.centery - y / 100
        rect_cursor.left = rect_nombre.right
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                raton = pygame.mouse.get_pos()
                for btn_peon in btns_peones:
                    if btn_peon[0].collidepoint(raton):
                        txt_nombre, peon_seleccionado, seguir = comprobar_nombre(num_jugador,
                                                    jugadoresActivos,
                                                    btn_peon[1],
                                                    txt_nombre)
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    peon = constantes.peones[0]
                    txt_nombre, peon_seleccionado, seguir = comprobar_nombre(num_jugador,
                                              jugadoresActivos,
                                              peon,
                                              txt_nombre)
                elif evento.key == pygame.K_BACKSPACE:
                    txt_nombre = txt_nombre[:-1]
                else:
                    txt_nombre += evento.unicode
                    txt_nombre = txt_nombre.capitalize()
        pantalla.blits(blit_sequence = ((renglon1, rect_renglon1),
                                        (nombre, rect_nombre),
                                        (cursor, rect_cursor),
                                        (renglon2, rect_renglon2)))
        pygame.display.update()
    return txt_nombre, peon_seleccionado

def comprobar_nombre(num_jugador, jugadoresActivos, peon, txt_nombre):
    seguir = False
    peon_seleccionado = peon
    if txt_nombre == '':
        seguir = True
        pygame.draw.rect(pantalla, constantes.blanco,
                         (x / 4, y / 4, x / 2, y / 2), 0, int(x / 50))
        mostrar_mensaje((('El nombre debe contener por lo menos un caracter', 0), ('', 0)))
        txt_nombre, peon_seleccionado = nombrar_jugador(num_jugador, jugadoresActivos)
    else:
        for jugador in jugadoresActivos:
            if jugador.nombre == txt_nombre:
                seguir = True
                pygame.draw.rect(pantalla, constantes.blanco,
                                 (x / 4, y / 4, x / 2, y / 2), 0, int(x / 50))
                mostrar_mensaje((('El nombre "' + txt_nombre + '" ya esta ocupado', 0), ('Por favor, elija otro', 0)))
                txt_nombre, peon_seleccionado = nombrar_jugador(num_jugador, jugadoresActivos)
    return txt_nombre, peon_seleccionado, seguir



def fuentes(ancho):
    fuente_numero = pygame.font.SysFont('impact', int(ancho / 3))
    fuente_provincia = pygame.font.SysFont('Impact', int(ancho / 5))
    fuente_nombre = pygame.font.SysFont('Impact', int(ancho / 4.5))
    fuente_valor = pygame.font.SysFont('Impact', int(ancho / 6))
    fuente_gigante = pygame.font.SysFont('comicsans', int(ancho))
    fuente_grande = pygame.font.SysFont('impact', int(ancho / 2.5))
    return (fuente_numero, fuente_provincia, fuente_nombre,
            fuente_valor, fuente_gigante, fuente_grande)

def dibujar_rectangulo_inclinado(pantalla, casillero, vertice1: tuple,
                                 ancho: int, alto: int, jugadores,
                                 seleccionables, accion, seleccionados=[],
                                  angulo=False):

    """Dibuja un rectangulo con una inclinacion(giro) se debe pasar por
    parametro: donde dibujar(pantalla), color como una tupla(R,G,B), el ancho,
    el alto, el angulo en grados(antihorario),
    y opcional, el espesor de la linea(defecto=relleno)"""

    if not angulo:
        angulo = casillero.angulo
    angulo_rad = math.radians(angulo)
    vertice2 = (math.cos(angulo_rad) * ancho + vertice1[0],
                vertice1[1] - math.sin(angulo_rad) * ancho)
    vertice4 = (math.cos(angulo_rad + math.pi / 2) * alto + vertice1[0],
                vertice1[1] - math.sin(angulo_rad + math.pi / 2) * alto)
    vertice3 = (math.cos(angulo_rad) * ancho + vertice4[0],
                vertice4[1] - math.sin(angulo_rad) * ancho)
    vertices = (vertice1, vertice2, vertice3, vertice4)
    centro = (vertice1[0] - math.sin(math.radians(angulo + 14)) * alto * 0.9,
               vertice1[1] - math.cos(math.radians(angulo + 14)) * alto * 0.9)

    color = casillero.color2
    if accion == 'Pedir' or accion == 'Ofrecer' or accion =='Subastar':
        if casillero not in seleccionables:
            color =  constantes.negro
        elif casillero in seleccionados:
            color = (100, 100, 255)
    else:
        if isinstance(casillero, tablero.Propiedad) and casillero.estado == 'Hipotecado':
            color = (255, 40, 50)
        if casillero in seleccionables:
            color =  constantes.verde
    pygame.draw.polygon(pantalla, color, vertices)
    pygame.draw.polygon(pantalla, constantes.negro, vertices, 2)

    en_casillero = []
    for jugador in jugadores:
        if jugador.ubicacion == casillero.numero:
            en_casillero.append(jugador)
    peones=[]
    for j_en_casillero in en_casillero:
        medio_arriba = ((vertice1[0] + vertice2[0]) / 2,
                        (vertice1[1] + vertice2[1]) / 2)
        centro_peon = (medio_arriba[0] - math.sin(math.radians(angulo)) * alto/(len(en_casillero) + 1) * (en_casillero.index(j_en_casillero) + 1),
                       medio_arriba[1] - math.cos(math.radians(angulo)) * alto/(len(en_casillero) + 1) * (en_casillero.index(j_en_casillero) + 1))
        peones.append((centro_peon,j_en_casillero.peon))
    if isinstance(casillero, tablero.Propiedad) and casillero.titular != 'Banco':
        vertice8 = (math.cos(angulo_rad + math.pi / 2) * alto * 0.8 + vertice1[0], vertice1[1] - math.sin(angulo_rad + math.pi / 2)*alto * 0.8)
        vertice9 = (math.cos(angulo_rad) * ancho + vertice8[0], vertice8[1] - math.sin(angulo_rad) * ancho)
        vertices3 = (vertice3, vertice4, vertice8, vertice9)
        for jugador in jugadores:
            if casillero.titular == jugador.nombre:
                color_dueño = constantes.peones_dic[jugador.peon]
                pygame.draw.polygon(pantalla, color_dueño, vertices3)
                pygame.draw.polygon(pantalla, constantes.negro, vertices3, 1)
    if isinstance(casillero, tablero.Campo):
        vertice6 = (math.cos(angulo_rad + math.pi / 2) * alto * 0.2 + vertice1[0], vertice1[1] - math.sin(angulo_rad + math.pi / 2) * alto * 0.2)
        vertice5 = (math.cos(angulo_rad) * ancho + vertice6[0], vertice6[1] - math.sin(angulo_rad) * ancho)
        vertices2 = (vertice1, vertice2, vertice5, vertice6)
        pygame.draw.polygon(pantalla, casillero.color, vertices2)
        pygame.draw.polygon(pantalla, constantes.negro, vertices2, 2)
        if casillero.edificaciones > 0:
            color_edificacion = constantes.azul
            cantidad = fuentes(ancho)[0].render(str(casillero.edificaciones), True, constantes.blanco)
            if casillero.edificaciones > 4:
                cantidad = fuentes(ancho)[0].render('', True, constantes.blanco)
                color_edificacion = constantes.rojo
            centro_edificaciones = ((vertice1[0] + vertice5[0]) / 2, (vertice1[1] + vertice5[1]) / 2)
            edificacion = pygame.draw.circle(pantalla, color_edificacion, centro_edificaciones, alto * -0.075)
            escribir_textos(pantalla, (cantidad,), (centro_edificaciones,), angulo)
    rellenar_casillero(pantalla, centro, ancho, casillero, angulo, alto, peones)
    casillero.vertices = vertices


def pintar_esquina(pantalla, casillero, vertice1: tuple, ancho: int, alto: int, jugadores, espesor: int = 0, ang = False):

    """Dibuja un romboide con una inclinacion(giro) se debe pasar por
    parametro: donde dibujar(pantalla), color como una tupla(R,G,B), el ancho,
    el alto, el angulo en grados(antihorario),
    y opcional, el espesor de la linea(defecto=relleno)"""

    angulo = casillero.angulo
    if ang:
        angulo = ang

    angulo_rad = math.radians(angulo)
    vertice2 = (vertice1[0] + math.cos(angulo_rad + math.radians(270)) * alto,
                vertice1[1] - math.sin(angulo_rad + math.radians(270)) * alto)
    vertice3 = (vertice1[0] + math.cos(angulo_rad + +math.radians(300)) * alto * 1.155,
                vertice1[1] - math.sin(angulo_rad + math.radians(300)) * alto * 1.155)
    vertice4 = (vertice1[0] + math.cos(angulo_rad + math.radians(330)) * alto,
                vertice1[1] - math.sin(angulo_rad + math.radians(330)) * alto)
    vertices = (vertice1, vertice2, vertice3, vertice4)
    pygame.draw.polygon(pantalla, casillero.color, vertices)
    pygame.draw.polygon(pantalla, constantes.negro, vertices, 2)
    centro = (vertice1[0] + math.sin(math.radians(angulo + 30)) * alto * 0.95,
              vertice1[1] + math.cos(math.radians(angulo + 30)) * alto * 0.95)
    en_casillero = []
    for jugador in jugadores:
        if jugador.ubicacion == casillero.numero:
            en_casillero.append(jugador)
    peones = []
    for j_en_casillero in en_casillero:
        centro_peon = (vertice1[0] + math.sin(math.radians(angulo + 30)) * alto / (len(en_casillero) + 1) * (en_casillero.index(j_en_casillero) + 1),
                       vertice1[1] + math.cos(math.radians(angulo + 30)) * alto / (len(en_casillero) + 1) * (en_casillero.index(j_en_casillero) + 1))
        peones.append((centro_peon, j_en_casillero.peon))
    rellenar_casillero(pantalla, centro, ancho, casillero, angulo + 30, -alto, peones)
    casillero.vertices = vertices

def rellenar_casillero(pantalla, centro, ancho, casillero, angulo, alto, peones):
    if casillero.numero != 0:
        if casillero.numero in (7, 14, 21, 28, 35):
            pygame.draw.circle(pantalla, constantes.negro, centro, ancho / 4)
        else:
            pygame.draw.circle(pantalla, constantes.rojo, centro, ancho / 4)
    fuente_numero, fuente_provincia, fuente_nombre, fuente_valor, fuente_gigante, fuente_grande = fuentes(ancho)
    numero = fuente_numero.render(casillero.numeroEnString, True, (255, 255, 0))
    textos = (numero,)
    centros = (centro,)
    if isinstance(casillero, tablero.Campo):
        provincia = fuente_provincia.render('PROVINCIA', True, constantes.negro)
        linea1 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.6,
                  centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.6)

        nombre = fuente_nombre.render(casillero.provincia, True, constantes.negro)
        linea2 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.5,
                  centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.5)

        zona = fuente_provincia.render('ZONA ' + casillero.zona, False, constantes.negro)
        linea3 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.3,
                   centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.3)

        valor = fuente_valor.render('Valor $' + str(casillero.valor), True, constantes.negro)
        linea4 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.2,
                   centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.2)
        textos = ((numero, provincia, nombre, zona, valor,))
        centros = (centro, linea1, linea2, linea3, linea4,)
    elif casillero.numero == 4 or casillero.numero == 41:
        frase = casillero.nombre.split(' ')
        renglon1 = fuente_nombre.render(frase[0], True, constantes.negro)
        renglon2 = fuente_nombre.render(frase[1] + ' ' + frase[2], True, constantes.negro)
        renglon3 = fuente_nombre.render(frase[3], True, constantes.negro)
        valor = fuente_valor.render(casillero.descripcion, True, constantes.negro)
        linea1 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.7,
                  centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.7)
        linea2 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.55,
                  centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.55)
        linea3 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.4,
                  centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.4)
        linea4 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.2,
                  centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.2)
        textos = ((numero, renglon1, renglon2, renglon3, valor,))
        centros = (centro, linea1, linea2, linea3, linea4,)
    elif isinstance(casillero, tablero.CasilleroTarjeta):
        if casillero.nombre == 'Destino':
            signo = '?'
        else:
            signo = '!'
        renglon1 = fuente_gigante.render(signo, True, constantes.blanco)
        renglon2 = fuente_nombre.render(casillero.nombre, True, constantes.blanco)
        linea1 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.6,
                  centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.6)
        linea2 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.25,
                  centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.25)
        textos = ((numero, renglon1, renglon2,))
        centros = (centro, linea1, linea2,)
    elif isinstance(casillero, tablero.Ferrocarril):
        imagen = pygame.transform.scale(pygame.image.load('img/tren.png'), (ancho * 0.8, ancho * 0.7))
        nombre = casillero.nombre.split(' ')
        renglon1 = fuente_provincia.render('FFCC', True, constantes.negro)
        renglon2 = fuente_provincia.render(nombre[1], True, constantes.negro)
        renglon3 = fuente_nombre.render(nombre[2]+'  ', True, constantes.negro)
        valor = fuente_valor.render('Valor $'+str(casillero.valor), True, constantes.negro)
        linea_imagen = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.75,
                        centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.75)
        linea1 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.58,
                  centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.58)
        linea2 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.5,
                  centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.5)
        linea3 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.4,
                  centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.4)
        linea_valor = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.2,
                       centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.2)
        textos = ((numero, renglon1, renglon2, renglon3, valor, imagen))
        centros = (centro, linea1, linea2, linea3, linea_valor, linea_imagen)
        if casillero.numero == 18 or casillero.numero == 22:
            renglon4 = fuente_nombre.render(nombre[3], True, constantes.negro)
            linea4 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.32,
                      centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.32)
            textos = ((numero, renglon1, renglon2, renglon3, renglon4, valor, imagen))
            centros = (centro, linea1, linea2, linea3, linea4, linea_valor, linea_imagen)
    elif isinstance(casillero, tablero.Compañia):
        size = (ancho * 0.8, ancho * 0.7)
        if casillero.numero == 8:
            png = 'img/petrolera.png'
        elif casillero.numero == 16:
            png = 'img/bodega.png'
            size = (ancho * 0.4, ancho * 0.65)
        else:
            png = 'img/ingenio.png'
        renglon = fuente_nombre.render(casillero.nombre, True, constantes.negro)
        linea = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.45,
                 centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.45)
        valor = fuente_valor.render('Valor $' + str(casillero.valor), True, constantes.negro)
        linea_valor = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.2,
                       centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.2)
        imagen = pygame.transform.scale(pygame.image.load(png), size)
        linea_imagen = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.7,
                        centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.7)
        textos = ((numero, renglon, valor, imagen))
        centros = (centro, linea, linea_valor, linea_imagen)
    else:
        if casillero.numero == 0:
            renglon1 = fuente_nombre.render('AL', True, (255, 255, 0))
            renglon2 = fuente_nombre.render('PASAR', True, (255, 255, 0))
            renglon3 = fuente_nombre.render('POR AQUI', True, (255, 255, 0))
            renglon4 = fuente_nombre.render('COBRE DEL', True, (255, 255, 0))
            renglon5 = fuente_nombre.render('BANCO $5000', True, (255, 255, 0))
            renglon6 = fuente_numero.render('SALIDA', True, (255, 255, 0))
            linea1 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.8,
                       centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.8)
            linea2 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.65,
                       centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.65)
            linea3 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.5,
                       centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.5)
            linea4 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.35,
                       centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.35)
            linea5 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.2,
                       centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.2)
            linea6 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * -0.0,
                       centro[1] - math.sin(math.radians(angulo - 90)) * alto * -0.0)
            textos = ((renglon1, renglon2, renglon3, renglon4, renglon5, renglon6))
            centros = (linea1, linea2, linea3, linea4, linea5, linea6)
        elif casillero.numero == 14 or casillero.numero == 21:
            renglon = fuente_grande.render(casillero.nombre.upper(), True, (255, 255, 0))
            linea = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.25,
                     centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.25)
            textos = (numero, renglon)
            centros = (centro, linea)
        else:
            nombre = casillero.nombre.split(' ')
            renglon1 = fuente_nombre.render(nombre[0].upper(), True, (255, 255, 0))
            renglon2 = fuente_nombre.render(nombre[1].upper(), True, (255, 255, 0))
            linea1 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.35,
                      centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.35)
            linea2 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.25,
                      centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.25)
            textos = (numero, renglon1, renglon2)
            centros = (centro, linea1, linea2)
            if casillero.numero == 7:
                renglon3 = fuente_provincia.render('COBRE', True, (255, 255, 0))
                renglon4 = fuente_provincia.render('$2500', True, (255, 255, 0))
                linea3 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.6,
                          centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.6)
                linea4 = (centro[0] + math.cos(math.radians(angulo - 90)) * alto * 0.5,
                          centro[1] - math.sin(math.radians(angulo - 90)) * alto * 0.5)
                textos = (numero, renglon1, renglon2, renglon3, renglon4)
                centros = (centro, linea1, linea2, linea3, linea4)
    escribir_textos(pantalla, textos, centros, angulo)
    for peon in peones:
        pygame.draw.circle(pantalla, constantes.peones_dic[peon[1]], peon[0], ancho / 4)
        if constantes.peones_dic[peon[1]] == constantes.negro:
            pygame.draw.circle(pantalla, constantes.blanco, peon[0], ancho / 10)
        else:
            pygame.draw.circle(pantalla, constantes.negro, peon[0], ancho / 10)


def escribir_textos(pantalla, textos, centros, angulo):
    index = 0
    for texto in textos:
        texto = pygame.transform.rotate(texto, angulo)
        rect_renglon = texto.get_rect()
        rect_renglon.center = centros[index]
        pantalla.blit(texto, rect_renglon)
        index += 1


def pintar_tablero(pantalla, largo_utilizable, x, y, jugadoresActivos, seleccionables = [], accion = '', seleccionados=[]):
    ancho_casillero = largo_utilizable * 0.057
    alto_casillero = largo_utilizable * 0.135
    origen_x = (x * 0.67 - ancho_casillero * 1.55)
    origen_y = ancho_casillero * math.sin(math.radians(120)) * 12 + alto_casillero
    delta_x_diagonal = ancho_casillero / 2
    delta_y_diagonal = ancho_casillero * math.sin(math.radians(60))
    fondo_original = pygame.image.load("img/centro_tableros.jpg").convert()
    ancho_fondo = 17 / 25 * largo_utilizable
    tamaño_fondo = (ancho_fondo, ancho_fondo * 0.879)
    fondo = pygame.transform.scale(fondo_original, (tamaño_fondo))
    rect_fondo = fondo.get_rect()
    rect_fondo.center = ((origen_x - 3 * ancho_casillero), y / 2)
    fondo.set_colorkey(constantes.negro)
    pantalla.fill((0, 0, 200))
    pantalla.blit(fondo, rect_fondo)
    for casillero in tablero.tablero:
        if casillero.numero in (0, 7, 14, 21, 28, 35):
            if casillero.numero == 0:
                vertice1 = (origen_x, origen_y)
                angulo = 0
            if casillero.numero == 7:
                vertice1 = (origen_x - 6 * ancho_casillero, origen_y)
                angulo = 300
            if casillero.numero == 14:
                vertice1 = (origen_x - 6 * (ancho_casillero + delta_x_diagonal), origen_y - delta_y_diagonal * 6)
                angulo = 240
            if casillero.numero == 21:
                vertice1 = (origen_x - 6 * ancho_casillero, origen_y - delta_y_diagonal * 12)
                angulo = 180
            if casillero.numero == 28:
                vertice1 = (origen_x, origen_y - delta_y_diagonal * 12)
                angulo = 120
            if casillero.numero == 35:
                vertice1 = (origen_x + 6 * (ancho_casillero * math.cos(math.radians(60))), origen_y - delta_y_diagonal * 6)
                angulo = 60
            pintar_esquina(pantalla, casillero, vertice1, ancho_casillero, alto_casillero, jugadoresActivos)

        else:
            if casillero.numero < 7:  # Horizontal abajo
                vertice1 = ((origen_x - ancho_casillero * casillero.numero), origen_y)
                angulo = 0

            elif casillero.numero < 14: # Diagonal \ izquierda
                origen_x2 = origen_x - ancho_casillero * 6
                origen_y2 = origen_y
                vertice1 = (origen_x2 - delta_x_diagonal * (casillero.numero - 7) , origen_y2 - delta_y_diagonal * (casillero.numero - 7))
                angulo = 300

            elif casillero.numero < 21: # Diagonal / izquierda
                origen_x2 = origen_x - (ancho_casillero * 6 + delta_x_diagonal * 7)
                origen_y2 = origen_y - 6 * delta_y_diagonal
                vertice1 = (origen_x2 + delta_x_diagonal * (casillero.numero - 13), origen_y2 - delta_y_diagonal * (casillero.numero - 14))
                angulo = 240

            elif casillero.numero < 28: # Horizontal arriba
                vertice1 = ((origen_x + ancho_casillero * (casillero.numero - 27)), alto_casillero)
                angulo = 180

            elif casillero.numero < 35: # Diagonal \ derecha
                origen_x2 = origen_x
                origen_y2 = origen_y - ancho_casillero * math.sin(math.radians(120))*11
                vertice1 = (origen_x2 + delta_x_diagonal * (casillero.numero - 28) , origen_y2 + delta_y_diagonal * (casillero.numero - 29 ))
                angulo = 120
            
            elif casillero.numero <= 41 : # Diagonal / derecha
                origen_x2 = origen_x + delta_x_diagonal*5
                origen_y2 = origen_y - delta_y_diagonal*5
                vertice1 = (origen_x2 - delta_x_diagonal * (casillero.numero - 36) , origen_y2 + delta_y_diagonal * (casillero.numero - 36))
                angulo = 60

            dibujar_rectangulo_inclinado(pantalla, casillero, vertice1,
                                         ancho_casillero, -alto_casillero,
                                         jugadoresActivos, seleccionables,
                                         accion, seleccionados)

def dibujar_tarjeta(pantalla, tarjeta, x):
    ancho_tarjeta = x / 2
    alto_tarjeta = ancho_tarjeta / 2
    if tarjeta.tipo == 'Destino':
        color = (0, 120, 0)
        color2 =  constantes.blanco
    else:
        color = (230, 170, 0)
        color2 =  constantes.negro
    x1 = (pantalla.get_size()[0] - ancho_tarjeta) / 2
    y1 = (pantalla.get_size()[1] - alto_tarjeta) / 2
    dibujo = pygame.draw.rect(pantalla, color, (x1, y1, ancho_tarjeta, alto_tarjeta))
    fuente = fuentes(ancho_tarjeta / 7)[0]
    textos = []
    
    if '   ' in tarjeta.texto:
        texto = tarjeta.texto.split('  ')
        linea1 = fuente.render(texto[0], True, color2)
        linea2 = fuente.render(texto[1], True, color2)
        linea3 = fuente.render(texto[2], True, color2)
        textos.append(linea1)
        textos.append(linea2)
        textos.append(linea3)

    elif '  ' in tarjeta.texto:
        texto = tarjeta.texto.split('  ')
        linea1 = fuente.render(texto[0], True, color2)
        linea2 = fuente.render(texto[1], True, color2)
        textos.append(linea1)
        textos.append(linea2)

    else:
        linea1 = fuente.render(tarjeta.texto, True, color2)
        textos.append(linea1)
    texto2 = fuente.render(str(tarjeta.id), True, color2)
    renglon = (x1 + alto_tarjeta, y1 + 20)
    rect_renglon = texto2.get_rect()
    rect_renglon.center = renglon
    pantalla.blit(texto2, rect_renglon)
    index = 0
    for texto in textos:
        rect_renglon = texto.get_rect()
        rect_renglon.center = (x1 + alto_tarjeta, y1 + (index + 1) * alto_tarjeta / (len(textos) + 1))
        pantalla.blit(texto, rect_renglon)
        index += 1
    pygame.display.update()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                return None



def mostrar_casillero(pantalla, raton, botones):
    escape = True
    medidas = pygame.display.get_window_size()
    jugadoresActivos = []
    casillero = identificar_click(botones, raton)
    if isinstance(casillero, int):
        return casillero
    if isinstance(casillero, tablero.Casillero):
        while escape:
            pantalla.fill(constantes.azul)
            if casillero.numero in (0, 7, 14, 21, 28, 35):
                pintar_esquina(pantalla, casillero, (x / 2, 0), 230, 560, jugadoresActivos, ang = 330)
            elif isinstance(casillero, tablero.Propiedad):
                x_inicial = x / 2 - 495
                fuente_numero, fuente_escritura, fuente_nombre, fuente_alquileres, fuente_gigante, fuente_grande = fuentes(150)
                pantalla.fill(constantes.azul)
                dibujar_rectangulo_inclinado(pantalla, casillero, (x_inicial + 10, 0), 230, -560, [], [], '', angulo = 360)
                pygame.draw.rect(pantalla, constantes.blanco, (x_inicial + 250, 0, 460, 560))
                pygame.draw.rect(pantalla, constantes.blanco, (x_inicial + 720, 0, 280, 560))
                escritura = 'ESCRITURA'
                dueno = 'DUEÑO:'
                numero = casillero.numeroEnString
                val_dueno = casillero.titular
                estado = 'ESTADO:'
                val_estado = casillero.estado
                textos1 = [dueno, val_dueno, estado, val_estado, escritura, numero]
                centros = ((x_inicial + 860, 140), (x_inicial + 860, 180),
                           (x_inicial + 860, 260), (x_inicial + 860, 300),
                           (x_inicial + 480, 140), (x_inicial + 480, 530))
                textos = []
                for texto in textos1:
                    textos.append(fuente_escritura.render(texto, 1, constantes.negro))
                escribir_textos(pantalla, textos, centros, 0)
                if isinstance(casillero, tablero.Campo):
                    pygame.draw.rect(pantalla, casillero.color, (x_inicial + 250, 0 , 460, 112))
                    pygame.draw.line(pantalla, constantes.negro, (x_inicial + 260, 385), (x_inicial + 700, 385), 3)
                    pygame.draw.line(pantalla, constantes.negro, (x_inicial + 260, 445), (x_inicial + 700, 445), 3)
                    nombre = fuente_nombre.render('Prov.' + casillero.nombre, 1, constantes.negro)
                    solo_campo = fuente_alquileres.render('Alquiler por solo el campo  ' + str(casillero.alquilerSolo), 1, constantes.negro)
                    chacra1 = fuente_alquileres.render('Idem con 1 chacra        '+str(casillero.alquiler1Chacra), 1, constantes.negro)
                    chacra2 = fuente_alquileres.render('Idem con 2 chacras       '+str(casillero.alquiler2Chacras), 1, constantes.negro)
                    chacra3 = fuente_alquileres.render('Idem con 3 chacras       '+str(casillero.alquiler3Chacras), 1, constantes.negro)
                    chacra4 = fuente_alquileres.render('Idem con 4 chacras       '+str(casillero.alquiler4Chacras), 1, constantes.negro)
                    estancia = fuente_alquileres.render('Idem con 1 estancia        '+str(casillero.alquiler1Estancia), 1, constantes.negro)
                    texto1 = fuente_alquileres.render('Teniendo una provincia completa, el', 1, constantes.negro)
                    texto2 = fuente_alquileres.render('Alquiler de los campos se duplica', 1, constantes.negro)
                    valor_chacra = fuente_alquileres.render('1 chacra vale '+str(casillero.precioChacra), 1, constantes.negro)
                    valor_estancia = fuente_alquileres.render('1 estancia vale '+str(casillero.precioChacra)+' mas 4 chacras', 1, constantes.negro)
                    textos = (nombre, solo_campo, chacra1, chacra2, chacra3, chacra4, estancia, texto1, texto2, valor_chacra, valor_estancia)
                    centros = ((x_inicial + 480, 180), (x_inicial + 480, 220),
                               (x_inicial + 480, 250), (x_inicial + 480, 280),
                               (x_inicial + 480, 310), (x_inicial + 480, 340),
                               (x_inicial + 480, 370), (x_inicial + 480, 400),
                               (x_inicial + 480, 430), (x_inicial + 480, 460),
                               (x_inicial + 480, 490))
                    escribir_textos(pantalla, textos, centros, 0)
                elif isinstance(casillero, tablero.Compañia):
                    nombre = fuente_nombre.render(casillero.nombre, 1, constantes.negro)
                    compania = '(Compañia)'
                    alquileres = 'Alquileres'
                    renglon1 = 'Teniendo 1 Cia. cobre 100'
                    renglon2 = 'veces lo que indican los dados'
                    renglon3 = 'Teniendo 2 Cia. cobre 200'
                    renglon5 = 'Teniendo 3 Cia. cobre 300'
                    textos1 = [compania, alquileres, renglon1, renglon2, renglon3, renglon2, renglon5, renglon2]
                    centros = ((x_inicial + 480, 180), (x_inicial + 480, 213),
                               (x_inicial + 480, 254), (x_inicial + 480, 290),
                               (x_inicial + 480, 312), (x_inicial + 480, 344),
                               (x_inicial + 480, 366), (x_inicial + 480, 398),
                               (x_inicial + 480, 420))
                    textos = [nombre]
                    for texto in textos1:
                        textos.append(fuente_alquileres.render(texto, 1, constantes.negro))
                    escribir_textos(pantalla, textos, centros, 0)
                    pygame.draw.line(pantalla, constantes.negro, (x_inicial + 340, 328), (x_inicial + 620, 328), 3)
                    pygame.draw.line(pantalla, constantes.negro, (x_inicial + 340, 384), (x_inicial + 620, 384), 3)
                elif isinstance(casillero, tablero.Ferrocarril):
                    nombre = fuente_nombre.render(casillero.nombre, 1, constantes.negro)
                    ferrocarril = '(Ferrocarril)'
                    alquileres = 'Alquileres'
                    renglon1 = 'Teniendo  1  F.C.___________ 500'
                    renglon2 = 'Teniendo  2  F.C.__________ 1000'
                    renglon3 = 'Teniendo  3  F.C.__________ 2000'
                    renglon4 = 'Teniendo  4  F.C.__________ 4000'
                    textos1 = [ferrocarril, alquileres, renglon1, renglon2, renglon3, renglon4]
                    centros = ((x_inicial + 480, 180), (x_inicial + 480, 213),
                               (x_inicial + 480, 254), (x_inicial + 480, 290),
                               (x_inicial + 480, 320), (x_inicial + 480, 350),
                               (x_inicial + 480, 380))
                    textos = [nombre]
                    for texto in textos1:
                        textos.append(fuente_alquileres.render(texto, 1, constantes.negro))
                    escribir_textos(pantalla, textos, centros, 0)
            else:
                dibujar_rectangulo_inclinado(pantalla, casillero,
                                             (x / 2 - 115, 50), 230, -560, [], [], '', angulo = 360)
            pygame.display.flip()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT or evento.type == pygame.MOUSEBUTTONDOWN:
                    escape = False

def identificar_click(botones, raton):
    for boton in botones:
        if boton[0].collidepoint(raton):
            return boton[1]
    for casillero in tablero.tablero:
        v1, v2, v3, v4 = casillero.vertices
        dis_a_x1 = raton[0] - v1[0]
        dis_a_x2 = raton[0] - v2[0]
        dis_a_y1 = raton[1] - v1[1]
        dis_a_y4 = raton[1] - v4[1]
        if casillero.numero in (0, 7, 14, 21, 28, 35):
            if casillero.numero == 0 or casillero.numero == 7:
                if (raton[0] > v1[0] - dis_a_y1 / math.tan(math.radians(casillero.angulo - 89.99999999999))
                and raton[0] < v1[0] - dis_a_y1 / math.tan(math.radians(casillero.angulo - 30.00000001))):
                    return casillero
            if casillero.numero == 21 or casillero.numero == 28:
                if (raton[0] < v1[0] - dis_a_y1 / math.tan(math.radians(casillero.angulo - 89.99999999999))
                and raton[0] > v1[0] - dis_a_y1 / math.tan(math.radians(casillero.angulo - 30.00000001))):
                    return casillero
            if casillero.numero == 14:
                if (raton[1] > v1[1] - dis_a_x1 * math.tan(math.radians(casillero.angulo - 90))
                and raton[1] < v1[1] - dis_a_x1 * math.tan(math.radians(casillero.angulo - 30))):
                    return casillero
            if casillero.numero == 35:
                if (raton[1] > v1[1] + dis_a_x1 * math.tan(math.radians(casillero.angulo - 90))
                and raton[1] < v1[1] + dis_a_x1 * math.tan(math.radians(casillero.angulo - 30))):
                    return casillero
        elif casillero.numero < 7:
            if raton[0] < v2[0] and raton[0] > v1[0] and raton[1] > v1[1] and raton[1] < v4[1]:
                return casillero
        elif casillero.numero < 21:
            if (v1[1]-dis_a_x1 * math.tan(math.radians(casillero.angulo - 90)) < raton[1]
            and v2[1]-dis_a_x2 * math.tan(math.radians(casillero.angulo - 90)) > raton[1]
            and v1[0]-dis_a_y1 / math.tan(math.radians(casillero.angulo)) > raton[0]
            and v4[0]-dis_a_y4 / math.tan(math.radians(casillero.angulo)) < raton[0]):
                return casillero
        elif casillero.numero < 28:
            if raton[0] > v2[0] and raton[0] < v1[0] and raton[1] < v1[1] and raton[1] > v4[1]:
                return casillero
        elif casillero.numero > 28:
            if (v1[1]-dis_a_x1 * math.tan(math.radians(casillero.angulo-90)) > raton[1]
            and v2[1]-dis_a_x2 * math.tan(math.radians(casillero.angulo-90)) < raton[1]
            and v1[0]-dis_a_y1/math.tan(math.radians(casillero.angulo)) < raton[0]
            and v4[0]-dis_a_y4/math.tan(math.radians(casillero.angulo)) > raton[0]):
                return casillero
        else:
            return None




def a(pantalla, botones):
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                raton = pygame.mouse.get_pos()
                return mostrar_casillero(pantalla, raton, botones)

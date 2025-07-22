import pygame
import tablero
import tarjetas
import vistas
import jugadores
import constantes

# inicializacion de targetas ""destino" y "suerte"
tarjetasDestino=tarjetas.listaTarjetasDestino
tarjetasSuerte=tarjetas.listaTarjetasSuerte

# inicializacion del banco
banco = jugadores.Jugador('Banco', 'ninguno')

# Asignacion de propiedades al banco
for casillero in tablero.tablero:
    if isinstance(casillero, tablero.Propiedad):
        banco.propiedades.append(casillero)

# Seleccion de cantidad de jugadores y creacion de los mismos
cantJugadores = vistas.inicio()
jugadoresActivos =[]
for i in range(cantJugadores):
    nombre, peon = vistas.nombrar_jugador(i+1,jugadoresActivos)
    jugador = jugadores.Jugador(nombre,peon)
    jugadoresActivos.append(jugador)
    constantes.peones.remove(peon)

# Asignacion de orden a los jugadores
jugadoresActivos = sorted(jugadoresActivos, reverse=True, key=lambda jugador: jugador.dados)
for jug in jugadoresActivos:
    jug.orden = jugadoresActivos.index(jug) + 1
    jug.dinero = 35000
    
def turno(jugador):
    '''Funcion que maneja el turno de un jugador, incluyendo acciones como tirar dados, comprar chacras, hipotecar propiedades, etc.'''
    if jugador.preso:
        respuesta = vistas.salir_carcel(jugador)
        if respuesta == 1: # Pagar fianza
            jugador.dinero -= 1000
            jugador.preso = False
            jugar(jugador)
        elif respuesta == 2: # Tirar dados
            dados = jugador.tirarDados(vistas.pantalla, vistas.x, vistas.y)
            jugador.intentos_salir -= 1
            if dados[3]: # Si saca doble
                jugador.preso = False
                jugar(jugador, dados, True)
            if jugador.intentos_salir < 0:
                jugador.preso = False
                jugar(jugador, dados, True)
            jugar(jugador)
        elif respuesta == 3: # Usar tarjeta Habeas Corpus
            tarjeta = jugador.tarjetas.pop(0)
            if tarjeta.tipo == 'Destino':
                tarjetasDestino.append(tarjeta)
            if tarjeta.tipo == 'Suerte':
                tarjetasSuerte.append(tarjeta)
            jugador.preso = False
    else:
        jugar(jugador)


def jugar(jugador, dados2 = 0, liberado = False):
    opcion = ""
    doble = 0
    dados = dados2
    habilitado = True
    if jugador.preso:
        habilitado = False
    if jugador.descansos > 0:
        habilitado = False
        jugador.descansos -= 1
    while opcion != 0 or habilitado:
        noEsNumero = True
        opciones_activas = []
        if habilitado and not jugador.preso and jugador.descansos == 0:
            if not liberado:
                opciones_activas.append(1) # Tirar dados
        for propiedad in jugador.propiedades:
            if isinstance(propiedad, tablero.Campo) and propiedad.completo and propiedad.edificaciones < 5:
                opciones_activas.append(2) # Comprar chacras
                break
        if jugador.chacras > 0:
            opciones_activas.append(3) # Vender chacras
        opciones_activas.append(4) # Listar propiedades por jugador
        if len(jugador.propiedades) > jugador.hipotecadas:
            opciones_activas.append(5) # Hipotecar propiedades
        if jugador.hipotecadas > 0:
            opciones_activas.append(6) # Levantar hipoteca
        opciones_activas.append(7) # Terminar turno
        if len(jugadoresActivos) > 2:
            opciones_activas.append(8) # Comerciar con otro jugador
        if not habilitado:
            opciones_activas.append(0) # Terminar turno
        vistas.pintar_tablero(vistas.pantalla, vistas.largo_utilizable, vistas.x, vistas.y, jugadoresActivos)
        botones = vistas.panel_opciones(opciones_activas, jugador, jugadoresActivos)
        if not liberado:
            opcion = vistas.a(vistas.pantalla, botones)
        else:
            opcion = 1
        pygame.display.update()
        if opcion == 1 and not jugador.preso:  # Tirar dados
            if habilitado:
                if not liberado:
                    dados = jugador.tirarDados(vistas.pantalla, vistas.x, vistas.y)
                else:
                    liberado = False
                habilitado = False
                if dados[3]:
                    doble += 1
                    habilitado = True
                if doble == 3:
                    habilitado = False
                    jugador.marchePreso()
                    vistas.pintar_tablero(vistas.pantalla, vistas.largo_utilizable, vistas.x, vistas.y, jugadoresActivos)
                    vistas.mostrar_mensaje(((jugador.nombre, 1), ('Usted ha sido detenido por abuso', 0), ('(sacar doble 3 veces consecutivas)', 0), ('MARCHE PRESO', 0)))
                else:
                    jugador.ubicacion += dados[2]
                    if jugador.ubicacion >= 42:
                        jugador.ubicacion -= 42
                        jugador.dinero += 5000
                        vistas.pintar_tablero(vistas.pantalla, vistas.largo_utilizable, vistas.x, vistas.y, jugadoresActivos)
                        vistas.mostrar_mensaje(((jugador.nombre, 1), ('Ha completado una vuelta', 0), ('Cobre $5000', 0)))
                    elif jugador.ubicacion == 14 or jugador.ubicacion == 35:
                        habilitado = False
                        vistas.pintar_tablero(vistas.pantalla, vistas.largo_utilizable, vistas.x, vistas.y, jugadoresActivos)
                        vistas.mostrar_mensaje(((jugador.nombre, 1), ('Usted ha sido detenido', 0), ('MARCHE PRESO', 0)))
                    else:
                        vistas.pintar_tablero(vistas.pantalla, vistas.largo_utilizable, vistas.x, vistas.y, jugadoresActivos)
                        vistas.info_jugador(jugador, jugadoresActivos)
                    casillero = tablero.tablero[jugador.ubicacion]
                    accionesCasillero(jugador, casillero, dados)
        elif opcion == 2:  # Comprar chacras/estancias
            seguir = True
            while seguir:
                edificables = []
                for propiedad in jugador.propiedades:
                    if isinstance(propiedad, tablero.Campo) and propiedad.completo and propiedad.edificaciones < 5:
                        edificables.append(propiedad)
                edificables = sorted(edificables, key=lambda it: it.numero)
                edificables2 = edificables.copy()
                for edificable in edificables2:
                    for zona in edificable.grupo:
                        if edificable.edificaciones > zona.edificaciones and edificable in edificables:
                            edificables.remove(edificable)
                if len(edificables) > 0:
                    rango = []
                    opcion2 = vistas.seleccionar_propiedad(edificables, jugadoresActivos, 'Edificar')
                    if opcion2 != 'C':
                        if opcion2.precioChacra <= jugador.dinero:
                            jugador.dinero -= opcion2.precioChacra
                            opcion2.edificaciones += 1
                            jugador.chacras += 1
                            if opcion2.edificaciones == 1:
                                opcion2.estado = '1 chacra'
                            elif opcion2.edificaciones == 2:
                                opcion2.estado = '2 chacras'
                            elif opcion2.edificaciones == 3:
                                opcion2.estado = '3 chacras'
                            elif opcion2.edificaciones == 4:
                                opcion2.estado = '4 chacras'
                            elif opcion2.edificaciones == 5:
                                opcion2.estado = '1 estancia'
                        else:
                            vistas.mostrar_mensaje((("Dinero insuficiente", 0), ('', 0)))
                    else:
                        vistas.mostrar_mensaje((('', 0), ('', 0), ("Terminado", 0), ('', 0)))
                        seguir = False
                else:
                    seguir = False
        elif opcion == 3:  # Vender chacras/estancias
            venderEdificaciones(jugador)
        elif opcion == 4:  # Listar propiedades por jugador
            vistas.listar_propiedades(jugadoresActivos)
        elif opcion == 5:  # Hipotecar propiedades
            hipotecar(jugador)
        elif opcion == 6:  # Des-hipotecar propiedades
            seguir = True
            while seguir:
                hipotecadas = []
                for propiedad in jugador.propiedades:
                    if propiedad.estado == 'Hipotecado':
                        hipotecadas.append(propiedad)
                if len(hipotecadas) > 0:
                    rango = []
                    for hipotecada in hipotecadas:
                        if hipotecada.debePagarDiesPorCiento:
                            print(hipotecadas.index(hipotecada), '.-', hipotecada.nombre, 'valor: $', hipotecada.valorHipotecado, '+ 10%($', hipotecada.valorHipotecado * 0.1, ')')
                        else:
                            print(hipotecadas.index(hipotecada), '.-', hipotecada.nombre, 'valor: $', hipotecada.valorHipotecado)
                        rango.append(hipotecadas.index(hipotecada))
                    opcion6 = vistas.seleccionar_propiedad(hipotecadas, jugadoresActivos, 'Deshipotecar')
                    if opcion6 != 'C':
                        aPagar = opcion6.valorHipotecado
                        if opcion6.debePagarDiesPorCiento:
                            aPagar *= 1.1
                        if aPagar <= jugador.dinero:
                            jugador.dinero -= aPagar
                            jugador.hipotecadas -= 1
                            hipotecada.debePagarDiesPorCiento = False
                            opcion6.completo = True
                            opcion6.estado = 'Solo campo'
                            for elemento in opcion6.grupo:
                                if not(elemento in jugador.propiedades) or elemento.estado == 'Hipotecado':
                                    opcion6.completo = False
                            if opcion6.completo:
                                for elemento in opcion6.grupo:
                                    elemento.estado = 'Provincia completa'
                                    elemento.completo = True
                            else:
                                opcion6.estado = 'Solo campo'
                        else:
                            print('Dinero insufisiente para levantar esta hipoteca')
                    else:
                        seguir = False
                else:
                    seguir = False
        elif opcion==7: # Comerciar con otro jugador
            comerciables = []
            for casillero in tablero.tablero:
                if isinstance(casillero, tablero.Propiedad) and casillero.titular != 'Banco':
                    comerciables.append(casillero)
            comerciar_otro(comerciables, jugador)
        elif opcion == 8:  # Subastar propiedades
            remate = vistas.rematar(jugador, jugadoresActivos)
            if remate:
                transferir(remate[0][1], jugador, remate[0][0], remate[1])


def comerciar_otro(comerciables, jugador):
    for casillero in comerciables:
        if isinstance(casillero, tablero.Campo):
            for hermano in casillero.grupo:
                if hermano.edificaciones > 0:
                    comerciables.remove(casillero)
                    break
    opcion7 = vistas.comerciar(comerciables, jugadoresActivos, jugador)
    if opcion7 != 'C':
        for propiedad in opcion7[0]:
            transferir(opcion7[4], jugador, 0, propiedad)
        for propiedad in opcion7[2]:
            transferir(jugador, opcion7[4], 0, propiedad)
        opcion7[4].dinero += int(opcion7[1])
        opcion7[4].dinero -= int(opcion7[3])
        jugador.dinero -= int(opcion7[1])
        jugador.dinero += int(opcion7[3])
    else:
        vistas.mostrar_mensaje((('Transaccion cancelada', 0), ('', 0)))


def accionesCasillero(jugador, casillero, dados):
    if isinstance(casillero, tablero.Propiedad):
        if casillero.titular == 'Banco':
            adquirir = vistas.mostrar_mensaje(((jugador.nombre, 1), ('Desea comprar', 0), (casillero.nombre, 1), ('Por $' + str(casillero.valor) + '?', 0)), True)
            if adquirir == 'S' or adquirir == 'SI':
                casillero.comprar(jugador, banco)
                vistas.mostrar_mensaje(((jugador.nombre, 1), ('Ha comprado', 0), (casillero.nombre, 1), ('por $' + str(casillero.valor), 0), ('Su saldo es $ ' + str(jugador.dinero), 0)))
            elif adquirir == 'N' and adquirir == 'NO ':
                vistas.mostrar_mensaje(((jugador.nombre, 1), ('NO ha comprado', 0), (casillero.nombre, 1)))
        elif casillero.titular != jugador.nombre:
            if casillero.estado != 'Hipotecado':
                if isinstance(casillero, tablero.Campo):
                    if casillero.estado == 'Solo campo':
                        valor = casillero.alquilerSolo
                    elif casillero.estado == 'Provincia completa':
                        valor = casillero.alquilerSolo * 2
                    elif casillero.estado == '1 chacra':
                        valor = casillero.alquiler1Chacra
                    elif casillero.estado == '2 chacras':
                        valor = casillero.alquiler2Chacras
                    elif casillero.estado == '3 chacras':
                        valor = casillero.alquiler3Chacras
                    elif casillero.estado == '4 chacras':
                        valor = casillero.alquiler4Chacras
                    elif casillero.estado == '1 estancia':
                        valor = casillero.alquiler1Estancia
                elif isinstance(casillero, tablero.Compañia):
                    valor = casillero.cantidad * dados[2] * 100
                elif isinstance(casillero, tablero.Ferrocarril):
                    valor = 500 * (2 ** (casillero.cantidad - 1))
                jugador.dinero -= valor
                for player in jugadoresActivos:
                    if player.nombre == casillero.titular:
                        dueño = player
                dueño.dinero += valor
                vistas.mostrar_mensaje(((jugador.nombre, 1), ('paga $' + str(valor), 0), ('a ' + dueño.nombre, 1), ('en concepto de alquiler por', 0), (casillero.nombre + ' ' + casillero.estado, 0)))
    elif isinstance(casillero, tablero.Especial):
        casillero.accion(jugador)
    elif isinstance(casillero, tablero.CasilleroTarjeta):
        vistas.mostrar_mensaje((('Usted ha llegado a un casillero de ' + casillero.nombre, 0), ('tome una tarjeta de la pila ' + casillero.nombre, 0)))
        if casillero.nombre == 'Suerte':
            tarjeta = tarjetasSuerte.pop(0)
            if not isinstance(tarjeta, tarjetas.TarjetaHabeasCorpus):
                tarjetasSuerte.append(tarjeta)
        else:
            tarjeta = tarjetasDestino.pop(0)
            if not isinstance(tarjeta, tarjetas.TarjetaHabeasCorpus):
                tarjetasDestino.append(tarjeta)
        vistas.dibujar_tarjeta(vistas.pantalla, tarjeta, vistas.x)
        tarjeta.accion(jugador, jugadoresActivos)
        if isinstance(tarjeta, tarjetas.TarjetaMover) or isinstance(tarjeta, tarjetas.TarjetaMoverHasta):
            casillero = tablero.tablero[jugador.ubicacion]
            accionesCasillero(jugador, casillero, dados)



def venderEdificaciones(jugador):
    seguir = True
    while seguir:
        vendibles=[]
        for propiedad in jugador.propiedades:
            if isinstance(propiedad,tablero.Campo) and propiedad.edificaciones>0:
                vendibles.append(propiedad)
        vendibles=sorted(vendibles, key=lambda it:it.numero)
        vendibles2 = vendibles.copy()
        for campo in vendibles2:
            for zona in campo.grupo:
                if campo.edificaciones < zona.edificaciones and campo in vendibles:
                    vendibles.remove(campo)
        if len(vendibles) > 0:
            rango = []
            for campo in vendibles:
                rango.append(vendibles.index(campo))
            opcion3 = vistas.seleccionar_propiedad(vendibles, jugadoresActivos, 'Vender chacras')
            if opcion3 != 'C':
                jugador.dinero += opcion3.precioChacra / 2
                opcion3.edificaciones -= 1
                jugador.chacras -= 1
                if opcion3.edificaciones == 1:
                    opcion3.estado = '1 chacra'
                elif opcion3.edificaciones == 2:
                    opcion3.estado = '2 chacras'
                elif opcion3.edificaciones == 3:
                    opcion3.estado = '3 chacras'
                elif opcion3.edificaciones == 4:
                    opcion3.estado = '4 chacras'
                elif opcion3.edificaciones == 0:
                    opcion3.estado = 'Provincia completa'
            else:
                vistas.mostrar_mensaje((('', 0), ('', 0), ("Terminado", 0), ('', 0)))
                seguir = False
        else:
            seguir = False


def hipotecar(jugador):
    seguir = True
    while seguir:
        hipotecables = []
        for campo in jugador.propiedades:
            if campo.estado == 'Solo campo' or campo.estado == 'Provincia completa' or (not isinstance(campo,tablero.Campo) and campo.estado != 'Hipotecado'):
                hipotecables.append(campo)
        for hipotecable in hipotecables:
            if isinstance(hipotecable,tablero.Campo):
                for campo in hipotecable.grupo:
                    if campo.edificaciones > 0 and hipotecable in hipotecables:
                        hipotecables.remove(hipotecable)
        if len(hipotecables) > 0:
            rango = []
            for hipotecable in hipotecables:
                rango.append(hipotecables.index(hipotecable))
            opcion5 = vistas.seleccionar_propiedad(hipotecables, jugadoresActivos, 'Hipotecar')
            if opcion5 != 'C':
                opcion5.estado = 'Hipotecado'
                jugador.hipotecadas += 1
                jugador.dinero += opcion5.valorHipotecado * 0.9
                if isinstance(opcion5, tablero.Campo):
                    for zona in opcion5.grupo:
                        if zona.estado == 'Provincia completa':
                            zona.estado = 'Solo campo'
                else:
                    for empresa in opcion5.grupo:
                        if empresa in jugador.propiedades:
                            empresa.cantidad -= 1
            else:
                seguir = False
        else:
            seguir = False



def transferir(comprador, vendedor, monto, campo):
    if campo.estado == 'Provincia completa':
        for hermano in campo.grupo:
            hermano.estado = 'Solo campo'
    campo.titular = comprador.nombre
    comprador.dinero -= monto
    comprador.propiedades.append(campo)
    comprador.propiedades = sorted(comprador.propiedades, key = lambda x:x.numero)
    vendedor.dinero += monto
    vendedor.propiedades.remove(campo)
    if campo.estado == 'Hipotecado':
        comprador.dinero -= (campo.valorHipotecado * 0.1)
        while True:
            respuesta = vistas.mostrar_mensaje(((comprador.nombre, 1),
                                                (campo.nombre + ' se encuentra bajo hipoteca.', 0),
                                                ('Desea levantar la hipoteca en este momento', 0),
                                                ('por $' + str(campo.valorHipotecado) + '?', 0),
                                                ('Recuerde que si no lo hace ahora', 0),
                                                ('cuando lo haga debera pagar un adicional del 10%', 0)), True)
            if respuesta == 'S' or respuesta == 'SI':
                comprador.dinero -= campo.valorHipotecado
                campo.estado = 'Solo campo'
                break
            elif respuesta == 'N' or respuesta == 'NO':
                campo.debePagarDiesPorCiento = True
                break
    if campo.estado != 'Hipotecado': # Esta linea debe ir asi, y no con un else, porque en el if anterior puede cambiar el estado de "campo.estado"
        campo.completo = True
        for elemento in campo.grupo:
            if not(elemento in comprador.propiedades):
                campo.completo = False
        if campo.completo:
            for elemento in campo.grupo:
                elemento.estado = 'Provincia completa'
                elemento.completo = True


def comprobarBancarrota():
    jugadores_quebrados = []
    for player in jugadoresActivos:
        while player.dinero < 0:
            opcion = vistas.saldo_negativo(player, jugadoresActivos)
            if opcion == 'edifcaciones':
                venderEdificaciones(player)
            elif opcion == 'hipotecar':
                hipotecar(player)
            elif opcion == 'propiedades':
                comerciar_otro(player.propiedades, player)
            elif opcion == 'rematar':
                remate = vistas.rematar(player, jugadoresActivos)
                if remate:
                    transferir(remate[0][1], player, remate[0][0], remate[1])
            elif opcion == 'bancarrota':
                vistas.mostrar_mensaje(((player.nombre,1),
                                        ('Ha sido declarado en BANCARROTA',0),
                                        ('y debe abandonar el juego.',0),
                                        ('Mas suerte en la proxima',1)))
                for propiedad in player.propiedades:
                    banco.propiedades.append(propiedad)
                    propiedad.titular = 'Banco'
                    propiedad.estado = ''
                    propiedad.debePagarDiesPorCiento = False
                    if isinstance(propiedad, tablero.Campo):
                        propiedad.edificaciones = 0
                    elif isinstance(propiedad, tablero.Ferrocarril) or isinstance(propiedad, tablero.Compañia):
                        propiedad.cantidad = 1
                jugadores_quebrados.append(player)
                break
    if len(jugadores_quebrados) > 0:
        for quebrado in jugadores_quebrados:
            jugadoresActivos.remove(quebrado)


def main():
    while len(jugadoresActivos) > 1:
        for jugador in jugadoresActivos:
            turno(jugador)
            comprobarBancarrota()
    vistas.mostrar_mensaje(((jugadoresActivos[0].nombre, 1),
                            ('FELICITACIONES', 1),
                            ('USTED HA GANADO', 1),
                            ('EL JUEGO', 1)))
    print('Ha ganado ' + jugadoresActivos[0].nombre)


main()
import vistas

class Casillero:
    def __init__(self, numero:int, nombre:str, color:tuple, angulo):
        self.numero = numero
        self.nombre = nombre
        self.numeroEnString = str(self.numero)
        self.color = color
        self.color2 =(255, 255, 255)
        self.angulo = angulo

    def __repr__(self) -> str:
        return f"{self.numeroEnString} {self.nombre}"


class Propiedad(Casillero):
    def __init__(self, numero, valor, grupo, nombre, color, angulo):
        super().__init__(numero, nombre, color, angulo)
        self.valor = valor
        self.titular = 'Banco'
        self.estado = ''
        self.grupo = grupo
        self.debePagarDiesPorCiento = False

    def comprar(self, jugador, banco):
        if self.titular == 'Banco' and jugador.dinero >= self.valor:
            self.titular = jugador.nombre
            jugador.dinero -= self.valor
            jugador.propiedades.append(self)
            jugador.propiedades = sorted(jugador.propiedades,
                                        key=lambda x: x.numero)
            banco.propiedades.remove(self)
            print('Dinero restante: $', jugador.dinero)

    def __repr__(self) -> str:
        return f"{super().__repr__()} {self.estado}"


class Campo(Propiedad):
    def __init__(self, numero, valor, nombre, zona, alquilerSolo,
    alquiler1Chacra, alquiler2Chacras, alquiler3Chacras, alquiler4Chacras,
    alquilerEstancia, precioChacra, grupo, color, angulo):
        super().__init__(numero, valor, grupo, nombre, color, angulo)
        self.grupoNumeros = grupo
        self.zona = zona
        self.provincia = nombre
        self.nombre = nombre + ' ' + self.zona
        self.alquilerSolo = alquilerSolo
        self.alquiler1Chacra = alquiler1Chacra
        self.alquiler2Chacras = alquiler2Chacras
        self.alquiler3Chacras = alquiler3Chacras
        self.alquiler4Chacras = alquiler4Chacras
        self.alquiler1Estancia = alquilerEstancia
        self.precioChacra = precioChacra
        self.valorHipotecado = valor / 2
        self.edificaciones = 0

    def comprar(self, jugador, banco):
        super().comprar(jugador, banco)
        self.completo = True
        for elemento in self.grupo:
            if not (elemento in jugador.propiedades):
                self.completo = False
        if self.completo:
            for elemento in self.grupo:
                elemento.estado = 'Provincia completa'
                elemento.completo = True
            print('Ha completado', self.provincia)
        else:
            self.estado = 'Solo campo'


class Ferrocarril(Propiedad):
    def __init__(self, numero, valor, nombre, grupo, valorHipotecado, color, angulo):
        super().__init__(numero, valor, grupo, nombre, color, angulo)
        self.grupo = grupo
        self.cantidad = 1
        self.valorHipotecado = valorHipotecado
        self.nombre = 'Ferrocarril: ' + nombre

    def comprar(self, jugador, banco):
        super().comprar(jugador, banco)
        cant = 0
        for propiedad in jugador.propiedades:
            if isinstance(propiedad, Ferrocarril):
                cant += 1
        for propiedad in jugador.propiedades:
            if isinstance(propiedad, Ferrocarril):
                propiedad.cantidad = cant
        print('Usted acumula', cant, 'Ferrocarril/es')



class Compañia(Propiedad):
    def __init__(self, numero, valor, nombre, grupo, color, angulo):
        super().__init__(numero, valor, grupo, nombre, color, angulo)
        self.grupo = grupo
        self.cantidad = 1
        self.valorHipotecado = 1900
        self.nombre = nombre

    def comprar(self, jugador, banco):
        super().comprar(jugador, banco)
        cant = 0
        for propiedad in jugador.propiedades:
            if isinstance(propiedad, Compañia):
                cant += 1
        for propiedad in jugador.propiedades:
            if isinstance(propiedad, Compañia):
                propiedad.cantidad = cant
        print('Usted acumula', cant, 'Compañia/s')


class CasilleroTarjeta(Casillero):
    def __init__(self, numero, nombre, color, angulo):
        super().__init__(numero, nombre, color, angulo)
        self.color2 = self.color


class Especial(Casillero):
    def __init__(self, numero, nombre, descripcion, color, angulo):
        super().__init__(numero, nombre, color, angulo)
        self.descripcion = descripcion
        self.color2 = self.color

    def accion(self, jugador):
        if self.numero != 21:
            vistas.mostrar_mensaje(((self.nombre, 1), (self.descripcion, 0)))
        if self.numero == 4:
            jugador.dinero -= 5000
        elif self.numero == 7:
            jugador.dinero += 2500
        elif self.numero == 14:
            jugador.marchePreso()
        elif self.numero == 21:
            quedarse = ''
            while quedarse != 'S' and quedarse != 'N':
                # quedarse=funciones.preguntaSiNo('¿Desea usted descansar por 2 turnos? s(pre-seleccionado,solo presione ENTER)/n: ')
                quedarse = vistas.mostrar_mensaje(((jugador.nombre, 1), ('Usted ha llegado a DESCANSO(21)', 0), ('Tiene derecho descansar por 2 turnos', 0), ('siempre y cuando, no saque doble en los dados', 0), ('¿Desea descansar?', 0)), True)
            if quedarse == 'S':
                dados = jugador.tirarDados(vistas.pantalla, vistas.x, vistas.y)
                print(dados[0], dados[1])
                if not dados[3]:
                    jugador.descansos = 2
                    vistas.mostrar_mensaje((('No ha sacado un doble, se queda 2 turnos a descansar', 0), ('', 0)),)
                else:
                    vistas.mostrar_mensaje((('Ha sacado un doble, no se puede quedar a descansar', 0), ('', 0)),)
                    print('Usted saco un doble, por lo cual, no se puede quedar a descansar')
        elif self.numero == 35:
            jugador.marchePreso()
        elif self.numero == 41:
            jugador.dinero -= 2000



cero = Especial(0, 'Salida', 'Al caer o pasar por aquí, cobre $5000 del BANCO', (0, 0, 0), 0)
uno = Campo(1, 1000, 'Formosa', 'Sur', 40, 200, 600, 1700, 3000, 4750, 1000, (1, 2, 3), (15, 100, 190), 0)
dos = Campo(2, 1000, 'Formosa', 'Centro', 40, 200, 600, 1700, 3000, 4750, 1000, (1, 2, 3), (15, 100, 190), 0)
tres = Campo(3, 1200, 'Formosa', 'Norte', 80, 400, 800, 3400, 6000, 9500, 1000, (1, 2, 3), (15, 100, 190), 0)
cuatro = Especial(4, 'Impuesto a los reditos', 'Pague $5000', (255, 255, 255), 0)
cinco = Campo(5, 2000, 'Rio Negro', 'Sur', 110, 570, 1700, 5150, 7600, 9500, 1000, (5, 6), (110, 190, 0), 0)
seis = Campo(6, 2200, 'Rio Negro', 'Norte', 150, 750, 2000, 5700, 8500, 11500, 1000, (5, 6), (110, 190, 0), 0)
siete = Especial(7, 'Premio ganadero', 'Cobre $2500', (50, 70, 0), 300)
ocho = Compañia(8, 3800, 'Petrolera', (8, 16, 31), (255, 255, 255), 300)
nueve = Campo(9, 2600, 'Salta', 'Sur', 200, 1000, 2800, 8500, 12000, 14200, 1500, (9, 11, 13), (250, 250, 0), 300)
dies = CasilleroTarjeta(10, 'Destino', (0, 120, 0), 300)
once = Campo(11, 2600, 'Salta', 'Centro', 200, 1000, 2800, 8500, 12000, 14200, 1500, (9, 11, 13), (250, 250, 0), 300)
doce = Ferrocarril(12, 3600, 'General Belgrano', (12, 18, 22, 27), 1900, (255, 255, 255), 300)
trece = Campo(13, 3000, 'Salta', 'Norte', 230, 1150, 3400, 9500, 13000, 17000, 1500, (9, 11, 13), (250, 250, 0), 300)
catorce = Especial(14, 'Comisaria', 'Usted ha sido detenido', (50, 70, 0), 240)
quince = CasilleroTarjeta(15, 'Suerte', (230, 170, 0), 240)
diesiseis = Compañia(16, 3800, 'Bodega', (8, 16, 31), (255, 255, 255), 240)
diesisiete = Campo(17, 3400, 'Mendoza', 'Sur', 250, 1350, 3800, 10500, 14200, 18000, 2000, (17, 19, 20), (200, 70, 180), 240)
diesiocho = Ferrocarril(18, 3600, 'General San Martin', (12, 18, 22, 27), 1800, (255, 255, 255), 240)
diesinueve = Campo(19, 3400, 'Mendoza', 'Centro', 250, 1350, 3800, 10500, 14200, 18000, 2000, (17, 19, 20), (200, 70, 180), 240)
veinte = Campo(20, 3800, 'Mendoza', 'Norte', 300, 1500, 4200, 11500, 15000, 19000, 2000, (17, 19, 20), (200, 70, 180), 240)
veintiuno = Especial(21, 'Descanso', 'Usted tiene derecho a descansar por 2 turnos', (50, 70, 0), 180)
veintidos = Ferrocarril(22, 3600, 'General Bartolome Mitre', (12, 18, 22, 27), 1800, (255, 255, 255), 180)
veintitres = Campo(23, 4200, 'Santa Fe', 'Sur', 350, 1700, 4750, 13000, 16000, 20000, 2500, (23, 24, 26), (0, 125, 0), 180)
veinticuatro = Campo(24, 4200, 'Santa Fe', 'Centro', 350, 1700, 4750, 13000, 16000, 20000, 2500, (23, 24, 26), (0, 125, 0), 180)
veinticinco = CasilleroTarjeta(25, 'Destino', (0, 120, 0), 180)
veintiseis = Campo(26, 4600, 'Santa Fe', 'Norte', 400, 2000, 5750, 14000, 17000, 21000, 2500, (23, 24, 26), (0, 125, 0), 180)
veintisiete = Ferrocarril(27, 3600, 'General Urquiza', (12, 18, 22, 27), 1700, (255, 255, 255), 180)
veintiocho = Especial(28, 'Libre Estacionamiento', 'Esta casilla no tiene ningun efecto', (50, 70, 0), 120)
veintinueve = Campo(29, 5000, 'Tucuman', 'Sur', 400, 2200, 6000, 15000, 18000, 21000, 3000, (29, 30), (250, 160, 0), 120)
treinta = Campo(30, 5400, 'Tucuman', 'Norte', 450, 2400, 6800, 16000, 19500, 23000, 3000, (29, 30), (250, 160, 0), 120)
treintayuno = Compañia(31, 5000, 'Ingenio', (8, 16, 31), (255, 255, 255), 120)
treintaydos = Campo(32, 6000, 'Cordoba', 'Sur', 500, 2500, 6500, 17000, 21000, 24000, 3000, (32, 33, 34), (0, 180, 240), 120)
treintaytres = Campo(33, 6000, 'Cordoba', 'Centro', 450, 2400, 6800, 16000, 19500, 23000, 3000, (32, 33, 34), (0, 180, 240), 120)
treintaycuatro = Campo(34, 6400, 'Cordoba', 'Norte', 550, 2850, 8500, 19000, 23000, 27000, 3000, (32, 33, 34), (0, 180, 240), 120)
treintaycinco = Especial(35, 'Marche preso', 'Usted ha sido detenido, dirijase a la comisaria(14)', (50, 70, 0), 60)
treintayseis = CasilleroTarjeta(36, 'Suerte', (230, 170, 0), 60)
treintaysiete = Campo(37, 7000, 'Bs. As.', 'Sur', 650, 3300, 9500, 22000, 25000, 30000, 4000, (37, 39, 40), (220, 30, 0), 60)
treintayocho = CasilleroTarjeta(38, 'Destino', (0, 120, 0), 60)
treintaynueve = Campo(39, 7000, 'Bs. As.', 'Centro', 650, 3300, 9500, 22000, 25000, 30000, 4000, (37, 39, 40), (220, 30, 0), 60)
cuarenta = Campo(40, 7400, 'Bs. As.', 'Norte', 1000, 4000, 12000, 26000, 31000, 36000, 4000, (37, 39, 40), (220, 30, 0), 60)
cuarentayuno = Especial(41, 'Impuesto a las ventas', 'Pague $2000', (255, 255, 255), 60)

uno.grupo = (uno, dos, tres)
dos.grupo = (uno, dos, tres)
tres.grupo = (uno, dos, tres)
cinco.grupo = (cinco, seis)
seis.grupo = (cinco, seis)
ocho.grupo = (ocho, diesiseis, treintayuno)
nueve.grupo = (nueve, once, trece)
once.grupo = (nueve, once, trece)
doce.grupo = (doce, diesiocho, veintidos, veintisiete)
trece.grupo = (nueve, once, trece)
diesiseis.grupo = (ocho, diesiseis, treintayuno)
diesisiete.grupo = (diesisiete, diesinueve, veinte)
diesiocho.grupo = (doce, diesiocho, veintidos, veintisiete)
diesinueve.grupo = (diesisiete, diesinueve, veinte)
veinte.grupo = (diesisiete, diesinueve, veinte)
veintidos.grupo = (doce, diesiocho, veintidos, veintisiete)
veintitres.grupo = (veintitres, veinticuatro, veintiseis)
veinticuatro.grupo = (veintitres, veinticuatro, veintiseis)
veintiseis.grupo = (veintitres, veinticuatro, veintiseis)
veintisiete.grupo = (doce, diesiocho, veintidos, veintisiete)
veintinueve.grupo = (veintinueve, treinta)
treinta.grupo = (veintinueve, treinta)
treintayuno.grupo = (ocho, diesiseis, treintayuno)
treintaydos.grupo = (treintaydos, treintaytres, treintaycuatro)
treintaytres.grupo = (treintaydos, treintaytres, treintaycuatro)
treintaycuatro.grupo = (treintaydos, treintaytres, treintaycuatro)
treintaysiete.grupo = (treintaysiete, treintaynueve, cuarenta)
treintaynueve.grupo = (treintaysiete, treintaynueve, cuarenta)
cuarenta.grupo = (treintaysiete, treintaynueve, cuarenta)

tablero = (cero, uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve,
           dies, once, doce, trece, catorce, quince, diesiseis, diesisiete,
           diesiocho, diesinueve, veinte, veintiuno, veintidos, veintitres,
           veinticuatro, veinticinco, veintiseis, veintisiete, veintiocho,
           veintinueve, treinta, treintayuno, treintaydos, treintaytres,
           treintaycuatro, treintaycinco, treintayseis, treintaysiete,
           treintayocho, treintaynueve, cuarenta, cuarentayuno)
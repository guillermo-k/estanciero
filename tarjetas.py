from random import shuffle


class Tarjeta:
    def __init__(self,id,tipo,texto,) -> None:
        self.tipo=tipo
        self.texto=texto
        self.id=id

    def __str__(self) -> str:
        return self.texto

    def accion(self,jugador,jugadoresActivos):
        print('Tarjeta ',self.tipo)
        print(self.texto)
        habilitado = True
        return habilitado


class TarjetaPagar(Tarjeta):
    def __init__(self, id, tipo, texto, monto) -> None:
        super().__init__(id, tipo, texto)
        self.monto=monto

    def accion(self, jugador,jugadoresActivos):
        super().accion(jugador,jugadoresActivos)
        jugador.dinero-=self.monto


class TarjetaCobrar(Tarjeta):
    def __init__(self, id, tipo, texto, monto) -> None:
        super().__init__(id, tipo, texto)
        self.monto=monto

    def accion(self, jugador,jugadoresActivos):
        super().accion(jugador,jugadoresActivos)
        jugador.dinero+=self.monto


class TarjetaMover(Tarjeta):
    def __init__(self, id, tipo, texto) -> None:
        super().__init__(id, tipo, texto)

    def accion(self, jugador,jugadoresActivos):
        super().accion(jugador,jugadoresActivos)
        jugador.ubicacion-=3


class TarjetaMoverHasta(Tarjeta):
    def __init__(self, id, tipo, texto, casilleroDestino, direccion) -> None:
        super().__init__(id, tipo, texto)
        self.casilleroDestino=casilleroDestino
        self.direccion=direccion

    def accion(self, jugador,jugadoresActivos):
        super().accion(jugador,jugadoresActivos)
        if self.direccion=='avanzar' and jugador.ubicacion>self.casilleroDestino:
            jugador.dinero+=5000
            print(jugador.nombre,' ha completado una vuelta, cobra $5000')
        jugador.ubicacion=self.casilleroDestino


class TarjetaHabeasCorpus(Tarjeta):
    def __init__(self, id, tipo, texto) -> None:
        super().__init__(id, tipo, texto)

    def accion(self, jugador,jugadoresActivos):
        super().accion(jugador,jugadoresActivos)
        jugador.tarjetas.append(self)

class TarjetaCobrarDeJugadores(Tarjeta):
    def __init__(self, id, tipo, texto) -> None:
        super().__init__(id, tipo, texto)
        self.monto=200

    def accion(self, jugador,jugadoresActivos):
        super().accion(jugador,jugadoresActivos)
        for player in jugadoresActivos:
            player.dinero-=200
        jugador.dinero+=200*len(jugadoresActivos)


class TarjetaMultaOSuerte(Tarjeta):
    def __init__(self, id, tipo, texto) -> None:
        super().__init__(id, tipo, texto)

    def accion(self, jugador,jugadoresActivos):
        super().accion(jugador,jugadoresActivos)
        noEsNumero=True
        while noEsNumero:
            print('Elija una opcion')
            print('1.- Pague 200 de multa')
            print('2.- Levante una tarjeta de SUERTE')
            try:
                opcion=int(input())
                noEsNumero=False
            except:
                print('Debe ingresar un numero')
        if opcion==1:
            jugador.dinero-=200
        elif opcion==2:
            nuevaTarjeta=listaTarjetasSuerte.pop(0)
            if not isinstance(nuevaTarjeta,TarjetaHabeasCorpus):
                listaTarjetasSuerte.append(nuevaTarjeta)
            nuevaTarjeta.accion(jugador,jugadoresActivos)


class TarjetaMarchePreso(Tarjeta):
    def __init__(self, id, tipo, texto) -> None:
        super().__init__(id, tipo, texto)

    def accion(self, jugador,jugadoresActivos):
        super().accion(jugador,jugadoresActivos)
        jugador.marchePreso()
        habilitado = False


class TarjetaPagarPorChacras(Tarjeta):
    def __init__(self, id, tipo, texto, monto) -> None:
        super().__init__(id, tipo, texto)
        self.monto=monto

    def accion(self, jugador,jugadoresActivos):
        super().accion(jugador,jugadoresActivos)
        montoAPagar=self.monto*jugador.chacras
        jugador.dinero-=montoAPagar
        print(jugador.nombre,' paga al banco $',montoAPagar)


s1=TarjetaMarchePreso(1,'Suerte','Marche preso directamente')
s2=TarjetaPagar(2,'Suerte','Multa caminera. Pague 400',400)
s3=TarjetaCobrar(3,'Suerte','Ha ganado la grande. Cobre 10000',10000)
s4=TarjetaMoverHasta(4,'Suerte','Haga un paseo hasta la bodega.  Si pasa por la salida cobre 5000',16,'avanzar')
s5=TarjetaHabeasCorpus(5,'Suerte','Habeas Corpus concedido. Con esta tarjeta   sale usted gratuitamente de la Comisaria.   Consérvela o véndala')
s6=TarjetaMover(6,'Suerte','Vuelva tres pasos atras')
s7=TarjetaPagar(7,'Suerte','Multa por exceso de velocidad. Pague 300',300)
s8=TarjetaCobrar(8,'Suerte','Gano en las carreras. Cobre 3000',3000)
s9=TarjetaMoverHasta(9,'Suerte','Siga hasta Salta zona Norte.  Si pasa por la salida cobre 5000',13,'avanzar')
s10=TarjetaPagarPorChacras(10,'Suerte','Por compra de semilla pague al banco  800 por cada chacra. 4000 por cada estancia', 800)
s11=TarjetaPagar(11,'Suerte','Pague 3000 por gastos colegiales',3000)
s12=TarjetaMoverHasta(12,'Suerte','Siga hasta Santa Fé zona Norte.  Si pasa por la salida cobre 5000',26,'avanzar')
s13=TarjetaCobrar(13,'Suerte','Cobre 1000 por intereses bancarios',1000)
s14=TarjetaMoverHasta(14,'Suerte','Siga hasta la salida',0,'avanzar')
s15=TarjetaPagarPorChacras(15,'Suerte','Sus propiedades tienen que ser reparadas.   Pague al banco 500 por cada chacra   y 2500 por cada estancia', 500)
s16=TarjetaMoverHasta(16,'Suerte','Siga hasta Buenos Aires zona Norte',40,'avanzar')

d1=TarjetaMoverHasta(1,'Destino','Vuelve atras hasta Formosa zona Sur',1,'retroceder')
d2=TarjetaCobrar(2,'Destino','Ha ganado un concurso agrícola. Cobre 2000',2000)
d3=TarjetaCobrar(3,'Destino','Error en los calculos del Banco. Cobre 4000',4000)
d4=TarjetaMultaOSuerte(4,'Destino','Pague 200 de multa o levante una tarjeta de SUERTE')
d5=TarjetaPagar(5,'Destino','Pague su póliza de seguro con 1000',1000)
d6=TarjetaCobrar(6,'Destino','5% de interés sobre cédulas hipotecrias.  Cobre 500',500)
d7=TarjetaHabeasCorpus(7,'Destino','Con esta tarjeta sale usted   gratuitamente de la Comisaria.   Consérvela o véndala')
d8=TarjetaCobrar(8,'Destino','Hereda 2000',2000)
d9=TarjetaMoverHasta(9,'Destino','Siga hasta la salida',0,'avanzar')
d10=TarjetaCobrar(10,'Destino','Devolución de impuesto. Cobre 400',400)
d11=TarjetaCobrarDeJugadores(11,'Destino','Es su cumpleaños.  Cobre 200 de cada uno de los jugadores')
d12=TarjetaPagar(12,'Destino','Gastos de Farmacia. Pague 1000',1000)
d13=TarjetaMarchePreso(13,'Destino','Marche preso directamente')
d14=TarjetaCobrar(14,'Destino','Ha obtenido un segundo premio de belleza.  Cobre 200',200)
d15=TarjetaCobrar(15,'Destino','Por venta de acciones. Cobre 1000',1000)
d16=TarjetaCobrar(16,'Destino','Ha ganado un concurso agrícola. Cobre 2000',2000)

listaTarjetasSuerte=[s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16]
shuffle(listaTarjetasSuerte)
listaTarjetasDestino=[d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14,d15,d16]
shuffle(listaTarjetasDestino)

def TarjetasSuerte():
    return listaTarjetasSuerte

def TarjetasDestino():
    return listaTarjetasDestino
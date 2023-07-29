from modelos import Competidor
class ServicioCompetidores():
    def agregarCompetidores(self,competidores,idevento):
        listaCompetidores=[]
        for item in competidores:
           
            probabilidad = float(item["probabilidad"])
            cuota = round((probabilidad / (1 - probabilidad)), 2)
            competidor = Competidor(nombre_competidor=item["competidor"],
                                    probabilidad=probabilidad,
                                    cuota=cuota,
                                    id_evento=idevento)
            listaCompetidores.append(competidor)
    
        return listaCompetidores
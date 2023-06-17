export class Evento {

  id: number;
  nombre_evento: string;
  abierta: boolean;
  usuario: number;
  competidores: Array<Competidor>;
  apuestas: Array<Apuesta>;
  tipo_evento: string;
  es_empate: boolean;


  constructor(
    id: number,
    nombre_evento: string,
    abierta: boolean,
    usuario: number,
    competidores: Array<Competidor>,
    apuestas: Array<Apuesta>,
    tipo_evento: string,
    es_empate: boolean
  ) {
    this.id = id,
      this.nombre_evento = nombre_evento,
      this.abierta = abierta,
      this.usuario = usuario,
      this.competidores = competidores,
      this.apuestas = apuestas,
      this.tipo_evento = tipo_evento,
      this.es_empate = es_empate
  }
}

export class Apuesta {
  id: number;
  valor_apostado: number;
  ganancia: number;
  nombre_apostador: string;
  id_competidor: number;
  id_evento: number;

  constructor(
    id: number,
    valor_apostado: number,
    ganancia: number,
    nombre_apostador: string,
    id_competidor: number,
    id_evento: number
  ) {
    this.id = id,
      this.valor_apostado = valor_apostado,
      this.ganancia = ganancia,
      this.nombre_apostador = nombre_apostador,
      this.id_competidor = id_competidor,
      this.id_evento = id_evento
  }
}

export class Competidor {
  id: number;
  nombre_competidor: string;
  probabilidad: number;

  constructor(
    id: number,
    nombre_competidor: string,
    probabilidad: number
  ) {
    this.id = id,
      this.nombre_competidor = nombre_competidor,
      this.probabilidad = probabilidad
  }
}

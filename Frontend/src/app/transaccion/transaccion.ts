export class Transaccion {
  id: number;
  tipo_transaccion: string;
  descripcion: string;
  fecha: string;
  es_leido: boolean;
  valor: number;
  id_usuario: number;

  constructor(
      id: number,
      tipo_transaccion: string,
      descripcion: string,
      fecha: string,
      es_leido: boolean,
      valor: number,
      id_usuario: number,
  ) {
      this.id = id;
      this.tipo_transaccion = tipo_transaccion;
      this.descripcion = descripcion;
      this.fecha = fecha;
      this.es_leido = es_leido;
      this.valor = valor;
      this.id_usuario = id_usuario;
  }
}

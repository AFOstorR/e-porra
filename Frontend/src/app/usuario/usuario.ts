export class Usuario {
  id?: number;
  nombre?: string;
  numero_tarjeta?: string;
  usuario?: string;
  contrasena?: string;
  es_apostador?: boolean;
  monedero?: number;

  constructor(
      id: number,
      nombre: string,
      numero_tarjeta: string,
      usuario: string,
      contrasena: string,
      es_apostador: boolean,
      monedero: number
  ) {
      this.id = id;
      this.nombre = nombre;
      this.usuario = usuario;
      this.contrasena = contrasena;
      this.numero_tarjeta = numero_tarjeta;
      this.es_apostador = es_apostador;
      this.monedero = monedero;
  }
}

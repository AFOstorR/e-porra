export class Apuesta {
    id?: number;
    valor_apostado?: number;
    nombre_apostador?: string;
    id_competidor?: number;
    id_evento?: number;

    constructor(
        id: number,
        valor_apostado: number,
        nombre_apostador: string,
        id_competidor: number,
        id_evento: number
    ) {
        this.id = id,
            this.valor_apostado = valor_apostado,
            this.nombre_apostador = nombre_apostador,
            this.id_competidor = id_competidor,
            this.id_evento = id_evento
    }
}

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Usuario } from '../usuario/usuario';
import { Transaccion } from '../transaccion/transaccion'

@Injectable({
  providedIn: 'root'
})

export class TransaccionService {

  private backUrl: string = "https://e-porra-grupo11.herokuapp.com/"

  constructor(private http: HttpClient) { }

  getTransacciones(id_usuario: number, token: string): Observable<Transaccion[]>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
    return this.http.get<Transaccion[]>(`${this.backUrl}/transaccion/${id_usuario}`, {headers: headers})
  }

  postTransaccion(id_usuario: number, token: string, valor: number, tipo_transaccion: string): Observable<Usuario> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
    let body = {"valor": valor, "tipo_transaccion": tipo_transaccion}
    return this.http.post<Usuario>(`${this.backUrl}/transaccion/${id_usuario}`, body, {headers: headers})
  }

  putTransaccion(transaccion: Transaccion, transaccionId: number, token: string): Observable<Transaccion> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.put<Transaccion>(`${this.backUrl}/transaccion/${transaccionId}`, transaccion, { headers: headers })
  }
}

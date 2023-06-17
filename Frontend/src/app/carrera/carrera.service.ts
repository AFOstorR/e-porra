import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Evento, Competidor } from './carrera';

@Injectable({
  providedIn: 'root'
})

export class CarreraService {

  private backUrl: string = "https://e-porra-grupo11.herokuapp.com/"


  constructor(private http: HttpClient) { }

  getAllCarreras(token:string): Observable<Evento[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.get<Evento[]>(`${this.backUrl}/carreras`, {headers})
  }

  crearCarrera(idUsuario: number, token: string, carrera: Evento): Observable<Evento> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.post<Evento>(`${this.backUrl}/usuario/${idUsuario}/carreras`, carrera, { headers: headers })
  }

  getCarrera(idCarrera: number, token: string): Observable<Evento> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.get<Evento>(`${this.backUrl}/carrera/${idCarrera}`, { headers: headers })
  }

  editarCarrera(token: string, idCarrera: number, carrera: Evento): Observable<Evento> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.put<Evento>(`${this.backUrl}/carrera/${idCarrera}`, carrera, { headers: headers })
  }

  eliminarCarrera(token: string, idCarrera: number): Observable<Evento> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.delete<Evento>(`${this.backUrl}/carrera/${idCarrera}`, { headers: headers })
  }

  actualizarGanador(token: string, idCompetidor: number): Observable<Competidor> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.put<Competidor>(`${this.backUrl}/carrera/${idCompetidor}/terminacion`, { headers: headers })
  }

  verReporteCarrera(token: string, idCarrera: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.get<Object>(`${this.backUrl}/carrera/${idCarrera}/reporte`, { headers: headers })
  }

}

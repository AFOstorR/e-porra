import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Usuario } from './usuario';

@Injectable({
    providedIn: 'root'
})
export class UsuarioService {

    private backUrl: string = "https://e-porra-grupo11.herokuapp.com/"


    constructor(private http: HttpClient) { }

    userLogIn(usuario: string, contrasena: string): Observable<any> {
        return this.http.post<any>(`${this.backUrl}/login`, { "usuario": usuario, "contrasena": contrasena });
    }

    userSignUp(usuario: Usuario): Observable<any> {
        return this.http.post<any>(`${this.backUrl}/signin`, usuario)
    }

    updateUsuario(newUsuario: Usuario, id_usuario: number, token: string): Observable<Usuario> {
      const headers = new HttpHeaders({
        'Authorization': `Bearer ${token}`
      })
      return this.http.put<Usuario>(`${this.backUrl}/usuario/${id_usuario}`, newUsuario, { headers: headers })
    }

    getApostadores(token: string){
      const headers = new HttpHeaders({
        'Authorization': `Bearer ${token}`
      });
      return this.http.get<Usuario[]>(`${this.backUrl}/apostadores`, {headers})
    }

}

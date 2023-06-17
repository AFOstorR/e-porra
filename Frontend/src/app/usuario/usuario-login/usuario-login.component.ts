import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { JwtHelperService } from "@auth0/angular-jwt";
import { UsuarioService } from '../usuario.service';
import { TransaccionService } from '../../transaccion/transaccion.service'

@Component({
  selector: 'app-usuario-login',
  templateUrl: './usuario-login.component.html',
  styleUrls: ['./usuario-login.component.css']
})
export class UsuarioLoginComponent implements OnInit {

  helper = new JwtHelperService();

  constructor(
    private usuarioService: UsuarioService,
    private router: Router
  ) { }

  error: boolean = false

  ngOnInit() {
  }

  onLogInUsuario(usuario: string, contrasena: string) {
    this.error = false
    localStorage.clear();
    this.usuarioService.userLogIn(usuario, contrasena)
      .subscribe(res => {
        localStorage.setItem('usuario', JSON.stringify(res.usuario));
        const decodedToken = this.helper.decodeToken(res.token);
        this.router.navigate([`/carreras/${decodedToken.sub}/${res.token}`])
      },
        error => {
          this.error = true
        })
  }
}

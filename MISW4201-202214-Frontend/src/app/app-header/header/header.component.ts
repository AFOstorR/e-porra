import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Usuario } from 'src/app/usuario/usuario';
import { Transaccion } from '../../transaccion/transaccion';
import { TransaccionService } from '../../transaccion/transaccion.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  usuario: Usuario;
  notificaciones: Array<Transaccion> = []
  constructor(
    private routerPath: Router,
    private transaccionService: TransaccionService,
    private router: ActivatedRoute
  ) { }

  ngOnInit(): void {
    var usuarioLocal = localStorage.getItem('usuario');
    if(usuarioLocal != null){
      this.usuario = JSON.parse(usuarioLocal)
      this.onNotificacion(parseInt(this.router.snapshot.params.userId))
    }
  }

  onNotificacion(id_usuario: number) {
    const token = this.router.snapshot.params.userToken;
    this.transaccionService.getTransacciones(id_usuario, token).subscribe(resTrans => {
      if(resTrans != null) {
        if(resTrans.length > 0){
          if(resTrans.filter(t => !t.es_leido).length > 0) {
            this.notificaciones = resTrans.filter(t => !t.es_leido);
          }
        }
      }
    },
      error => {
        error = true
    })
  }

  goTo(menu: string) {
    const userId = parseInt(this.router.snapshot.params.userId);
    const token = this.router.snapshot.params.userToken;
    if (menu === "logIn") {
      this.routerPath.navigate([`/`])
    }
    else if (menu === "carrera") {
      this.routerPath.navigate([`/carreras/${userId}/${token}`])
    }
    else if (menu == "perfil"){
      this.routerPath.navigate([`/usuario/perfil/${userId}/${token}`])
    }
    else if (menu == "depositar"){
      this.routerPath.navigate([`transacciones/depositar/${userId}/${token}`])
    }
    else if (menu == "retirar"){
      this.routerPath.navigate([`transacciones/retirar/${userId}/${token}`])
    }
    else if (menu == "transacciones") {
      this.routerPath.navigate([`transacciones/ver/${userId}/${token}`])
    }
    else {
      this.routerPath.navigate([`/apuestas/${userId}/${token}`])
    }
  }

  eliminarNotificacion(id:number) {
    const token = this.router.snapshot.params.userToken;
    this.transaccionService.putTransaccion(this.notificaciones[id], this.notificaciones[id].id, token).subscribe(resp => {
      window.location.reload();
    },
      error => {
        error = true
    })
  }
}

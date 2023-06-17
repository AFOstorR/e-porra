import { Component, OnInit } from '@angular/core';
import { ActivatedRoute,Router } from '@angular/router';
import { Usuario } from '../../usuario/usuario';
import { TransaccionService } from '../transaccion.service'
import { ToastrService } from 'ngx-toastr';
import { Transaccion } from '../transaccion';


@Component({
  selector: 'app-ver-transacciones',
  templateUrl: './ver-transacciones.component.html',
  styleUrls: ['./ver-transacciones.component.css']
})
export class VerTransaccionesComponent implements OnInit {

  userId: number;
  token: string;
  usuario: Usuario;
  transacciones: Transaccion[];
  transacciones_mostrar: Transaccion[];
  mostrar_todo: boolean = false;


  constructor(
    private transaccionService: TransaccionService,
    private router: ActivatedRoute,
    private routerPath: Router,
    private toastr: ToastrService) { }

  ngOnInit() {
    if (!parseInt(this.router.snapshot.params.userId) || this.router.snapshot.params.userToken === " ") {
      this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
    }
    else {
      this.userId = parseInt(this.router.snapshot.params.userId)
      this.token = this.router.snapshot.params.userToken
      var usuarioLocal = localStorage.getItem('usuario');
      if (usuarioLocal != null){
        this.usuario = JSON.parse(usuarioLocal)
      }
    }
    this.transaccionService.getTransacciones(this.userId, this.token)
      .subscribe(transacciones => {
        this.transacciones = transacciones.filter(transaccion => transaccion.valor != 0);
        this.transacciones_mostrar = this.transacciones.slice(0,5);
      },
        error => {
          if (error.statusText === "UNAUTHORIZED") {
            this.showWarning("Su sesión ha caducado, por favor vuelva a iniciar sesión.");
          }
          else if (error.statusText === "UNPROCESSABLE ENTITY") {
            this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.");
          }
          else {
            this.showError("Ha ocurrido un error. " + error.message);
          }
        })
  }

  regresar() {
    this.routerPath.navigate([`/carreras/${this.userId}/${this.token}`]);
  }

  verMas(){
    if (this.transacciones.length > 5){
      this.mostrar_todo = true;
      this.transacciones_mostrar = this.transacciones;
    }
  }


  verMenos(){
    this.mostrar_todo = false;
    this.transacciones_mostrar = this.transacciones.slice(0,5);
  }

  showError(error: string) {
    this.toastr.error(error, "Error")
  }

  showWarning(warning: string) {
    this.toastr.warning(warning, "Error de autenticación");
  }


}

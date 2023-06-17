import { Component, OnInit } from '@angular/core';
import { ActivatedRoute,Router } from '@angular/router';
import { Usuario } from '../../usuario/usuario';
import { TransaccionService } from '../transaccion.service'
import { ToastrService } from 'ngx-toastr';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';


@Component({
  selector: 'app-usuario-retirar',
  templateUrl: './retirar.component.html',
  styleUrls: ['./retirar.component.css']
})


export class RetirarComponent implements OnInit {

  userId: number;
  token: string;
  retirarForm: FormGroup;
  usuario: Usuario;

  constructor(
    private transaccionService: TransaccionService,
    private router: ActivatedRoute,
    private formBuilder: FormBuilder,
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
      this.retirarForm = this.formBuilder.group({
        valor: ['', [Validators.required, Validators.required, Validators.min(1), Validators.max(Number(this.usuario.monedero)), Validators.pattern('[0-9]*$')]],
        monedero: ['************'+this.usuario.numero_tarjeta?.toString().slice(12)]
      })
    }
  }

  showError(error: string) {
    this.toastr.error(error, "Error")
  }

  retirarDinero(valor: number) {
    this.transaccionService.postTransaccion(this.userId, this.token, valor, 'RETIRO')
      .subscribe(usuario => {
        localStorage.setItem('usuario', JSON.stringify(usuario));
        this.showSuccess(usuario);
        this.retirarForm.reset();
        this.routerPath.navigate([`/carreras/${this.userId}/${this.token}`]);
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

  cancelRetirar() {
    this.retirarForm.reset();
    this.routerPath.navigate([`/carreras/${this.userId}/${this.token}`]);
  }

  showWarning(warning: string) {
    this.toastr.warning(warning, "Error de autenticación");
  }

  showSuccess(usuario: Usuario) {
    localStorage.setItem('usuario', JSON.stringify(usuario));
    this.toastr.success(`El dinero fue retirado de la cuenta.`, "Transacción exitosa");
  }
}

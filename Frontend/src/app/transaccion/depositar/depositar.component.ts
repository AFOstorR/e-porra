import { Component, OnInit } from '@angular/core';
import { ActivatedRoute,Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { TransaccionService } from '../transaccion.service';
import { Usuario } from 'src/app/usuario/usuario';

@Component({
  selector: 'app-usuario-depositar',
  templateUrl: './depositar.component.html',
  styleUrls: ['./depositar.component.css']
})

export class DepositarComponent implements OnInit {

  userId: number;
  token: string;
  depositarForm: FormGroup;
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
      this.depositarForm = this.formBuilder.group({
        valor: ["", [Validators.required, Validators.min(5000), Validators.pattern('[0-9]*$')]]
      })
      var usuarioLocal = localStorage.getItem('usuario');
      if (usuarioLocal != null){
        this.usuario = JSON.parse(usuarioLocal)
      }
    }
  }

  showError(error: string) {
    this.toastr.error(error, "Error")
  }

  depositarDinero(valor: number) {
    this.transaccionService.postTransaccion(this.userId, this.token, valor, 'DEPOSITO')
      .subscribe(usuario => {
        localStorage.setItem('usuario', JSON.stringify(usuario));
        this.showSuccess(usuario);
        this.depositarForm.reset();
        this.routerPath.navigate([`/carreras/${this.userId}/${this.token}`]);
      },
        error => {
          if (error.statusText === "UNAUTHORIZED") {
            this.showWarning("Su sesión ha caducado, por favor vuelva a iniciar sesión.")
          }
          else if (error.statusText === "UNPROCESSABLE ENTITY") {
            this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
          }
          else {
            this.showError("Ha ocurrido un error. " + error.message)
          }
        })
  }

  cancelDepositar() {
    this.depositarForm.reset();
    this.routerPath.navigate([`/carreras/${this.userId}/${this.token}`]);
  }

  showWarning(warning: string) {
    this.toastr.warning(warning, "Error de autenticación")
  }

  showSuccess(usuario: Usuario) {
    localStorage.setItem('usuario', JSON.stringify(usuario));
    this.toastr.success(`El dinero fue depositado a la cuenta.`, "Transacción exitosa");
  }
}

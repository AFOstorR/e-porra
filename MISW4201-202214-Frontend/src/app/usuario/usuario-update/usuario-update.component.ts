import { Component, OnInit } from '@angular/core';
import { ActivatedRoute,Router } from '@angular/router';
import { Usuario } from '../usuario';
import { UsuarioService } from '../usuario.service';
import { ToastrService } from 'ngx-toastr';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-usuario-update',
  templateUrl: './usuario-update.component.html',
  styleUrls: ['./usuario-update.component.css']
})
export class UsuarioUpdateComponent implements OnInit {

  userId: number;
  token: string;
  updateForm: FormGroup;
  usuario: Usuario;

  constructor(
    private usuarioService: UsuarioService,
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
      this.updateForm = this.formBuilder.group({
        correo_electronico: [this.usuario.usuario, [Validators.required, Validators.pattern('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$')]],
        numero_tarjeta: [`************${this.usuario.numero_tarjeta?.slice(12)}`, [Validators.required, Validators.pattern('[0-9]{16}$')]],
      })


    }
  }

  updateUsuario(newUsuario: Usuario) {
    this.usuarioService.updateUsuario(newUsuario, this.userId, this.token)
      .subscribe(usuario => {
        localStorage.setItem('usuario', JSON.stringify(usuario));
        this.showSuccess(usuario);
        this.updateForm.reset();
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
            this.showError(`Ha ocurrido un error: ${error.error}`)
          }
        })
  }

  showError(error: string) {
    this.toastr.error(error, "Error")
  }

  cancelUpdate() {
    this.updateForm.reset();
    this.routerPath.navigate([`/carreras/${this.userId}/${this.token}`]);
  }

  showWarning(warning: string) {
    this.toastr.warning(warning, "Error de autenticación")
  }

  showSuccess(usuario: Usuario) {
    localStorage.setItem('usuario', JSON.stringify(usuario));
    this.toastr.success(`La información de usuario fue actualizada`, "Actualización exitosa");
  }
}

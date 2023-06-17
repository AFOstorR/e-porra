import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { JwtHelperService } from "@auth0/angular-jwt";
import { ToastrService } from 'ngx-toastr';
import { Usuario } from '../usuario';
import { UsuarioService } from '../usuario.service';



@Component({
  selector: 'app-usuario-signup',
  templateUrl: './usuario-signup.component.html',
  styleUrls: ['./usuario-signup.component.css']
})
export class UsuarioSignupComponent implements OnInit {

  helper = new JwtHelperService();
  usuarioForm: FormGroup;

  emailPattern: string = "^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$";
  creditCardPattern: string = "[0-9]{16}";
  registerUser:Usuario = {};

  constructor(
    private usuarioService: UsuarioService,
    private formBuilder: FormBuilder,
    private router: Router,
    private toastr: ToastrService
  ) { }

  ngOnInit() {
    this.usuarioForm = this.formBuilder.group({
      usuario: ["", [Validators.required, Validators.pattern(this.emailPattern)]],
      nombre: ["", [Validators.required, Validators.maxLength(50)]],
      tarjetaCredito:["",[Validators.required,Validators.pattern(this.creditCardPattern)]],
      password: ["", [Validators.required, Validators.maxLength(50), Validators.minLength(4)]],
      confirmPassword: ["", [Validators.required, Validators.maxLength(50), Validators.minLength(4)]]
    })
  }

  registrarUsuario() {
    this.registerUser = {
      usuario: this.usuarioForm.get('usuario')?.value,
      nombre: this.usuarioForm.get('nombre')?.value,
      numero_tarjeta: this.usuarioForm.get('tarjetaCredito')?.value,
      contrasena: this.usuarioForm.get('password')?.value,
    }


    this.usuarioService.userSignUp(this.registerUser)
      .subscribe(res => {
        const decodedToken = this.helper.decodeToken(res.token);
        console.log(res)
        this.router.navigate([`/carreras/${decodedToken.sub}/${res.token}`])
        localStorage.setItem('usuario', JSON.stringify(res.usuario));
        this.showSuccess()
      },
        error => {
          this.showError(`Ha ocurrido un error: ${error.error}`
          )
          console.log(error);
        })

  }

  showError(error: string) {
    this.toastr.error(error, "Error")
  }

  showSuccess() {
    this.toastr.success(`Se ha registrado exitosamente`, "Registro exitoso");
  }

}

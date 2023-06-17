import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { UsuarioLoginComponent } from './usuario-login/usuario-login.component';
import { UsuarioSignupComponent } from './usuario-signup/usuario-signup.component';
import { UsuarioUpdateComponent } from './usuario-update/usuario-update.component';
import { AppHeaderModule } from '../app-header/app-header.module';


@NgModule({
  declarations: [UsuarioLoginComponent, UsuarioSignupComponent, UsuarioUpdateComponent] ,
  imports: [
    CommonModule, ReactiveFormsModule, AppHeaderModule
  ],
  exports: [UsuarioLoginComponent, UsuarioSignupComponent, UsuarioUpdateComponent]
})
export class UsuarioModule { }

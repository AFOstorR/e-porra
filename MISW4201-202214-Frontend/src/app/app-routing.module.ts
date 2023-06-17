import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ApuestaCreateComponent } from './apuesta/apuesta-create/apuesta-create.component';
import { ApuestaEditComponent } from './apuesta/apuesta-edit/apuesta-edit.component';
import { ApuestaListComponent } from './apuesta/apuesta-list/apuesta-list.component';
import { CarreraCreateComponent } from './carrera/carrera-create/carrera-create.component';
import { CarreraEditComponent } from './carrera/carrera-edit/carrera-edit.component';
import { CarreraFinishComponent } from './carrera/carrera-finish/carrera-finish.component';
import { CarreraListComponent } from './carrera/carrera-list/carrera-list.component';
import { CarreraReportComponent } from './carrera/carrera-report/carrera-report.component';
import {RetirarComponent } from './transaccion/retirar/retirar.component'
import { UsuarioLoginComponent } from './usuario/usuario-login/usuario-login.component';
import { DepositarComponent } from './transaccion/depositar/depositar.component';
import { UsuarioSignupComponent } from './usuario/usuario-signup/usuario-signup.component';
import { UsuarioUpdateComponent } from './usuario/usuario-update/usuario-update.component';
import { VerTransaccionesComponent } from './transaccion/ver-transacciones/ver-transacciones.component';

const routes: Routes = [
  {
    path: '',
    component: UsuarioLoginComponent,
    pathMatch: 'full'
  },
  {
    path: 'signin',
    component: UsuarioLoginComponent,
    pathMatch: 'full'
  },
  {
    path: 'signup',
    component: UsuarioSignupComponent,
    pathMatch: 'full'
  },

  {
    path: 'usuario/perfil/:userId/:userToken',
    component: UsuarioUpdateComponent
  },

  {
    path: 'transacciones/depositar/:userId/:userToken',
    component: DepositarComponent
  },

  {
    path: 'transacciones/retirar/:userId/:userToken',
    component: RetirarComponent
  },
  {
    path: 'transacciones/ver/:userId/:userToken',
    component: VerTransaccionesComponent
  },
 {
    path: 'carreras/:userId/:userToken',
    component: CarreraListComponent
  },
  {
    path: 'carreras/crear/:userId/:userToken',
    component: CarreraCreateComponent
  },
  {
    path: 'carreras/editar/:carreraId/:userId/:userToken',
    component: CarreraEditComponent
  },
  {
    path: 'carreras/terminar/:carreraId/:userId/:userToken',
    component: CarreraFinishComponent
  },
  {
    path: 'carreras/reporte/:carreraId/:userId/:userToken',
    component: CarreraReportComponent
  },
  {
    path: 'apuestas/:userId/:userToken',
    component: ApuestaListComponent
  },
  {
    path: 'apuestas/crear/:userId/:userToken',
    component: ApuestaCreateComponent
  },
  {
    path: 'apuestas/editar/:apuestaId/:userId/:userToken',
    component: ApuestaEditComponent
  }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

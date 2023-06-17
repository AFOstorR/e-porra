import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { RetirarComponent } from './retirar/retirar.component';
import { DepositarComponent } from './depositar/depositar.component';
import { VerTransaccionesComponent } from './ver-transacciones/ver-transacciones.component';
import { AppHeaderModule } from '../app-header/app-header.module';

@NgModule({
  imports: [
    CommonModule, AppHeaderModule, ReactiveFormsModule
  ],
  declarations: [ RetirarComponent, DepositarComponent, VerTransaccionesComponent],
  exports: [ RetirarComponent, DepositarComponent, VerTransaccionesComponent]
})
export class TransaccionModule { }

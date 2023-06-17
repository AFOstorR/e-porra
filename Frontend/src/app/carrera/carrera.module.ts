import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AppHeaderModule } from '../app-header/app-header.module';
import { CarreraCreateComponent } from './carrera-create/carrera-create.component';
import { CarreraDetailComponent } from './carrera-detail/carrera-detail.component';
import { CarreraEditComponent } from './carrera-edit/carrera-edit.component';
import { CarreraFinishComponent } from './carrera-finish/carrera-finish.component';
import { CarreraListComponent } from './carrera-list/carrera-list.component';
import { CarreraReportComponent } from './carrera-report/carrera-report.component';


@NgModule({
  declarations: [CarreraListComponent, CarreraDetailComponent, CarreraCreateComponent, CarreraEditComponent, CarreraFinishComponent, CarreraReportComponent],
  imports: [
    CommonModule, ReactiveFormsModule, AppHeaderModule, FormsModule
  ],
  exports: [CarreraListComponent, CarreraDetailComponent, CarreraCreateComponent, CarreraEditComponent, CarreraFinishComponent, CarreraReportComponent]
})
export class CarreraModule { }

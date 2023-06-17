import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';

import { Evento } from '../carrera';
import { CarreraService } from '../carrera.service';

@Component({
  selector: 'app-carrera-create',
  templateUrl: './carrera-create.component.html',
  styleUrls: ['./carrera-create.component.css']
})
export class CarreraCreateComponent implements OnInit {

  userId: number
  token: string
  carreraForm: FormGroup
  tipo_eventos: any = ['CARRERA','MARCADOR'];

  constructor(
    private carreraService: CarreraService,
    private formBuilder: FormBuilder,
    private router: ActivatedRoute,
    private toastr: ToastrService,
    private routerPath: Router
  ) { }


  ngOnInit() {
    if (!parseInt(this.router.snapshot.params.userId) || this.router.snapshot.params.userToken === " ") {
      this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
    }
    else {
      this.userId = parseInt(this.router.snapshot.params.userId);
      this.token = this.router.snapshot.params.userToken;

      this.carreraForm = this.formBuilder.group({
        nombre: ["", [Validators.required, Validators.minLength(1), Validators.maxLength(128)]],
        competidores: new FormArray([]),
        tipo_evento : ['',[Validators.required]]
      });


    }
  }

  get carreraFormControls() {
    return this.carreraForm.controls;
  }

  get competidorformArray() {
    return this.carreraFormControls.competidores as FormArray;
  }

  get marcadorformArray() {
    return this.carreraFormControls.marcadores as FormArray;
  }

  private createCompetidorForm(item?: any): FormGroup {
    return this.formBuilder.group({
      competidor: [item == null ? '' : item.competidor ,[Validators.required, Validators.minLength(1), Validators.maxLength(128)]],
      probabilidad: [item == null ? '' : item.probabilidad, [Validators.required, Validators.min(0), Validators.max(1)]],

    });
  }


  onTipoEventoSelect(e:any):void{
    if(e == 'MARCADOR'){
      this.competidorformArray.clear();
      this.competidorformArray.push(this.createCompetidorForm());
      this.competidorformArray.push(this.createCompetidorForm());
      this.competidorformArray.push(this.createCompetidorForm({competidor:'Empate',disabled:true}));

    }else if (e == 'CARRERA'){
      this.competidorformArray.clear();
      this.competidorformArray.push(this.createCompetidorForm());
    }
  }
  onAddCompetidor() {
    this.competidorformArray.push(this.createCompetidorForm());
  }

  onRemoveCompetidor(index: number) {
    this.competidorformArray.removeAt(index);
  }

  cancelCreate() {
    this.carreraForm.reset()
    this.routerPath.navigate([`/carreras/${this.userId}/${this.token}`])
  }

  createCarrera(newCarrera: Evento) {
    let sum_probabilidades:number = 0;
    newCarrera.competidores.forEach((c,i) => {
        sum_probabilidades = sum_probabilidades  + Number(c.probabilidad);
    });

    if(sum_probabilidades != 1){
      this.showWarning(`La suma de las probabilidades de todos los competidores es: ${sum_probabilidades}. Verifique los datos, ya que la probabilidad debe ser igual a 1`,'Crear Evento')
      return;
    }
    this.carreraService.crearCarrera(this.userId, this.token, newCarrera)
      .subscribe(carrera => {
        this.showSuccess(carrera)
        this.carreraForm.reset()
        this.routerPath.navigate([`/carreras/${this.userId}/${this.token}`])
      },
        error => {
          if (error.statusText === "UNAUTHORIZED") {
            this.showWarning("Su sesión ha caducado, por favor vuelva a iniciar sesión.",'Error de Autenticación')
          }
          else if (error.statusText === "UNPROCESSABLE ENTITY") {
            this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
          }
          else {
            this.showError("Ha ocurrido un error: " + error.message)
          }
        })
  }

  showError(error: string) {
    this.toastr.error(error, "Error")
  }

  showWarning(mensaje: string,titulo:string) {
    this.toastr.warning(mensaje, titulo)
  }

  showSuccess(carrera: Evento) {
    this.toastr.success(`La carrera ${carrera.nombre_evento} fue creada`, "Creación exitosa");
  }
}

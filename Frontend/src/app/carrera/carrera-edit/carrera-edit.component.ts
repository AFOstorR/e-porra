import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Evento } from '../carrera';
import { CarreraService } from '../carrera.service';

@Component({
  selector: 'app-carrera-edit',
  templateUrl: './carrera-edit.component.html',
  styleUrls: ['./carrera-edit.component.css']
})
export class CarreraEditComponent implements OnInit {

  userId: number;
  token: string;
  carreraId: number;
  carreraForm!: FormGroup;
  tipo_eventos: any = ['CARRERA','MARCADOR'];

  constructor(

    private carreraService: CarreraService,
    private formBuilder: FormBuilder,
    private router: ActivatedRoute,
    private toastr: ToastrService,
    private routerPath: Router) { }

  ngOnInit() {
    if (!parseInt(this.router.snapshot.params.userId) || this.router.snapshot.params.userToken === " ") {
      this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
    }
    else {
      this.userId = parseInt(this.router.snapshot.params.userId)
      this.token = this.router.snapshot.params.userToken
      this.carreraService.getCarrera(parseInt(this.router.snapshot.params.carreraId), this.token)
        .subscribe(carrera => {

          this.carreraId = carrera.id;
          this.carreraForm = this.formBuilder.group({
            nombre: [carrera.nombre_evento, [Validators.required, Validators.minLength(1), Validators.maxLength(128)]],
            tipo_evento:[{value:carrera.tipo_evento, disabled:true},[Validators.required]],
            competidores: new FormArray([]),
          })

            if (carrera.competidores.length > 0) {
              carrera.competidores.forEach((item, index) => {
                this.competidorformArray.push(this.createCompetidorForm(item));
              });
            }
        })
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
      id: [item == null ? '' : item.id],
      competidor: [item == null ? '' : item.nombre_competidor, [Validators.required, Validators.minLength(1), Validators.maxLength(128)]],
      probabilidad: [item == null ? '' : Number(item.probabilidad).toFixed(2), [Validators.required, Validators.min(0), Validators.max(1)]]
    });
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

  editarCarrera(newCarrera: Evento) {
    let sum_probabilidades:number = 0;
    newCarrera.competidores.forEach((c,i) => {
      sum_probabilidades = sum_probabilidades + Number(c.probabilidad);
    });

    if(sum_probabilidades != 1){
      this.showWarning(`La suma de las probabilidades de todos los competidores es: ${sum_probabilidades}. Verifique los datos, ya que la probabilidad debe ser igual a 1`,'Editar Evento')
      return;
    }

    this.carreraService.editarCarrera(this.token, this.carreraId, newCarrera)
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
            this.showError("Ha ocurrido un error. " + error.message)
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
    this.toastr.success(`La carrera ${carrera.nombre_evento} fue editada`, "Edición exitosa");
  }

}

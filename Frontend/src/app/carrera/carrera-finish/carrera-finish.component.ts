import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from "ngx-toastr";
import { Evento, Competidor } from '../carrera';
import { CarreraService } from '../carrera.service';

@Component({
  selector: 'app-carrera-finish',
  templateUrl: './carrera-finish.component.html',
  styleUrls: ['./carrera-finish.component.css']
})

export class CarreraFinishComponent implements OnInit {

  carrera: Evento;
  userId: number;
  token: string;
  competidores: Array<Competidor>
  competidorGanador: Competidor
  competidorGanadorForm!: FormGroup;

  constructor(
    private carreraService: CarreraService,
    private router: ActivatedRoute,
    private formBuilder: FormBuilder,
    private toastr: ToastrService,
    private routerPath: Router) { }

  ngOnInit(): void {
    if (!parseInt(this.router.snapshot.params.userId) || this.router.snapshot.params.userToken === " ") {
      this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
    }
    else {
      this.userId = parseInt(this.router.snapshot.params.userId)
      this.token = this.router.snapshot.params.userToken

      this.competidorGanadorForm = this.formBuilder.group({
        id_competidor: ["", [Validators.required]]
      });

      this.carreraService.getCarrera(parseInt(this.router.snapshot.params.carreraId), this.token)
        .subscribe(carreraEncontrada => {
          this.carrera = carreraEncontrada
          this.competidores = carreraEncontrada.competidores || [];
        })
    }
  }

  showError(error: string) {
    this.toastr.error(error, "Error")
  }

  showWarning(warning: string) {
    this.toastr.warning(warning, "Error de autenticación")
  }

  backToDetails() {
    this.routerPath.navigate([`/carreras/${this.userId}/${this.token}`])
  }

  terminarCarrera(form: any) {
    this.carreraService.actualizarGanador(this.token, form.id_competidor)
      .subscribe(competidor => {
        this.competidorGanador = competidor
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

    this.routerPath.navigate([`carreras/reporte/${this.carrera.id}/${this.userId}/${this.token}`])
  }
}

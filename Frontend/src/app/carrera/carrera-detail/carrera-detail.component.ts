import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Usuario } from 'src/app/usuario/usuario';
import { Evento } from '../carrera';
import { CarreraService } from '../carrera.service';

@Component({
  selector: 'app-carrera-detail',
  templateUrl: './carrera-detail.component.html',
  styleUrls: ['./carrera-detail.component.css']
})
export class CarreraDetailComponent implements OnInit {

  @Input() carrera: Evento;

  userId: number;
  token: string;
  user: Usuario;
  constructor(
    private carreraService: CarreraService,
    private toastr: ToastrService,
    private routerPath: Router,
    private router: ActivatedRoute
  ) { }

  ngOnInit() {
    this.userId = parseInt(this.router.snapshot.params.userId)
    this.token = this.router.snapshot.params.userToken
    this.user=JSON.parse(localStorage.getItem('usuario')!)

  }

  getCompetidor(id_competidor: any) {
    var competidor = this.carrera.competidores.filter(x => x.id == id_competidor)[0]
    if(competidor){

      return competidor.nombre_competidor;
    }else{
      return 'Empate';
    }
  }

  goToEdit() {
    this.routerPath.navigate([`/carreras/editar/${this.carrera.id}/${this.userId}/${this.token}`])
  }

  apostar() {
    this.routerPath.navigate([`/carreras/apostar/${this.carrera.id}/${this.userId}/${this.token}`])
  }

  eliminarCarrera() {
    if(confirm(`¿Está seguro de borrar el evento: ${this.carrera.nombre_evento}?`)) {
      if (this.carrera.apuestas.length) {
        this.showError(`El evento: ${this.carrera.nombre_evento} no se puede eliminar porque tiene ${this.carrera.apuestas.length} apuesta(s) asociada`,'Eliminar Evento')
      } else {
        this.carreraService.eliminarCarrera(this.token, this.carrera.id)
        .subscribe(carrera => {
          window.location.reload();
          this.showSuccess();
        },
          error => {
            if (error.statusText === "UNAUTHORIZED") {
              this.showWarning("Su sesión ha caducado, por favor vuelva a iniciar sesión.","Error de autenticación")
            }
            else if (error.statusText === "UNPROCESSABLE ENTITY") {
              this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.","Error de autenticación")
            }
            else {
              this.showError("Ha ocurrido un error. " + error.message, 'Error')
            }
          })
      this.ngOnInit()
      }
    }

  }

  terminarCarrera() {
    this.routerPath.navigate([`/carreras/terminar/${this.carrera.id}/${this.userId}/${this.token}`])
  }
  showError(error: string, titulo:string) {
    this.toastr.error(error, titulo)
  }

  showWarning(warning: string, titulo:string) {
    this.toastr.warning(warning, titulo)
  }

  showSuccess() {
    this.toastr.success(`La carrera fue eliminada`, "Eliminada exitosamente");
  }
}

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from "ngx-toastr";
import { Usuario } from 'src/app/usuario/usuario';
import { Evento } from '../carrera';
import { CarreraService } from '../carrera.service';

@Component({
  selector: 'app-carrera-list',
  templateUrl: './carrera-list.component.html',
  styleUrls: ['./carrera-list.component.css']
})
export class CarreraListComponent implements OnInit {

  constructor(
    private carreraService: CarreraService,
    private router: ActivatedRoute,
    private toastr: ToastrService,
    private routerPath: Router
  ) { }

  userId: number
  token: string
  carreras: Array<Evento>
  mostrarCarreras: Array<Evento>
  carreraSeleccionada: Evento
  indiceSeleccionado: number
  user:Usuario;

  ngOnInit() {
    if (!parseInt(this.router.snapshot.params.userId) || this.router.snapshot.params.userToken === " ") {
      this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
    }
    else {
      this.userId = parseInt(this.router.snapshot.params.userId)
      this.token = this.router.snapshot.params.userToken
      this.user=JSON.parse(localStorage.getItem('usuario')!)

      this.getCarreras();
    }
  }

  getCarreras(): void {
    this.carreraService.getAllCarreras( this.token)
      .subscribe(carreras => {
        this.carreras = carreras
        this.mostrarCarreras = carreras
        if (carreras.length > 0) {
          this.onSelect(this.mostrarCarreras[0], 0)
        }
      },
        error => {
          console.log(error)
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

  }

  onSelect(a: Evento, index: number) {
    this.indiceSeleccionado = index
    this.carreraSeleccionada = a
  }

  buscarCarrera(busqueda: string, tipoEvento: string, estadoEvento: string) {
    let carrerasBusqueda: Array<Evento> = []

    this.carreras.map(carrera => {
      
     if (carrera.nombre_evento?.toLocaleLowerCase().includes(busqueda.toLowerCase())) {
        carrerasBusqueda.push(carrera)
      }
    })

    if (tipoEvento != '') {
      carrerasBusqueda = carrerasBusqueda.filter((c) => c.tipo_evento == tipoEvento)
    }

    if (estadoEvento != '') {
      carrerasBusqueda = carrerasBusqueda.filter((c) => c.abierta == Boolean(Number(estadoEvento)))
    }

    this.mostrarCarreras = carrerasBusqueda
  }

  irCrearCarrera() {
    this.routerPath.navigate([`/carreras/crear/${this.userId}/${this.token}`])
  }

  showError(error: string) {
    this.toastr.error(error, "Error de autenticación")
  }

  showWarning(warning: string) {
    this.toastr.warning(warning, "Error de autenticación")
  }
}
